# cython: linetrace=True

from cython.view cimport array as cvarray
import numpy as np
import random
from timeit import default_timer as timer
from utils import printime


class Document:
    def __init__(self, long[:] doc_tokens, long[:] doc_topics, long[:] doc_topic_counts):
        # doc length array
        self.doc_tokens = doc_tokens
        # doc length array
        self.doc_topics = doc_topics
        # K length array
        self.doc_topic_counts = doc_topic_counts


cdef class LDAGibbsSampler:
    cdef long[:] topic_totals
    cdef long[:,:] word_topics

    cdef int K
    cdef int vocab_size
    cdef int iterations

    cdef double[:] topic_probs
    cdef double[:] topic_normalizers
    cdef float doc_smoothing
    cdef float word_smoothing
    cdef float smoothing_times_vocab_size

    documents = []
    vocab = []

    # for statistics
    Z_swap = []

    def __init__(self, data, params):
        self.vocab.extend(data.vocab)
        self.vocab_size = data.vocab_size
        self.K = params['K']
        self.iterations = params['iterations']
        self.doc_smoothing = params['doc_smoothing']
        self.word_smoothing = params['word_smoothing']
        self.smoothing_times_vocab_size = self.word_smoothing * self.vocab_size

        self.topic_totals = np.zeros(self.K, dtype=int)
        self.word_topics = np.zeros((self.vocab_size, self.K), dtype=int)

    def add_document(self, doc):
        cdef int token_id
        cdef int topic

        self.documents.append(doc)

        for i in range(len(doc.doc_tokens)):
            token_id = doc.doc_tokens[i]
            topic = doc.doc_topics[i]

            # Update counts:
            self.word_topics[token_id, topic] += 1
            self.topic_totals[topic] += 1
            doc.doc_topic_counts[topic] += 1

    def learn(self):
        cdef int old_topic, new_topic, word, topic, word_i, doc_length, document_i, iteration
        cdef double sampling_sum = 0
        cdef double sample
        cdef long[:] word_topic_counts

        cdef long[:] doc_tokens
        cdef long[:] doc_topics
        cdef long[:] doc_topic_counts

        cdef double[:] uniform_variates
        cdef double[:] topic_normalizers = np.zeros(self.K, dtype=float)
        cdef double[:] topic_probs = np.zeros(self.K, dtype=float)

        cdef int Z_swap_count = 0

        # calculate the denominator for the p_z_wt
        for topic in range(self.K):
            topic_normalizers[topic] = 1.0 / (self.topic_totals[topic] + self.smoothing_times_vocab_size)

        for iteration in range(self.iterations):
            if iteration % 10 == 0:
                printime('Sample iteration', iteration)
            for document_i in range(len(self.documents)):
                document = self.documents[document_i]
                doc_tokens = document.doc_tokens
                doc_topics = document.doc_topics
                doc_topic_counts = document.doc_topic_counts
                doc_length = len(doc_tokens)
                uniform_variates = np.random.random_sample(doc_length)

                for word_i in range(doc_length):
                    word = doc_tokens[word_i]
                    old_topic = doc_topics[word_i]
                    word_topic_counts = self.word_topics[word, :]

                    # erase the effect of this token
                    word_topic_counts[old_topic] -= 1
                    self.topic_totals[old_topic] -= 1
                    doc_topic_counts[old_topic] -= 1
                    topic_normalizers[old_topic] = 1.0 / (self.topic_totals[old_topic] + self.smoothing_times_vocab_size)

                    # sample dist
                    sampling_sum = 0.0
                    for topic in range(self.K):
                        topic_probs[topic] = (doc_topic_counts[topic] + self.doc_smoothing) * \
                                             (word_topic_counts[topic] + self.word_smoothing) * \
                                             topic_normalizers[topic]
                        sampling_sum += topic_probs[topic]

                    sample = uniform_variates[word_i] * sampling_sum

                    new_topic = 0
                    while sample > topic_probs[new_topic]:
                        sample -= topic_probs[new_topic]
                        new_topic += 1

                    # add back in the effect of this token
                    word_topic_counts[new_topic] += 1
                    self.topic_totals[new_topic] += 1
                    doc_topic_counts[new_topic] += 1
                    topic_normalizers[new_topic] = 1.0 / (self.topic_totals[new_topic] + self.smoothing_times_vocab_size)

                    doc_topics[word_i] = new_topic

                    # This check is for statistics
                    if new_topic != old_topic:
                        Z_swap_count += 1

            # for statistics
            self.Z_swap.append(Z_swap_count)
            Z_swap_count = 0

        printime('Sampling was completed.', '')


    def print_all_topics(self, words_2_print):
        top_words = []
        for topic in range(self.K):
            sorted_words = sorted(zip(self.word_topics[:, topic], self.vocab), reverse=True)
            words = " ".join([w for x, w in sorted_words[:words_2_print]])
            print(words)
            top_words.append(words)

        return top_words


    def getStats(self):
        return self.Z_swap



