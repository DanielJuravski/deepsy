

DOC_PATH = '/home/daniel/deepsy/TM/Dirs_of_Docs/c_500_words/Documents/א2_10.12.14.docx.json.parsed1.txt'
STOP_WORD_PATH = '/home/daniel/deepsy/TM/pre_process/STOP_WORDS_DIRS/by_words/ALL_STOP.txt'


def loadDocument():
    with open(DOC_PATH, 'r') as f:
        document_content = f.readline().split()

    return document_content


def loadStopWords():
    with open(STOP_WORD_PATH, 'r') as f:
        stop_words = f.read().splitlines()

    return stop_words


def makeStat(document_content, stop_words):
    dropped_words = []
    passed_words = []

    for word in document_content:
        if word in stop_words:
            dropped_words.append(word)
        else:
            passed_words.append(word)

    num_document_words = len(document_content)
    num_unique_document_words = len(set(document_content))
    num_dropped_words = len(dropped_words)
    num_unique_dropped_words = len(set(dropped_words))
    num_passed_words = len(passed_words)
    num_unique_passed_words = len(set(passed_words))

    stats = {}
    stats['num_document_words'] = num_document_words
    stats['num_unique_document_words'] = num_unique_document_words
    stats['num_dropped_words'] = num_dropped_words
    stats['num_unique_dropped_words'] = num_unique_dropped_words
    stats['num_passed_words'] = num_passed_words
    stats['num_unique_passed_words'] = num_unique_passed_words

    return stats


def printStats(stats):
    num_document_words = stats['num_document_words']
    num_unique_document_words = stats['num_unique_document_words']
    num_dropped_words = stats['num_dropped_words']
    num_unique_dropped_words = stats['num_unique_dropped_words']
    num_passed_words = stats['num_passed_words']
    num_unique_passed_words = stats['num_unique_passed_words']

    print()
    print('Original num of words in the document: {}'.format(num_document_words))
    print('Original num of unique words in the document: {}\n'.format(num_unique_document_words))
    print('Num of dropped words: {}'.format(num_dropped_words))
    print('Num of unique dropped words: {}'.format(num_unique_dropped_words))
    print('Num of passed words: {}'.format(num_passed_words))
    print('Num of unique passed words: {}'.format(num_unique_passed_words))


if __name__ == '__main__':
    '''
    Why: I want to get some stats about the documents when they imported to the MALLET, i.e when all the STOP WORDS are dropped.
    How: python wordStat.py $document_fill_path
    '''
    document_content = loadDocument()
    stop_words = loadStopWords()

    stats = makeStat(document_content, stop_words)
    printStats(stats)
