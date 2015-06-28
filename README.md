weiboSearchCrawler
===================
A distributed Sina Weibo Search spider based on Scrapy, Redis and MongoDB. And for the crawled page, extract user info, forward info and pictures and so on.

##Reference
[scrapy-redis](https://github.com/darkrho/scrapy-redis)

[weibosearch](https://github.com/tpeng/weibosearch)

[weibo_login](https://github.com/yoyzhou/weibo_login) 

## Installation
    $ sudo apt-get install mongodb
    $ sudo apt-get install redis-server
    $ sudo apt-get install pymongo
    $ sudo pip install -r requirements.txt

## Usage
1. put your keywords in items.txt(just for test for me). Also, you can read keywords from mysql. 
2. `scrapy crawl weibosearch -a username=your_weibo_account -a password=your_weibo_password`
3. you can test the process of parsing locally, see weibosearch/spiders/tests.py for more
3. add another spider with *scrapy crawl weibosearch -a username=another_weibo_account -a password=another_weibo_password*

