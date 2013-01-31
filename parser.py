#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
from soupselect import select
from urllib2 import urlopen
from pprint import pprint
import json

url = "http://www.kissfm.ua/news.html"

doc = BeautifulSoup(urlopen(url))

structure = []

for comm in select(doc, "div.news-item-content"):
    elem = {}
    for item in select(comm, "a.main-item-title"):
        elem["link"] = item["href"]
        elem["title"] = item.string
        break # there are duplicates of links here
    for item in select(comm, "img"):
        elem["thumb"] = item["src"]
    for item in select(comm, "div.news-block-item-date"):
        elem["date"] = item.string.strip()

    structure.append(elem)

for item  in structure:
    link = "http://www.kissfm.ua%s" % item["link"]
    doc = BeautifulSoup(urlopen(link))

    for comm in select(doc, "div.content"):
        for img in select(comm, "img"):
            item["img"] = img["src"]
            break

        for content in select(comm, "table tbody tr td div"):
             item["content"] = "%s" % content

print json.dumps(structure)
