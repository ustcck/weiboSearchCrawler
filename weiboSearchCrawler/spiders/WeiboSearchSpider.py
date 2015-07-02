# -*- coding=utf-8 -*-

from datetime import datetime
import urllib
import re
import json
import logging

from scrapy.conf import settings
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from scrapy.utils.reqser import request_to_dict
from lxml.html import tostring
from bs4 import BeautifulSoup

from weiboSearchCrawler.sina.feeds import SearchPage
from weiboSearchCrawler.items import ScrapyWeiboItem
from weiboSearchCrawler.sina.query import QueryFactory
from weiboSearchCrawler.sina import weiboLogin
from weiboSearchCrawler.sina import _epoch
from weiboSearchCrawler.db import readKeywords
from weiboSearchCrawler.sina import parsePage


class WeiboSearchSpider(CrawlSpider):
    name = 'weiboSpider'
    allowed_domains = ['weibo.com']
    username = 'echobfy@163.com'
    password = 'udms1234'
    cookieFile = 'weibo_login_cookies'
    saveIntoDB = 'True'
    logger = logging.getLogger('weibo')

    def __init__(self, name=None, login=True, saveIntoDB=True, **kwargs):
        super(WeiboSearchSpider, self).__init__(name, **kwargs)
        self.logined = False
        self.saveIntoDB = saveIntoDB

        self.logger.info(' ---> [%-30s] try to login in weibo with username(%s)......'
                         % ('', self.username))

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
            self.logger.info(' ---> [%-30s] login in weibo successfully......' % '')
            self.logined = True

            bootstrap = settings.get('BOOTSTRAP')
            self.logger.info(' ---> [%-30s] read keywords from %s......' % ('', bootstrap))
            # FIXME: use last scheduled time instead of today, otherwise queue filter will not work
            today = datetime.now()

            keywords = readKeywords.readKeywords()
            # TODO: 对于一段时间区间进行爬虫。。。。

            for keyword in keywords:
                start = _epoch()
                url = QueryFactory.create_timerange_query(urllib.quote(keyword.encode('utf8')), start, today)

                self.logger.debug(' ---> [%-30s](%s-%s) send the keyword query to server...' %
                                  (keyword, '', ''))

                request = Request(url=url, callback=self.parse_weibo, meta={
                    'keyword': keyword,
                    'start': start.strftime("%Y-%m-%d %H:%M:%S"),
                    'end': today.strftime("%Y-%m-%d %H:%M:%S"),
                    'last_fetched': today.strftime("%Y-%m-%d %H:%M:%S")})
                yield request
        else:
            self.logger.error(' ---> [%-30s] login failed: errno=%s, reason=%s @@@@@@'
                              % (feedbackJson.get('errno', ''), feedbackJson.get('reason', '')))

    def parse_weibo(self, response):
        keyword = response.meta['keyword']
        start = datetime.strptime(response.meta['start'], "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(response.meta['end'], "%Y-%m-%d %H:%M:%S")
        #open_in_browser(response)
        validHtmlDoc = parsePage.getContent(response.body)
        if validHtmlDoc == None:
            self.logger.warning(' ---> [%-30s] can not find the feed list, maybe structure of weibo if change'
                                % (keyword))
            # TODO: 当出现validHtmlDoc为空的时候说明weibo结构发生了改变，或者该账号被封了。应记录下该response
            return

        soup = BeautifulSoup(validHtmlDoc)

        # there is no weibo about this topic in the timerange.
        if not parsePage.isThereResult(soup):
            self.logger.warning()
            return

        pageNode = soup.find('div', attrs={"node-type": "feed_list_page_morelist"})
        searchPage = SearchPage.wrap(pageNode)

        # request for more pages and parse the first page.
        for i in range(len(searchPage)):
            url = searchPage[i]
            request = Request(url=url, callback=self.parse_page)
            request.meta['keyword'] = keyword
            yield request

        for item in self.parse_page(response):
            yield item


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



