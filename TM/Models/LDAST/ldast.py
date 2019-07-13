from datetime import datetime
from utils import Documents
from utils import Vectors
from utils import printime
from config import params
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
from scipy.special import softmax
import os
import matplotlib.pyplot as plt
import pickle


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

    for word in emb.data_vocab:
        values.append(emb.vectors[word])

    dist = euclidean_distances(values)

    return dist


def getMostSimilar(gaussians, params):
    """
    create list of data tokens, and their most similar words by the pre-computed gaussians matrix
    :param gaussians:
    :return:
    """
    num_of_most_similar_tokens = params['num_of_most_similar_tokens']
    msg = 'Sorting ' + str(num_of_most_similar_tokens) + ' most similar tokens ...'
    printime(msg, '')

    # shift can be +1 because starts from index 1 and not 0
    shift = 0
    most_similar = []
    for token in gaussians:
        token_most_similar = (-token).argsort()[shift:num_of_most_similar_tokens+shift]
        most_similar.append(token_most_similar)

    most_similar = np.asarray(most_similar)
    return most_similar


def getNormalProbs(emb, params):
    """
    number of centroids is as the size of vocab
    make n*n matrix and calculate every cell gaussian probability
    :param emb:
    :return:
    """
    printime('Generating Normal Probabilities ...', '')
    values = []
    sigma = params['sigma']

    for word in emb.data_vocab:
        values.append(emb.vectors[word])
    values_np = np.asarray(values)

    # for mem saving
    del emb.vectors

    values = np.vstack(values_np)
    dist = euclidean_distances(values)
    word_word_probs = softmax(-dist/sigma, axis=1)

    return word_word_probs


def getGaussians(emb, params):
    # dists = getVecDists(emb)
    gaussians = getNormalProbs(emb, params)

    most_similar = getMostSimilar(gaussians, params)

    return gaussians, most_similar


def write2file(topics_top_words, file_name):
    with open(file_name, 'w') as f:
        for line in topics_top_words:
            f.write(line)
            f.write('\n')


def writeInfo(info_file, params, run_time, data):
    with open(info_file, 'w') as f:
        # params
        for param in params.items():
            line = str(param[0]) + ': ' + str(param[1]) + '\n'
            f.writelines(line)

        # data statistics
        data_stats = []
        f.writelines('\n')
        data_stats.append("Num of documents: {0}\n".format(len(data.documents)))
        data_stats.append("Num of words before droping: {0}\n".format(data.words_num_before))
        data_stats.append("Num of words after droping: {0}\n".format(data.words_num_after))
        data_stats.append("Num of tokens: {0}\n".format(data.vocab_size))
        data_stats.append("Num of stop words: {0}\n".format(len(data.stop_words_set)))
        data_stats.append("Num of initially emb vocab: {0}\n".format(data.all_emb_words_len))
        for stat in data_stats:
            f.writelines(stat)

        # stop words files
        print("Stop words were loaded from:")
        for file_name in data.stop_words_files_names:
            f.writelines('\n')
            f.writelines(file_name)

        # times
        f.writelines('\n\n')
        line = 'Running time: {0}\n'.format(run_time)
        f.writelines(line)


def generateOutputFiles():
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    directory = 'logs/' + str(timestamp)

    if not os.path.exists(directory):
        os.makedirs(directory)

    info_file = directory + '/info.txt'
    keys_file = directory + '/keys.txt'
    tokens_keys_file = directory + '/tokens_keys.txt'

    return info_file, keys_file, tokens_keys_file, directory


def plotSwaps(Z_swap, S_swap, directory):
    plt.plot(Z_swap, label='Z')
    plt.plot(S_swap, label='S')
    plt.xlabel('Iteration')
    plt.ylabel('Swaps')
    plt.legend(loc='upper right')
    plt.savefig(directory+'/swaps.png')


def saveMatrices(directory, subtopic_topic_mat, tokens_subtopics_mat, tokens_topic, tokens_count):
    np.save(directory + '/subtopic_topic.npy', subtopic_topic_mat.base)
    np.save(directory + '/tokens_subtopics.npy', tokens_subtopics_mat.base)
    np.save(directory + '/tokens_topic.npy', tokens_topic)

    with open(directory + '/tokens_count.pkl', 'wb') as f:
        pickle.dump(tokens_count, f)


def main():
    script_starttime = datetime.now()

    info_file, keys_file, tokens_keys_file, directory = generateOutputFiles()

    data = Documents(documents_dir_name=params['DOCUMENTS_DIR'],
                     stop_words_dir_name=params['STOP_WORDS_DIR'],
                     K=params['K'],
                     emb_vocab_file_name=params['VOCAB_FILE'])

    emb = Vectors(emb_file_path=params['EMB_FILE'],
                  emb_format='npy',
                  vocab_file_path=params['VOCAB_FILE'],
                  data_vocab=data.tokens_ids)

    gaussians, most_similar_tokens = getGaussians(emb, params)
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

    topics_top_centroids = model.print_all_topics(params['topic_num_words_to_print'])
    write2file(topics_top_centroids, keys_file)

    writeInfo(info_file, params, run_time, data)

    Z_swap, S_swap, S_samples_index = model.getStats()
    plotSwaps(Z_swap, S_swap, directory)

    subtopic_topic_mat, tokens_subtopics_mat, tokens_topic, tokens_topic_printed = model.getMatrices()
    write2file(tokens_topic_printed, tokens_keys_file)
    # for extended info
    saveMatrices(directory, subtopic_topic_mat, tokens_subtopics_mat, tokens_topic, data.tokens_count)

    pass


if __name__ == '__main__':
    main()
