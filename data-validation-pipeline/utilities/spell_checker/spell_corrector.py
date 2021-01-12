import os
import re
import json
import pandas as pd
import time
from math import floor

# Function to calculate the
# Jaro Similarity of two strings
def jaro_distance(s1, s2) :
    # If the strings are equal
    if (s1 == s2) :
        return 1.0
    # Length of two strings
    len1 = len(s1)
    len2 = len(s2)
    if (len1 == 0 or len2 == 0) :
        return 0.0
    # Maximum distance upto which matching
    # is allowed
    max_dist = (max(len(s1), len(s2)) // 2 ) - 1
    # Count of matches
    match = 0
    # Hash for matches
    hash_s1 = [0] * len(s1) 
    hash_s2 = [0] * len(s2) 
    # Traverse through the first string
    for i in range(len1) :
        # Check if there is any matches
        for j in range( max(0, i - max_dist),
                    min(len2, i + max_dist + 1)) :
            # If there is a match
            if (s1[i] == s2[j] and hash_s2[j] == 0) :
                hash_s1[i] = 1
                hash_s2[j] = 1
                match += 1
                break
    # If there is no match
    if (match == 0) :
        return 0.0
    # Number of transpositions
    t = 0
    point = 0
    # Count number of occurences
    # where two characters match but
    # there is a third matched character
    # in between the indices
    for i in range(len1) :
        if (hash_s1[i]) :
            # Find the next matched character
            # in second string
            while (hash_s2[point] == 0) :
                point += 1

            if (s1[i] != s2[point]) :
                point += 1
                t += 1
            else :
                point += 1
        t /= 2
    # Return the Jaro Similarity
    return ((match / len1 + match / len2 +
            (match - t) / match ) / 3.0)

# Jaro Winkler Similarity
def jaro_Winkler(s1, s2) :
    jaro_dist = jaro_distance(s1, s2)
    # If the jaro Similarity is above a threshold
    if (jaro_dist > 0.8) :
        # Find the length of common prefix
        prefix = 0
        for i in range(min(len(s1), len(s2))) :
            # If the characters match
            if (s1[i] == s2[i]) :
                prefix += 1
            # Else break
            else :
                break
        # Maximum of 4 characters are allowed in prefix
        prefix = min(4, prefix)
        # Calculate jaro winkler Similarity
        jaro_dist += 0.1 * prefix * (1 - jaro_dist)
    return jaro_dist

def editDistDP(str1, str2, m, n):
    # Create a table to store results of subproblems
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]
    # Fill d[][] in bottom up manner
    for i in range(m + 1):
        for j in range(n + 1):
            # If first string is empty, only option is to
            # insert all characters of second string
            if i == 0:
                dp[i][j] = j    # Min. operations = j
            # If second string is empty, only option is to
            # remove all characters of second string
            elif j == 0:
                dp[i][j] = i    # Min. operations = i
            # If last characters are same, ignore last char
            # and recur for remaining string
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            # If last character are different, consider all
            # possibilities and find minimum
            else:
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert
                                   dp[i-1][j],        # Remove
                                   dp[i-1][j-1])      # Replace
    return dp[m][n]


#Calculate the Jaccardian co-efficient between the two bigrams
def calculate_jc(w1,w2):
    #Create a set from the two bigram lists
    set_a = set(w1)
    set_b = set(w2)
    #Find the intersection between the two sets
    intersection = set_a.intersection(set_b)
    #Jaccardian co-efficent = 1 - |X n Y| / |X u Y|
    return len(intersection)/(len(set_a)+len(set_b)-len(intersection))


def get_set_word_case(w):
    if(w.isupper()):
        return 0,w.lower()
    elif(w[0].isupper()):
        return 1,w.lower()
    else:
        return 2,w


def spell_corrector(df,lang1='en',lang2='hi'):
    #Read the dictionary file
    with open("./json_files/words_sfx_rules_rel.json",'r') as f:
        word_list = json.loads(f.read())
    #Create a text blob to apply regular expressions for search
    txt = '\n'.join(list(word_list.keys()))
    #New list to create df of corrected sentences
    corrected_sent_list = []
    for sent in df[lang1]:
        corr_sent = ''
        for w in re.split(r'\b',sent):
            if not w.isalpha() or re.search(r'\b'+w+r'\b',txt,re.IGNORECASE):
                corr_sent += w
            else:
                case,w = get_set_word_case(w)
                short_listed_words = {'word':[],'jc':[],'jw':[],'ed':[]}
                for word in word_list.keys():
                    jw = jaro_Winkler(w,word)
                    short_listed_words['jw'].append(jw)
                    short_listed_words['word'].append(word)
                    if(jw > 0.8):
                        short_listed_words['jc'].append(calculate_jc(w,word))
                        short_listed_words['ed'].append(editDistDP(word,w,len(word),len(w)))
                    else:
                        short_listed_words['jc'].append(None)
                        short_listed_words['ed'].append(None)
                shdf = pd.DataFrame.from_dict(short_listed_words)
                shdf = shdf.sort_values(by=['ed','jc','jw'],ascending=[True,False,False])
                corr_word = list(shdf['word'])[0]
                if(case == 0):
                    corr_word = corr_word.upper()
                elif(case == 1 ):
                    corr_word = corr_word[0].upper()+corr_word[1:]
                corr_sent += corr_word
        corrected_sent_list.append(corr_sent)
    return pd.DataFrame(corrected_sent_list,columns=[lang1])


#Driver code for testing
if __name__ == "__main__":
    start = time.time()
    #['nonxadpayment amount is not applicable.'],['postxadmortem report not given'],['Calndars are not brought yet']
    l = [['nonxadpayment amount is not applicable.'],['postxadmortem report not given'],['Calndars are not brought yet'],['Plaese alliow me tao introdduce myhelf, I am a man of waelth und tiaste']]
    df = pd.DataFrame(l,columns=['en'])
    corr_df = spell_corrector(df)
    print(corr_df)
    print(time.time()-start)
