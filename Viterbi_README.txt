This program makes a table of the prior probabilities for each Part of Speech (POS) tag (bigram model) and a likelihood table from the training corpus. It implements a Viterbi HMM POS tagger using the prior probabilities and likelihood tables, taking input in the format of the test corpus and producing output in the format of the training corpus.

The tagging program uses 1/1000 as the likelihood for out of vocabulary (OOV) items. 

Prior probabilities not found in the training corpus are set to a default value of 1/1000. 

The command to run the program is 'python Viterbi_HMM_POS.py arg1 arg2 arg3'.

The arguments are to be in the format as follows:

arg1 -- .pos training file

arg2 -- .words input file for tagging program

arg3 -- .pos output file

The 2 types of files:

1) file.pos -- two columns separated by a tab
   1st column: token
   2nd column: POS tag
   Blank line: sentence separator

2) file.words -- one token per line, blank line between sentences

Ex: 'python Viterbi_HMM_POS.py WSJ_02-21.pos WSJ_23.words submission.pos'