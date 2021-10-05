#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 16:38:54 2021

@author: richardzhu
"""

import numpy as np
import sys

#Training
file = open(sys.argv[1], 'r')
readFile = file.readlines()

words = []
likelihoodTable = {}
transitionTable = {}

previousState = 'Start'
for i in range(len(readFile)):
    fields = readFile[i].split('\t')
    if len(fields) == 1: continue
    word = fields[0]
    pos = fields[1]

    #Words
    if word not in words:
        words.append(word)
    
    #Likelihood table
    if pos in likelihoodTable:
        if word in likelihoodTable[pos]:
            likelihoodTable[pos][word]+=1
        else:
            likelihoodTable[pos][word]=1
    else:
        likelihoodTable[pos]={}
        likelihoodTable[pos][word]=1
    
    #Transition table
    if previousState in transitionTable:
        if pos in transitionTable[previousState]:
            transitionTable[previousState][pos]+=1
        else:
            transitionTable[previousState][pos]=1
    else:
        transitionTable[previousState]={}
        transitionTable[previousState][pos]=1
    
    previousState=pos
    
    #End of sentence
    if pos == '.' or pos == '!' or pos == '?':
        if pos in transitionTable:
            if 'End' in transitionTable[pos]:
                transitionTable[pos]['End']+=1
            else:
                transitionTable[pos]['End']=1
        else:
            transitionTable[pos]={}
            transitionTable[pos]['End']=1
        previousState = 'Start'
        
#Convert to probabilities
for POS in likelihoodTable:
    total = 0
    for count in likelihoodTable[POS]:
        total+=likelihoodTable[POS][count]
    for count in likelihoodTable[POS]:
        likelihoodTable[POS][count]/=total
        
for POS1 in transitionTable:
    total = 0
    for POS2 in transitionTable[POS1]:
        total+=transitionTable[POS1][POS2]
    for POS2 in transitionTable[POS1]:
        transitionTable[POS1][POS2]/=total
        
#Fill in transitions
keys_list = list(transitionTable)
for POS in transitionTable:
    for keys in keys_list:
        if keys not in transitionTable[POS]:
            if not (POS == '.' and keys == 'Start'):
                transitionTable[POS][keys]=1/1000
                
#Transducer
#Input
inputFile = open(sys.argv[2], 'r')
inp = inputFile.readlines()
        
viterbi = [[0 for x in range(len(inp))] for y in range(len(keys_list)+2)] 
pointer = [None]*len(inp)

#Viterbi algorithm 
for q in range(0, len(keys_list)):
    try:
        likelihood = likelihoodTable[keys_list[q]][inp[0][0:len(inp[0])-1]]
        viterbi[q][0] = transitionTable['Start'][keys_list[q]]*likelihood
    except:
        None
POS = ''
for w in range(1, len(inp)):
    if pointer[w] != None:
        continue
    a = np.array([col[w-1] for col in viterbi])
    m = max(a)
    s = np.where(a == m)[0][0]
    prevPos = keys_list[s]
    for q in range(1, len(keys_list)):
        try:
            likelihood = likelihoodTable[keys_list[q]][inp[w][0:len(inp[w])-1]]
            viterbi[q][w] = transitionTable[prevPos][keys_list[q]]*likelihood
        except:
            None
    #OOV
    if [col[w] for col in viterbi] == [0]*len(viterbi) and inp[w] != '\n':
        likelihood = 1/1000
        for q in range(1, len(keys_list)):
            try:
                viterbi[q][w] = transitionTable[prevPos][keys_list[q]]*likelihood
            except:
                None
    #Assign POS
    pointer[w-1] = keys_list[s]
    
#Output
output = open(sys.argv[3], "w")
for i in range(len(inp)):
    if i == len(inp)-1:
        output.write('\n')
        continue
    if str(pointer[i]) == 'Start':
        output.write('\n')
        continue
    line = str(inp[i][0:len(inp[i])-1]) + '\t' + str(pointer[i])
    output.write(line)
output.close()