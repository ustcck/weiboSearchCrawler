#-*- coding: utf-8 -*-
# A weibo parser.
#
# tpeng <pengtaoo@gmail.com>
# 2012/9/21
#
from datetime import datetime
import re
import sys
import xml.dom.minidom as Dom

from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')


class SearchPage():
    def __init__(self, values):
        if values is None or len(values) == 0:
            self.values = []
        else:
            self.values = values

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        return self.values[key]

    def __iter__(self):
        return iter(self.values)

    @staticmethod
    def wrap(morePageNode):
        if morePageNode == None: return []
        values = []
        for linkNode in morePageNode.find_all('a'):
            morelink = linkNode.get('href')
            if morelink.startswith('/'):
                morelink = '%s%s' % ('http://s.weibo.com', morelink)
                values.append(morelink)
        return SearchPage(values)


# the author info
class Author():
    def __init__(self, userId, userName, userHomepageUrl, userImgUrl):
        self.userId = userId
        self.userName = userName
        self.userHomepageUrl = userHomepageUrl
        self.userImgUrl = userImgUrl

    @staticmethod
    def wrap(html):
        soup = BeautifulSoup(html)
        userName = soup.find('a')['title']
        userHomepageUrl = soup.find('a')['href']
        userImgUrl = soup.find('a').find('img')['src']
        userId = re.search('id=(\d+)&', soup.find('a').find('img')['usercard'], re.I).group(1)

        return Author(userId, userName, userHomepageUrl, userImgUrl)

    def format(self):
        dictOfAuthor = {}
        dictOfAuthor['userId'] = self.userId
        dictOfAuthor['userName'] = self.userName
        dictOfAuthor['userHomepageUrl'] = self.userHomepageUrl
        dictOfAuthor['userImgUrl'] = self.userImgUrl
        return dictOfAuthor

    def __str__(self):
        return 'Author(userId=%s, userName=%s)' % (self.userId, self.userName)


# the forward info
class Forward():
    def __init__(self, weiboId, userName, content):
        self.weiboId = weiboId
        self.userName = userName
        self.content = content

    @staticmethod
    def wrap(html):
        soup = BeautifulSoup(html).find('div', attrs={"node-type": "feed_merge_list_item"})
        weiboId = soup.get('mid')

        contentNode = soup.find('span', attrs={"node-type": "feed_list_forwardContentAgg"})
        userName = contentNode.get('nick-name')
        content = contentNode.get_text()

        return Forward(weiboId, userName, content)

    def format(self):
        dictOfForward = {}
        dictOfForward['weiboId'] = self.weiboId
        dictOfForward['userName'] = self.userName
        dictOfForward['content'] = self.content
        return dictOfForward

    def __str__(self):
        return 'Forward(weiboId=%s, userName=%s)' % (self.weiboId, self.userName)

# feed_from info
class FeedFrom():
    def __init__(self, timestamp, source):
        self.timestamp = timestamp
        self.source = source

    @staticmethod
    def wrap(html):
        soup = BeautifulSoup(html)

        timeAndSourceNode = soup.find_all('a')
        time = timeAndSourceNode[0]['date']
        timestamp = datetime.fromtimestamp(long(time) / 1000)
        source = timeAndSourceNode[1].get_text()

        return FeedFrom(timestamp, source)

    def format(self):
        dictOfFeedFrom = {}
        dictOfFeedFrom['pubDate'] = self.timestamp
        dictOfFeedFrom['source'] = self.source
        return dictOfFeedFrom

    def __str__(self):
        return 'FeedFrom(pubDate=%s, source=%s)' % (self.timestamp, self.source)


class Pictures():
    def __init__(self, pictureList):
        self.pictureList = pictureList

    @staticmethod
    def filter(tag):
        return tag.name == 'img' and tag.has_attr('action-type')

    @staticmethod
    def wrap(html):
        pictureList = []
        soup = BeautifulSoup(html)
        picturesNode = soup.find_all(Pictures.filter)
        for pt in picturesNode:
            pictureList.append(pt.get('src'))

        return Pictures(pictureList)

    @staticmethod
    def formatXML(picturesList):
        pictures = []
        for i in picturesList:
            pictures.extend(i.pictureList)

        doc = Dom.Document()
        rootNode = doc.createElement('Picture')
        doc.appendChild(rootNode)

        index = 1
        for picture in pictures:
            pNode = doc.createElement('img%d' % index)
            pNode.setAttribute('url', picture)
            pNode.setAttribute('path', '')
            rootNode.appendChild(pNode)
        return doc.toprettyxml(indent='\t', newl='\n', encoding='utf-8')

    @staticmethod # get the first url of pictureXML
    def parseXML(xml):
        doc = Dom.parseString(xml)
        root = doc.documentElement
        firstImg = root.getElementsByTagName('img1')
        if not firstImg: return None
        return firstImg[0].getAttribute('url')

    def __str__(self):
        return 'Picture(numberOfPicture=%d)' % len(self.pictureList)


class Feed():

    def __init__(self, weiboId, author, forwardList, content,
                 picturesXML, retweets, replies, feedFrom):
        self.weiboId = weiboId
        self.author = author
        self.forwardList = forwardList
        self.content = content
        self.picturesXML = picturesXML
        self.retweets = retweets
        self.replies = replies
        self.feedFrom = feedFrom

    @staticmethod
    def wrap(html):
        replies = retweets = 0
        forwardList = []
        pictureList = []

        soup = BeautifulSoup(html)
        feedAction = soup.find('div', class_="feed_action clearfix").get_text()

        author = Author.wrap(str(soup.find('div', class_="face")))
        weiboId = soup.find('div', attrs={"action-type": "feed_list_item"}).get('mid')
        content = soup.find('p', attrs={"node-type": "feed_list_content"}).get_text()


        # get retweets and replies
        retweetsMatch = re.search(ur'转发(\d+)', feedAction, re.M | re.I | re.U)
        if retweetsMatch:
            retweets = int(retweetsMatch.group(1))
        repliesMatch = re.search(ur'评论(\d+)', feedAction, re.M | re.I | re.U)
        if repliesMatch:
            replies = int(repliesMatch.group(1))

        # get the time and the source of weibo
        feedFromNode = soup.find('div', class_="feed_from W_textb")
        feedFrom = FeedFrom.wrap(str(feedFromNode))

        # get the forwards
        forwardsNode = soup.find('div', attrs={"node-type": "feed_merge_lists"})
        if forwardsNode != None:
            forwards = forwardsNode.find_all('div', attrs={"node-type": "feed_merge_list_item"})
            for forward in forwards:
                forwardList.append(Forward.wrap(str(forward)))

        # get the media list
        mediaNode = soup.find('div', attrs={"node-type": "feed_list_media_prev"})
        if mediaNode != None:
            medias = mediaNode.find_all('div', class_="media_box")
            for media in medias:
                pictureList.append(Pictures.wrap(str(media)))
        picturesXML = Pictures.formatXML(pictureList)

        return Feed(weiboId, author, forwardList, content, picturesXML, retweets, replies, feedFrom)

    def __str__(self):
        return 'Feed(weiboId=%s, replies=%s, retweets=%s, feedFrom=%s, ' \
                    'author=%s, forwardList=%s, content=%s, picturesXML=%s)' \
               % (self.weiboId, self.replies, self.retweets, self.feedFrom,
                  self.author, ' '.join(str(f) for f in self.forwardList),
                  self.content, self.picturesXML)
