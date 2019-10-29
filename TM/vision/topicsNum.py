import sys
print(sys.version, '\n')

import matplotlib.pyplot as plt
import numpy as np
from copy import deepcopy
import yaml
import re
import os


TOPIC_DIST_THRESHOLD = 0.0005
ORS_FILE_PATH = '/home/daniel/deepsy/SBS_Analize/Trans_ORS/trans_ors.yml'
WORKSPACE_PATH = '/home/daniel/deepsy/TM/Dirs_of_Docs/c_1turns_words/results_mini_small'  # change
HTML_DIR_PATH = WORKSPACE_PATH + '/HTMLs_200'  # change
COMPOSITION_FILE_PATH = WORKSPACE_PATH + '/composition_200.txt'  # change

def getOptions():
    if '--input' in sys.argv:
        input_option_i = sys.argv.index('--input')
        file_name = sys.argv[input_option_i + 1]
    else:
        file_name = COMPOSITION_FILE_PATH

    if '--output' in sys.argv:
        output_option_i = sys.argv.index('--output')
        output_name = sys.argv[output_option_i + 1]
    else:
        output_name = '.'

    if '--client2view' in sys.argv:
        output_option_i = sys.argv.index('--client2view')
        client2view_name = sys.argv[output_option_i + 1]
    else:
        client2view_name = 'עה'
    
    print("Visualizing: {0}".format(file_name))
    print("Visualizing only for {0}".format(client2view_name))

    return file_name, output_name, client2view_name


def process_file(file_name, client2view_name):
    '''
    making object with the documents' topics composition
    :param file_name:
    :return: list, where each var is a list of doc number, doc name, doc topics.
    '''
    print("Proccesing for {}".format(client2view_name))
    composition_obj = []
    composition_obj_sorted = []
    all_doc_names = []
    with open(file_name, 'r') as f:
        for line in f:
            # handle comment lines
            if line[0] == '#':
                continue
            line_details = line.split()
            doc_name = line_details[1].split('/')[-1]
            all_doc_names.append(doc_name)
            patientName_sessionNumber = line_details[1].split('/')[-1].split('.docx.json.parsed')[0].split('_')[0]

            # extracting patient name and drop if patient name option is given
            patientName = ''.join([i for i in patientName_sessionNumber if not i.isdigit()])
            if client2view_name is not None and patientName != client2view_name:
                continue

            # extracting session number and int it
            doc_number_listed = [int(s) for s in list(patientName_sessionNumber) if s.isdigit()]
            doc_number = int(''.join(str(e) for e in doc_number_listed))
            doc_topics_probs = line_details[2:]
            doc_topics = line_details[2:]
            composition_obj.append((doc_number, patientName_sessionNumber, doc_name, doc_topics))

    # check that the returned object not empty
    if client2view_name is not None:
        if len(composition_obj) <= 0:
            print("There are not documents fot {0} client, returned object is empty.".format(client2view_name))
            print("Exiting.")
            sys.exit()

    # sort doc full names, and recreated composition object by the that sorted.
    all_doc_names_sorted = sorted_alphanumeric(all_doc_names)
    for d_s in all_doc_names_sorted:
        for d_object in composition_obj:
            if d_object[2] == d_s:
                composition_obj_sorted.append(d_object)

    return composition_obj_sorted


def sorted_alphanumeric(data):
    """
    used by _ and returning the same sort order as the os does.
    :param data:
    :return:
    """
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)


def countTopicsAvg(doc_topics):
    dt_avg = []
    dt_unique = []
    d_prev = d_curr = doc_topics[0][0]
    t_avg_calc = list()  # only for calculating
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
    print("Topics of single doc:{}".format(doc_topics))
    print("Topics avg per session:{}".format(doc_topics_avg))
    print("Num of topics per session (U):{}".format(dt_unique))

    return doc_topics, doc_topics_avg, dt_unique


