import sys
print(sys.version, '\n')

import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy

# Import from internal src
from visualizeTopics import process_file


TOPIC_DIST_THRESHOLD = 0.01


def getOptions():
    if '--input' in sys.argv:
        input_option_i = sys.argv.index('--input')
        file_name = sys.argv[input_option_i + 1]
    else:
        # file_name = '/home/daniel/deepsy/TM/Dirs_of_Docs/c01_sessions/results/inferencer.txt'
        # file_name = '/home/daniel/deepsy/TM/Dirs_of_Docs/c_sessions/results/composition.txt'
        file_name = '/home/daniel/deepsy/TM/Dirs_of_Docs/b_1000_words/results/composition_100.txt'
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
        client2view_name = 'ד'

    print("Visualizing: {0}".format(file_name))
    print("Visualizing only for {0}".format(client2view_name))

    return file_name, output_name, client2view_name


def countTopicsAvg(doc_topics):
    dt_avg = []
    dt_unique = []
    d_prev = d_curr = doc_topics[0][0]
    t_avg_calc = list()  #  only for calculating
    t_unique = set()

    for dt in doc_topics:
        d_curr = dt[0]
        t_count = dt[1]
        t_set = dt[2]
        if d_curr != d_prev:
            avg = sum(t_avg_calc)/float(len(t_avg_calc))
            dt_avg.append((d_prev, avg))
            t_avg_calc = list()

            t_unique_count = len(t_unique)
            dt_unique.append((d_prev, t_unique_count))
            t_unique = set()

        t_avg_calc.append(int(t_count))
        t_unique = t_unique.union(t_set)
        d_prev = d_curr
    # handle last doc
    t_count_avg = sum(t_avg_calc) / float(len(t_avg_calc))
    dt_avg.append((d_prev, t_count_avg))
    t_unique_count = len(t_unique)
    dt_unique.append((d_prev, t_unique_count))

    return dt_avg, dt_unique


def boolList2Set(topics_over_threshold):
    topics_id = set()
    for i, val in enumerate(topics_over_threshold):
        if val == True:
            topics_id.add(i)

    return topics_id


def countTopics(composition_obj):
    doc_topics = []  # tuple of session number + topics number in that session
    for doc in composition_obj:
        session_number = doc[0]
        topics_count = sum(float(prob) > TOPIC_DIST_THRESHOLD for prob in doc[3])
        topics_over_threshold = [float(prob) > TOPIC_DIST_THRESHOLD for prob in doc[3]]
        topics_over_threshold = boolList2Set(topics_over_threshold)
        doc_topics.append((session_number, topics_count, topics_over_threshold))

    doc_topics_avg, dt_unique = countTopicsAvg(doc_topics)
    print(doc_topics)
    print(doc_topics_avg)
    print(dt_unique)

    return doc_topics, doc_topics_avg, dt_unique


def make_graph(doc_topics_num, doc_topics_avg, dt_unique):
    # doc_topics_num is a list of tuples (doc-session number, topic count in that session)
    # doc_topics_avg is a list of tuples (doc-session number, avg topic count in all those sessions)
    # dt_unique is a list of tuples (doc-session number, count unique topics is the session)

    # doc_topics_num process
    # make list of the topic counters
    topic_counts = [i[1] for i in doc_topics_num]
    # make list of the session numbers
    session_numbers = [i[0] for i in doc_topics_num]

    # doc_topics_avg process
    topic_avg_counts = deepcopy(session_numbers)
    for i, session_number in enumerate(session_numbers):
        for j in doc_topics_avg:
            if j[0] == session_number:
                topic_avg_counts[i] = j[1]

    # dt_unique process
    topic_unique_counts = deepcopy(session_numbers)
    for i, session_number in enumerate(session_numbers):
        for j in dt_unique:
            if j[0] == session_number:
                topic_unique_counts[i] = j[1]

    plt.plot(topic_counts)
    plt.plot(topic_avg_counts)
    plt.plot(topic_unique_counts)

    plt.suptitle('Session - Topics num {0}'.format(TOPIC_DIST_THRESHOLD), fontsize=20)
    plt.xlabel('Session number', fontsize=10)
    plt.ylabel('Number of Topics', fontsize=10)
    plt.xticks(np.arange(len(session_numbers)), session_numbers, rotation=90)
    plt.margins(x=0)
    plt.gca().legend(('#Topics', 'Avg #Topics / Session', 'Unique #Topics in Session'))
    plt.grid()
    plt.show()


if __name__ == '__main__':
    file_name, output_name, client2view_name = getOptions()
    composition_obj = process_file(file_name, client2view_name)
    doc_topics_num, doc_topics_avg, dt_unique = countTopics(composition_obj)
    make_graph(doc_topics_num, doc_topics_avg, dt_unique)