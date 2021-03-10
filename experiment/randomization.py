#####################################################
### SRC2 Python Code
### 2018.03.08 Latest Version
### Author: Cher YANG
### Research Lab: UW-Madison LCNL
#####################################################
from __future__ import print_function
from collections import Counter
import random
import math
import numpy as np
import os
import pprint as p
import pandas as pd

### params ###
YES='z'
NO='n'
INITFILE='trials/init.csv'

'''
This method is to read in init csv file:
	block order and return a list of tuples for each trial
'''
def readInit():
	df=pd.read_csv(INITFILE, header=0)
	
	blockA=[]
	blockB=[]
	blockC=[]
	blockD=[]
	
	for row in df.itertuples():
#		trialNum=int(row[0])+1
		tar=row[1]
		block=row[2]
		tarType=str(tar)[0]
		rc='rc'+str(int(''.join(ele for ele in tar if ele.isdigit())))
		correctResp=correctResponsesHelper(tarType)
		tup=(block, rc,tarType, tar, correctResp)
		
		if block == 'A':
			blockA.append(tup)
		if block == 'B':
			blockB.append(tup)
		if block == 'C':
			blockC.append(tup)
		if block == 'D':
			blockD.append(tup)
	
	return (blockA, blockB, blockC, blockD)

'''
constaints for correct responses:
    4 successive trials: cannot have same correct responses
    if return true, which means 5 successive trials have same correct Response
    need to regenerate
'''
def respConstraints(rand_block):
	passTest=True
	step = 5
#	for block in cond_blocks:
	i = 0
	while i < (len(rand_block)-step+1): # iterate through randomized ref number list
		tempList = [resp[2] for resp in rand_block[i:i+step]]
#		print ('test03:',tempList) : ['n', 'z', 'n', 'n', 'z']
		# get corr responses for each target type
		correctRespList=[correctResponsesHelper(targetType) for targetType in tempList]
#		print ('test02:',correctRespList)
		if (correctRespList.count(YES) > 4) | (correctRespList.count(NO) > 4):
			passTest = False
			break
		i=i+1
	return passTest


'''
this helper function is to identify the correct answer depending 
on the target type
For example: 
    r,o - YES 'z'
    s,u - NO 'n'
'''
def correctResponsesHelper(targetType):
    correctResponse = ''
    if targetType=='r': 
        correctResponse = YES   #z
    if targetType=='o': 
        correctResponse = YES   #z
    if targetType=='s': 
        correctResponse = NO    #n
    if targetType=='u':
        correctResponse = NO    #n
    return correctResponse


'''
	This function is to export randomized trials into a text file
'''
def exportRandBlocks(randomizedBlocks, filepath):
	dataFile=open(filepath, 'w')
	dataColName=('\t'.join(['trialNum','block','RefCat','targetType','target','correctResp']) +'\n')
	dataFile.write(dataColName)

	# export randomized order
	trialCount=0
	for i in range(len(randomizedBlocks)):
		for j in range(len(randomizedBlocks[i])):
			trialCount=trialCount+1
			row = [str(trialCount)] # trial number
			row.extend([e for e in randomizedBlocks[i][j]])
			dataFile.write('\t'.join(row)+'\n')
	dataFile.close()

'''
This function is to do randomization within each blocks
'''
def shuffleTrials(cond, filepath):
	init=readInit()	# (A,B,C,D)
	for block in init:	# shuffle
		random.shuffle(block)
		# resp constraints
		while not respConstraints(block):	# not pass constrain test
			print ('not pass test: redo shuffle!!!')
			random.shuffle(block)
		print ('pass test!!!')

	rand_blocks=[]
	if cond==1:
		rand_blocks=list(init) #ABCD
	if cond==2:
		rand_blocks=[init[3], init[0], init[1], init[2]] # DABC
	if cond==3:
		rand_blocks=[init[2], init[3], init[0], init[1]] # CDAB
	if cond==4:
		rand_blocks=[init[1], init[2], init[3], init[0]] # BCDA
        
	exportRandBlocks(rand_blocks, filepath)
	return rand_blocks

#shuffleTrials(3, 'trials/test01.txt')
#exportRandBlocks('2', 'trials/test02.txt')
#exportRandBlocks('3', 'trials/test03.txt')
#exportRandBlocks('4', 'trials/test04.txt')
