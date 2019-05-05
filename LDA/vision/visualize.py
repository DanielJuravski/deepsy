import sys
print(sys.version, '\n')

import numpy as np
from pandas import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt
from operator import itemgetter


def getOptions():
    if '--input' in sys.argv:
        input_option_i = sys.argv.index('--input')
        file_name = sys.argv[input_option_i + 1]
    else:
        file_name = '../client_5/topic-composition.txt'

    if '--output' in sys.argv:
        output_option_i = sys.argv.index('--output')
        output_name = sys.argv[output_option_i + 1]
    else:
        output_name = '.'

    if '--client2view' in sys.argv:
        output_option_i = sys.argv.index('--client2view')
        client2view_name = sys.argv[output_option_i + 1]
        print("Visualizing only for {0}".format(client2view_name))
    else:
        client2view_name = None

    print("Visualizing: {0}".format(file_name))

    return file_name, output_name, client2view_name


def process_file(file_name, client2view_name):
    '''
    making object with the documents' topics composition
    :param file_name:
    :return: list, where each var is a list of doc number, doc name, doc topics.
    '''
    composition_obj = []
    with open(file_name, 'r') as f:
        for line in f:
            # handle comment lines
            if line[0] == '#':
                continue
            line_details = line.split()
            # patientName_sessionNumber
            doc_name = line_details[1].split('/')[-1].split('.docx.json.parsed')[0].split('_')[0]

            # extracting patient name and drop if patient name option is given
            patientName = ''.join([i for i in doc_name if not i.isdigit()])
            if client2view_name is not None and patientName != client2view_name:
                continue

            # extracting session number and int it
            doc_number_listed = [int(s) for s in list(doc_name) if s.isdigit()]
            doc_number = int(''.join(str(e) for e in doc_number_listed))
            doc_topics = line_details[2:]
            composition_obj.append((doc_number, doc_name, doc_topics))

    # check that the returned object not empty
    if client2view_name is not None:
        if len(composition_obj) <= 0:
            print("There are not documents fot {0} client, returned object is empty.".format(client2view_name))
            print("Exiting.")
            sys.exit()

    composition_obj.sort(key=itemgetter(0))

    return composition_obj


def make_graph(composition_obj):
    docs_topics_dist_list = []
    docs_number = []
    for doc in composition_obj:
        docs_number.append(doc[0])
        docs_topics_dist_list.append(doc[2])
    docs_topics_dist = np.array(docs_topics_dist_list)

    df = DataFrame(docs_topics_dist, dtype=float, index=docs_number).T

    # annot: show values over the cells
    dashboard = sns.heatmap(df, annot=False)
    dashboard.set_xticklabels(dashboard.get_xticklabels(), rotation=30)

    plt.show()
    # plt.show(block=False)
    # input("Hit Enter To Close")
    # plt.close()


if __name__ == '__main__':
    file_name, output_name, client2view_name = getOptions()
    composition_obj = process_file(file_name, client2view_name)
    make_graph(composition_obj)
    
    pass