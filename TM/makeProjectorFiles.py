import re
import os
import random

COMPOSITION_FILE = '/home/daniel/deepsy/TM/Dirs_of_Docs/b_1000_words/results/composition_100.txt'

VECTOR_FILE_NAME = 'vector_file.txt'
METADATA_FILE_NAME = 'metadata_file.txt'


def getCurrentResultsDir(file_name):
    # find results path of the current composition file.
    # assumption: composition file is only one level in the results dir
    results_path = file_name[:file_name.rindex('/')+1]

    return results_path


def loadFile(file):
    print('Loading ...')
    composition = []
    with open(file, 'r') as f:
        for line in f:
            line = line.split()
            composition.append(line)

    return composition


def generateFiles(composition):
    print('Generating files ...')
    vectors2write = []
    metadatas2write = []

    for line in composition:
        file_num = line[0]
        file_path = line[1]
        vector = line[2:]

        vector_str = ""
        for i in vector:
            vector_str += i + '\t'
        vectors2write.append(vector_str)

        file_name = file_path.split('/')[-1]
        patientName_sessionNumber = file_name.split('.docx.json.parsed')[0].split('_')[0]
        client_name = ''.join([i for i in patientName_sessionNumber if not i.isdigit()])
        session_number = re.sub("[^0-9]", "", patientName_sessionNumber)
        parsed_part = re.sub("[^0-9]", "", file_name.split('.docx.json.parsed')[1])
        metadata_str = file_num + '\t' + client_name + '\t' + session_number + '\t' + parsed_part
        metadatas2write.append(metadata_str)

    # Generate files
    meta_data_first_line = 'Vec_num\tClient_name\tSession_number\tParsed_part\n'
    with open(METADATA_FILE_NAME, 'a') as f_meta:
        f_meta.writelines(meta_data_first_line)
    for i, vec in enumerate(vectors2write):
        with open(VECTOR_FILE_NAME, 'a') as f_vec:
            with open(METADATA_FILE_NAME, 'a') as f_meta:
                f_vec.writelines(vec)
                f_vec.writelines('\n')
                f_meta.writelines(metadatas2write[i])
                f_meta.writelines('\n')


def cleanFiles():
    os.remove(VECTOR_FILE_NAME)
    os.remove(METADATA_FILE_NAME)


if __name__ == '__main__':
    cleanFiles()
    composition = loadFile(COMPOSITION_FILE)
    generateFiles(composition)
    pass