# input:    single embedding file where the word and the vector in the same line
#           word 1.1 1.3 324.2 4.35 345.34 56.26 ...
#           for example Glove format
# output:   2 files:
#           1. vocab file with at each line there is a word (.txt)
#           2. vector file, where every line is a vector of a word at the vocab's line (.npy)

import numpy as np


INPUT_FILE = '/home/daniel/Documents/Word_Embeddings/Glove/glove.6B.50d.txt'
OUTPUT_VOCAB_FILE = '/home/daniel/Documents/Word_Embeddings/Glove/glove.6B.50d.vocab.txt'
OUTPUT_EMB_FILE = '/home/daniel/Documents/Word_Embeddings/Glove/glove.6B.50d.vectors.npy'

words = []
vecs = []
with open(INPUT_FILE, 'r') as f:
    for line in f:
        details = line.split()
        word = details[0]
        vec = np.array(details[1:])
        vec_np = vec.astype(np.float)

        words.append(word)
        vecs.append(vec_np)

    pass

with open(OUTPUT_VOCAB_FILE, 'w') as f:
    for word in words:
        f.writelines(word)
        f.writelines('\n')

np.save(OUTPUT_EMB_FILE, vecs)