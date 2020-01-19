import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
from scipy.special import softmax

size = 16000

values = []
for i in range(size):
    a = np.random.random_sample(100)
    values.append(a)
values_np = np.asarray(values, dtype=np.float16)
values = np.vstack(values_np)
dist = euclidean_distances(values)

word_word_probs = softmax(-dist/3, axis=1)

pass