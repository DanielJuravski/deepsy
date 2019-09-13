import sys
print(sys.version, '\n')

import matplotlib.pyplot as plt
import numpy as np

# Import from internal src
from visualizeTopics import process_file


TOPIC_DIST_THRESHOLD = 0.05


def getOptions():
    if '--input' in sys.argv:
        input_option_i = sys.argv.index('--input')
        file_name = sys.argv[input_option_i + 1]
    else:
        # file_name = '/home/daniel/deepsy/TM/Dirs_of_Docs/c01_sessions/results/inferencer.txt'
        # file_name = '/home/daniel/deepsy/TM/Dirs_of_Docs/c_sessions/results/composition.txt'
        file_name = '/home/daniel/deepsy/TM/Dirs_of_Docs/c_500_words/results/composition_100.txt'
        # file_name = '/home/daniel/deepsy/TM/Dirs_of_Docs/c_5turns_words/results/composition_100.txt'

    if '--output' in sys.argv:
        output_option_i = sys.argv.index('--output')
        output_name = sys.argv[output_option_i + 1]
    else:
        output_name = '.'

    if '--client2view' in sys.argv:
        output_option_i = sys.argv.index('--client2view')
        client2view_name = sys.argv[output_option_i + 1]
    else:
        client2view_name = 'ג'

    print("Visualizing: {0}".format(file_name))
    print("Visualizing only for {0}".format(client2view_name))

    return file_name, output_name, client2view_name


def countTopics(composition_obj):
    doc_topics = []  # tuple of session number + topics number in that session
    for doc in composition_obj:
        session_number = doc[0]
        topics_count = sum(float(prob) > TOPIC_DIST_THRESHOLD for prob in doc[2])
        doc_topics.append((session_number, topics_count))

    print(doc_topics)

    return doc_topics


def make_graph(doc_topics_num):
    # doc_topics_num is a list of tuples (doc-session number, topic count in that session)

    # make list of the topic counters
    topic_counts = [i[1] for i in doc_topics_num]
    # make list of the session numbers
    session_numbers = [i[0] for i in doc_topics_num]

    plt.plot(topic_counts)
    plt.suptitle('Session - Topics num {0}'.format(TOPIC_DIST_THRESHOLD), fontsize=20)
    plt.xlabel('Session number', fontsize=10)
    plt.ylabel('Number of Topics', fontsize=10)
    plt.xticks(np.arange(len(session_numbers)), session_numbers, rotation=90)
    plt.margins(x=0)
    plt.grid()
    plt.show()


if __name__ == '__main__':
    file_name, output_name, client2view_name = getOptions()
    composition_obj = process_file(file_name, client2view_name)
    doc_topics_num = countTopics(composition_obj)
    make_graph(doc_topics_num)