from datetime import datetime
from TM.Models.vanilla_LDA import utils
import numpy as np
np.warnings.filterwarnings('ignore', r'arrays to stack must be passed as a "sequence"')
from collections import defaultdict
from scipy.special import gamma, gammaln
from numpy import log, pi, linalg, exp
import numpy as np
import scipy.stats
import math
from math import lgamma
from scipy.special import gammaln
from scipy.spatial import distance


class Vectors(object):
    def __init__(self, emb_file_path):
        self.emb_file_path = emb_file_path
        self.vectors = {}
        self.dim = None

        self.loadVectors(self.emb_file_path)

    def loadVectors(self, emb_file_path):
        print("Loading vectors ...")
        f = open(emb_file_path, 'r')
        vectors = {}
        for line in f:
            splitLine = line.split()
            word = splitLine[0]
            embedding = np.array([float(val) for val in splitLine[1:]])
            vectors[word] = embedding
        print("Done.", len(vectors), " words loaded!")
        self.vectors = vectors
        self.dim = len(embedding)

    def w2v(self, word):
        return self.vectors[word]


class Wishart(object):
    # init Wishart params wrt embeddings vectors
    def __init__(self, data_vectors):
        # make matrix of vectors
        vectors_batch = np.vstack(data_vectors)
        # vectors_batch = np.vstack(word_vectors.vectors.values())
        # p*p matrix, What is the definition?
        self.psi = np.eye(N=vectors_batch.shape[1])
        # nu (v) is defined as degrees of freedom, number of dims
        self.nu = vectors_batch.shape[1]
        self.kappa = 0.1
        # mean vector (at the paper was set to zero, but at the code the mean was sampled over the vectors)
        self.mu = np.mean(vectors_batch, axis=0)
        # self.mu = np.zeros(shape=len(vectors_batch))


