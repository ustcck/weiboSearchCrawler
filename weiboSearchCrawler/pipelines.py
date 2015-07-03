#-*- coding: utf-8 -*-
# See: http://doc.scrapy.org/en/0.14/topics/item-pipeline.html
# tpeng <pengtaoo@gmail.com>
#
from scrapy.conf import settings
import pymongo
import json

from weiboSearchCrawler.sina.feeds import *
from weiboSearchCrawler.utils.readKeywords import *


class MongoDBPipeline(object):

    def __init__(self):
        self.cnx = pymongo.MongoClient(**settings.get('MONGO_CONFIG'))
        db = self.cnx.admin
        db.authenticate("udms", "123456")
        self.coll = self.cnx.Doctopus.WeiboNew

    def process_item(self, item, spider):

        try:
            feed = Feed.wrap(item['html'])
        except Exception, e:
            # TODO: add a log
            return
             #raise DropItem('Feed.wrap error: %s' % item['html'])

        doc = {
            "keyword": item['keyword'],
            "keywordId": item['keywordId'],
            "downDate": item['downDate'],
            "weibo_id": feed.weiboId,
            "author": feed.author.format(),
            "forward": [forward.format() for forward in feed.forwardList],
            "content": feed.content,
            "retweets": feed.retweets,
            "replies": feed.replies,
            "feedFrom": feed.feedFrom.format(),
            "pictureXML": feed.picturesXML,
        }
        if spider.saveIntoDB:
            mongodbId = self.coll.insert(doc)
        return item



class JsonPipeline(object):

    def __init__(self):
        self.keywords = readKeywordsFromSinglersFile()

    def process_item(self, item, spider):
        try:
            feed = Feed.wrap(item['html'])
        except Exception, e:
            return

        fetchDay = str(feed.feedFrom.timestamp).split(' ')[0]
        f = open('../singersData/singerWeibo' + str(fetchDay), 'a')

        result = {}
        result['weiboId'] = self.quoteString(feed.weiboId)
        result['downdate'] = item['downDate'].replace(' ', 'T') + ' '
        result['text'] = self.quoteString(feed.content)

        if Pictures.parseXML(feed.picturesXML) != None:
            result['thumbPicURL'] = self.quoteString(Pictures.parseXML(feed.picturesXML))
            result['OriPicURL'] = result['thumbPicURL'].replace('thumbnail', 'large')
            result['BMidPicURL'] = result['thumbPicURL'].replace('thumbnail', 'bmiddle')

        result['reship'] = str(feed.retweets)
        result['revert'] = str(feed.replies)
        result['hotIndex'] = str(feed.replies + feed.retweets)
        result['site'] = self.quoteString(feed.feedFrom.source)
        tmp = str(feed.feedFrom.timestamp).replace(' ', 'T').split(':')
        result['pubDate'] = tmp[0] + ':' + tmp[1]
        result['singername'] = self.quoteString(item['keyword'])
        result['remoteSingerId'] = self.quoteString(str(item['keywordId']))
        result['otherSingers'] = self.findRelatedSinger(item['keyword'], feed.content)
        resultDump = json.dumps(result, ensure_ascii=False, encoding="utf-8") + '\n'

        f.write(resultDump.encode('utf-8'))
        f.flush()

    def findRelatedSinger(self, name, content):
        otherSingers = ""
        for singer in self.keywords:
            singerId = self.keywords[singer]
            if singer != name and singer in content:
                otherSingers += "'" + singerId + " " + \
                                singer.replace("'", r"\'") + "'" + "|"
        if not otherSingers:
            return "''"
        return otherSingers.rstrip("|")

    def quoteString(self, value):
        return "'" + value.replace("'", r"\'").rstrip('\\') + "'"
