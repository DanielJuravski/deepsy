import numpy as np
import random
from timeit import default_timer as timer
from utils import printime


class Document:
    # def __init__(self, long[:] doc_tokens, long[:] doc_topics, long[:] doc_topic_counts):
    def __init__(self, doc_tokens, doc_topics, doc_topic_counts, doc_subtopics, doc_subtopics_counts):
        # doc length array
        self.doc_tokens = doc_tokens
        # doc length array
        self.doc_topics = doc_topics
        # K length array
        self.doc_topic_counts = doc_topic_counts
        # doc length array
        self.doc_subtopics = doc_subtopics
        # S length array
        self.doc_subtopics_counts = doc_subtopics_counts


class LDASTGibbsSampler:
    # cdef long[:] topic_totals
    # cdef long[:,:] word_topics
    #
    # cdef int K
    # cdef int vocab_size
    # cdef int iterations
    #
    # cdef double[:] topic_probs
    # cdef double[:] topic_normalizers
    # cdef float doc_smoothing
    # cdef float word_smoothing
    # cdef float smoothing_times_vocab_size

    documents = []
    vocab = []

    def __init__(self, data, params, gaussians):
        self.vocab.extend(data.vocab)
        self.vocab_size = data.vocab_size
        self.K = params['K']
        self.S = params['S']
        self.iterations = params['iterations']
        self.doc_smoothing = params['doc_smoothing']
        self.subtopic_smoothing = params['subtopic_smoothing']
        self.smoothing_times_centroids_size = self.subtopic_smoothing * self.vocab_size
        # self.emb = emb
        self.gaussians = gaussians

        self.topic_totals = np.zeros(self.K, dtype=int)
        # self.word_topics = np.zeros((self.vocab_size, self.K), dtype=int)
        self.subtopics_topics = np.zeros((self.S, self.K), dtype=int)

    def add_document(self, doc):
        # cdef int token_id
        # cdef int topic

        self.documents.append(doc)

        for i in range(len(doc.doc_tokens)):
            #token_id = doc.doc_tokens[i]
            topic = doc.doc_topics[i]
            subtopic = doc.doc_subtopics[i]

            # Update counts:
            self.topic_totals[topic] += 1
            # self.word_topics[token_id, topic] += 1
            self.subtopics_topics[subtopic, topic] += 1
            doc.doc_topic_counts[topic] += 1
            doc.doc_subtopics_counts[subtopic] += 1

    def learn(self):
        # cdef int old_topic, new_topic, word, topic, word_i, doc_length, document_i, iteration
        # cdef double sampling_sum = 0
        # cdef double sample
        # cdef long[:] word_topic_counts
        #
        # cdef long[:] doc_tokens
        # cdef long[:] doc_topics
        # cdef long[:] doc_topic_counts
        #
        # cdef double[:] uniform_variates
        # cdef double[:] topic_normalizers = np.zeros(self.K, dtype=float)
        # cdef double[:] topic_probs = np.zeros(self.K, dtype=float)

        topic_normalizers = np.zeros(self.K, dtype=float)
        #topic_probs = np.zeros(self.K, dtype=float)

        # calculate the denominator for the p_zs
        for topic in range(self.K):
            topic_normalizers[topic] = 1.0 / (self.topic_totals[topic] + self.smoothing_times_centroids_size)

        for iteration in range(self.iterations):
            if iteration % 1 == 0:
                printime('Training iteration', iteration)
                pass
            for document_i in range(len(self.documents)):
                if document_i % 10 == 0:
                    printime('Documemnt', document_i)
                document = self.documents[document_i]
                doc_tokens = document.doc_tokens
                doc_topics = document.doc_topics
                doc_topic_counts = document.doc_topic_counts
                doc_subtopics = document.doc_subtopics
                doc_subtopics_count = document.doc_subtopics_counts
                doc_length = len(doc_tokens)

                for pos_i in range(doc_length):
                    token_id = doc_tokens[pos_i]
                    old_subtopic = doc_subtopics[pos_i]
                    old_topic = doc_topics[pos_i]
                    # subtopic-topic counts
                    old_subtopic_topic_count = self.subtopics_topics[old_subtopic, :]

                    ######################
                    #      sample Z      #
                    ######################
                    # remove the effect of this token
                    old_subtopic_topic_count[old_topic] -= 1
                    self.topic_totals[old_topic] -= 1
                    doc_topic_counts[old_topic] -= 1

                    topic_normalizers[old_topic] = 1.0 / (
                                self.topic_totals[old_topic] + self.smoothing_times_centroids_size)

                    this_doc_topic_counts = doc_topic_counts + self.doc_smoothing
                    this_subtopic_counts = old_subtopic_topic_count + self.subtopic_smoothing
                    this_normalizer = topic_normalizers

                    p = this_doc_topic_counts * this_subtopic_counts * this_normalizer
                    sampling_sum = np.sum(p)

                    topic_probs = p / sampling_sum
                    new_topic = np.random.choice(self.K, p=topic_probs)
                    doc_topics[pos_i] = new_topic

                    # add back in the effect of this token
                    old_subtopic_topic_count[new_topic] += 1
                    self.topic_totals[new_topic] += 1
                    doc_topic_counts[new_topic] += 1

                    ######################
                    #      sample S      #
                    ######################
                    subtopic_topic_counts = self.subtopics_topics[:, new_topic]
                    # remove the effect of this token
                    subtopic_topic_counts[old_subtopic] -= 1
                    doc_subtopics_count[old_subtopic] -= 1

                    subtopic_normalizer = 1.0 / (self.topic_totals[new_topic] + self.smoothing_times_centroids_size)

                    this_doc_topic_counts = (doc_topic_counts[new_topic] + self.doc_smoothing)
                    this_subtopic_counts = subtopic_topic_counts + self.subtopic_smoothing
                    this_normalizer = subtopic_normalizer

                    p = this_doc_topic_counts * this_subtopic_counts * this_normalizer
                    g = self.gaussians[token_id, :]

                    subtopic_probs = p*g
                    sampling_sum = np.sum(subtopic_probs)
                    subtopic_probs /= sampling_sum
                    new_subtopic = np.random.choice(self.S, p=subtopic_probs)
                    doc_subtopics[pos_i] = new_subtopic

                    subtopic_topic_counts[new_subtopic] += 1
                    doc_subtopics_count[new_subtopic] += 1

            pass
        printime('Training was completed.', '')


    def updateTopicsCounters(self, topic, subtopic_topic_counts, doc_topic_counts, operation):
        if operation == "-":
            subtopic_topic_counts[topic] -= 1
            self.topic_totals[topic] -= 1
            doc_topic_counts[topic] -= 1

        elif operation == "+":
            subtopic_topic_counts[topic] += 1
            self.topic_totals[topic] += 1
            doc_topic_counts[topic] += 1

    def updateSubTopicsCounters(self, subtopic, subtopic_topic_counts, doc_subtopics_count, operation):
        if operation == "-":
            subtopic_topic_counts[subtopic] -= 1
            self.subtopics_topics[subtopic] -= 1
            doc_subtopics_count[subtopic] -= 1

        elif operation == "+":
            subtopic_topic_counts[subtopic] += 1
            self.subtopics_topics[subtopic] += 1
            doc_subtopics_count[subtopic] += 1


    def sampleZ(self, topic_normalizers, old_topic, topic_probs, doc_topic_counts, subtopic_topic_counts, uniform_variates, pos_i):

        topic_normalizers[old_topic] = 1.0 / (self.topic_totals[old_topic] + self.smoothing_times_centroids_size)

        # sample dist
        sampling_sum = 0.0
        for topic in range(self.K):
            topic_probs[topic] = (doc_topic_counts[topic] + self.doc_smoothing) * \
                                 (subtopic_topic_counts[topic] + self.subtopic_smoothing) * \
                                 topic_normalizers[topic]
            sampling_sum += topic_probs[topic]

        sample = uniform_variates[pos_i] * sampling_sum

        new_topic = 0
        while sample > topic_probs[new_topic]:
            sample -= topic_probs[new_topic]
            new_topic += 1

        return new_topic

    def sampleS(self, current_topic, doc_topic_counts, uniform_variates, word_i):

        # subtopic_normalizers = np.zeros(self.S, dtype=float)
        subtopic_probs = np.zeros(self.S, dtype=float)

        # for subtopic_i in range(self.S):
        #     subtopic_normalizers[subtopic_i] = 1.0 / (self.topic_totals[current_topic] + self.smoothing_times_centroids_size)

        subtopic_normalizer = 1.0 / (self.topic_totals[current_topic] + self.smoothing_times_centroids_size)

        # sample dist
        sampling_sum = 0.0
        for subtopic in range(self.S):
            p = (doc_topic_counts[current_topic] + self.doc_smoothing) * \
                                 (self.subtopics_topics[subtopic, current_topic] + self.subtopic_smoothing) * \
                                 subtopic_normalizer
            g = self.gaussians[word_i, subtopic]

            subtopic_probs[subtopic] = p * g
            sampling_sum += subtopic_probs[subtopic]

        sample = uniform_variates[word_i] * sampling_sum

        new_subtopic = 0
        while sample > subtopic_probs[new_subtopic]:
            sample -= subtopic_probs[new_subtopic]
            new_subtopic += 1
        print(new_subtopic)
        return new_subtopic

    def print_all_topics(self, words_2_print):
        top_words = []
        for topic in range(self.K):
            sorted_words = sorted(zip(self.subtopics_topics[:, topic], self.vocab), reverse=True)
            words = " ".join([w for x, w in sorted_words[:words_2_print]])
            print(words)
            top_words.append(words)

        return top_words
