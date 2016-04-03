#encoding=utf-8

import os
import pickle
from news import News

newsTypes = ['人才培养','学校要闻','校友之苑','理论学习','媒体看工大','他山之石','时势关注','校园文化','科研在线','国际合作','服务管理','深度策划','综合新闻']

docId = 1

os.mkdir('Documents')

for newsType in newsTypes:
    os.mkdir('Documents/%s' % newsType)
    with open('../DataCrawer/Data/%s.obj' % newsType, 'r') as inputFile:
        newsObjs = pickle.load(inputFile)
    counter = 0
    startId = docId
    for newsObj in newsObjs:
        with open('Documents/%s/%d.obj' % (newsType, docId), 'w') as outFile:
            pickle.dump(newsObj, outFile)
        counter += 1
        docId += 1
    endId = docId - 1
    with open('Documents/%s/index.obj' % newsType, 'w') as outFile:
        index = (startId, endId)
        pickle.dump(index, outFile)
    print 'finish %d documents.' % counter
    print index
