import os


class Documents(object):
    """
    Batch of imported documents object
    """
    def __init__(self, documents_dir_name, stop_words_dir_name):

        # Documents dir with all documents files. No validation checks, assumes the dir is valid.
        self.documents_dir_name = documents_dir_name

        # Vocabulary of the files that created the documents. Each word is unique.
        self.vocab = {}

        # Each time work inserted to vocab - tokenize it with this value and increase it.
        self.last_word_token = 0

        # List of tokenized documents
        self.documents = []

        # In stop_words_dir_name there are files that contain the stop-words. Stop-words should not be tokenized.
        self.stop_words_dir_name = stop_words_dir_name

        # Set of all the stop words that in the 'self.stop_words_dir_name'.
        # If the documents contain that words, they won't be tokenized.
        self.stop_words_set = set()

        # load stop-words
        self.loadStopWords()

        # load and process the documents files
        self.loadDocs()

        # print statistics
        self.statistics()

    def loadDocs(self):
        print('Loading documents ...')

        dir = os.fsencode(self.documents_dir_name)
        for doc in os.listdir(dir):
            doc_name = os.fsdecode(doc)
            doc_full_path = self.documents_dir_name + str(doc_name)
            #print('loading document: {0}'.format(doc_name))

            with open(doc_full_path, 'r') as f:
                doc_words = f.read().split()
                doc_tokens = self.add2Vocab(doc_words)
                self.documents.append(doc_tokens)

        print("Loading was done successfully.")

    def add2Vocab(self, doc_words, filter_uni=True, filter_bi=False):
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

                # add to vocab
                if word not in self.vocab:
                    self.vocab[word] = self.last_word_token
                    self.last_word_token += 1

                # tokenize doc
                token = self.vocab[word]
                # print(word)
                doc_tokens.append(token)

        return doc_tokens

    def loadStopWords(self):
        """
        load stop words files. iterate over the stop-words dir, open each file and extract the words that in the file.
        words that will be in the stop-words set won't be tokenized
        :param
        :return:
        """
        dir = os.fsencode(self.stop_words_dir_name)
        for file in os.listdir(dir):
            file_name = os.fsdecode(file)
            file_full_path = self.stop_words_dir_name + str(file_name)
            print('Loading stop-words: {0}'.format(file_name))

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
        print("Num of tokens: {0}".format(self.last_word_token))

        print("Num of stop words: {0}".format(len(self.stop_words_set)))


if __name__ == '__main__':
    myDocs = Documents(documents_dir_name='/home/daniel/deepsy/LDA/client_5_mini_turns/', #/home/daniel/deepsy/LDA/client_5_mini_turns/
                       stop_words_dir_name='/home/daniel/deepsy/LDA/LDAST/STOP_WORDS/')
