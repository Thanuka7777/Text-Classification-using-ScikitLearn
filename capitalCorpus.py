__author__ = 'Daniel'

import numpy as np


class capitalCorpus(object):
    def __init__(self):
        self.data = np.array([])
        self.target = np.array([])
        self.target_names = np.array([])

    #take in one text string
    #append to the list of texts
    def appendText(self, text, label, name):
        self.data = np.append(self.data, text)
        self.target = np.append(self.target, label)
        self.target_names = np.append(self.target_names,name)