def make_graph(doc_topics_num, doc_topics_avg, dt_unique, html_t_counts, html_t_threshold_counts,
               sessions_ors, client2view_name, file_name):
    # doc_topics_num is a list of tuples (doc-session number, topic count in that session)
    # doc_topics_avg is a list of tuples (doc-session number, avg topic count in all those sessions)
    # dt_unique is a list of tuples (doc-session number, count unique topics is the session)
    # html_t_counts is a list of number of topics at each document by the HTML parsing script
    # html_t_threshold_counts is a list of number of topics at each document by the HTML parsing script
    #   (that passed the count threshold)
    # sessions_ors is a list of tuples (doc-session number, ors score of that session)

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

    # sessions_ors process
    sessions_ors_scores = deepcopy(session_numbers)
    for i, session_number in enumerate(session_numbers):
        for j in sessions_ors:
            if j[0] == session_number:
                sessions_ors_scores[i] = j[1]

    # # html_t_counts process
    # html_t_counts_only = deepcopy(session_numbers)
    # for i, session_number in enumerate(session_numbers):
    #     for j in html_t_counts:
    #         if j[0] == session_number:
    #             html_t_counts_only[i] = j[1]

    plt.plot(topic_counts)
    plt.plot(topic_avg_counts)
    plt.plot(topic_unique_counts)
    plt.plot(sessions_ors_scores)
    plt.plot(html_t_counts)
    plt.plot(html_t_threshold_counts)

    plt.suptitle('Session-Topics num {0} client:{1}'.format(TOPIC_DIST_THRESHOLD, client2view_name), fontsize=20)
    plt.title(file_name.replace('/home/daniel/deepsy/TM/Dirs_of_Docs/', ''))
    plt.xlabel('Session number', fontsize=10)
    plt.ylabel('Number of Topics / ORS', fontsize=10)
    plt.xticks(np.arange(len(session_numbers)), session_numbers, rotation=90)
    plt.margins(x=0)
    plt.gca().legend(('#Topics', 'Avg #Topics / Session', 'Unique #Topics in Session', 'ORS',
                      '#Topics (HTML)', '#Topics threshold (HTML)'))
    plt.grid()
    plt.show()


def getORS(client2view_name):
    sessions_ors = []
    with open(ORS_FILE_PATH, 'r') as f:
        ors_data = yaml.safe_load(f)
        for (key, val) in ors_data.items():
            if val['he_char'] == client2view_name:
                session_number = val['session_number']
                ors_sum = val['ors_sum']
                sessions_ors.append((session_number, ors_sum))

    sessions_sorted_ors = sorted(sessions_ors)
    print("ORS:{}".format(sessions_sorted_ors))

    return sessions_sorted_ors


def fileName2SessionNumber(file):
    patientName_sessionNumber = file.split('.docx.json.parsed')[0].split('_')[0]

    # extracting session number and int it
    session_number_listed = [int(s) for s in list(patientName_sessionNumber) if s.isdigit()]
    session_number = int(''.join(str(e) for e in session_number_listed))

    return session_number


def HTMLCounts(client2view_name):
    # Get the counts from the HTML script parsing

    # Get relevant client's files
    client_files = []
    for file in os.listdir(HTML_DIR_PATH):
        patientName_sessionNumber = file.split('.docx.json.parsed')[0].split('_')[0]

        # extracting patient name
        patientName = ''.join([i for i in patientName_sessionNumber if not i.isdigit()])
        if client2view_name is not None and patientName != client2view_name:
            continue

        client_files.append(file)

    # Smart sort
    client_files = sorted_alphanumeric(client_files)

    # Get counts from HTML files
    TOPICS_STR = 'Number of topics (above threshold):'
    t_counts = []
    t_threshold_counts = []
    for file in client_files:
        file_path = HTML_DIR_PATH + '/' + file
        session_number = fileName2SessionNumber(file)
        with open(file_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if TOPICS_STR in line:
                    line_details = line.split(TOPICS_STR)  # => [Number of topics (above threshold):, number (number)]
                    t_count = line_details[1].split('(')[0]
                    t_threshold_count = line_details[1].split('(')[1].split(')')[0]

                    # some unity checks:
                    try:
                        t_count = int(t_count)
                    except TypeError:
                        print("Can not parse HTML counts, probably something happened.")

                    try:
                        t_threshold_count = int(t_threshold_count)
                    except TypeError:
                        print("Can not parse HTML counts, probably something happened.")

                    # t_counts.append((session_number, t_count))
                    # t_threshold_counts.append((session_number, t_threshold_count))
                    t_counts.append(t_count)
                    t_threshold_counts.append(t_threshold_count)

    print("HTML Topics Counts:{}".format(t_counts))
    print("HTML Topics threshold Counts:{}".format(t_threshold_counts))

    return t_counts, t_threshold_counts


if __name__ == '__main__':
    file_name, output_name, client2view_name = getOptions()
    composition_obj = process_file(file_name, client2view_name)
    doc_topics_num, doc_topics_avg, dt_unique = countTopics(composition_obj)
    sessions_ors = getORS(client2view_name)
    html_t_counts, html_t_threshold_counts = HTMLCounts(client2view_name)
    make_graph(doc_topics_num, doc_topics_avg, dt_unique, html_t_counts, html_t_threshold_counts,
               sessions_ors, client2view_name, file_name)