# -*- coding: UTF-8 -*-
#!/usr/bin/python

from define import *

def duanyu(keywordsPath, duanyuPath):
    f1 = open(keywordsPath)
    f2 = open(duanyuPath,'w')
    ffenci = open(FENCI_PATH)
    while(True):
        line = f1.readline()
        fenci = ffenci.readline().strip('\n').split(' ')
        if(not line):
            break
        segs = line.strip('\n').split('\t')
        origin = segs[1] #test
        f2.write(segs[0] + '\t' + origin + '\n')  # test
        keyw = segs[3]
        keywList = keyw.split(',')
        tup = ()
        for word in fenci:
            if(word in keywList and word not in tup):
                tup += (word,)
            if(word in ',.!?，。！？' and len(tup)>0):
                #print tup
                #f2.write(segs[0] + '\t' + ','.join(tup)+'\n')
                f2.write(','.join(tup) + '\n') #test
                tup = ()
        if(len(tup)>0):
            f2.write(','.join(tup) + '\n')  # test
            #f2.write(segs[0] + '\t' + ','.join(tup) + '\n')
    f1.close()
    f2.close()



duanyu(KEY_WORDS_PATH, DUANYU_PATH)



