from datetime import datetime
import pyximport
pyximport.install()

from deepsy.LDA.LDAST import LDAGibbs
from utils import Documents
from utils import printime


def write2file(topics_top_words, file_name):
    with open(file_name, 'w') as f:
        for line in topics_top_words:
            f.write(line)
            f.write('\n')


def writeInfo(info_file, params, run_time):
    with open(info_file, 'w') as f:
        for param in params.items():
            line = str(param[0]) + ':\t' + str(param[1]) + '\n'
            f.writelines(line)

        line = 'Running time:\t{0}\n'.format(run_time)
        f.writelines(line)


def main():
    script_starttime = datetime.now()

    # params
    params = {}
    K = int(50)
    doc_smoothing = 0.5  # alpha (theta)
    word_smoothing = 0.01  # beta (phi)
    iterations = 1000
    topic_num_words_to_print = 20

    params['K'] = K
    params['doc_smoothing'] = doc_smoothing
    params['word_smoothing'] = word_smoothing
    params['iterations'] = iterations
    params['topic_num_words_to_print'] = topic_num_words_to_print

    info_file = 'info.txt'
    keys_file = 'keys.txt'

    data = Documents(documents_dir_name='/home/daniel/deepsy/LDA/client_5_mini_turns/',
                     stop_words_dir_name='/home/daniel/deepsy/LDA/LDAST/STOP_WORDS/',
                     K=K)

    model = LDAGibbs.LDAGibbsSampler(data, params)

    for document in data.documents:
        c_doc = LDAGibbs.Document(document["doc_tokens"],
                                  document["doc_topics"],
                                  document["topic_counts"])
        model.add_document(c_doc)

    model.learn()
    topics_top_words = model.print_all_topics(topic_num_words_to_print)
    write2file(topics_top_words, keys_file)

    run_time = datetime.now() - script_starttime
    print("Run time: {0}". format(run_time))

    writeInfo(info_file, params, run_time)

    pass


if __name__ == '__main__':
    main()
