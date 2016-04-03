#encoding=utf-8

import math
import cPickle

with open('../InvertedIndexBuilder/Inverted Index.txt', 'r') as inputFile:
    #for line in inputFile:
    line = inputFile.readline()
    documentCounters = {}
    while line:
        lineAttrs = line.strip().split('\t')
        word = lineAttrs[0]
        word = unicode(word, 'utf-8')
        counter = int(lineAttrs[1])
        documentCounters[word] = counter
        for i in range(counter):
            inputFile.readline()
        line = inputFile.readline()
    
    documentsSum = 37251.0
    for word in documentCounters:
        documentCounters[word] = math.log(documentsSum / documentCounters[word], 2)

    with open('../InvertedIndexBuilder/IDF.obj', 'w') as outFile:
        cPickle.dump(documentCounters, outFile)
