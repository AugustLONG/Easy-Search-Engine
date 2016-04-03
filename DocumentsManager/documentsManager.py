#encoding=utf-8

import pickle
from news import News

class DocumentsManager:
    def __init__(self):
        self.newsTypes = {}.fromkeys(['人才培养','学校要闻','校友之苑','理论学习','媒体看工大','他山之石','时势关注','校园文化','科研在线','国际合作','服务管理','深度策划','综合新闻'], None)
        for newsType in self.newsTypes:
            with open('DocumentsManager/Documents/%s/index.obj' % newsType, 'r') as inputFile:
                indexTuple = pickle.load(inputFile)
                self.newsTypes[newsType] = indexTuple

    def searchDocument(self, docId):
        for newsType in self.newsTypes:
            startId, endId = self.newsTypes[newsType]
            if startId <= docId and docId <= endId:
                thatType = newsType
                break
        with open('DocumentsManager/Documents/%s/%d.obj' % (newsType, docId), 'r') as inputFile:
            document = pickle.load(inputFile)
        return document
