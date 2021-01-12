# Spell Checker

## Overview

In the process of obtaining data, various errors compromise the quality of data. One of those errors, usually caused by OCR or text encoding conversions, is spelling errors. Spelling errors at the start seem innocent but in the later stages, beautifully adhering to Chaos effect, develops into a huge threat, completely changing the meaning of sentences in a few cases. This module of the proposed data validation pipeline tries to reduce these errors which inherently increases the quality of the corpus. Spell corrector is not yet completed, still in the process of it.

###  Basic Idea

The journey begins by categorizing words as either correct or incorrect. Sadly, this is the end of the journey for correct words, it just gets appended back to the sentence. But in the case of incorrect ones, it gets more exciting. Going on a little detour to get some preliminaries out of the way. These incorrect words (iw from henceforth) can be corrected by going through the list of correct words for that language (Dictionary) and selecting the word that is closest to it. This is achieved by edit distances, they give a count of how many operations (insert,delete or replace) are needed to convert this iw into a correct word. The edit distance used here is Levenshtien Edit Distance. Calculating edit distances for all the valid words is quite computationally extensive and time consuming. So, various smart methods are used to reduce the number of words on which edit distance is to be calculated. These methods are Jaccardian similarity, which gives a similarity ratio between two words based on the intersection of the two, and n-gram sampling. Together they cut down the list quite a bit. Now back on track, all the iws travel on this path getting filtered out at each stop and finally coming out correct. But in a case of few, even these methods together won't be able to shrink it down to one. In those cases n-gram probability is used to select the correct word based on the context it is used in. In the end, these words are appended back to the sentence to complete it.

### Working
<div class="text-red mb-2">
  .text-red on white
</div>

The above explained idea is for now implemented using:

    Hunspell : http://hunspell.github.io/

A python binding of the above named cyhunspell is used. The exposed API is:

    Method name         :   spell_corrector
    Input Parameters    :   Pandas Dataframe consisting of one sentence per row in column L1, lang code of language1, lang code of language2
    Output              :   Pandas Dataframe consisting of corrected sentence per row in column L1 

### Experiments

Experiments are still going on, alongside devevlopment.