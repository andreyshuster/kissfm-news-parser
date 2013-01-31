#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
from soupselect import select
from urllib2 import urlopen
from pprint import pprint
import json

class KissFMParser:
    def __init__(self):
        self.structure = []

    def parse_base(self):
        base_url = "http://www.kissfm.ua/news.html"
        doc = BeautifulSoup(urlopen(base_url))
        for comm in select(doc, "div.news-item-content"):
            elem = {}
            for item in select(comm, "a.main-item-title"):
                elem["link"] = item["href"]
                elem["title"] = item.string
            for item in select(comm, "img"):
                elem["thumb"] = item["src"]
            for item in select(comm, "div.news-block-item-date"):
                elem["date"] = item.string.strip()

            self.structure.append(elem)

    def parse_inner(self):
        for item  in self.structure:
            link = "http://www.kissfm.ua%s" % item["link"]
            doc = BeautifulSoup(urlopen(link))
            for comm in select(doc, "div.content"):
                for img in select(comm, "img"):
                    item["img"] = img["src"]
                    break
            for content in select(comm, "table tbody tr td div"):
                item["content"] = "%s" % content

    def run(self):
        self.parse_base()
        self.parse_inner()
        print self.structure

if __name__ == "__main__":
    parser = KissFMParser()
    parser.run()


