import re

def tokenize_eng_file(mainString):
    sentences = []
    e = '((?<=[^A-Z])\. *(?=[A-Z|"])|\? |\n|\*\*|\([MDCLXVImdclxvi]+\)|^[0-9]+\.[^0-9])'
    mainString = re.sub('(?<=[0-9][0-9])\.','. ',mainString)
    mainString = re.sub('(?<=[A-Z][A-Z])\. ',' .',mainString)
    mainString = re.sub('(?<=[a-z])\. +','. ',mainString)
    mainString = mainString.replace('Prof. ','Prof.')
    mainString = mainString.replace('Dr. ','Dr.')
    mainString = mainString.replace('Mr. ','Mr.')
    mainString = mainString.replace('Mrs. ','Mrs.')
    mainString = mainString.replace('Ms. ','Ms.')
    mainString = mainString.replace('viz. ','viz.')
    mainString = mainString.replace('Hon. ','Hon.')
    mainString = mainString.replace('i.e. ','i.e.')
    mainString = mainString.replace('Smt. ','Smt.')
    mainString = mainString.replace('Shri. ','Shri.')
    mainString = mainString.replace('St. ','St.')
    mainString = mainString.replace('Lt. ','Lt.')
    mainString = mainString.replace('i.e.','i.e. ')
    splitString = re.split(e,mainString)
    # print(splitString)
    for i,s in enumerate(splitString):
        if(s.strip() == ''):
            continue
        if(s == '\n'):
            continue
        if(re.search('\([MDCLXVImdclxvi]+\)$',s) is not None):
            splitString[i+1] = s + splitString[i+1]
            continue
        if(re.search('^\.$',s.strip()) is not None):
            # sentences[-1] += s[0]
            # splitString[i+1] = s[2] + splitString[i+1]
            continue
        if(re.search('\? $',s) is not None):
            sentences[-1] += s[0]
            continue
        if(re.search('^[0-9]+$',s.strip()) is not None):
            continue
        if(re.search('^[a-z]+$',s.strip()) is not None):
            continue
        if('*' in s):
            continue
        sentences.append(s.strip().replace('. ','.'))
    return sentences

def tokenize_hi_file(mainHinString):
    e = '(। +|\? |\n|\*\*|\([MDCLXVImdclxvi]+\)|[0-9]+\.[^0-9])'
    sentences = []
    splitString = re.split(e,mainHinString)
    for i,s in enumerate(splitString):
        if(s.strip() == ''):
            continue
        if(s == '\n'):
            continue
        if(re.search('\? $',s) is not None):
            sentences[-1] += s[0]
            continue
        if(re.search('\([MDCLXVImdclxvi]+\)$',s) is not None):
            # splitString[i+1] = s + splitString[i+1]
            continue
        if(re.search('। +$',s) is not None):
            # sentences[-1] += s[0]
            continue
        if(re.search('^[0-9]+\.$',s.strip()) is not None):
            continue
        if(re.search('^[a-z]+$',s.strip()) is not None):
            continue
        if('*' in s):
            continue
        sentences.append(s.strip())
    return sentences
