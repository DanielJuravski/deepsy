import sys
print(sys.version, '\n')
import os
import numpy as np
from pandas import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt
import json
import re
from pathlib import Path

# TOPICS_TO_SHOW = []
# TOPICS_TO_SHOW = [81, 199, 166, 61, 48, 153, 22, 111, 94, 50, 199, 2, 72, 15, 160, 152, 171, 139, 19, 9, 15]  # ALL (neg->pos)
# TOPICS_TO_SHOW = [81, 199, 166, 61, 72, 160, 152, 171]  # ORS (neg->pos)
# TOPICS_TO_SHOW = [48, 153, 22, 111, 139, 19, 9, 15]  # POMS (neg->pos)
# TOPICS_TO_SHOW = [94, 50, 199, 2]  # HSCL

TOPICS_TO_SHOW = [22, 165, 133, 48]  # PSQ

TOPIC_DIST_BASE_NAME = '_probs_dist.txt'
METADATA_BASE_NAME = '_metadata.txt'

PLT_SHOW = False
PLT_SAVE = True
DPI = 1200
TOP_TOPICS_K = 4


def getOptions():
    if '--client2view' in sys.argv:
        output_option_i = sys.argv.index('--client2view')
        client2view_name = sys.argv[output_option_i + 1]
    else:
        client2view_name = 'עא'
        # client2view_name = 'א סד ו מא עח יא ש נח ג ח מז עז מג נג לט כ נ כג ז נו עא מח יד ס כה ב כו לב כא עט צ לח ר עד ט ד ע כב ק כח פא ת נא יז י טו מט עג מד מו סה כד נב פ יג עה סו ל כט מה לז יב יט יח ה סב נט עו טז סט מב סא כז מ'

    if '--input' in sys.argv:
        input_option_i = sys.argv.index('--input')
        file_name = sys.argv[input_option_i + 1]
    else:
        # file_name = '/home/daniel/deepsy/TM/Dirs_of_Docs/c_sessions/results_no_inference/composition_200.txt'
        file_name = '/home/daniel/deepsy/TM/Dirs_of_Docs/c_sessions/results/inferencer_200-c_1turns_words_mini_small.txt'

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


def filterTopics(composition_obj):
    filtered_composition_obj = composition_obj

    # all that thing happens only when there are special topics to show
    if len(TOPICS_TO_SHOW) > 0:

        filtered_composition_obj = []
        for item in composition_obj:
            session_num = item[0]
            client_name_session_number = item[1]
            file_name = item[2]
            t_probs = item[3]
            t_probs_ordered = {}
            for t in TOPICS_TO_SHOW:
                if t not in t_probs:
                    raise "topic {0} is unvalid".format(t)
                t_probs_ordered[t] = t_probs[t]
            # create new sorted_composition_obj (same as composition_obj) where only the dists are different
            filtered_composition_obj.append((session_num, client_name_session_number, file_name, t_probs_ordered))

    return filtered_composition_obj


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
            doc_topics = {}
            for t, t_p in enumerate(doc_topics_probs):
                doc_topics[t] = t_p

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

    # filter certain topics
    composition_obj = filterTopics(composition_obj_sorted)

    return composition_obj


