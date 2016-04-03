#encoding=utf-8

import re

def twoGramSplitWord(text):
    unicodeText = text
    textSize = len(unicodeText)
    #init inverted index
    wordsVector = {}
    #handle english word
    englishWordMatchList = re.finditer(r'[a-zA-Z]+', unicodeText)
    for englishWordMatch in englishWordMatchList:
        word = englishWordMatch.group()
        wordsVector[word] = wordsVector[word] + 1 if word in wordsVector else 1
    #handle chinese word
    isChinese = lambda uchar: (uchar >= u'\u4e00' and uchar <= u'\u9fa5')
    i = 0
    while i < textSize - 1:
        while i < textSize - 1 and (not isChinese(unicodeText[i]) or not isChinese(unicodeText[i + 1])):
            i += 1
        if i < textSize - 1:
            word = unicodeText[i: i + 2]
            wordsVector[word] = wordsVector[word] + 1 if word in wordsVector else 1
            i += 1
    #handle OK.
    return wordsVector