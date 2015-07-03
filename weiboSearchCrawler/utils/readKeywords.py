__author__ = 'bfy'

import MySQLdb
import codecs
from scrapy.conf import settings

def readKeywordsFromMysql():
    cnx = MySQLdb.connect(**settings.get('MYSQL_CONFIG'))
    cursor = cnx.cursor()
    cursor.execute('select * from topic')
    keywords = []

    for item in cursor:
        if item[2] == None or item[2] == '': continue

        words = item[2].split(' ')
        for word in words:
            if word != '':
                keywords.append(word)
    cnx.close()

    return keywords


def readKeywordsFromFile():
    keywords = []

    lines = tuple(codecs.open('../../items.txt', 'r', 'utf-8'))
    for line in lines:
        if line.startswith("#"): continue
        keywords.append(line)

    return keywords


# you can read keywords to crawl from file or mysql, from file just for test
def readKeywords():
    keywords = []

    bootstrap = settings.get('BOOTSTRAP', 'file')
    if bootstrap == 'file':
        keywords = readKeywordsFromFile()
    else:
        keywords = readKeywordsFromMysql()
    return keywords
