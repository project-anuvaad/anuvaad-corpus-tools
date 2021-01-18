#Using cyhunspell for Hunspell spelling correction engine
from hunspell import Hunspell
import time
import pandas as pd
import re

#Takes in a pandas dataframe with one sentence per row in column L1
#Returns a pandas dataframe with corrected sentences, one per row in column L1
def spell_corrector(df,lang1,lang2):
    #Create an object of the Hunspell class
    h = Hunspell()
    print('I am spell_checker')
    #An empty list to hold the corrected sentences which would later be made into a dataframe
    corr_sent_list = {'L1':[],'L2':[]}
    #For each sentence in the dataframe
    for sent in df['L1']:
        
        #Empty string to which the corrected words are appended
        corr_sent = ''
        #For every word in the sentence. Which is split by word boundary
        for w in re.split(r'\b',sent):
            #If the split part is not a word (punctuation marks, spaces) or if it is a correct word, append it to corr_sent 
            if not w.isalpha() or h.spell(w):
                corr_sent += w
            #If the split part is word and is incorrect
            else:
                #Suggest possible correct candidates to the incorrect word
                suggest = h.suggest(w)
                #If more than one word is suggested, more processing is required to select a word
                if len(suggest) > 1:
                    #TODO : Parse the list and find the n-gram probability to find the best candidate. For now it just appends the first word
                    corr_sent += suggest[0]
                #If only one word is suggested, append it to corr_sent
                else:
                    corr_sent += suggest[0]
        #When all the words in the sentence is traversed, append the corrected_sentence to corr_sent_list
        corr_sent_list['L1'].append(corr_sent)
    #Convert the corrected sentences list into pandas dataframe to return
    if lang2 is not None:
        corr_sent_list['L2'].extend(list(df['L2']))
        return pd.DataFrame.from_dict(corr_sent_list)
    else:
        return pd.DataFrame(corr_sent_list['L1'],columns=['L1'])


#Driver code for testing
if __name__ == "__main__":
    start = time.time()
    #Input:
    l = [['nonxadpayment amount is not paid.'],['postxadmortem report is not yet available'],['Plaese alliow me to introdduce myhelf, I am a man of waelth und tiaste']]
    #Output : [['nonpayment amount is not paid.']['postmortem report is not yet available'],['Please allow me to introduce myself, I am a man of wealth ind chaste']]
    df = pd.DataFrame(l,columns=['L1'])
    df = spell_corrector(df,'en',None)
    for sent in df['L1']:
        print(sent)
    print(time.time() - start)