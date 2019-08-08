# encoding: utf-8

from conf.confParser import cf

CODE_PATH = cf.get('path','work_path')
DATA_PATH = cf.get('path','data_path')

# data
USER_WORS_PATH = CODE_PATH + '/data/userWords'
STOP_WORD_PATH = CODE_PATH + '/data/stopWords2'

ORIGIN_PATH = DATA_PATH + '/origin'
IDF_PATH = DATA_PATH + '/idf'
FENCI_PATH = DATA_PATH + '/fenci'
TFIDF_PATH = DATA_PATH + '/tfidf'
TEXTRANK_PATH = DATA_PATH + '/textrank'
FP_GROWTH_PATH = DATA_PATH + '/fp_growth'
KEY_WORDS_PATH = DATA_PATH + '/keywords'

DUANYU_PATH = DATA_PATH + '/duanyu'



