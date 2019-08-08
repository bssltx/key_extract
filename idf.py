# -*- coding: UTF-8 -*-
#!/usr/bin/python
import json

import numpy as np


from define import *

import math

def getIdf(originPath,objPath,delimiter):

    wordDict = {}
    f = open(originPath, 'r')

    lineCnt = 0.1

    for line in f:
        lineCnt += 1
        line = line.rstrip('\n')
        words = line.split(delimiter)
        for word in wordDict:
            wordDict[word][2] = 0
        for word in words:
            if(not word):
                continue
            if(wordDict.has_key(word)):
                wordDict[word][0] += 1
                if(wordDict[word][2]==0):
                    wordDict[word][1] += 1
                    wordDict[word][2] = 1
            else:
                wordDict[word] = [1,1,1] #代表totalwordcnt,totalwordlinecnt,if_this_line_has_this_word

    f.close()

    for word in wordDict:
        wordDict[word] = wordDict[word][0:2]

    wordlist = []

    for word in wordDict:
        idf = math.log(lineCnt/wordDict[word][1])
        #wordlist.append(unicode(word + ' ' + str(idf), 'utf-8'))
        wordlist.append(word + ' ' + str(idf))

    tmp = np.array(wordlist)

    np.savetxt(objPath,tmp,'%s')


getIdf(FENCI_PATH,IDF_PATH,' ')


