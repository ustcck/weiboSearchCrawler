__author__ = 'bfy'

import unittest
from scrapy.http import Response
from scrapy.http import Request

from WeiboSearchSpider import WeiboSearchSpider

class WeiboSearchSpiderTest(unittest.TestCase):

    def setUp(self):
        # when testing, we just import the local file and the item parsed should not dump to DB
        self.spider = WeiboSearchSpider(login=False, saveIntoDB=False)
        self.body = open('tmp.html', 'r').read()

    def tearDown(self):
        pass

    def test_parse_weibo(self):
        request = Request(url='http://pat.zju.edu.cn',meta={'keyword': 'scrapy',
                                        'keywordId': 1,
                                        'start': '2015-06-27 11:00:00',
                                        'end': '2015-06-27 11:00:00',})
        generator = self.spider.parse_weibo(response=Response(url='', body=self.body, request=request))
        for obj in generator:
            pass

        self.assertEqual(True, True)


    def test_parse_page(self):
        request = Request(url='http://pat.zju.edu.cn',meta={'keyword': 'scrapy',
                                        'keywordId': 1,
                                        'start': '2015-06-27 11:00:00',
                                        'end': '2015-06-27 11:00:00',})
        generator = self.spider.parse_page(response=Response(url='', body=self.body, request=request))
        for obj in generator:
            pass
        self.assertEqual(True, True)

    def test_parse(self):
        response = Response(url='', body='parent.sinaSSOController.'
                                         'feedBackUrlCallBack({"result":true,"userinfo":'
                                         '{"uniqueid":"5341604164","userid":null,"displayname":'
                                         'null,"userdomain":"?wvr=5&lf=reg"}})')
        generator = self.spider.parse(response)

        for obj in generator:
            print obj



if __name__ == '__main__':
    unittest.main()
