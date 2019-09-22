import gzip
import numpy as np
from collections import defaultdict
import yaml
import operator

GZ_FILE_PATH = '/home/daniel/deepsy/TM/Dirs_of_Docs/c_500_words/results/topic-state_100.gz'
# GZ_FILE_PATH = '/home/daniel/deepsy/TM/Dirs_of_Docs/c_5turns_words/results/topic-state_50.gz'
# DOCUMENT_PATH = 'א5_31.12.14.docx.json.parsed3.txt'
DOCUMENT_PATH = 'א2_10.12.14.docx.json.parsed9.txt'
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

# HTML props
#PAGE_COLOR = 'powderblue'

def loadFile():
    print("Loading gz ...")
    file_content = []

    # unzip gz
    with gzip.open(GZ_FILE_PATH, 'r') as fin:
        for line in fin.read().splitlines():
            line_details = line.decode("utf-8").split()
            doc_name = line_details[INDEX_DOC_SOURCE].split('/')[-1]
            if line_details[0] == '#alpha':
                # num of alphas minus first and second cells
                num_topics = len(line_details)-2
            # check doc name
            if doc_name == DOCUMENT_PATH:
                file_content.append(line_details)

    return file_content, num_topics


def getColors():
    # load colors yaml fron static file
    # that static file was generated with generateHTMLColors.py script
    with open(FILE_NAME, 'r') as f:
        topic_color = yaml.safe_load(f)

    return topic_color


def processData(topic_state):
    topic_instances = defaultdict(int)  # which topics were in the current trans and how many
    numOfWords = 0
    words_info = list()

    for line in topic_state:
        word = line[INDEX_TOKEN_WORD]
        numOfWords += 1
        topic = line[INDEX_TOPIC]
        topic_instances[topic] += 1
        words_info.append((word, topic))

    return words_info, numOfWords, topic_instances


def generateTable(topic_instances):
    table = """
    <center>
    <table>
        <th>Count</th>
        <th>Topic</th>
        <th>#</th>
    """

    sorted_topic_instances = sorted(topic_instances.items(), key=lambda item: item[1], reverse=True)
    for i, (t,c) in enumerate(sorted_topic_instances):
        table += """
        <tr>
            <td>{0}</td>
            <td>{1}</td>
            <td>{2}</td>
        </tr>
        """.format(c, t, i+1)

    table += """
    </table>
    </center>
    """

    return table


def getWordColor(t_colors_dict, topic, topic_instances):
    if topic_instances[topic] > TOPIC_INSTANCE_THRESHOLD_TO_COLOR:
        color = t_colors_dict[topic]
    else:
        color = 'transparent'

    return color


def generateHTML(words_info, numOfWords, topic_instances):
    print("Generating HTML file ...")
    t_colors_dict = getColors()

    # init
    code = """
    <!DOCTYPE html>
    <html dir="rtl" lang="he">
    <head>
    <meta charset="utf-8">
    <style>
    body {background-color: powderblue;}
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
    code += """<h1 dir="ltr"><center><u>{0}</u></center></h1>""".format(DOCUMENT_PATH)

    # words
    code += """
    <p_words style="font-size:30px; font-family:Arial">
    """
    for w_info in words_info:
        word = w_info[0]
        topic = w_info[1]
        topic_color = getWordColor(t_colors_dict, topic, topic_instances)

        code += """
        <span style="background-color:{1}" title="{2}"> {0} </span>
        """.format(word, topic_color, topic)
    code += "</p_words><br><br><br>"

    # stats
    code += """
    <p_stats style="font-size:30px; font-family:Arial; text-align:center">
    <center>
    Number of words: {0} <br>
    Number of topics: {1} <br>
    </center>
    </p_stats>
    """.format(numOfWords,
               len(topic_instances))
    code += generateTable(topic_instances)

    # end
    code += """
    </body>
    </html>
    """

    return code


def exportHTML(code):
    print("Saving HTML file ...")
    html_file = open("colorized_topics.html", "w")
    html_file.write(code)
    html_file.close()





if __name__ == '__main__':
    topic_state, num_topics = loadFile()
    words_info, numOfWords, topic_instances = processData(topic_state)
    code = generateHTML(words_info, numOfWords, topic_instances)
    exportHTML(code)
