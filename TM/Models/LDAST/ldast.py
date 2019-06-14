from datetime import datetime
from utils import Documents
from utils import Vectors
import LDASTGibbs
import numpy as np
from scipy.stats import multivariate_normal
from utils import printime


def getNaiveGaussiansProbs(emb):
    """
    number of centroids is as the size of vocab
    make n*n matrix and calculate every cell gaussian probability
    :param emb:
    :return:
    """
    c_size = len(emb.vectors)
    probs = np.zeros(shape=[c_size, c_size])

    for i, (centroid_key, centroid_vec) in enumerate(emb.vectors.items()):
        for j, (word_key, word_vec) in enumerate(emb.vectors.items()):
            prob = multivariate_normal.pdf(word_vec, mean=centroid_vec)
            probs[i, j] = prob

    return probs


def getGaussians(emb):
    printime('Generating Gaussians ...', '')

    gaussians = getNaiveGaussiansProbs(emb)

    return gaussians


def main():
    script_starttime = datetime.now()

    # params
    params = {}
    K = int(2)
    doc_smoothing = 0.5  # alpha (theta)
    subtopic_smoothing = 0.01  # beta (phi)
    iterations = 1000
    topic_num_words_to_print = 20

    params['K'] = K
    params['doc_smoothing'] = doc_smoothing
    params['subtopic_smoothing'] = subtopic_smoothing
    params['iterations'] = iterations
    params['topic_num_words_to_print'] = topic_num_words_to_print

    emb = Vectors(emb_file_path='glove.6B.50d_partial.txt')

    gaussians = getGaussians(emb)
    # S = emb.num_of_vectors
    S = 8
    params['S'] = S

    data = Documents(documents_dir_name='test_data/',#'/home/daniel/deepsy/TM/client_5_mini_turns/',
                     stop_words_dir_name='/deepsy/TM/STOP_WORDS/',
                     K=K, S=S)

    model = LDASTGibbs.LDASTGibbsSampler(data, params, emb, gaussians)

    for document in data.documents:
        c_doc = LDASTGibbs.Document(document["doc_tokens"],
                                           document["doc_topics"],
                                           document["topic_counts"],
                                           document["doc_subtopics"],
                                           document["doc_subtopics_counts"])
        model.add_document(c_doc)

    model.learn()

    pass
    # run_time = datetime.now() - script_starttime
    # print("Run time: {0}".format(run_time))

if __name__ == '__main__':
    main()