# -*- coding: UTF-8 -*-
#!/usr/bin/python

import json
import math

import fp_growth
import numpy as np
import chardet
import jieba.analyse
from define import *





def fenci(originPath, objPath, contentNo):
    f1 = open(originPath)
    f2 = open(objPath, 'w')
    for line in f1:
        segList = []
        if not line:
            aa=1
        else:
            content = line.strip('\n').split('\t')[contentNo]
            tmpList = jieba.cut(content)
            for word in tmpList:
                segList.append(word.encode('utf-8'))
        fenciLine = ' '.join(segList)
        f2.write(fenciLine + '\n')
    f1.close()
    f2.close()


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



'''
def getfenci(originPath, fenciPath):
    f1 = open(originPath)
    f2 = open(fenciPath, 'w')
    for line in f1:
        fenciLine = line.strip().split('\t')[3]
        f2.write(fenciLine+'\n')
    f1.close()
    f2.close()
'''

#originTextPath = pathPre + 'unclassified'
#fenciPath = pathPre + 'unclassified_fenci'



#=======tf-idf========

def getTfidf(originTextPath, contentNo, tfidfPath):
    f1 = open(originTextPath)
    f2 = open(tfidfPath, 'w')
    for line in f1:
        wordList = []
        if not line:
            aa = 1
        else:
            content = line.strip('\n').split('\t')[contentNo]
            tags = jieba.analyse.extract_tags(content, topK=20, allowPOS=('n','a','us'))
            for word in tags:
                wordList.append(word.encode('utf-8'))
        tfidfLine = ' '.join(wordList)
        f2.write(tfidfLine+'\n')
    f1.close()
    f2.close()



#=========text-rank===========
def getTextRank(originPath, textrankPath, contentNo):
    f1 = open(originPath)
    f2 = open(textrankPath, 'w')
    for line in f1:
        wordList = []
        if not line:
            aa = 1
        else:
            content = line.strip('\n').split('\t')[contentNo]
            tags = jieba.analyse.textrank(content, topK=20, allowPOS=('ns', 'n', 'vn', 'v','a','d','us'), withWeight=False)
            for word in tags:
                wordList.append(word.encode('utf-8'))
        tfidfLine = ' '.join(wordList)
        f2.write(tfidfLine + '\n')
    f1.close()
    f2.close()



#=========fp-growth=========
def getFpgrowth(sourcePath, seporator):
    f1 = open(sourcePath)
    retDict = {}
    transactions = []
    for line in f1:
        line = line.strip('\n')
        # transactions.append([r.encode('utf-8') for r in line.split(' ')])
        transactions.append(line.split(seporator))
    frequentSet = fp_growth.find_frequent_itemsets(transactions, 10, include_support=True)
    for item in frequentSet:
        if not item:
            break
        if len(item[0]) == 2 and '' not in item[0] and ' ' not in item[0]:
            for i in (0, 1):
                retDict[item[0][i]] = 1
    f1.close()
    return retDict



#=========得到完整dict===========
def getDict(fpSourcePath, fpSep, tfidfPath):
    retDict = getFpgrowth(fpSourcePath, fpSep)
    f1 = open(tfidfPath)
    for line in f1:
        if not line:
            continue
        ll = line.split(' ')
        for word in ll:
            retDict[word] = 1
    f1.close()
    uselessWords = ['还有', '老师','老师上课', '孩子','小朋友', '感觉', '上课', '课程', '基本', '发现', '教师', '一节课', '有点', '貌似', '给予', '直到', '能够', '予以','就让', '一节', '即使']
    for word in uselessWords:
        if (retDict.has_key(word)):
            retDict.pop(word)
    return retDict


#=========获取key words=========
def getKeywords(originPath, contentNo, objPath, wordDic):
    f1 = open(originPath)
    f2 = open(objPath, 'w')
    for line in f1:
        alternativeWords = []
        lineList = line.strip().split('\t')
        content = lineList[contentNo]
        words = jieba.cut(content)
        for word in words:
            word = word.encode('utf-8')
            if (wordDic.has_key(word)):
                alternativeWords.append(word)
        if (len(alternativeWords) < 4):
            tags = jieba.analyse.extract_tags(content)
        else:
            tags = jieba.analyse.textrank(''.join(alternativeWords), topK=20, allowPOS=('n', 'vn', 'v','us'))
            if (tags > 4):
                tags = jieba.analyse.extract_tags(''.join(tags), allowPOS=('ns', 'n', 'vn', 'v', 'a','us'))
        #print line.split()
        #tmp = unicode(line.split(), 'utf-8') + '\t' + ','.join(tags) + u'\n'
        tmp = unicode(lineList[0],'utf-8') + '\t' + unicode(lineList[contentNo],'utf-8')  \
              + '\t' + ','.join([unicode(i,'utf-8') for i in alternativeWords]) + '\t' + ','.join(tags) + '\n'
        tmp = tmp.encode('utf-8')
        f2.write(tmp)
    f1.close()
    f2.close()




#=========main==============

columnNo = 1

jieba.load_userdict(USER_WORS_PATH)

fenci(ORIGIN_PATH,FENCI_PATH,columnNo)
getIdf(FENCI_PATH,IDF_PATH,' ')

try:
    jieba.analyse.set_idf_path(IDF_PATH)
    print('add idf error!')
except Exception:
    jieba.analyse.set_idf_path(IDF_PATH)

getTfidf(ORIGIN_PATH, columnNo, TFIDF_PATH)
getTextRank(ORIGIN_PATH, TEXTRANK_PATH, columnNo)


wordDic = getDict(TEXTRANK_PATH, ' ', TFIDF_PATH)

getKeywords(ORIGIN_PATH, columnNo, KEY_WORDS_PATH, wordDic)


