# -*- coding: utf-8 -*-
__author__ = 'bfy'

import unittest

from scrapy.http import Response
from scrapy.http import Request

import pipelines
from weiboSearchCrawler.spiders.WeiboSearchSpider import WeiboSearchSpider

class MongoDBPipelineTest(unittest.TestCase):

    def setUp(self):
        self.mongoPipeline = pipelines.MongoDBPipeline()
        self.spider = WeiboSearchSpider(login=False, saveIntoDB=True)
        self.body = open('spiders/tmp.html', 'r').read()

    def tearDown(self):
        self.mongoPipeline.cnx.close()

    def test_process_item(self):
        request = Request(url='http://pat.zju.edu.cn',meta={'keyword': 'scrapy',
                                                            'keywordId': 1,
                                        'start': '2015-06-27 11:00:00',
                                        'end': '2015-06-27 11:00:00',})
        generator = self.spider.parse_page(response=Response(url='', body=self.body, request=request))
        for item in generator:
            res = self.mongoPipeline.process_item(item, self.spider)
        self.assertEqual(True, True)


class JsonPipelineTest(unittest.TestCase):

    def setUp(self):
        self.jsonPipeline = pipelines.JsonPipeline()
        self.spider = WeiboSearchSpider(login=False, saveIntoDB=False)
        self.body = open('spiders/tmp.html', 'r').read()

    def tearDown(self):
        pass


    def test_process_item(self):
        request = Request(url='http://pat.zju.edu.cn',meta={'keyword': '刘德华',
                                                            'keywordId': 1,
                                        'start': '2015-06-27 11:00:00',
                                        'end': '2015-06-27 11:00:00',})
        generator = self.spider.parse_page(response=Response(url='', body=self.body, request=request))
        for item in generator:
            print item
            res = self.jsonPipeline.process_item(item, self.spider)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
