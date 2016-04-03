#coding=utf-8

import os
import sys
import pickle
import urllib2
from bs4 import BeautifulSoup as bs
from news import News

def getNewsClass(url, typeName):
    page = urllib2.urlopen(url)
    html = page.read()
    soup = bs(html)
    articleBody = soup.find('div', class_ = 'article')
    title = articleBody.find('h1').getText()
    title = title.strip()
    timeStamp = articleBody.find('span', class_ = 'arti_update').getText()
    timeStamp = timeStamp.strip()
    fromWhere = articleBody.find('span', class_ = 'arti_from').getText()
    fromWhere = fromWhere.strip()
    content = ''
    if articleBody.findAll('p', class_ = 'p_text_indent_2'):
        for part in articleBody.findAll('p', class_ = 'p_text_indent_2'):
            content += part.getText().strip()
    if not content and articleBody.find('div', class_ = 'content_old'):
        content = articleBody.find('div', class_ = 'content_old').getText()
    if not content and articleBody.find('div', class_ = 'wp_articlecontent'):
        content = articleBody.find('div', class_ = 'wp_articlecontent').getText()
    content = content.strip()
    if not content:
        print title, url, 'have no content'
    return News(url, typeName, timeStamp, fromWhere, content, title)

def getNewsofType(typeName):
    urls = None
    with open('Url/%s' % typeName, 'r') as inFile:
        urls = pickle.load(inFile)
    newsList = []
    for url in urls:
        if url == '/4d/17/c416a19735/page.htm' or url.startswith('http'):
            continue
        news = getNewsClass('http://news.hit.edu.cn' + url, typeName)
        newsList.append(news)
    os.mkdir('Data')
    with open('Data/%s.obj' % typeName, 'w') as outFile:
        pickle.dump(newsList, outFile)

if __name__ == '__main__':
    newsTypes = ['人才培养','学校要闻','校友之苑','理论学习','媒体看工大','他山之石','时势关注','校园文化','科研在线','国际合作','服务管理','深度策划','综合新闻']
    for newsType in newsTypes:
        getNewsofType(newsType)