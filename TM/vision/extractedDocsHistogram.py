import os
import matplotlib.pyplot as plt


DIR_OF_DOCS_PATH = '/home/daniel/deepsy/TM/Dirs_of_Docs/b_900_words/Documents'


def loadDocsStats():
    print("Loading files ...")
    docs_words = []
    docs = os.listdir(DIR_OF_DOCS_PATH)
    for file in docs:
        file_path = DIR_OF_DOCS_PATH + '/' + file
        with open(file_path, 'r') as f:
            words = f.read().split()
            num_of_words = len(words)
            docs_words.append(num_of_words)

    return docs_words


def makeGraph(docs_words_len):
    print("Plotting ...")
    plt.hist(docs_words_len, bins=20)
    plt.ylabel('No of times')
    plt.show()


if __name__ == '__main__':
    docs_words_len = loadDocsStats()
    makeGraph(docs_words_len)
