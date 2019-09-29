import sys
print(sys.version, '\n')
import os

import numpy as np
from pandas import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt
from operator import itemgetter
import re

TOPICS_TO_FILTER = [0,1]
TOPICS_TO_SAVE = []

TOPIC_DIST_BASE_NAME = '_probs_dist.txt'
PLT_SHOW = True
PLT_SAVE = False


def getOptions():
    if '--input' in sys.argv:
        input_option_i = sys.argv.index('--input')
        file_name = sys.argv[input_option_i + 1]
    else:
        # file_name = '/home/daniel/deepsy/TM/Dirs_of_Docs/c01_sessions/results/inferencer.txt'
        # file_name = '/home/daniel/deepsy/TM/Dirs_of_Docs/c_sessions/results/composition.txt'
        # file_name = '/home/daniel/deepsy/TM/Dirs_of_Docs/c_5turns_words/results/composition_100.txt'
        file_name = '/home/daniel/deepsy/TM/Dirs_of_Docs/b_1000_words/results/tmp/alpha_2.5/composition_100.txt'
        # file_name = '/home/daniel/deepsy/TM/Dirs_of_Docs/c_5turns_words/results/composition_100.txt'

    if '--client2view' in sys.argv:
        output_option_i = sys.argv.index('--client2view')
        client2view_name = sys.argv[output_option_i + 1]
    else:
        client2view_name = 'א'
        # client2view_name = 'א סד ו מא עח יא ש נח ג ח מז עז מג נג לט כ נ כג ז נו עא מח יד ס כה ב כו לב כא עט צ לח ר עד ט ד ע כב ק כח פא ת נא יז י טו מט עג מד מו סה כד נב פ יג עה סו ל כט מה לז יב יט יח ה סב נט עו טז סט מב סא כז מ'

    if '--output' in sys.argv:
        output_option_i = sys.argv.index('--output')
        output_path = sys.argv[output_option_i + 1]
    else:
        # output_path = '.'
        output_path = getCurrentResultsDir(file_name) + 'Topic_Visualize/'
    ifNotExistCreate(output_path)

    print("Visualizing: {0}".format(file_name))
    print("Visualizing only for {0}".format(client2view_name))

    return file_name, output_path, client2view_name


def getCurrentResultsDir(file_name):
    # find results path of the current composition file.
    # assumption: composition file is only one level in the results dir
    results_path = file_name[:file_name.rindex('/')+1]

    return results_path


def ifNotExistCreate(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def filterTopics(docs_topics_dist):
    docs_topics_dist_T = docs_topics_dist.T
    # docs_topics_dist_T_list = list(docs_topics_dist_T)
    for topic_number, dists in enumerate(docs_topics_dist_T):
        if topic_number in TOPICS_TO_FILTER:
            docs_topics_dist_T = np.delete(docs_topics_dist_T, topic_number, 0)

    docs_topics_dist = docs_topics_dist_T.T

    return docs_topics_dist


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


def make_graph(composition_obj, output_path, client2view_name):
    print("Plotting/Saving for {}".format(client2view_name))
    docs_topics_dist_list = []
    docs_number = []
    for doc in composition_obj:
        docs_number.append(doc[0])
        docs_topics_dist_list.append(doc[3])
    docs_topics_dist = np.array(docs_topics_dist_list)

    # filter certain topics
    # docs_topics_dist_filtered = filterTopics(docs_topics_dist)

    df = DataFrame(docs_topics_dist, dtype=float, index=docs_number).T

    # annot: show values over the cells
    dashboard = sns.heatmap(df, annot=False)
    # just rotate the xticks labels
    dashboard.set_xticklabels(dashboard.get_xticklabels(), rotation=30)
    dashboard.grid()
    plt.suptitle('Client name: \n{0}'.format(reverse(client2view_name)), fontsize=15)
    plt.xlabel('Session number', fontsize=10)
    plt.ylabel('Topic', fontsize=10)

    if PLT_SAVE:
        out_str = output_path + client2view_name + '.png'
        plt.savefig(out_str, dpi=1500)

    if PLT_SHOW:
        plt.show()

    plt.close()


def exportTopicsDist(composition_obj, output_path, client2view_name):
    out_str = output_path + client2view_name + TOPIC_DIST_BASE_NAME
    with open(out_str, 'w') as f:
        for instance in composition_obj:
            dist = instance[2]
            for prob in dist:
                f.write(prob + '\t')
            f.write('\n')


def reverse(s):
    return s[::-1]


def sorted_alphanumeric(data):
    """
    used by _ and returning the same sort order as the os does.
    :param data:
    :return:
    """
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)


if __name__ == '__main__':
    file_name, output_path, client2view_name_list = getOptions()

    for client2view_name in client2view_name_list.split():
        composition_obj = process_file(file_name, client2view_name)
        exportTopicsDist(composition_obj, output_path, client2view_name)
        make_graph(composition_obj, output_path, client2view_name)

