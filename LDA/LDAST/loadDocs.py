import os


class Documents(object):
    """
    Bach of imported documents
    """
    def __init__(self, documents_dir_name):

        # Documents dir with all documents files. No validation checks, assumes the dir is valid.
        self.documents_dir_name = documents_dir_name

        # Vocabulary of the files that created the documents. Each word is unique.
        self.vocab = {}

        # Each time work inserted to vocab - tokenize it with this value and increase it.
        self.last_word_token = 0

        # List of tokenized documents
        self.documents = []

        # load and process the documents files
        self.load()

        # print statistics
        self.statistics()

    def load(self):
        dir = os.fsencode(self.documents_dir_name)
        for doc in os.listdir(dir):
            doc_name = os.fsdecode(doc)
            doc_full_path = self.documents_dir_name + str(doc_name)
            print('loading {0}'.format(doc_name))

            with open(doc_full_path, 'r') as f:
                doc_words = f.read().split()
                doc_tokens = self.add2Vocab(doc_words)
                self.documents.append(doc_tokens)

    def add2Vocab(self, doc_words):
        """
        add new works to vocab and return tokenized doc representation
        :param doc_words:
        :return: doc_tokens
        """
        doc_tokens = []
        for word in doc_words:

            # add to vocab
            if word not in self.vocab:
                self.vocab[word] = self.last_word_token
                self.last_word_token += 1

            # tokenize doc
            token = self.vocab[word]
            doc_tokens.append(token)

        return doc_tokens

    def statistics(self):
        print()
        print("Loading has done successfully.")
        print("Num of documents: {0}".format(len(self.documents)))
        print("Num of tokens: {0}".format(self.last_word_token))


if __name__ == '__main__':
    myDocs = Documents('/home/daniel/deepsy/LDA/client_5_mini_turns/')