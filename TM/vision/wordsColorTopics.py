import gzip
import numpy as np
from collections import defaultdict

GZ_FILE_PATH = '/home/daniel/deepsy/TM/Dirs_of_Docs/c_500_words/results/topic-state_100.gz'
# GZ_FILE_PATH = '/home/daniel/deepsy/TM/Dirs_of_Docs/c_5turns_words/results/topic-state_50.gz'
DOCUMENT_PATH = 'א2_10.12.14.docx.json.parsed4.txt'
# CLIENT_NAME = 'א'

INDEX_DOC_NUMBER = 0
INDEX_DOC_SOURCE = 1
INDEX_WORD_POS = 2  # word position in the doc
INDEX_TOKEN_NUMBER = 3
INDEX_TOKEN_WORD = 4
INDEX_TOPIC = 5


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


def generateColors(num_topics):
    topic_color = {}
    for t in range(num_topics):
        color = np.random.choice(range(256), size=3)
        color_format = "rgb({0} {1} {2})".format(color[0], color[1], color[2])
        topic_color[str(t)] = color_format

    return topic_color


def generateHTML(topic_state, num_topics):
    print("Generating HTML file ...")
    t_colors_dict = generateColors(num_topics)

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
    topic_instances = defaultdict(int)  # which topics were in the current trans and how many
    numOfWords = 0
    for line in topic_state:
        word = line[INDEX_TOKEN_WORD]
        numOfWords += 1
        topic = line[INDEX_TOPIC]
        topic_instances[topic] += 1
        topic_color = t_colors_dict[topic]
        code += """
        <span style="background-color:{1}" title="{2}"> {0} </span>
        """.format(word, topic_color, topic)
    code += "</p_words><br><br><br>"

    # stats
    code += """
    <p_stats style="font-size:30px; font-family:Arial"><center>
    Number of words: {0} <br>
    Number of topics: {1} <br>
    </center></p_stats>
    """.format(numOfWords,
               len(topic_instances))

    code += """
    </body>
    </html>
    """

    return code


def exportHTML(code):
    print("Saving HTML file ...")
    Html_file = open("colorized_topics.html", "w")
    Html_file.write(code)
    Html_file.close()


if __name__ == '__main__':
    topic_state, num_topics = loadFile()
    code = generateHTML(topic_state, num_topics)
    exportHTML(code)
