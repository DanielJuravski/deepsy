from utils import Vectors
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import euclidean_distances

import seaborn as sns


def getVars(emb):
    vars = []
    words, values = [], []
    word2idx = {}

    for idx, (word, value) in enumerate(emb.vectors.items()):
        words.append(word)
        values.append(value)
        word2idx[idx] = word

    dist = euclidean_distances(values)

    for i in range(emb.num_of_vectors):
        indices_i = np.argsort(dist[i])[:50]
        dist_i = dist[i, indices_i]
        if (i % 1000) == 0:
            print(f"center: {words[i]}: " + " ".join(words[idx] for idx in indices_i))
        avg = np.average(dist_i)
        vars.append(avg)


    return vars

def plot(x):
    sns.distplot(x, kde=False)
    # plt.hist(x, density=True, bins=30)
    plt.show()


if __name__ == '__main__':
    TOP_WORDS = 50
    # emb_file = 'glove.6B.50d_partial.txt'
    emb_file = '/home/daniel/Documents/Word_Embeddings/Glove/glove.6B.50d_10K_lines.txt'
    # emb_file = '/home/daniel/Documents/Word_Embeddings/Glove/glove.6B.50d.txt'
    emb = Vectors(emb_file_path=emb_file)
    vars = getVars(emb)
    print(vars)
    print(len(vars))
    plot(vars)