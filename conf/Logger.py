# -*- coding: UTF-8 -*-
#!/usr/bin/python

import os
import logging.config

from confParser import cf

absDir = os.path.dirname(os.path.realpath(__file__))

#print absDir + "/logger.conf"

logFile = cf.get('path','log_path') + '/log'

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename=logFile, level=logging.DEBUG, format=LOG_FORMAT)

log = logging.getLogger()

'''
logging.config.fileConfig(absDir + "/logger.conf")
log = logging.getLogger("example02")
'''

