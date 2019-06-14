import os
import datetime
import random
import numpy as np
from collections import Counter


class Documents(object):
    def __init__(self, documents_dir_name, stop_words_dir_name, K, S):
        """
        Batch of imported documents and their vocabulary object.
        The 'Documents' object include 2 macro information:
        Documents.documents: list of dicts, where each dist got:
        1. The original document words
        2. Tokenized words of the document (After stop-words filter)
        3. List of size K, that indicates the count of each topic in this document.
        Documents.vocab: list of the tokens (words in stop-words files are not in the vocab.
        :param documents_dir_name: dir where all the documents files.
        :param stop_words_dir_name: dir where all the stop-words files.
        :param K: number of topics
        :param S: number of sub-topics
        """

        # Documents dir with all documents files. No validation checks, assumes the dir is valid.
        self.documents_dir_name = documents_dir_name

        # Vocabulary of the tokens that created the documents. Each word is unique.
        self.vocab = []

        # Vocabulary size (length)
        self.vocab_size = 0

        # Vocab's tokens id's
        self.tokens_ids = {}

        # Count all the words in the input documents before the stop-word filtering.
        self.words_num_before = 0

        # Count all the words in the input documents after the stop-word filtering.
        self.words_num_after = 0

        # List of tokenized documents
        self.documents = []

        # In stop_words_dir_name there are files that contain the stop-words. Stop-words should not be tokenized.
        self.stop_words_dir_name = stop_words_dir_name

        # Set of all the stop words that in the 'self.stop_words_dir_name'.
        # If the documents contain that words, they won't be tokenized.
        self.stop_words_set = set()

        # Dict of tokens and their count
        self.tokens_count = Counter()

        # init K - num of topics
        self.K = K

        # init S - num of sub topics
        self.S = S

        # load stop-words
        self.loadStopWords(ignore_stop_words=False)

        # load and process the documents files
        self.loadDocs()

        # print statistics
        self.statistics()

        # Randomize first time topics to each word and update counters respectively.
        self.initTopics()

    def loadDocs(self):
        printime('Loading documents ...', '')
        dir = os.fsencode(self.documents_dir_name)
        for doc in os.listdir(dir):
            doc_name = os.fsdecode(doc)
            doc_full_path = self.documents_dir_name + str(doc_name)
            # print('loading document: {0}'.format(doc_name))

            with open(doc_full_path, 'r') as f:
                doc_words = f.read().split()
                doc_tokens = self.add2Vocab(doc_words)
                doc_topic_counts = np.zeros(self.K, dtype=int)
                doc_subtopic_counts = np.zeros(self.S, dtype=int)

                self.documents.append({"original": doc_words,
                                       "token_strings": doc_tokens,
                                       "topic_counts": doc_topic_counts,
                                       "doc_subtopics_counts": doc_subtopic_counts})

                self.words_num_before += len(doc_words)
                self.words_num_after += len(doc_tokens)

        self.vocab = list(self.tokens_count.keys())
        self.vocab_size = len(self.vocab)
        self.tokens_ids = {w: i for (i, w) in enumerate(self.vocab)}

        printime('Loading was done successfully.', '')

    def add2Vocab(self, doc_words, filter_uni=True, filter_bi=True):
        """
        add new works to vocab and return tokenized doc representation
        :param doc_words: list of lists with doc's words
        :param filter_uni: if true - ignore all the unigrams words (one char) in the document (good for HE/good for EN)
        :param filter_bi: if true - ignore all the bigrams words (two chars) in the document (bad for HE/good for EN)
        :return: doc_tokens
        """
        doc_tokens = []
        for word in doc_words:

            # drop strings with 1 char only
            if filter_uni:
                if len(word) == 1:
                    continue

            # drop strings with 2 chars only
            if filter_bi:
                if len(word) == 2:
                    continue

            # validate stop-word
            if word not in self.stop_words_set:

                doc_tokens.append(word)

        self.tokens_count.update(doc_tokens)

        return doc_tokens

    def loadStopWords(self, ignore_stop_words=False):
        """
        load stop words files. iterate over the stop-words dir, open each file and extract the words that in the file.
        words that will be in the stop-words set won't be tokenized
        :param ignore_stop_words: ignore the stop-words file. Do NOT load them.
        :return:
        """
        if ignore_stop_words == True:
            printime('Ignoring stop-words files. Stop-words files were NOT loaded!', '')
        else:
            dir = os.fsencode(self.stop_words_dir_name)
            for file in os.listdir(dir):
                file_name = os.fsdecode(file)
                file_full_path = self.stop_words_dir_name + str(file_name)
                printime('Loading stop-words:', file_name)

                with open(file_full_path, 'r') as f:
                    words = f.read().split()
                    for word in words:
                        self.stop_words_set.add(word)

    def statistics(self):
        """
        print statistics of the relevant variables
        :return:
        """
        print()
        print("Num of documents: {0}".format(len(self.documents)))
        print("Num of words before droping: {0}".format(self.words_num_before))
        print("Num of words after droping: {0}".format(self.words_num_after))
        print("Num of tokens: {0}".format(self.vocab_size))
        print("Num of stop words: {0}".format(len(self.stop_words_set)))
        print()

    def initTopics(self):
        for document in self.documents:
            tokens_list = document["token_strings"]

            doc_tokens_ids = np.ndarray(len(tokens_list), dtype=int)
            doc_topics = np.ndarray(len(tokens_list), dtype=int)
            doc_subtopics = np.ndarray(len(tokens_list), dtype=int)

            for i, w in enumerate(tokens_list):
                token_id = self.tokens_ids[w]
                topic = random.randrange(self.K)
                subtopic = random.randrange(self.S)

                doc_tokens_ids[i] = token_id
                doc_topics[i] = topic
                doc_subtopics[i] = subtopic

            document["doc_tokens"] = doc_tokens_ids
            document["doc_topics"] = doc_topics
            document["doc_subtopics"] = doc_subtopics




def printime(msg, param):
    time_now = datetime.datetime.now().strftime("%H:%M:%S:%f")
    print('{0} {1} {2}'.format(time_now, msg, param))


def i2w(index, vocab):
    """
    get word with index i from the word vocab
    :param index:
    :return:
    """
    for key, value in vocab.items():
        if value == index:
            return key


class Vectors(object):
    def __init__(self, emb_file_path):
        self.emb_file_path = emb_file_path
        self.vectors = {}
        self.dim = None

        self.loadVectors(self.emb_file_path)
        self.num_of_vectors = len(self.vectors)

    def loadVectors(self, emb_file_path):
        printime("Loading vectors ...",'')
        f = open(emb_file_path, 'r')
        vectors = {}
        for line in f:
            splitLine = line.split()
            word = splitLine[0]
            embedding = np.array([float(val) for val in splitLine[1:]])
            vectors[word] = embedding

        msg = 'Loading was done. ' + str(len(vectors)) + ' words loaded!'
        printime(msg, '\n')
        self.vectors = vectors
        self.dim = len(embedding)

    def w2v(self, word):
        return self.vectors[word]


if __name__ == '__main__':
    pass