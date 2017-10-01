#!/usr/bin/env python3
import techcrunch

print("testing techcrunch")

tc = techcrunch.ArchiveLoader.load(2017, 9, 25)

print("site name is " + tc.site)
for article in tc.articles:
    print("title is :" + str(article.title))
    print("timestamp is :" + str(article.timestamp))
    print("tags are is :" + str(article.tags))
    print("links are :" + str(article.links))
    print("content is :" + str(article.text))
print("timestamp is " + str(tc.timestamp))
print("url name is " + str(tc.url))
