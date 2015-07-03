class QueryFactory:
  @staticmethod
  def create_query(query):
    return 'http://s.weibo.com/weibo/%s&Refer=g&scope=ori' % query

  @staticmethod
  def create_paging_query(query, page):
    return 'http://s.weibo.com/weibo/%s&page=%d' % (query, page)

  @staticmethod
  def create_timerange_query(query, start, end):
    s = start.strftime('%Y-%m-%d')
    e = end.strftime('%Y-%m-%d')
    return 'http://s.weibo.com/weibo/%s&Refer=g&timescope=custom:%s-0:%s-23&typeall=1' \
           % (query, s, e)


  @staticmethod
  def create_singer_query(query, start, end):
    s = start.strftime('%Y-%m-%d')
    e = end.strftime('%Y-%m-%d')
    return 'http://s.weibo.com/weibo/%s&Refer=g&timescope=custom:%s-0:%s-23&xsort=hot' \
           % (query, s, e)


