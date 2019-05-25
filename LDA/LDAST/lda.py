from LDA.LDAST import utils
from LDA.LDAST.utils import printime
import copy
from random import randint
import numpy as np


def initTA(data, params):
    """
    init TA (topic assignment) list. list of lists where each sub-list represents a document topics.
    randomly assign each word in each document to one of the K topics.
    ta object is similar to the documents by its structure,
    the difference is the assignment of the topic indexed instead of the tokens indexes
    :param data: Documents object
    :param params: model parameters
    :return: initialized ta
    """
    K = params['K']
    ta = copy.deepcopy(data.documents)

    printime('Initializing TA list', '')
    # iterate over all the docs
    for doc in ta:
        # iterate over every word in the current doc
        for word_i in range(len(doc)):
            rand_k = randint(0, K-1)
            doc[word_i] = rand_k

    return ta


def updateWT(wt, documents, ta):
    """
    iterate over the documents and the ta, calculate and update each word-topic co-accurance
    :param wt:
    :param documents:
    :param ta:
    :return:
    """
    for doc in zip(documents, ta):
        for word_i in range(len(doc[0])):
            token = doc[0][word_i]
            topic = doc[1][word_i]
            wt[token][topic] += 1

    return wt


def initWT(data, params, ta):
    """
    initialize WT (Word Topic) matrix which is the count of each word being assigned to each topic.
    :param data: Documents object
    :param params: model parameters
    :param ta: initialized ta list
    :return: initialized wt
    """
    printime('Initializing WT matrix', '')

    K = params['K']
    vocab_len = len(data.vocab)

    # init matrix
    wt = [[0 for i in range(K)] for j in range(vocab_len)]
    wt = updateWT(wt, data.documents, ta)

    return wt


def updateDT(dt, documents, ta):
    """
    iterate over the the ta, calculate and update each document-topic co-accurance.
    Count how many times each topic was in each document.
    :param dt:
    :param documents:
    :param ta:
    :return:
        """
    for doc_i in range(len(ta)):
        doc = ta[doc_i]
        for word_i in range(len(doc)):
            topic = doc[word_i]
            dt[doc_i][topic] += 1

    return dt


def initDT(data, params, ta):
    """
    initialize DT (Document Topic) matrix,
    which is the number of words assigned to each topic for each document (distribution of the topic assignment list)
    :param data: Documents object
    :param params: model parameters
    :param ta: initialized ta list
    :return: initialized dt
    """
    printime('Initializing DT matrix', '')

    K = params['K']
    documents_len = len(data.documents)

    # init matrix
    dt = [[0 for i in range(K)] for j in range(documents_len)]
    dt = updateDT(dt, data.documents, ta)

    return dt


def sanityMatrices(ta, wt, dt, data):
    # check sum of appearance, need to be summarized to the num of words
    wt_sum = sum(sum(wt, []))
    if wt_sum != data.words_num:
        raise Exception('wt matrix values are incorrect')

    # check sum of appearance, need to be summarized to the num of words
    dt_sum = sum(sum(dt, []))
    if dt_sum != data.words_num:
        raise Exception('dt matrix values are incorrect')

    # check tokens count, token sigma over each topic need to be summarized to the token appearance in the documents
    for token_i in range(len(wt)):
        token_topics = wt[token_i]
        for token_name, token_id in data.vocab.items():
            if token_id == token_i:
                token = token_name
        if sum(token_topics) != data.tokens_count[token]:
            raise Exception('wt matrix values are incorrect token {0} has more/few attributions to topics then it needs to'.format(token_i))


def initMatrices(data, params):
    """
    init ta list and wt, dt matrices
    ta: topic assignment
    wt: word topic
    dt: document topic
    :param data: Documents data
    :param params: model params
    :return: initialized ta, wt, dt
    """
    ta = initTA(data, params)
    wt = initWT(data, params, ta)
    dt = initDT(data, params, ta)

    sanityMatrices(ta, wt, dt, data)

    return ta, wt, dt


