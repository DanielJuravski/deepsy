# cython: linetrace=True

import Cython.Compiler.Options


import numpy as np
import random
from timeit import default_timer as timer
from utils import printime


class Document:
    # def __init__(self, doc_tokens, long[:] doc_topics, long[:] doc_topic_counts, long[:] doc_subtopics, long[:] doc_subtopics_counts):
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


    documents = []
    vocab = []

    def __init__(self, data, params, gaussians, most_similar_tokens):
        self.vocab.extend(data.vocab)
        self.vocab_size = data.vocab_size
        self.K = params['K']
        self.S = params['S']
        self.num_of_most_similar_tokens = params['num_of_most_similar_tokens']
        self.iterations = params['iterations']
        self.doc_smoothing = params['doc_smoothing']
        self.subtopic_smoothing = params['subtopic_smoothing']
        self.smoothing_times_centroids_size = self.subtopic_smoothing * self.vocab_size
        self.gaussians = gaussians
        self.most_similar_tokens = most_similar_tokens.copy()

        self.topic_totals = np.zeros(self.K, dtype=int)
        self.subtopics_topics = np.zeros((self.S, self.K), dtype=int)

    def add_document(self, doc):

        self.documents.append(doc)

        for i in range(len(doc.doc_tokens)):
            topic = doc.doc_topics[i]
            subtopic = doc.doc_subtopics[i]

            # Update counts:
            self.topic_totals[topic] += 1
            self.subtopics_topics[subtopic, topic] += 1
            doc.doc_topic_counts[topic] += 1
            doc.doc_subtopics_counts[subtopic] += 1


    def learn(self):
        sampling_sum = 0
        topic_normalizers = np.zeros(self.K, dtype=float)
        subtopic_normalizers = np.zeros(self.S, dtype=float)
        topic_probs = np.zeros(self.K, dtype=float)
        subtopic_probs = np.zeros(self.S, dtype=float)

        for topic in range(self.K):
            topic_normalizers[topic] = 1.0 / (self.topic_totals[topic] + self.smoothing_times_centroids_size)

        for iteration in range(self.iterations):
            if iteration % 5 == 0:
                self.print_all_topics(20)
                printime('Training iteration', iteration)
            for document_i in range(len(self.documents)):
                if document_i % 100 == 0:
                    #printime('doc num', document_i)
                    pass
                document = self.documents[document_i]
                doc_tokens = document.doc_tokens
                doc_topics = document.doc_topics
                doc_topic_counts = document.doc_topic_counts
                doc_subtopics = document.doc_subtopics
                doc_subtopics_count = document.doc_subtopics_counts
                doc_length = len(doc_tokens)
                z_uniform_variates = np.random.random_sample(doc_length)
                s_uniform_variates = np.random.random_sample(doc_length)

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

                    sampling_sum = 0.0
                    for topic in range(self.K):
                        topic_probs[topic] = (doc_topic_counts[topic] + self.doc_smoothing) * \
                                             (old_subtopic_topic_count[topic] + self.subtopic_smoothing) * \
                                             topic_normalizers[topic]
                        sampling_sum += topic_probs[topic]


                    sample = z_uniform_variates[pos_i] * sampling_sum

                    new_topic = 0
                    while sample > topic_probs[new_topic]:
                        sample -= topic_probs[new_topic]
                        new_topic += 1
                    doc_topics[pos_i] = new_topic

                    # add back in the effect of this token
                    old_subtopic_topic_count[new_topic] += 1
                    self.topic_totals[new_topic] += 1
                    doc_topic_counts[new_topic] += 1
                    topic_normalizers[new_topic] = 1.0 / (
                                self.topic_totals[new_topic] + self.smoothing_times_centroids_size)


                    ######################
                    #      sample S      #
                    ######################
                    subtopic_topic_counts = self.subtopics_topics[:, new_topic]
                    # remove the effect of this token
                    subtopic_topic_counts[old_subtopic] -= 1
                    doc_subtopics_count[old_subtopic] -= 1

                    sampling_sum = 0.0
                    token_id_most_similar_tokens = self.most_similar_tokens[token_id]
                    for i in range(self.num_of_most_similar_tokens):
                        subtopic = token_id_most_similar_tokens[i]

                        p = (doc_topic_counts[new_topic] + self.doc_smoothing) * \
                            (subtopic_topic_counts[subtopic] + self.subtopic_smoothing) / \
                            (doc_length + self.smoothing_times_centroids_size)

                        g = self.gaussians[token_id, subtopic]

                        prob = p*(g)

                        subtopic_probs[subtopic] = prob
                        sampling_sum += prob

                    sample = s_uniform_variates[pos_i] * sampling_sum

                    new_subtopic = 0
                    while sample > subtopic_probs[new_subtopic]:
                        sample -= subtopic_probs[new_subtopic]
                        new_subtopic += 1

                    subtopic_topic_counts[new_subtopic] += 1
                    doc_subtopics_count[new_subtopic] += 1
                    doc_subtopics[pos_i] = new_subtopic

                    # clean subtopic_probs to zero
                    for i in range(self.num_of_most_similar_tokens):
                        clean_index = token_id_most_similar_tokens[i]
                        subtopic_probs[clean_index] = 0

        printime('Training was completed.', '')


    def printArray(self, arr, info=None):
        print("printing {0}".format(info))
        print(len(arr))
        content = ""
        for i in arr:
            content = content + "  " + str(i)
        print(content)



    def print_all_topics(self, words_2_print):
        top_words = []
        for topic in range(self.K):
            sorted_words = sorted(zip(self.subtopics_topics[:, topic], self.vocab), reverse=True)
            words = " ".join([w for x, w in sorted_words[:words_2_print]])
            print(words)
            top_words.append(words)

        return top_words