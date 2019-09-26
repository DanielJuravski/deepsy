import gzip
from collections import defaultdict
import yaml
import json
import os
import re

WORKSPACE_PATH = '/home/daniel/deepsy/TM/Dirs_of_Docs/b_1000_words'
# WORKSPACE_PATH = '/tmp/trans_tmp'
# WORKSPACE_PATH = '/home/daniel/deepsy/TM/Dirs_of_Docs/c_500_words/'
GZ_FILE_PATH = WORKSPACE_PATH + '/results/topic-state_100.gz'
DOCUMENTS_PATH = WORKSPACE_PATH + '/Documents'
OUTPUT_PATH = '/home/daniel/deepsy/TM/vision' + '/HTMLs'
# GZ_FILE_PATH = '/home/daniel/deepsy/TM/Dirs_of_Docs/c_5turns_words/results/topic-state_50.gz'
# DOCUMENT_PATH = 'א5_31.12.14.docx.json.parsed3.txt'
# DOCUMENT_PATH = 'א2_10.12.14.docx.json.parsed1.txt'
# CLIENT_NAME = 'א'
TOPIC_INSTANCE_THRESHOLD_TO_COLOR = 5

# yaml colors file
TOPICS_NUM = 100
FILE_NAME = str(TOPICS_NUM) + '_HMTL_colors.yml'

INDEX_DOC_NUMBER = 0
INDEX_DOC_SOURCE = 1
INDEX_WORD_POS = 2  # word position in the doc
INDEX_TOKEN_NUMBER = 3
INDEX_TOKEN_WORD = 4
INDEX_TOPIC = 5


def loadFile():
    print("Loading gz ...")
    file_content = defaultdict(list)

    # unzip gz
    with gzip.open(GZ_FILE_PATH, 'r') as fin:
        for line in fin.read().splitlines():
            line_details = line.decode("utf-8").split()
            if line_details[0] == '#alpha':
                # num of alphas minus first and second cells
                num_topics = len(line_details)-2
                continue
            if line_details[0] == '#doc' or line_details[0] == '#beta':
                continue

            # add data by the document name
            doc_name = line_details[INDEX_DOC_SOURCE].split('/')[-1]
            file_content[doc_name].append(line_details)

    return file_content, num_topics


def getColors():
    # load colors yaml from static file
    # that static file was generated with generateHTMLColors.py script
    with open(FILE_NAME, 'r') as f:
        topic_color = yaml.safe_load(f)

    return topic_color


def processData(topic_state, doc):
    topic_instances = defaultdict(int)  # which topics were in the current trans and how many
    numOfWords = 0
    words_info = list()

    current_doc_topic_state = topic_state[doc]  # topic_state is defaultdict(list)
    for line in current_doc_topic_state:
        word = line[INDEX_TOKEN_WORD]
        numOfWords += 1
        topic = line[INDEX_TOPIC]
        topic_instances[topic] += 1
        words_info.append((word, topic))

    return words_info, numOfWords, topic_instances


def generateTable(topic_instances, t_colors_dict):
    table = """
    <center>
    <table>
        <th>Count</th>
        <th>Topic</th>
        <th>#</th>
    """

    sorted_topic_instances = sorted(topic_instances.items(), key=lambda item: item[1], reverse=True)
    for i, (t,c) in enumerate(sorted_topic_instances):
        bgcolor, font_color = getWordColor(t_colors_dict, t, topic_instances)
        table += """
        <tr>
            <td style="background-color:{3}; color:{4}">{0}</td>
            <td style="background-color:{3}; color:{4}">{1}</td>
            <td style="background-color:{3}; color:{4}">{2}</td>
        </tr>
        """.format(c, t, i+1, bgcolor, font_color)

    table += """
    </table>
    </center>
    """

    return table


def getWordColor(t_colors_dict, topic, topic_instances):
    if topic_instances[topic] > TOPIC_INSTANCE_THRESHOLD_TO_COLOR:
        bg_color = t_colors_dict[topic]
        font_color = 'black'
    else:
        bg_color = 'transparent'
        font_color = 'red'

    return bg_color, font_color