def decreaseMatricesCount(doc_i, word_i, token, ta, wt, dt):
    topic = ta[doc_i][word_i]
    dt[doc_i][topic] -= 1
    wt[token][topic] -= 1

    return dt, wt


def train(ta, wt, dt, data, params):
    iterations = params['iterations']
    K = params['K']
    alpha = params['alpha']
    eta = params['eta']
    documents = data.documents
    tokens_num = data.tokens_num
    words_num = data.words_num

    printime('Train started', '')
    for iteration in range(iterations):
        if iteration % 10 == 0:
            # printime('Training iteration', iteration)
            pass
        for doc_i in range(len(documents)):
            if iteration % 10 == 0:
                # printime('Training doc', doc_i)
                pass
            doc = documents[doc_i]
            for word_i in range(len(doc)):
                token = doc[word_i]

                # z_-i means that we do not include token w in our word-topic and document-topic count matrix when
                # sampling for token w, only leave the topic assignments of all other tokens for current document
                dt, wt = decreaseMatricesCount(doc_i, word_i, token, ta, wt, dt)

                # calculate probs for every topic
                next_topic_probs = []
                for topic in range(K):
                    wt_wj = wt[token][topic]
                    wt_sigma = sum([wt[i][topic] for i in range(tokens_num)])
                    dt_dj = dt[doc_i][topic]
                    dt_sigma = sum([dt[doc_i][j] for j in range(K)])

                    prob_topic = ((wt_wj + eta)/(wt_sigma + tokens_num * eta)) * ((dt_dj + alpha)/(dt_sigma + K * alpha))
                    next_topic_probs.append(prob_topic)

                normalized_next_topic_probs = [next_topic_probs[i]/sum(next_topic_probs) for i in range(K)]
                sampled_topic = np.random.choice(a=K, p=normalized_next_topic_probs)

                # update matrices
                ta[doc_i][word_i] = sampled_topic
                wt[token][sampled_topic] += 1
                dt[doc_i][sampled_topic] += 1
                # sanityMatrices(ta, wt, dt, data)
    printime('Train ended', '')

    return ta, wt, dt


def printTopics(wt, data, params):
    K = params['K']
    eta = params['eta']
    tokens_to_print = params['tokens_to_print']

    for topic in range(K):
        phi = []
        for token in data.vocab:
            token_i = data.vocab[token]
            wt_wj = wt[token_i][topic]
            wt_sigma = sum([wt[i][topic] for i in range(data.tokens_num)])
            phi_ij = (wt_wj + eta) / (wt_sigma + data.tokens_num * eta)
            phi.append((token, phi_ij))

        # calculate prov sum to for validating it is 1
        prob_topic_i = sum(phi[i][1] for i in range(len(phi)))

        phi = [sorted(phi, key=lambda x: x[1], reverse=True)[i][0] for i in range(len(phi))]
        phi = phi[:tokens_to_print]

        msg = "sum prob over topic {0}: {1}".format(topic, prob_topic_i)
        print(msg)
    print()


def printOutput(ta, wt, dt, data, params):
    printTopics(wt, data, params)


if __name__ == '__main__':
    """
    That is a vanilla impl of the LDA topic model
    """
    K = 10
    alpha = 1
    eta = 0.001
    iterations = 500
    # how many words print in the Topic-Key print
    tokens_to_print = 20

    params = dict()
    params['K'] = K
    params['alpha'] = alpha
    params['eta'] = eta
    params['iterations'] = iterations
    params['tokens_to_print'] = tokens_to_print

    data = utils.Documents(documents_dir_name='/home/daniel/deepsy/LDA/test/',
                       # documents_dir_name=/home/daniel/deepsy/LDA/client_5_mini_turns/,
                       stop_words_dir_name='/home/daniel/deepsy/LDA/LDAST/STOP_WORDS/')

    ta, wt, dt = initMatrices(data, params)
    ta, wt, dt = train(ta, wt, dt, data, params)

    printOutput(ta, wt, dt, data, params)






