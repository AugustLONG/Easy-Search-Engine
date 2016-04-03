#encoding=utf-8

import cPickle
from InvertedIndexBuilder.invertedIndex import WordNode, InvertedIndex
from InvertedIndexBuilder.createSubInvertedIndex import BTreeNode

class IndexSearcher:
    def __init__(self):
        with open('InvertedIndexBuilder/BTreeRoot/node', 'r') as inFile:
            self.root = cPickle.load(inFile)

    def search(self, someKey):
        current = self.root
        findOut = False
        currentPath = 'InvertedIndexBuilder/BTreeRoot'
        while not current.isKeyExist(someKey):
            nextPos = current.getCorrectChild(someKey)
            if nextPos == -1:
                return None
            currentPath = currentPath + '/%d' % nextPos
            with open('%s/node' % currentPath, 'r') as inFile:
                current = cPickle.load(inFile)
        offset = current.keyValue[someKey]
        with open('InvertedIndexBuilder/Inverted Index.txt', 'r') as inputFile:
            return self.readInvertedIndexInDiskForOneWord(inputFile, offset)

    def readInvertedIndexInDiskForOneWord(self, fileHandler, offset):
        fileHandler.seek(offset)
        line = fileHandler.readline()
        word, indexSize = line.strip().split('\t')
        indexSize = int(indexSize)
        invertedInfomations = []
        for i in range(indexSize):
            line = fileHandler.readline()
            docId, frequency, positionStr = line.strip().split('\t')
            docId = int(docId)
            frequency = int(frequency)
            wordNode = WordNode(word, docId, None, frequency)
            for pos in positionStr.split(','):
                wordNode.addPosition(int(pos))
            invertedInfomations.append(wordNode)
        return invertedInfomations