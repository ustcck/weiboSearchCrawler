# Scrapy settings for scrapy_weibo project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'weiboSearchCrawler'

SPIDER_MODULES = ['weiboSearchCrawler.spiders']
NEWSPIDER_MODULE = 'weiboSearchCrawler.spiders'

# scrapy_redis config
REDIS_CONFIG = {
    'host': '10.13.91.251',
    'port': 6379,
}

# mysql config
MYSQL_CONFIG = {
    "db": "D-Insight-2",
    "user": "udms",
    "passwd": "123456",
    "host": "10.13.91.251",
    "port": 3306,
    "charset": "utf8",
}

# mongodb config
MONGO_CONFIG = {
    'host': '10.13.91.251',
    'port': 27017,
}

# Don't cleanup scrapy_redis queues, allows to pause/resume crawls.
SCHEDULER_PERSIST = False
QUEUE_KEY = '%(spider)s:requests'
DUPEFILTER_KEY = '%(spider)s:dupefilter'
SCHEDULER = "weiboSearchCrawler.scrapy_redis.scheduler.Scheduler"

# pipelines config
ITEM_PIPELINES = {
    'weiboSearchCrawler.pipelines.MongoDBPipeline': 50,
}

DOWNLOAD_DELAY = 10
LOG_LEVEL = 'INFO'

# read keywords from 'file' or 'utils'
BOOTSTRAP = 'file'

# fetch time range HISTORY or YESTERDAY
FREQUENCY = 'YESTERDAY'
# the range is in [FETCH_START, FETCH_END)
FETCH_START = '2015-06-01'
FETCH_END = '2015-06-25'
