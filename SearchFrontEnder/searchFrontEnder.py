#encoding=utf-8

import re
import math
import cPickle
from DocumentsManager.documentsManager import DocumentsManager
from IndexSearcher.indexSearcher import IndexSearcher
from InvertedIndexBuilder.createSubInvertedIndex import BTreeNode
from InvertedIndexBuilder.invertedIndex import WordNode, InvertedIndex
from Utils.utils import twoGramSplitWord

class Similarity:
    def __init__(self, docId, sim):
        self.docId, self.sim = docId, sim

class SearchFrontEnder:
    def __init__(self):
        print 'init enviroment...'
        self.indexSearcher = IndexSearcher()
        self.documentsManager = DocumentsManager()
        with open('InvertedIndexBuilder/IDF.obj', 'r') as inputFile:
            self.idf = cPickle.load(inputFile)
        print 'init enviroment OK...'
    def searchRequest(self, line, k = 5):
        #2-gram split word
        line = line.strip()
        line = unicode(line, 'utf-8')
        wordsVector = twoGramSplitWord(line)
        #calculate vector
        for word in wordsVector.keys():
            if word not in self.idf:
                del wordsVector[word]
            else:
                wordsVector[word] = (math.log(wordsVector[word], 2) + 1) * self.idf[word] 
        #get every word's document lists
        documentsArrayOfArray = []
        for word in wordsVector:
            documentsArray = self.indexSearcher.search(word)
            documentsArray.sort(cmp = lambda x, y: cmp(x.docId, y.docId))
            documentsArrayOfArray.append(documentsArray)
        #get each word's document lists union
        intersectingDocumentsIndex = self.getIntersectingDocuments(documentsArrayOfArray)#intersectingDocumentsIndex: key = docid, value = wordNodes array.
        intersectingDocuments = {}#intersectingDocuments: key = docid, value = document object.
        if not intersectingDocumentsIndex:#no result
            return
        for docId in intersectingDocumentsIndex:
            intersectingDocuments[docId] = self.documentsManager.searchDocument(docId)
        #filter the document and sort
        finalDocuments = self.documentFilterAndSort(line, \
            wordsVector, \
            intersectingDocumentsIndex, \
            intersectingDocuments, k)

        for docId in finalDocuments:
            self.displayOneResult(intersectingDocuments[docId], intersectingDocumentsIndex[docId])

    def getIntersectingDocuments(self, documentsArrayOfArray):
        if not documentsArrayOfArray:
            return None
        pointers = [0 for array in documentsArrayOfArray]
        pointersEnd = [len(array) for array in documentsArrayOfArray]
        size = len(pointers)

        def pointerValid():
            for pointer, end in zip(pointers, pointersEnd):
                if pointer >= end:
                    return False
            return True

        def checkEqual():
            maxVal = documentsArrayOfArray[0][pointers[0]].docId
            isEqual = True
            for i in range(1, size):
                if documentsArrayOfArray[i][pointers[i]].docId > maxVal:
                    maxVal = documentsArrayOfArray[i][pointers[i]].docId
                    isEqual = False
                elif documentsArrayOfArray[i][pointers[i]].docId < maxVal:
                    isEqual = False
            return (isEqual, maxVal)
            #when isEqual, maxVal is equalValue, else, maxVal is maxValue

        intersectingDocumentsIndex = {}

        while pointerValid():
            isEqual, maxValue = checkEqual()
            if isEqual:
                thatDocId = documentsArrayOfArray[0][pointers[0]].docId
                intersectingDocumentsIndex[thatDocId] = \
                [documentsArrayOfArray[i][pointers[i]] for i in range(size)]
                #all point + 1
                for i in range(size):
                    pointers[i] += 1
            else:
                #all point move to where v[point] >= maxValue
                for i in range(size):
                    while pointers[i] < pointersEnd[i] and documentsArrayOfArray[i][pointers[i]].docId < maxValue:
                        pointers[i] += 1
        return intersectingDocumentsIndex

    def documentFilterAndSort(self, line, wordsVector, intersectingDocumentsIndex, intersectingDocuments, k):
        def calculateVectorForResult():
            resultWordsVector = {}.fromkeys(intersectingDocumentsIndex.keys(), 0)
            for docId in resultWordsVector:
                vector = {}
                for wordNode in intersectingDocumentsIndex[docId]:
                    vector[unicode(wordNode.word, 'utf-8')] = (math.log(wordNode.frequency, 2) + 1) * self.idf[unicode(wordNode.word, 'utf-8')]
                resultWordsVector[docId] = vector
            return resultWordsVector

        def isWordsNeighbor(document):
            content = document.title + unicode('。', 'utf-8') + document.content
            phrases = re.split('\s+', line)
            for phrase in phrases:
                if content.find(phrase) == -1:
                    return False
            return True

        def calculateSimilarity(v1, v2):
            fz = 0
            for k in v1:
                fz += (v1[k] * v2[k])
            fm1 = 0
            for k in v1:
                fm1 += (v1[k] **2)
            fm1 = fm1 ** 0.5
            fm2 = 0
            for k in v2:
                fm2 += (v2[k] **2)
            fm2 = fm2 ** 0.5
            return fz / (fm1 * fm2)

        resultWordsVector = calculateVectorForResult()
        wordsNeighborDocs = []#docs that words in neibor
        wordsUnneighborDocs = []#docs that words not in neibor
        for docId in intersectingDocuments:
            if isWordsNeighbor(intersectingDocuments[docId]):
                wordsNeighborDocs.append(Similarity(docId, \
                    calculateSimilarity(wordsVector, resultWordsVector[docId])))
            else:
                wordsUnneighborDocs.append(Similarity(docId, \
                    calculateSimilarity(wordsVector, resultWordsVector[docId])))
        #sort by TF*IDF sim
        wordsNeighborDocs.sort(cmp=lambda x,y: cmp(x.sim, y.sim), reverse=True)
        wordsUnneighborDocs.sort(cmp=lambda x,y: cmp(x.sim, y.sim), reverse=True)
        wordsNeighborDocs.extend(wordsUnneighborDocs)
        results = [i.docId for i in wordsNeighborDocs[: k]]
        return results

    def displayOneResult(self, document, wordNodes):
        print '-' * 10
        print '\033[0;32m%s\033[0m' % document.title,
        print '\033[4;34m[%s]\033[0m' % document.url
        print '*' * 10
        highLightPositions = []
        for wordNode in wordNodes:
            wordSize = len(unicode(wordNode.word, 'utf-8'))
            for pos in wordNode.position:
                if pos == 359:
                    print 359, 'who!', wordNode.word
                    content = document.title + unicode('。', 'utf-8') + document.content
                    print content[359:361]
                if pos == 491:
                    print 491, 'who!', wordNode.word
                    content = document.title + unicode('。', 'utf-8') + document.content
                    print content[491:493]
                if pos == 360:
                    print 360, 'who!', wordNode.word
                    content = document.title + unicode('。', 'utf-8') + document.content
                    print content[360:362]
                highLightPositions.append((pos, pos + wordSize))
        highLightPositions.sort(cmp = lambda x, y: cmp(x[0], y[0]))

        def highLightPositionsReduce():
            newHighLightPositions = []
            start, end = highLightPositions[0]
            for istart, iend in highLightPositions[1:]:
                if end < istart:
                    newHighLightPositions.append((start, end))
                    start = istart
                end = iend
            newHighLightPositions.append((start, end))
            return newHighLightPositions

        highLightPositions = highLightPositionsReduce()
        content = document.title + unicode('。', 'utf-8') + document.content
        
        startOffet, endOffset = highLightPositions[0][0], highLightPositions[-1][1]

        def highLightDisplay():
            output = '...'
            size = len(highLightPositions)
            for i in range(size - 1):
                start, end = highLightPositions[i]
                nextstart = highLightPositions[i + 1][0]
                output += '\033[0;31m%s\033[0m' % (content[start: end])
                output += content[end: nextstart]
            output += '\033[0;31m%s\033[0m...' % (content[highLightPositions[-1][0]: highLightPositions[-1][1]])
            print output

        highLightDisplay()
        print '*' * 10