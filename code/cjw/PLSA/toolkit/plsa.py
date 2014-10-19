import re

import numpy as np

from cjw.PLSA.myPLSA.utils import normalize


"""
Author: 
Alex Kong (https://github.com/hitalex)

Reference:
http://blog.tomtung.com/2011/10/plsa
"""

np.set_printoptions(threshold='nan')

class Document(object):

    '''main element in Document
    #filepath, file, lines, words
    '''

    '''
    Splits a text file into an ordered list of words.
    '''

    # List of punctuation characters to scrub. Omits, the single apostrophe,
    # which is handled separately so as to retain contractions.
    PUNCTUATION = ['(', ')', ':', ';', ',', '-', '!', '.', '?', '/', '"', '*']

    # Carriage return strings, on *nix and windows.
    CARRIAGE_RETURNS = ['\n', '\r\n']

    # Final sanity-check regex to run on words before they get
    # pushed onto the core words list.
    WORD_REGEX = "^[a-z']+$"

    def __init__(self):
        self.lines = []
        self.words = []

    def __init__(self, filepath):
        '''
        Set source file location, build contractions list, and initialize empty
        lists for lines and words.
        '''

        self.filepath = filepath
        self.file = open(self.filepath)#this document
        self.lines = []#total line of this document
        self.words = []#the clean words of this document


    def split(self, STOP_WORDS_SET):
        '''
        Split file into an ordered list of words. Scrub out punctuation;
        lowercase everything; preserve contractions; disallow strings that
        include non-letters.
        '''
        self.lines = [line for line in self.file]
        for line in self.lines:
            words = line.split(' ')
            for word in words:
                clean_word = self._clean_word(word)
                #filter word in STOP_WORDS_SET
                if clean_word and (clean_word not in STOP_WORDS_SET) and (len(clean_word) > 1): # omit stop words
                    self.words.append(clean_word)


    def _clean_word(self, word):
        '''
        Parses a space-delimited string from the text and determines whether or
        not it is a valid word. Scrubs punctuation, retains contraction
        apostrophes. If cleaned word passes final regex, returns the word;
        otherwise, returns None.
        '''
        word = word.lower()
        for punc in Document.PUNCTUATION + Document.CARRIAGE_RETURNS:
            word = word.replace(punc, '').strip("'")
        return word if re.match(Document.WORD_REGEX, word) else None

    def split1(self, STOP_WORDS_SET,title, content):
        self.title_words = title.split(' ')
        self.content_words = content.split(' ')
        for word in self.title_words:
            clean_word = self._clean_word(word)
            if clean_word and (clean_word not in STOP_WORDS_SET) and (len(clean_word) > 1): # omit stop words
                self.title_words.append(clean_word)
        for word in self.content_words:
            clean_word = self._clean_word(word)
            if clean_word and (clean_word not in STOP_WORDS_SET) and (len(clean_word) > 1): # omit stop words
                self.content_words.append(clean_word)


