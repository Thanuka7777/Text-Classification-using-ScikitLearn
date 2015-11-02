__author__ = 'Daniel'



from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
"""
Text transformer class which bundles several transfoming functionalities such as stemming, stopwords, lowercase
"""

class textTransformer(object):
   def __init__(self, stemmer = PorterStemmer(), stopWordsList=stopwords.words('english')):
        self.stemmer = stemmer
        self.stopWords = stopWordsList

   #Input: text string
   #Output: text string
   #Effect: remove all the stopwords and make the text lowercase
   def transform(self,text, delimiter = ' '):
       wordList = text.split(delimiter)

       non_char_pattern = re.compile(r'[^A-Za-z]')

       transformedList = []
       for w in wordList:
           w = re.sub(non_char_pattern,'',str.lower(w))
           w = self.stemmer.stem(w)
           if w not in self.stopWords:
               transformedList.append(w)
       return ' '.join(transformedList)


