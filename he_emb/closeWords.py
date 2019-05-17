import numpy as np
import sys

TARGET_WORDS = ["דתי"]

VOCAB_FILE = '/home/daniel/Documents/he_emb/ron_shemesh/words_list.txt'
EMB_FILE = '/home/daniel/Documents/he_emb/ron_shemesh/words_vectors.npy'


def getOptions():
    vocab_file = emb_file = target_word = None

    if '--vocab' in sys.argv:
        option_i = sys.argv.index('--vocab')
        vocab_file = sys.argv[option_i + 1]
    else:
        vocab_file = VOCAB_FILE

    if '--emb' in sys.argv:
        option_i = sys.argv.index('--emb')
        emb_file = sys.argv[option_i + 1]
    else:
        emb_file = EMB_FILE

    if '--word' in sys.argv:
        option_i = sys.argv.index('--word')
        target_word = sys.argv[option_i + 1:]
    else:
        target_word = TARGET_WORDS

    if vocab_file == None or \
            emb_file == None:
        print("Usage:\n"
              "python3 closeWords.py [--vocab $VOCAB_FILE] [--emb $EMB_FILE] [--word $WORD]\n"
              "Exiting.")
        sys.exit()

    return vocab_file, emb_file, target_word


def loadData(vocab_file, emb_file, target_word):
    print("Loading vocab")
    with open(vocab_file, 'r') as f:
        vocab = f.read().splitlines()
    print("vocab has been loaded\nvocab length is {0}".format(len(vocab)))

    print("Loading emb")
    emb = np.load(emb_file)
    print("emb has been loaded\nemb length is {0}".format(len(emb)))

    # take care if single word, then split it. for the list iteration.
    target_word = target_word.split() if type(target_word) is not list else target_word

    return vocab, emb, target_word


def get_close_words(vocab, emb, target_words, num_of_close, remove_first=False):
    start_index = -2 if remove_first else -1
    results = {}
    # tokenize words
    w2i = {w:i for i, w in enumerate(vocab)}

    for target_word in target_words:
        target_v = emb[w2i[target_word]]
        dot_products = emb.dot(target_v)
        most_similar_ids = dot_products.argsort()[start_index:-(num_of_close+2):-1]
        target_results = [vocab[i] for i in most_similar_ids]
        results[target_word] = target_results

    return results


def printThis(results):
    for target in results:
        close_words = str()
        print("\nTarget: " + target[::-1])
        for word in reversed(results[target]):
            close_words += ' ,' + str(word[::-1])
        print("Close words: " + close_words)


if __name__ == '__main__':
    vocab_file, emb_file, target_word = getOptions()
    vocab, emb, target_word = loadData(vocab_file, emb_file, target_word)

    results = get_close_words(vocab, emb, target_word, num_of_close=20, remove_first=False)

    printThis(results)
