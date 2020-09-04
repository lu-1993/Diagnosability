'''
/**
 * The file to computer the distance from initial state to every other transition.
 * The initial state is default by 1.

 * Also, this file also computer the min distance from the first fault to initial state
 *
 * @author Lulu HE
 * @Email helulu@lri.fr
**/
'''

import os
import re

# coding = utf-8
# -*- coding: cp936 -*-

#orimodel-indexmodel
fileori = open('model.txt', 'r')
fileindex = open('indexmodel.txt','w')

line = fileori.readlines()
fileindex.write(line[0])

from collections import defaultdict



# dict : transindex  key: distance value: transitions
# note: every transition only in one key, this distance is min of all possible distance for this transition(because cycle)
transindex = defaultdict(list)



# the transition which from initial state (1). the distance of this transition is 1.
for i in range(1, len(line)):
    if line[i].split(' ')[0] == '1' :
        transindex[str(1)].append(line[i])
        line[i] = '0 0 0\n'


# line[0] is parameter

parameter = line[0]
bound = int(line[0].split(' ')[1])
k = line[0].split(' ')[3]

nqclist = []
qulist = []
indexlen = [len(transindex[str(1)])]

for f in range (2,bound+2):
    for i in range(1, len(line)):
        for j in range(0, len(transindex[str(f-1)])):
            if line[i].split(' ')[0] == transindex[str(f-1)][j].split(' ')[2].split('\n')[0]:
                nqclist.append(line[i])
                qulist = list(set(nqclist))
                transindex[str(f)]=qulist
                line[i] = '0 0 0\n'
    indexlen.append(len(qulist))
    nqclist = []
    qulist = []

# order transitions and write to fileindex <file>indexmodel.txt</file>
for i in range (1,bound):
    for j in range(0,len(transindex[str(i)])):
        fileindex.write(transindex[str(i)][j-1])




# computer the min distance from the first fault to initial state
for value in transindex.values():
    for item in value:
        if 'f' in item:
            for key in transindex.keys():
                if value == transindex[key]:
                    min_f_distance = key
                    #print("The min distance from initial state to first fault is:", min_f_distance)
                    break
            else:
                continue
            break
    else:
        continue
    break


fileori.close()
fileindex.close()



# creat dict to stored all transition by key is start state.
dict_start_key = defaultdict(list)
dict_end_key = defaultdict(list)
dict_event_key = defaultdict(list)
file = open("model.txt","r")
list_trans = file.readlines()

for i in range(1,len(list_trans)):


    start_state = list_trans[i].split(" ")[0]
    event = list_trans[i].split(" ")[1]
    end_state = list_trans[i].split(" ")[2].split("\n")[0]
    dict_start_key[start_state].append(list_trans[i])
    dict_end_key[end_state].append(list_trans[i])
    dict_event_key[event].append(list_trans[i])


file.close()




