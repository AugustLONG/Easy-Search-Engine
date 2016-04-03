#encoding=utf-8

import re
import pickle
import cPickle
from news import News
from invertedIndex import InvertedIndex

class BTreeNode(object):
    def __init__(self, isLeaf = True):
        self.isLeaf = isLeaf
        self.keys = []
        self.childs = []
    def isFull(self):
        t = 200
        return len(self.keys) == 2 * t - 1
    def insertKey(self, newKey):
        self.keys.append(newKey)
        j = len(self.keys) - 2
        while j >= 0 and self.keys[j] > newKey:
            self.keys[j + 1] = self.keys[j]
            j -= 1
        self.keys[j + 1] = newKey
    def getCorrectChild(self, newKey):
        if self.isLeaf:
            return -1
        j = len(self.keys) - 1
        while j >= 0 and self.keys[j] > newKey:
            j -= 1
        return j + 1

    def isKeyExist(self, key):
        return key in self.keys
    
    def midKey(self):
        return self.keys[len(self.keys) / 2]
    
    def insertNoFull(self, newKey):
        if self.isLeaf:
            self.insertKey(newKey)
        else:
            childPos = self.getCorrectChild(newKey)
            if self.childs[childPos].isFull():
                self.splitChild(self.childs[childPos], childPos)
                if self.keys[childPos] < newKey:
                    childPos += 1
            self.childs[childPos].insertNoFull(newKey)

    def createKeyValue(self, wordPosition):
        self.keyValue = {}
        values = [wordPosition[key] for key in self.keys]
        for k, v in zip(self.keys, values):
            self.keyValue[k] = v
    
    def splitChild(self, child, i):
        parent = self
        midPos = len(child.keys) / 2
        midKey = child.midKey()
        newRightChild = BTreeNode(child.isLeaf)
        newRightChild.keys = child.keys[midPos + 1: ]
        newRightChild.childs = child.childs[midPos + 1: ]
    
        child.keys = child.keys[: midPos]
        child.childs = child.childs[: midPos + 1]
    
        parent.keys.insert(i, midKey)
        parent.childs.insert(i + 1, newRightChild)
        parent.isLeaf = False

class BTree(object):
    def __init__(self):
        self.root = BTreeNode()
    
    def insert(self, newKey):
        if self.root.isFull():
            newRoot = BTreeNode(False)
            newRoot.childs = [self.root]
            newRoot.splitChild(self.root, 0)
            self.root = newRoot
        self.root.insertNoFull(newKey)
    
    def saveAsFileSystem(self, wordPosition):
        import os
        queue = [(self.root, 'BTreeRoot')]
        while queue:
            top = queue.pop(0)
            node, savePwd = top[0], top[1]
            os.mkdir(savePwd)
            for i, child in enumerate(node.childs):
                newAdd = (child, '%s/%d' % (savePwd, i))
                queue.append(newAdd)
            node.childs = None
            node.createKeyValue(wordPosition)
            with open('%s/node' % savePwd, 'w') as outFile:
                cPickle.dump(node, outFile)

def buildInvertedIndex4ContentOfOneDoc(docId, unicodeText):
    textSize = len(unicodeText)
    #init inverted index
    invertedIndex = InvertedIndex()
    #handle english word
    englishWordMatchList = re.finditer(r'[a-zA-Z]+', unicodeText)
    for englishWordMatch in englishWordMatchList:
        word = englishWordMatch.group()
        position = englishWordMatch.span()
        invertedIndex.addWord(word, position[0], docId)
    #handle chinese word
    isChinese = lambda uchar: (uchar >= u'\u4e00' and uchar <= u'\u9fa5')
    i = 0
    while i < textSize - 1:
        while i < textSize - 1 and (not isChinese(unicodeText[i]) or not isChinese(unicodeText[i + 1])):
            i += 1
        if i < textSize - 1:
            word, position = unicodeText[i: i + 2], i
            invertedIndex.addWord(word, position, docId)
            i += 1
    #handle OK.
    return invertedIndex

def buildInvertedIndex4OneDoc(docPath, docId):
    with open(docPath, 'r') as inputFile:
        document = pickle.load(inputFile)
    content = document.title + unicode('。', 'utf-8') + document.content
    return buildInvertedIndex4ContentOfOneDoc(docId, content)

def merge2FinalInvertedIndex(invertedIndexList):
    print 'now merge sub inverted index...'
    prevInvertedIndex = invertedIndexList[0]
    counter = 1
    for index in invertedIndexList[1:]:
        prevInvertedIndex.mergeFromOtherIndex(index)
        counter += 1
    print 'merge sub invertedindex OK.'
    return prevInvertedIndex
    #save by word

def saveFinalInvertedIndexAsFile(invertedIndex):
    print 'going to save inverted index...'
    with open('Inverted Index.txt', 'w') as outFile:
        wordPosition = invertedIndex.save2File(outFile)
    print 'save inverted index OK.'
    print 'create Btree...'
    btree = BTree()
    allWords = invertedIndex.getWords()
    for word in allWords:
        btree.insert(word)
    btree.saveAsFileSystem(wordPosition)
    print 'save Btree OK.'

def buildInvertedIndex4Docs():
    print 'read in documents and build sub inverted index...'
    newsTypes = ['人才培养','学校要闻','校友之苑','理论学习','媒体看工大','他山之石','时势关注','校园文化','科研在线','国际合作','服务管理','深度策划','综合新闻']
    invertedIndexList = []
    for newsType in newsTypes:
        with open('../DocumentsManager/Documents/%s/index.obj' % newsType, 'r') as inputFile:
            indexTuple = pickle.load(inputFile)
        for docId in range(indexTuple[0], indexTuple[1] + 1):
            path = '../DocumentsManager/Documents/%s/%d.obj' % (newsType, docId)
            currentInvertedIndex = buildInvertedIndex4OneDoc(path, docId)
            invertedIndexList.append(currentInvertedIndex)
    print 'read in documents and build sub inverted index OK.'
    return merge2FinalInvertedIndex(invertedIndexList)

if __name__ == '__main__':
    invertedIndex = buildInvertedIndex4Docs()
    saveFinalInvertedIndexAsFile(invertedIndex)