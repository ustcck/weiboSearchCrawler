__author__ = 'bfy'

import unittest
from readKeywords import readKeywordsFromMysql
from readKeywords import readKeywordsFromFile

class ReadKeywordsTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_read_keywords_from_mysql(self):
        keywords = readKeywordsFromMysql()
        print keywords


if __name__ == '__main__':
    unittest.main()
