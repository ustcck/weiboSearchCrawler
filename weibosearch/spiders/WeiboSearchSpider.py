#coding=utf-8
# weibosearch spider
# tpeng <pengtaoo@gmail.com>
#
from datetime import datetime
import urllib
import re
import json

from scrapy import log
from scrapy.conf import settings
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from scrapy.utils.reqser import request_to_dict
from lxml.html import tostring
from bs4 import BeautifulSoup

from weibosearch.sina.feeds import SearchPage
from weibosearch.items import ScrapyWeiboItem
from weibosearch.sina.query import QueryFactory
from weibosearch.sina import weiboLogin
from weibosearch.sina import _epoch
from weibosearch.db import readKeywords
from weibosearch.sina import parsePage


class WeiboSearchSpider(CrawlSpider):
    name = 'weibosearch'
    allowed_domains = ['weibo.com']
    username = 'echobfy@163.com'
    password = 'udms1234'
    cookieFile = 'weibo_login_cookies'
    saveIntoDB = 'True'

    def __init__(self, name=None, login=True, saveIntoDB=True, **kwargs):
        super(WeiboSearchSpider, self).__init__(name, **kwargs)
        self.logined = False
        self.saveIntoDB = saveIntoDB

        self.log('login with %s' % self.username)
        if login:
            login_url = weiboLogin.login(self.username, self.password, self.cookieFile)
            if login_url:
                self.start_urls.append(login_url)

    # only parse the login page
    def parse(self, response):
        if response.body.find('feedBackUrlCallBack') != -1:
            feedbackJson = json.loads(re.search(r'feedBackUrlCallBack\((.*?)\)', response.body, re.I).group(1))
            result = feedbackJson.get('result', '')

        assert result == True
        if result:
            self.logined = True

            bootstrap = settings.get('BOOTSTRAP')
            log.msg('bootstrap from %s' % bootstrap, level=log.INFO)
            # FIXME: use last scheduled time instead of today, otherwise queue filter will not work
            today = datetime.now()

            # you can read keywords to crawl from file or mysql, from file just for test
            if bootstrap == 'file':
                keywords = readKeywords.readKeywordsFromFile()
            else:
                keywords = readKeywords.readKeywordsFromMysql()
            # TODO: 对于一段时间区间进行爬虫。。。。


            for keyword in keywords:
                start = _epoch()
                url = QueryFactory.create_timerange_query(urllib.quote(keyword.encode('utf8')), start, today)
                print url
                request = Request(url=url, callback=self.parse_weibo, meta={
                    'keyword': keyword,
                    'start': start.strftime("%Y-%m-%d %H:%M:%S"),
                    'end': today.strftime("%Y-%m-%d %H:%M:%S"),
                    'last_fetched': today.strftime("%Y-%m-%d %H:%M:%S")})
                yield request
        else:
            self.log('login failed: errno=%s, reason=%s' % (''), (''))

    def parse_weibo(self, response):
        keyword = response.meta['keyword']
        start = datetime.strptime(response.meta['start'], "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(response.meta['end'], "%Y-%m-%d %H:%M:%S")
        #open_in_browser(response)
        validHtmlDoc = parsePage.getContent(response.body)
        if validHtmlDoc == None:
            return

        soup = BeautifulSoup(validHtmlDoc)
        pageNode = soup.find('div', attrs={"node-type": "feed_list_page_morelist"})
        searchPage = SearchPage.wrap(pageNode)

        # parse the first page and then parse the next pages.
        request = Request(url=response.url, callback=self.parse_page,
                          meta={'keyword': keyword,}, dont_filter=True)
        yield request
        for i in range(len(searchPage)):
            url = searchPage[i]
            request = Request(url=url, callback=self.parse_page)
            request.meta['keyword'] = keyword
            yield request

    # parse single weibo page
    def parse_page(self, response):
        validHtmlDoc = parsePage.getContent(response.body)
        if validHtmlDoc == None:
            return
        print response.url
        soup = BeautifulSoup(validHtmlDoc)
        persons = soup.find_all('div', attrs={"class": "WB_cardwrap S_bg2 clearfix"})

        for person in persons:
            item = ScrapyWeiboItem()
            item['html'] = str(person)
            item['keyword'] = response.meta['keyword']
            yield item



