__author__ = 'bfy'

from scrapy.conf import settings
from datetime import *

def readTimeRange():
    fetchRange = settings.get('FREQUENCY', 'YESTERDAY')

    if fetchRange.startswith('H'): # if fetch the data of history
        start = settings.get('FETCH_START')
        end = settings.get('FETCH_END')

        start = datetime.strptime(start, '%Y-%m-%d')
        end = datetime.strptime(end, '%Y-%m-%d')

        return (start, end)
    else:
        end = datetime.combine(date.today(), \
            time(0, 0, 0))
        start = end - timedelta(days=1)
        return (start, end)





