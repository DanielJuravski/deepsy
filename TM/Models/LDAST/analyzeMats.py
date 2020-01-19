import sys
import numpy as np
import pickle as pkl
import matplotlib.pyplot as plt

DIR = '2019_07_31_15_58_00'

def getDirPath():
    if '--dir' in sys.argv:
        option_i = sys.argv.index('--dir')
        dir = sys.argv[option_i + 1]
    else:
        dir = DIR

    path = '/home/daniel/deepsy/TM/Models/LDAST/logs/' + dir + '/'

    return path


def loadObjects(path):
    print("Loading ...")

    tokens_subtopics = np.load(path + 'tokens_subtopics.npy')
    tokens_topic = np.load(path + 'tokens_topic.npy')
    with open(path + 'tokens_ids_rev.pkl', 'rb') as f:
        tokens_ids_rev = pkl.load(f)

    # vanilla word_topics
    vanilla_word_topics = np.load('/home/daniel/deepsy/TM/Models/vanilla_LDA/word_topics.npy')
    with open('/home/daniel/deepsy/TM/Models/vanilla_LDA/tokens_ids.pkl', 'rb') as f:
        vanilla_tokens_ids = pkl.load(f)

    return tokens_subtopics, tokens_topic, tokens_ids_rev, vanilla_word_topics, vanilla_tokens_ids


def analyze(path, tokens_subtopics, tokens_topic, tokens_ids_rev, vanilla_word_topics, vanilla_tokens_ids):
    '''
    find the topics of the words that in the same centroids
    '''
    print("Analyzing ...")

    # make tokens_groups: each cell is a list of tokens that appear in the same centroid
    tokens_groups = []
    for centroid in range(tokens_subtopics.shape[1]):
        centroid_tokens = np.where(tokens_subtopics[:, centroid] != 0)[0]
        tokens_groups.append(centroid_tokens)

    # find each group topics & count the number of topics at each group
    tokens_groups_topics = []
    tokens_groups_topics_count = []
    tokens_groups_words = []
    for tg in tokens_groups:
        topics = set()
        words = set()
        for tkn in tg:
            t_topics = np.where(tokens_topic[tkn] != 0)[0]
            topics.update(t_topics)
            words.add(tokens_ids_rev[tkn])
        tokens_groups_topics.append(topics)
        tokens_groups_topics_count.append(len(topics))
        tokens_groups_words.append(words)
    tokens_groups_topics_count_sorted = sorted(tokens_groups_topics_count, reverse=True)


    ### vs LDA vanilla ###
    # make vanilla tokens group
    vanilla_tokens_groups = []
    vanilla_tokens_groups_topics = []
    vanilla_tokens_groups_topics_count = []
    for gr in tokens_groups_words:
        tokens = []
        for word in gr:
            token = vanilla_tokens_ids[word]
            tokens.append(token)
        vanilla_tokens_groups.append(tokens)

    for vtg in vanilla_tokens_groups:
        topics = set()
        for tkn in vtg:
            t_topics = np.where(vanilla_word_topics[tkn] != 0)[0]
            topics.update(t_topics)
        vanilla_tokens_groups_topics.append(topics)
        vanilla_tokens_groups_topics_count.append(len(topics))
    vanilla_tokens_groups_topics_count_sorted = sorted(vanilla_tokens_groups_topics_count, reverse=True)


    # plot topics count
    plt.plot(tokens_groups_topics_count_sorted, label='LDAST')
    plt.plot(vanilla_tokens_groups_topics_count_sorted, label='vanilla')
    plt.legend(loc='upper right')
    plt.savefig(path+'topic_f')
    plt.show()



if __name__ == '__main__':
    # load the relevant log dir objects and analyze the results.
    path = getDirPath()
    tokens_subtopics, tokens_topic, tokens_ids_rev, vanilla_word_topics, vanilla_tokens_ids = loadObjects(path)
    analyze(path, tokens_subtopics, tokens_topic, tokens_ids_rev, vanilla_word_topics, vanilla_tokens_ids)