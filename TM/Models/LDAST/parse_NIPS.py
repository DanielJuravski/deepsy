# create from NIPS papers.csv directory with documents, where each document is an abstract of each paper.


import pandas as pd
import re

FILE_PATH = "/home/daniel/Documents/Data_Sets/NIPS_papers/papers.csv"
TARGET_DIR = "/home/daniel/Documents/Data_Sets/NIPS_papers/docs/"


def parse():
    papers = pd.read_csv(FILE_PATH)
    papers.head()
    papers = papers.drop(["id", "event_type", "pdf_name"], axis=1)
    papers.head()
    papers['abstract_processed'] = papers['abstract'].map(lambda x: re.sub('[,\.!?]', '', x))
    papers['abstract_processed'] = papers['abstract_processed'].map(str.lower)

    docs = []

    for i in papers.itertuples():
        abstract = i[5]
        if abstract != 'abstract missing':
            abstract = abstract.translate({ord(i):None for i in '!@#$!@#$%^&*())_+-=\][/.,;`~"'})
            docs.append(abstract)

    for i, doc in enumerate(docs):
        file_name = TARGET_DIR + 'doc' + str(i) + ".txt"
        with open(file_name, 'w') as f:
            f.writelines(doc)
    pass




if __name__ == '__main__':
    parse()