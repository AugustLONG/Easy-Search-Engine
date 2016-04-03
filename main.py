#encoding=utf-8

import sys
sys.path.append('DocumentsManager')
from SearchFrontEnder.searchFrontEnder import SearchFrontEnder
from InvertedIndexBuilder.createSubInvertedIndex import BTreeNode

fe = SearchFrontEnder()
fe.searchRequest('不断提高 哈工大')
