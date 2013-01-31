#!/usr/bin/env python
# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
from soupselect import select
from urllib2 import urlopen
import json
import re

class KissFMParser:
    def __init__(self, pages):
        self.pages = pages
        self.structure = []

    def parse_base(self):
        for page in range(self.pages):
            base_url = "http://www.kissfm.ua/news.html?p=%s" % str(page)
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
            # to remove ... character from url if any
            link = link.replace(u"\u2026", "") 
            doc = BeautifulSoup(urlopen(link))
            for comm in select(doc, "div.content"):
                for img in select(comm, "img"):
                    item["img"] = img["src"]
                    break

                if select(comm, "table tbody tr td div"):
                    for content in select(comm, "table tbody tr td div"):
                        item["content"] = "%s" % content
                else:
                    for content in select(doc, "div.content"):
                        soup = BeautifulSoup(str(content))
                        [s.extract() for s in soup('script')]
                        result = re.sub('<[^<]+?>', '', str(soup))
                        result = result.replace("Поделиться:", "")
                        result = result.replace("fresh news", "")
                        item["content"] = result.strip()

    def engage(self):
        self.parse_base()
        self.parse_inner()
        self.print_json()

    def print_json(self):
        print json.dumps(self.structure)

if __name__ == "__main__":
    parser = KissFMParser(3)
    parser.engage()


