__author__ = 'Daniel'

import os
from capitalCorpus import capitalCorpus
from textTransformer import textTransformer
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB
import numpy as np

#Input a directory name (also the continent name), corpus
#Return a new corpus which have new label and text appended
def getText(dir,corpus, transformer):

    label_index = dir[0]
    label_name = dir[1]

    files = os.listdir('txt/%s'%dir[1])

    for fname in files:
        with open('txt/%s/%s'%(dir[1], fname), 'r') as f:
            text = transformer.transform(f.readline())
            corpus.appendText(text,label_index,label_name)

    return corpus


def main():
    corpus = capitalCorpus()
    transformer = textTransformer()

    continents = np.array(os.listdir('txt/'))

    for continent_dir in enumerate(continents):
        corpus = getText(continent_dir,corpus,transformer)


    #Split corpus into training set and test set
    train_X, test_X, train_Y, test_Y = train_test_split(corpus.data,
                                                            corpus.target, test_size = 0.25, random_state=54321)

    #Build a pipeline
    clf = MultinomialNB()
    count_vect = CountVectorizer()
    tfidf_transformer = TfidfTransformer(use_idf = True)

    clf_pipe = Pipeline(
        [
            ('vectorizer', count_vect),
            ('tfidf', tfidf_transformer),
            ('classifier', clf)
        ]
    ).fit(train_X, train_Y)

    predicted = clf_pipe.predict(test_X)

    print(classification_report(test_Y, predicted))



if __name__ == '__main__':
    main()
