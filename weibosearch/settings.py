# Scrapy settings for scrapy_weibo project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'weibosearch'

SPIDER_MODULES = ['weibosearch.spiders']
NEWSPIDER_MODULE = 'weibosearch.spiders'

# scrapy-redis config
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

# Don't cleanup scrapy-redis queues, allows to pause/resume crawls.
SCHEDULER_PERSIST = False
QUEUE_KEY = '%(spider)s:requests'
DUPEFILTER_KEY = '%(spider)s:dupefilter'
SCHEDULER = "weibosearch.scrapy-redis.scheduler.Scheduler"

# pipelines config
ITEM_PIPELINES = {
    'weibosearch.pipelines.MongoDBPipeline': 50,
}

DOWNLOAD_DELAY = 10
LOG_LEVEL = 'INFO'
TIME_DELTA = 30

# read keywords from 'file' or 'db'
BOOTSTRAP = 'db'

# how many feeds can fetch from a item
FEED_LIMIT = 300000