def makeGraph(composition_obj, output_path, client2view_name):
    print("Plotting/Saving for {}".format(client2view_name))
    docs_topics_dist_list = []
    docs_number = []
    for doc in composition_obj:
        docs_number.append(doc[0])
        probs_dict = doc[3]
        if len(TOPICS_TO_SHOW) > 0:
            # dont sort by the numerical topic number. use the TOPICS_TO_SHOW order
            docs_topics_dist_list.append([probs_dict[key] for key in (probs_dict.keys())])
        else:
            docs_topics_dist_list.append([probs_dict[key] for key in sorted(probs_dict.keys())])
    docs_topics_dist = np.array(docs_topics_dist_list)
    docs_topics_numbers_list = [str(i) for i in list(probs_dict.keys())]

    df = DataFrame(docs_topics_dist, dtype=float, index=docs_number).T

    # annot: show values over the cells
    dashboard = sns.heatmap(df, annot=False)
    # just rotate the xticks labels
    dashboard.set_xticklabels(dashboard.get_xticklabels(), rotation=0)
    if len(TOPICS_TO_SHOW) > 0:
        T = np.arange(len(docs_topics_numbers_list))+0.5
        dashboard.set_yticks(T)
        # just rotate (straight) the yticks labels
        dashboard.set_yticklabels(docs_topics_numbers_list, rotation=0)
        # dashboard.grid()
    else:
        dashboard.set_yticklabels(docs_topics_numbers_list, minor=True)
        dashboard.grid()

    # plt.suptitle('Client Name: \n{0}'.format(reverse(client2view_name)), fontsize=15)
    # plt.suptitle('Gali\'s ORS topics (poor outcome)'.format(reverse(client2view_name)), fontsize=15)
    # plt.suptitle('Noya\'s ORS topics (good outcome)'.format(reverse(client2view_name)), fontsize=15)
    plt.suptitle('Gali\'s PSQ topics (poor outcome)'.format(reverse(client2view_name)), fontsize=15)
    # plt.suptitle('Noya\'s PSQ topics (good outcome)'.format(reverse(client2view_name)), fontsize=15)

    plt.xlabel('Session Number', fontsize=10)
    plt.ylabel('Topic Number', fontsize=10)

    if PLT_SAVE:
        out_str = output_path + client2view_name + '.png'
        if DPI is not None:
            plt.savefig(out_str, dpi=DPI)
        else:
            plt.savefig(out_str)

    if PLT_SHOW:
        plt.show()

    plt.close()


def extractMetaData(composition_obj):
    metadatas2write = []

    for line in composition_obj:
        file_num = line[0]
        file_path = line[2]
        vector = line[3:]

        file_name = file_path.split('/')[-1]
        patientName_sessionNumber = file_name.split('.docx.json.parsed')[0].split('_')[0]
        client_name = ''.join([i for i in patientName_sessionNumber if not i.isdigit()])
        session_number = re.sub("[^0-9]", "", patientName_sessionNumber)
        parsed_part = re.sub("[^0-9]", "", file_name.split('.docx.json.parsed')[1])
        metadata_str = client_name + '\t' + session_number + '\t' + parsed_part
        metadatas2write.append(metadata_str)

    return metadatas2write


def exportTopicsDist(composition_obj, output_path, client2view_name):
    vec_f_name = output_path + client2view_name + TOPIC_DIST_BASE_NAME
    metadata_f_name = output_path + client2view_name + METADATA_BASE_NAME
    cleanFiles(metadata_f_name)

    with open(vec_f_name, 'w') as f:
        for instance in composition_obj:
            dist = instance[3]
            for (t, prob) in dist.items():
                f.write(prob + '\t')
            f.write('\n')

    metadatas2write = extractMetaData(composition_obj)
    meta_data_first_line = 'Client_name\tSession_number\tParsed_part\n'
    with open(metadata_f_name, 'a') as f_meta:
        f_meta.writelines(meta_data_first_line)
    with open(metadata_f_name, 'a') as f_meta:
        for i in metadatas2write:
            f_meta.writelines(i)
            f_meta.writelines('\n')


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


def cleanFiles(file_path):
    if Path(file_path).exists():
        os.remove(file_path)


def getTopTopics(composition_obj):
    top_dict = {}  # where key is the session number and value is the top topics
    for item in composition_obj:
        session_num = item[0]
        session_dists = item[3]
        top_topics = sorted(session_dists.items(), key=lambda item: float(item[1]), reverse=True)
        k_top_topics = []
        for k in range(TOP_TOPICS_K):
            k_top_topics.append(top_topics[k][0])
        top_dict[session_num] = k_top_topics

    print("Top Topics per Session:")
    for key, val in top_dict.items():
        print("\t", key, val)


if __name__ == '__main__':
    file_name, output_path, client2view_name_list = getOptions()

    for client2view_name in client2view_name_list.split():
        composition_obj = process_file(file_name, client2view_name)
        exportTopicsDist(composition_obj, output_path, client2view_name)
        getTopTopics(composition_obj)
        makeGraph(composition_obj, output_path, client2view_name)

