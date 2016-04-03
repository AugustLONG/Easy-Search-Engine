#coding=utf-8

import os
import sys
import pickle
import urllib2
from bs4 import BeautifulSoup as bs

def getNewsUrlsInPage(url):
    page = urllib2.urlopen(url)
    html = page.read()
    soup = bs(html)
    nextPageUrl = soup.find('a', class_ = 'next').get('href')
    newsSpans = soup.findAll('span', class_ = 'Article_Title')
    newsLinks = []
    for newsSpan in newsSpans:
        newsLink = newsSpan.find('a').get('href')
        newsLinks.append(newsLink)
    noend = True if nextPageUrl != 'javascript:void(0);' else False
    return newsLinks, nextPageUrl, noend

def getNewsUrls(startUrl, typeName):
    newsUrls = []
    print 'start crawling %s' % typeName
    newsUrlsInPage, nextPageUrl, noend = getNewsUrlsInPage(startUrl)
    print 'get %d urls.' % len(newsUrlsInPage)
    newsUrls.extend(newsUrlsInPage)
    while noend:
        nextPageUrl = 'http://news.hit.edu.cn' + nextPageUrl
        print 'start crawling %s' % nextPageUrl
        newsUrlsInPage, nextPageUrl, noend = getNewsUrlsInPage(nextPageUrl)
        print 'get %d urls.' % len(newsUrlsInPage)
        if newsUrlsInPage:
            newsUrls.extend(newsUrlsInPage)
    os.mkdir('Url')
    with open('Url/%s' % typeName, 'w') as outFile:
        pickle.dump(newsUrls, outFile)
    print '%s %d urls OK.' % (typeName, len(newsUrls))
    return newsUrls

if __name__ == '__main__':
    newsTypes = ['人才培养','学校要闻','校友之苑','理论学习','媒体看工大','他山之石','时势关注','校园文化','科研在线','国际合作','服务管理','深度策划','综合新闻']

    urls = ['http://news.hit.edu.cn/81/list.htm',
    'http://news.hit.edu.cn/xxyw/list.htm','http://news.hit.edu.cn/86/list.htm',
    'http://news.hit.edu.cn/215/list.htm','http://news.hit.edu.cn/87/list.htm',
    'http://news.hit.edu.cn/92/list.htm','http://news.hit.edu.cn/88/list.htm',
    'http://news.hit.edu.cn/85/list.htm','http://news.hit.edu.cn/82/list.htm',
    'http://news.hit.edu.cn/84/list.htm','http://news.hit.edu.cn/83/list.htm',
    'http://news.hit.edu.cn/sdch/list.htm','http://news.hit.edu.cn/zhxw/list.htm',
    ]

    for startUrl, typeName in zip(urls, newsTypes):
        getNewsUrls(startUrl, typeName)


