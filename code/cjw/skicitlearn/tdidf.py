# __author__ = 'cjweffort'
# _*_coding: cp936_*_

from sklearn.feature_extraction.text import CountVectorizer
corpus = [
     'This is the first document.',
     'This is the second second document.',
     'And the third one.',
     'Is this the first document?',
 ]
X = vectorizer.fit_transform(corpus)
analyze = vectorizer.build_analyzer()
