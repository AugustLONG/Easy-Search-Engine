#encoding=utf-8

class WordNode(object):
    def __init__(self, word, docId, position, frequency = 1):
        self.__word, self.__docId = word, docId
        self.__frequency = frequency
        self.__position = [position] if position != None else []
    @property
    def word(self):
        return self.__word
    @property
    def position(self):
        return self.__position
    def addPosition(self, position):
        self.__position.append(position)
    @property
    def frequency(self):
        return self.__frequency
    def addFrequency(self):
        self.__frequency += 1
    @property
    def docId(self):
        return self.__docId
    def save2File(self, fileHandler):
        fileHandler.write('%d\t%d\t' % (self.__docId, self.__frequency))
        for pos in self.__position[: -1]:
            fileHandler.write('%d,' % pos)
        fileHandler.write('%d\n' % self.__position[-1])

class InvertedIndex(object):
    def __init__(self):
        self.wordHash = {}

    def ifWordExist(self, word):
        return word in self.wordHash

    def getWords(self):
        """get words of inverted index"""
        return self.wordHash.keys()

    def addWord(self, word, position, docId):
        """after create an inverted index for a doc, insert doc's word to it"""
        if word in self.wordHash:
            self.wordHash[word][0].addFrequency()
            self.wordHash[word][0].addPosition(position)
        else:
            self.wordHash[word] = [WordNode(word, docId, position)]

    def mergeFromOtherIndex(self, otherInvertedIndex):
        """"merge other inverted index to this"""
        for word, nodes in otherInvertedIndex.wordHash.items():
            if word not in self.wordHash:
                self.wordHash[word] = []
            self.wordHash[word].extend(nodes)
        del otherInvertedIndex

    def save2File(self, fileHandler):
        wordPosition = {}.fromkeys(self.getWords(), -1)
        for word in self.wordHash:
            wordNodeArray = self.wordHash[word]
            wordPosition[word] = fileHandler.tell()
            documentCounter = len(wordNodeArray)
            fileHandler.write(word.encode('utf-8') + '\t' + '%d' % documentCounter + '\n')
            for wordNode in wordNodeArray:
                wordNode.save2File(fileHandler)
        return wordPosition