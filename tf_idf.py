import nltk
from nltk.corpus import stopwords
import string
from nltk.probability import FreqDist
import numpy as np
import re

class TfIdf:
    # We expect docs to be a dict with some keys indicating the labels and strings being the documents
    def __init__(self, docs, stop_words=None, tokenize_function=None):
        if stop_words:
            self.stop_words = set(stop_words)
        else:
            self.stop_words = set(stopwords.words('english'))
            
        tokenize = self.tokenize if not tokenize_function else tokenize_function
        self.docs_fd = dict([(label, FreqDist(tokenize(doc))) for label, doc in docs.items()])
        self.N = len(docs)
        self.doc_lengths = { label: len(tokenize(doc)) for label, doc in docs.items() }
        
        
    def tf(self, label, token):
        freq_dist = self.docs_fd[label]
        return freq_dist[token] / self.doc_lengths[label]


    def df(self, token):
        n = 0
        for label, freq_dist in self.docs_fd.items():
            if freq_dist[token] > 0:
                n += 1
        return n

    def tokenize(self, text):
        text = text.replace("\n", " ")
        text = text.lower() # lower case
        text = re.sub('(\'|’)\w*', '', text) # removing apostrophes
        text = text.translate(str.maketrans(dict.fromkeys(string.punctuation))) # remove punctuation
        text = re.sub('\d', '', text) # removing numbers
        text = re.sub(r'\s\s+', ' ', text) # replacing all white space with single space
        words = text.split(' ')
        isNumber = lambda w: w.isnumeric()
        tokens = [w for w in words if len(w) and not w.lower() in self.stop_words and not isNumber(w)]
        return tokens

    # N being the total amount of tokens in the document
    def idf(self, token):
        return np.log10(self.N / (self.df(token) + 1)) #add 0.1 to avoid division by zero

    def tf_idf(self, label, token):
        return self.tf(label, token) * self.idf(token)
    
    def all_tf_idf(self, label):
        tfidfs = dict([])
        for token in self.docs_fd[label].keys():
            tfidfs[token] = self.tf_idf(label, token)
        return tfidfs