class Corpus(object):

    #words in the corpus can be seen as features

    '''
    A collection of documents.
    '''

    def __init__(self):
        '''
        Initialize empty document list.
        '''
        self.documents = [] # documents


    def add_document(self, document):
        '''
        Add a document to the corpus.
        '''
        self.documents.append(document)

    #build corpus for all total documents
    def build_vocabulary(self):
        '''
        Construct a list of unique words in the corpus.
        '''
        # ** ADD ** #
        # exclude words that appear in 90%+ of the documents
        # exclude words that are too (in)frequent
        discrete_set = set()
        for document in self.documents:
            for word in document.words:
                discrete_set.add(word)
        self.vocabulary = list(discrete_set) #unique words in the corpus
        


    def plsa(self, number_of_topics, max_iter):

        '''
        Model topics.
        '''
        print "EM iteration begins..."
        # Get vocabulary and number of documents.
        self.build_vocabulary()
        number_of_documents = len(self.documents)
        vocabulary_size = len(self.vocabulary)

        #build IDF(Inverse Document Frequency) Matrix
        reverse_word_doc = {}
        for t_doc in self.documents:
            tag = True
            for word in t_doc.words:
                reverse_word_doc.setdefault(word, 0)
                if tag:
                    tag = False
                    reverse_word_doc[word] += 1

        #build TF-IDF(Term Frequence-Inverse DDocument Frequence) Matrix
        # build term-doc matrix(numbers of specific word occurring in this document)
        fp_term_doc_matrix = open('term_doc_matrix.csv', 'w')
        term_doc_matrix = np.zeros([number_of_documents, vocabulary_size], dtype = np.float64)
        for d_index, doc in enumerate(self.documents):
            term_count = np.zeros(vocabulary_size, dtype = np.int)
            for word in doc.words:
                # t_idf_item = math.log(1.0 * number_of_documents / (reverse_word_doc[word] + 1))
                if word in self.vocabulary:
                    w_index = self.vocabulary.index(word)
                    term_count[w_index] = (term_count[w_index] + 1) #* t_idf_item

            count = 0
            number_of_is_not_zero = 0
            for i in xrange(vocabulary_size):
                fp_term_doc_matrix.write('%d ' %term_count[i])
                if term_count[i] != 0:
                    number_of_is_not_zero += 1
                count += term_count[i]
            print 'index:%d number of words in document[index]:%d number of specific word in document[index]:%d' %(d_index, count, number_of_is_not_zero)
            fp_term_doc_matrix.write('\n')
            term_doc_matrix[d_index] = term_count
            flag = True
            for i in xrange(vocabulary_size):
                fp_term_doc_matrix.write('%d ' %term_doc_matrix[d_index][i])
                if term_doc_matrix[d_index][i] != 0:
                    flag = False
            if flag:
                print "bug!"
        fp_term_doc_matrix.close()

        # Create the counter arrays.
        self.document_topic_prob = np.zeros([number_of_documents, number_of_topics], dtype=np.float) # P(z | d)  z;topic d:document
        self.topic_word_prob = np.zeros([number_of_topics, len(self.vocabulary)], dtype=np.float) # P(w | z)  w:word z:topic
        self.topic_prob = np.zeros([number_of_documents, len(self.vocabulary), number_of_topics], dtype=np.float) # P(z | d, w)

        # Initialize
        print "Initializing..."
        # randomly assign values
        self.document_topic_prob = np.random.random(size = (number_of_documents, number_of_topics))
        for d_index in range(len(self.documents)):
            normalize(self.document_topic_prob[d_index]) # normalize for each document
        self.topic_word_prob = np.random.random(size = (number_of_topics, len(self.vocabulary)))
        for z in range(number_of_topics):
            normalize(self.topic_word_prob[z]) # normalize for each topic

        # Run the EM algorithm
        for iteration in range(max_iter):
            print "Iteration #" + str(iteration + 1) + "..."
            print "E step:"
            for d_index, document in enumerate(self.documents):
                for w_index in range(vocabulary_size):
                    prob = self.document_topic_prob[d_index, :] * self.topic_word_prob[:, w_index]
                    if sum(prob) == 0.0:
                        print "d_index = " + str(d_index) + ",  w_index = " + str(w_index)
                        print "self.document_topic_prob[d_index, :] = " + str(self.document_topic_prob[d_index, :])
                        print "self.topic_word_prob[:, w_index] = " + str(self.topic_word_prob[:, w_index])
                        print "topic_prob[d_index][w_index] = " + str(prob)
                        exit(0)
                    else:
                        normalize(prob)
                    self.topic_prob[d_index][w_index] = prob
            print "M step:"
            # update P(w | z)
            for z in range(number_of_topics):
                for w_index in range(vocabulary_size):
                    s = 0
                    for d_index in range(len(self.documents)):
                        count = term_doc_matrix[d_index][w_index]
                        s = s + count * self.topic_prob[d_index, w_index, z]
                    self.topic_word_prob[z][w_index] = s
                normalize(self.topic_word_prob[z])
            
            # update P(z | d)
            for d_index in range(len(self.documents)):
                for z in range(number_of_topics):
                    s = 0
                    for w_index in range(vocabulary_size):
                        count = term_doc_matrix[d_index][w_index]
                        s = s + count * self.topic_prob[d_index, w_index, z]
                    self.document_topic_prob[d_index][z] = s
#                print self.document_topic_prob[d_index]
#                assert(sum(self.document_topic_prob[d_index]) != 0)
                normalize(self.document_topic_prob[d_index])
