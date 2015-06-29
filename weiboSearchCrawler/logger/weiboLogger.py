__author__ = 'bfy'

import logging
import datetime

logger = logging.getLogger('weibo')
logger.setLevel(logging.DEBUG)

def setFileHandler():
    now = datetime.datetime.now()
    now = str(now).split(' ')[0]
    fh = logging.FileHandler(r'logs/' + now)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    fh.setLevel(logging.DEBUG)
    return fh

def setConsoleHandler():
    ch = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)

    ch.setLevel(logging.DEBUG)
    return ch

logger.addHandler(setFileHandler())
logger.addHandler(setConsoleHandler())






