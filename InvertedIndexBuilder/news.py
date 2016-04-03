class News(object):
    def __init__(self, url, typeName, timeStamp, source, content, title):
        self.__url = url
        self.__typeName = typeName
        self.__timeStamp = timeStamp
        self.__source = source
        self.__content = content
        self.__title = title
    def display(self):
        print self.__title
        print self.__timeStamp, self.__source
        print self.__content
        print self.__url
    @property
    def title(self):
        return self.__title
    @property
    def url(self):
        return self.__url
    @property
    def typename(self):
        return self.__typeName
    @property
    def timestamp(self):
        return self.__timeStamp
    @property
    def source(self):
        return self.__source
    @property
    def content(self):
        return self.__content
    @property
    def docId(self):
        return self.__docId
    @docId.setter
    def docId(self, aDocId):
        self.__docId = aDocId