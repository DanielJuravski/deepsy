from utils import Vectors

import numpy as np
from scipy.special import softmax
from sklearn.metrics.pairwise import euclidean_distances


def sample_toy_data_with_distances(vectors,
                    n_docs=100,
                    n_vocab=10000,
                    doc_len=50,
                    n_topics=4,
                    doc_pseudo=0.5, vocab_pseudo=0.001):

    vocab = []
    vocab_vecs = []
    for idx, (word, vec) in enumerate(vectors.items()):
        vocab.append(word)
        vocab_vecs.append(vec)
        if idx > n_vocab:
            break

    vocab_dist = [np.random.dirichlet(np.ones(n_vocab)*vocab_pseudo)
                  for _ in range(n_topics)]
    vocab_vecs = np.vstack(vocab_vecs)
    sqr_dists = euclidean_distances(vocab_vecs, squared=True)
    sigma = 3.5
    # Transfrom into exponential distances, as in gaussian setting
    # ~ exp { (x - mu)^T E^-1 (x - mu)}
    # if E == lambda*I then this is: 1/lambda*(x-mu)^T(x - mu)
    word_word_probs = softmax(-sqr_dists/sigma, axis=1)

    docs = []
    centroid_docs = []
    doc_dists = []
    for d in range(n_docs):
        topic_dist = np.random.dirichlet(np.ones(n_topics)*doc_pseudo)
        doc_dists.append(topic_dist)
        assignments = np.random.choice(n_topics, size=doc_len, p=topic_dist)
        doc = []
        centroid_doc = []
        for topic in assignments:
            pivot_word_idx = np.random.choice(n_vocab, p=vocab_dist[topic])
            pivot_probs = word_word_probs[pivot_word_idx, :]
            pivot_word = vocab[pivot_word_idx]
            # now sample actual word
            word_idx = np.random.choice(n_vocab, p=pivot_probs)
            sampled_word = vocab[word_idx]
            # print(pivot_word, sampled_word)
            doc.append(sampled_word)
            centroid_doc.append(pivot_word)
        docs.append(" ".join(doc))
        centroid_docs.append(" ".join(centroid_doc))
    return docs, centroid_docs, vocab_dist, doc_dists


if __name__ == '__main__':
    emb_file = '/home/daniel/Documents/Word_Embeddings/Glove/glove.6B.50d_10K_lines.txt'
    # emb_file = '/home/daniel/Documents/Word_Embeddings/Glove/glove.6B.50d.txt'
    emb = Vectors(emb_file_path=emb_file)

    docs, centroid_docs, vocab_dist, doc_dists = sample_toy_data_with_distances(emb.vectors)
    doc_idx = 1
    for doc, cent_doc in zip(docs, centroid_docs):
        print("*"*20)
        print(doc)
        print(cent_doc)
        print()

        doc_name = "Generated_Data/doc" + str(doc_idx)
        with open(doc_name, 'w') as f:
            f.writelines(doc)
        doc_idx += 1