class GLDA(object):
    def __init__(self, data, word_vectors, params):
        self.data = data
        self.word_vectors = word_vectors
        self.params = params

        self.doc_topic_count = np.zeros(shape=[len(data.documents), params['K']], dtype=int)
        self.word_topic_count = np.zeros(shape=[data.vocab_size, params['K']], dtype=int)
        self.vector_dim = word_vectors.dim  # = M
        self.topics_params = defaultdict(dict)

        # make list of only data's words vectors
        self.data_vectors = []
        for word in data.vocab:
            self.data_vectors.append(word_vectors.vectors[word])

        self.priors = Wishart(self.data_vectors)

        self.init(self.data)

    def init(self, data):
        # update doc topic matrix and word topic matrix
        for doc_i in range(len(data.documents)):
            doc = data.documents[doc_i]
            for topic, word_id in zip(doc['doc_topics'], doc['doc_tokens']):
                self.doc_topic_count[doc_i][topic] += 1
                self.word_topic_count[word_id][topic] += 1

        # init Wishart params for each topic
        for k in range(params['K']):
            self.updateTopicWishartParams(k)

        print("Intialization done.")

    def updateTopicWishartParams(self, k):
        N_k = np.sum(self.doc_topic_count[:, k], axis=0)

        K_k = self.priors.kappa + N_k
        V_k = self.priors.nu + N_k

        V_bar_k, C_k = self.get_topic_k_mean(k, N_k)

        V_bar_k_minus_mu = V_bar_k - self.priors.mu
        psi_k = self.priors.psi + C_k + (self.priors.kappa*N_k/K_k) * np.dot(V_bar_k_minus_mu, V_bar_k_minus_mu.T)

        mu_k = ((self.priors.kappa * self.priors.mu) + (N_k * V_bar_k)) / K_k
        sigma_k = psi_k / (V_k - self.vector_dim + 1)

        # self.topics_params[k]['K_k'] = K_k
        # self.topics_params[k]['V_k'] = V_k
        # self.topics_params[k]['V_bar_k'] = V_bar_k
        # self.topics_params[k]['C_k'] = C_k
        # self.topics_params[k]['psi_k'] = psi_k
        # self.topics_params[k]['mu_k'] = mu_k
        # self.topics_params[k]['sigma_k'] = sigma_k
        self.topics_params[k]["Topic Count"] = N_k
        self.topics_params[k]["Topic Kappa"] = K_k
        self.topics_params[k]["Topic Nu"] = V_k
        self.topics_params[k]["Topic Mean"] = mu_k
        self.topics_params[k]["Topic Covariance"] = sigma_k
        self.topics_params[k]["Inverse Covariance"] = np.linalg.inv(sigma_k)
        self.topics_params[k]["Covariance Determinant"] = np.linalg.det(sigma_k)

    def get_topic_k_mean(self, k, N_k):
        # unique_words_in_k = [self.word_topic_count[word_id,k] != 0 for word_id in range(self.data.vocab_size)]
        # topic_k_words_vectors = np.zeros(shape=[sum(unique_words_in_k), self.vector_dim], dtype=float)
        topic_k_words_vectors = []

        # find all words in topic k
        # index = 0
        for word_count, word_id in zip(self.word_topic_count[:,k], range(len(self.word_topic_count[:,k]))):
            for i in range(word_count):  # add the vector as number of times it is appears (count bigger then 0)
                word_vec = self.word_vectors.vectors[self.data.vocab[word_id]]
                topic_k_words_vectors.append(word_vec)
                # index += 1

        topic_k_words_vectors = np.vstack(topic_k_words_vectors)

        V_bar_k = np.sum(topic_k_words_vectors, axis=0) / N_k

        mean_shifted = topic_k_words_vectors - V_bar_k
        C_k = np.dot(mean_shifted.T, mean_shifted)

        return V_bar_k, C_k

    def sample(self):
        for iteration_i in range(self.params['iterations']):
            print("Iteration: {0}".format(iteration_i))
            for doc_i in range(len(self.data.documents)):
                doc = self.data.documents[doc_i]
                for word_topic, word_id, word_position in zip(doc['doc_topics'], doc['doc_tokens'], range(len(doc['doc_topics']))):
                    self.doc_topic_count[doc_i, word_topic] -= 1
                    self.word_topic_count[word_id, word_topic] -= 1

                    self.updateTopicWishartParams(word_topic)

                    posterior = []
                    for k in range(self.params['K']):
                        log_p_wt = self.get_p_wt(word_id, k)
                        # log_p_wt = self.dmvt(word_id, k)
                        Nkd = self.doc_topic_count[doc_i, k]
                        log_posterior = log(Nkd + self.params['doc_smoothing']) * log_p_wt
                        posterior.append(log_posterior)

                    # print("posterior={0}".format(posterior))
                    # post_sum = np.sum(posterior)
                    # print("post_sum={0}".format(post_sum))
                    # normalized_posterior = posterior / post_sum
                    # print("normalized_post={0}".format(normalized_posterior))
                    # new_word_topic = np.argmax(np.random.multinomial(1, pvals=normalized_posterior))
                    # new_topic = new_word_topic

                    max_posterior = np.max(posterior)
                    posterior -= max_posterior
                    normalized_posterior = np.exp(np.asarray(posterior) - np.log(np.sum(np.exp(posterior))))
                    new_topic = np.argmax(np.random.multinomial(1, pvals=normalized_posterior))
                    print(normalized_posterior)

                    print("New topic: {0}".format(new_topic))
                    new_word_topic = new_topic
                    self.doc_topic_count[doc_i, new_word_topic] += 1
                    self.word_topic_count[word_id, new_word_topic] += 1
                    self.data.documents[doc_i]['doc_topics'][word_position] = new_word_topic

                    self.updateTopicWishartParams(new_word_topic)

                    pass

    def get_p_wt(self, word_id, word_topic):
        inv_cov = self.topics_params[word_topic]["Inverse Covariance"]
        cov_det = self.topics_params[word_topic]["Covariance Determinant"]
        # print(cov_det)
        Nk = self.topics_params[word_topic]["Topic Count"]
        centered = self.word_vectors.vectors[self.data.vocab[word_id]] - self.priors.mu

        LLcomp = centered.T.dot(inv_cov).dot(centered)
        d = self.vector_dim
        nu = self.priors.nu + Nk - d + 1

        log_prop = gammaln(nu + d / 2) - \
                   (gammaln(nu / 2) + d / 2 * (log(nu) + log(pi)) + 0.5 * log(cov_det) + (nu + d) / 2 * log(1 + LLcomp / nu))

        return log_prop

    def dmvt(self, word_id, topic_i):
        '''
        Multivariate t-student density. Returns the density
        of the function at points specified by x.

        input:
            x = parameter (n x d numpy array)
            mu = mean (d dimensional numpy array)
            Sigma = scale matrix (d x d numpy array)
            df = degrees of freedom
            log = log scale or not

        '''
        sigma = self.topics_params[topic_i]['Topic Covariance']
        p = sigma.shape[0]  # Dimensionality
        dec = np.linalg.cholesky(sigma)
        df = self.priors.nu
        x = self.word_vectors.vectors[self.data.vocab[word_id]]
        R_x_m = np.linalg.solve(dec, np.matrix.transpose(x) - self.priors.mu)
        rss = np.power(R_x_m, 2).sum(axis=0)
        logretval = lgamma(1.0 * (p + df) / 2)\
                    - (lgamma(1.0 * df / 2) + np.sum(np.log(dec.diagonal())) + p / 2 * np.log(math.pi * df)) - 0.5 * (df + p) * math.log1p((rss / df))

        return (np.exp(logretval))

    def results(self):
        # print topics words by word-topic count table
        topics_words = []
        K = self.params['K']
        for topic_i in range(K):
            words = []
            print("\nTopic {0}:".format(topic_i))
            sorted_words = sorted(zip(self.word_topic_count[:, topic_i], self.data.vocab), reverse=True)
            words = " ".join([w for x, w in sorted_words[:self.params['topic_num_words_to_print']]])
            print(words)
            topics_words.append(words)

        # print topics words by vector similarity to topic mean
        results = {}
        for topic_i in range(K):
            target_v = self.topics_params[topic_i]['Topic Mean']
            dot_products = np.asarray(self.data_vectors).dot(target_v)
            most_similar_ids = dot_products.argsort()[:self.params['topic_num_words_to_print']]
            target_results = [self.data.vocab[i] for i in most_similar_ids]
            results[topic_i] = target_results
            print("\nTopic {0}:".format(topic_i))
            print(target_results)



if __name__ == '__main__':
    script_starttime = datetime.now()

    # params
    params = {}
    K = int(2)
    doc_smoothing = 0.5  # alpha (theta)
    iterations = 100
    topic_num_words_to_print = 20

    params['K'] = K
    params['doc_smoothing'] = doc_smoothing
    params['iterations'] = iterations
    params['topic_num_words_to_print'] = topic_num_words_to_print

    data = utils.Documents(documents_dir_name='/home/daniel/deepsy/TM/test02/',
                stop_words_dir_name='/home/daniel/deepsy/TM/STOP_WORDS/',
                K=K)

    word_vectors = Vectors(emb_file_path='/home/daniel/Documents/Word_Embeddings/Glove/glove.6B.50d_partial.txt')

    model = GLDA(data, word_vectors, params)
    model.sample()

    model.results()


    pass