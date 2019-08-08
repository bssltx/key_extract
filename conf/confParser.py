# -*- coding: UTF-8 -*-
#!/usr/bin/python

import ConfigParser
import os

absDir = os.path.dirname(os.path.realpath(__file__))

cf = ConfigParser.ConfigParser()
cf.read(absDir + '/conf.ini')

def getParameter(key,value):
    return cf.get(key,value)