def generateHTML(words_info, numOfWords, topic_instances, doc_name, next_doc, prev_doc):
    print("Generating HTML file ...")
    t_colors_dict = getColors()

    # init
    code = """
    <!DOCTYPE html>
    <html dir="rtl" lang="he">
    <head>
    <meta charset="utf-8">
    <style>
    body {background-color: #f5f5f5;}
    h1 {color: blue;}
    p_words {color: black;}
    p_stats {color: black;}
    table {border-collapse: collapse;}
    table, th, td {border: 1px solid black; text-align: left}
    th, td {}
    th {text-align: left; padding: 10px}
    </style>
    </head>
    <body>
    """

    # title
    code += """<h1 dir="ltr"><center><u>{0}</u></center></h1>""".format(doc_name)

    # Next-Prev buttons next_doc, prev_doc
    next_doc_path = next_doc + '.html'
    prev_doc_path = prev_doc + '.html'

    if next_doc == 'NULL':
        code += """
                   <center>&nbsp;<a href="{0}"><--הקודם</a></center><br><br>
                   """.format(prev_doc_path)
    elif prev_doc == 'NULL':
        code += """
                   <center><a href="{0}">הבא--></a> &nbsp;</center><br><br>
                   """.format(next_doc_path)
    else:
        code += """
                   <center><a href="{0}"><--הקודם</a> &nbsp;<a href="{1}">הבא--></a></center><br><br>
                   """.format(prev_doc_path, next_doc_path)

    # words
    code += """
    <p_words style="font-size:30px; font-family:Arial">
    """
    for w_info in words_info:
        word = w_info[0]
        topic = w_info[1]
        topic_color, font_color = getWordColor(t_colors_dict, topic, topic_instances)

        code += """
        <span style="background-color:{1}" title="{2}"> {0} </span>
        """.format(word, topic_color, topic)
    code += "</p_words><br><br>"

    # stats
    code += """
    <p_stats style="font-size:30px; font-family:Arial; text-align:center">
    <center>
    Number of words: {0} <br>
    Number of topics: {1} <br>
    Topic Instance threshold: {2} <br>
    </center>
    </p_stats>
    """.format(numOfWords,
               len(topic_instances),
               TOPIC_INSTANCE_THRESHOLD_TO_COLOR)
    code += generateTable(topic_instances, t_colors_dict)

    # end
    code += """
    </body>
    </html>
    """

    return code


def exportHTML(code, doc_name):
    file_name = doc_name + '.html'
    print("Saving {} file ...".format(file_name))
    ifNotExistCreate(OUTPUT_PATH)

    file_path = OUTPUT_PATH + '/' + file_name
    html_file = open(file_path, "w")
    html_file.write(code)
    html_file.close()


def ifNotExistCreate(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def getNextPrevDoc(documents_names, i):
    documents_number = len(documents_names)
    if i == 0:
        prev = 'NULL'
    else:
        prev = documents_names[i-1]

    if i == documents_number-1:
        next = 'NULL'
    else:
        next = documents_names[i+1]

    return next, prev


def sorted_aphanumeric(data):
    """
    used by listdir and getting the same sort order as the os does.
    :param data:
    :return:
    """
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)


if __name__ == '__main__':
    # get documents names
    documents_names = list()
    for file_name in sorted_aphanumeric(os.listdir(DOCUMENTS_PATH)):
        documents_names.append(file_name)

    # get info from topic_state file
    topic_state, num_topics = loadFile()

    # generate HTMLs
    for i, doc in enumerate(documents_names):
        next_doc, prev_doc = getNextPrevDoc(documents_names, i)
        words_info, numOfWords, topic_instances = processData(topic_state, doc)
        code = generateHTML(words_info, numOfWords, topic_instances, doc, next_doc, prev_doc)
        exportHTML(code, doc)
