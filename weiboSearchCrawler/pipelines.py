#-*- coding: utf-8 -*-
# See: http://doc.scrapy.org/en/0.14/topics/item-pipeline.html
# tpeng <pengtaoo@gmail.com>
#
from scrapy.conf import settings
import pymongo

from weiboSearchCrawler.sina.feeds import Feed


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
            return
             #raise DropItem('Feed.wrap error: %s' % item['html'])

        doc = {
            "keyword": item['keyword'],
            "keywordId": item['keywordId'],
            "weibo_id": feed.weiboId,
            "author": feed.author.format(),
            "forward": [forward.format() for forward in feed.forwardList],
            "content": feed.content,
            "retweets": feed.retweets,
            "replies": feed.replies,
            "pubDate": feed.timestamp,
            "pictureXML": feed.picturesXML,
        }
        if spider.saveIntoDB:
            mongodbId = self.coll.insert(doc)
        return item