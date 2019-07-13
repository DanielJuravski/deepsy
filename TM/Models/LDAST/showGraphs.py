import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import interactive
import pickle as pkl

DIR = '2019_07_12_13_28_49'


def getDirPath():
    if '--dir' in sys.argv:
        option_i = sys.argv.index('--dir')
        dir = sys.argv[option_i + 1]
    else:
        dir = DIR

    path = '/home/daniel/deepsy/TM/Models/LDAST/logs/' + dir + '/'

    return path


def makeGraphs(path, tokens_subtopics, tokens_count):
    # make centroid frequency graph
    centroids_appearance_count = [sum(tokens_subtopics[:,i]) for i in range(tokens_subtopics.shape[1])]
    centroids_appearance_count_sorted = sorted(centroids_appearance_count, reverse=True)
    plt.plot(centroids_appearance_count, label='Token count')
    plt.plot(centroids_appearance_count_sorted, label='Sorted')
    plt.xlabel('Centroids id')
    plt.ylabel('Count')
    plt.legend(loc='upper right')
    plt.savefig(path + 'cf')

    # make data word frequency graph, sorted data.
    plt.clf()
    vocab_counters = list(tokens_count.values())
    vocab_counters_sorted = sorted(list(tokens_count.values()), reverse=True)
    plt.plot(vocab_counters, label='Token count')
    plt.plot(vocab_counters_sorted, label='Sorted')
    plt.xlabel('Tokens id')
    plt.ylabel('Count')
    plt.legend(loc='upper right')
    plt.savefig(path + 'wf.png')

    # make cf vs wf graph - effect can be seen only in plt.show()
    plt.clf()
    plt.plot(centroids_appearance_count_sorted, label='Centroids Sorted')
    plt.plot(vocab_counters_sorted, label='Tokens Sorted')
    plt.xlabel('id')
    plt.ylabel('Count')
    plt.legend(loc='upper right')
    plt.savefig(path + 'wf_vs_cf.png')
    plt.show()

    # make centroid-radios graph.
    # how many tokens appears in every centroid.
    plt.clf()
    centroids_radius_count = [len(np.where((tokens_subtopics[:,i]) != 0)[0]) for i in range(tokens_subtopics.shape[1])]
    centroids_radius_count_sorted = sorted(centroids_radius_count, reverse=True)
    plt.plot(centroids_radius_count, label='Count')
    plt.plot(centroids_radius_count_sorted, label='Sorted')
    plt.xlabel('Centroid')
    plt.ylabel('Tokens count')
    plt.legend(loc='upper right')
    plt.savefig(path + 'centroid_radios.png')
    plt.show()


def loadObjects(path):
    tokens_subtopics = np.load(path + 'tokens_subtopics.npy')
    with open(path + 'tokens_count.pkl', 'rb') as f:
        tokens_count = pkl.load(f)

    return tokens_subtopics, tokens_count


if __name__ == '__main__':
    # plot the matrices that created by the LDAST process
    # save the plots to the same dir
    path = getDirPath()
    tokens_subtopics, tokens_count = loadObjects(path)
    makeGraphs(path, tokens_subtopics, tokens_count)