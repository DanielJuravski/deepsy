from datetime import datetime
from utils import Documents
from utils import Vectors
from utils import printime
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
from scipy.special import softmax
# import LDASTGibbs


import pyximport
pyximport.install()
from deepsy.TM.Models.LDAST import LDASTGibbs
# import py_LDASTGibbs as LDASTGibbs


def getVecDists(emb):
    """
    number of centroids is as the size of vocab
    make n*n matrix and calculate every cell gaussian probability
    :param emb:
    :return:
    """
    printime('Generating Dists Gaussians ...', '')
    values = []

    # for idx, (word, value) in enumerate(emb.vectors.items()):
    #     words.append(word)
    #     values.append(value)

    for word in emb.data_vocab:
        values.append(emb.vectors[word])

    dist = euclidean_distances(values)

    return dist


def getMostSimilar(gaussians, MOST_SIMILAR_TOKENS):
    """
    create list of data tokens, and their most similar words by the pre-computed gaussians matrix
    :param gaussians:
    :return:
    """
    msg = 'Sorting ' + str(MOST_SIMILAR_TOKENS) + ' most similar tokens ...'
    printime(msg, '')

    # shift can be +1 because starts from index 1 and not 0
    shift = 0
    most_similar = []
    for token in gaussians:
        token_most_similar = (-token).argsort()[shift:MOST_SIMILAR_TOKENS+shift]
        most_similar.append(token_most_similar)

    most_similar = np.asarray(most_similar)
    return most_similar


def getNormalProbs(emb):
    """
    number of centroids is as the size of vocab
    make n*n matrix and calculate every cell gaussian probability
    :param emb:
    :return:
    """
    printime('Generating Normal Probabilities ...', '')
    values = []

    # for idx, (word, value) in enumerate(emb.vectors.items()):
    #     words.append(word)
    #     values.append(value)

    for word in emb.data_vocab:
        values.append(emb.vectors[word])
    values_np = np.asarray(values)

    values = np.vstack(values_np)
    dist = euclidean_distances(values)
    sigma = 2
    word_word_probs = softmax(-dist/sigma, axis=1)

    return word_word_probs


def getGaussians(emb, MOST_SIMILAR_TOKENS):
    # dists = getVecDists(emb)
    gaussians = getNormalProbs(emb)

    most_similar = getMostSimilar(gaussians, MOST_SIMILAR_TOKENS)

    # for mem saving
    del emb.vectors

    return gaussians, most_similar


def main():
    script_starttime = datetime.now()

    # params
    params = {}
    K = int(50)
    doc_smoothing = 0.5  # alpha (theta)
    z_subtopic_smoothing = 0.01  # beta (phi)
    s_subtopic_smoothing = 0.01  # beta (phi)
    subtopic_smoothing = 0.01  # for py_ version
    iterations = 10000
    topic_num_words_to_print = 20
    num_of_most_similar_tokens = 100

    params['K'] = K
    params['doc_smoothing'] = doc_smoothing
    params['z_subtopic_smoothing'] = z_subtopic_smoothing
    params['s_subtopic_smoothing'] = s_subtopic_smoothing
    params['subtopic_smoothing'] = subtopic_smoothing
    params['iterations'] = iterations
    params['topic_num_words_to_print'] = topic_num_words_to_print
    params['num_of_most_similar_tokens'] = num_of_most_similar_tokens

    VOCAB_FILE = '/home/daniel/Documents/he_emb/ron_shemesh/words_list.txt'
    EMB_FILE = '/home/daniel/Documents/he_emb/ron_shemesh/words_vectors.npy'

    # emb = Vectors(emb_file_path='/home/daniel/Documents/Word_Embeddings/Glove/glove.6B.50d.txt')

    data = Documents(documents_dir_name='/home/daniel/deepsy/TM/client_5_mini_turns/',
                     #documents_dir_name = 'Generated_Data/',
                     #documents_dir_name='/home/daniel/deepsy/TM/tmp/samples/',
                     stop_words_dir_name='/home/daniel/deepsy/TM/STOP_WORDS/',
                     K=K,
                     emb_vocab_file_name=VOCAB_FILE)

    emb = Vectors(emb_file_path=EMB_FILE,
                  emb_format='npy',
                  vocab_file_path=VOCAB_FILE,
                  data_vocab=data.tokens_ids)

    gaussians, most_similar_tokens = getGaussians(emb, num_of_most_similar_tokens)
    # gaussians = None
    S = emb.num_of_vectors
    params['S'] = S

    data.initTopics(S=S)

    print()
    printime('Initializing Model ...', '')
    model = LDASTGibbs.LDASTGibbsSampler(data, params, gaussians, most_similar_tokens)

    for document in data.documents:
        c_doc = LDASTGibbs.Document(document["doc_tokens"],
                                    document["doc_topics"],
                                    document["topic_counts"],
                                    document["doc_subtopics"],
                                    document["doc_subtopics_counts"])
        model.add_document(c_doc)

    model.learn()

    run_time = datetime.now() - script_starttime
    print("Run time: {0}".format(run_time))

    topics_top_words = model.print_all_topics(topic_num_words_to_print)


if __name__ == '__main__':
    main()