import json
import os
import sys
from collections import defaultdict, Counter

########################## Params - Start ##########################
TRANS_DIR = '/home/daniel/deepsy/TM/client_5_mini_turns/'
WORD_FREQ_THRESHOLD = 0.9
RARE_WORDS_FILE_NAME = 'common_strings_' + str(WORD_FREQ_THRESHOLD) + '.txt'
########################## Params - End   ##########################

# Transcription json file
PLAIN_TEXT_PARSED_WORD = 'plainText_parsed_word'
PLAIN_TEXT_PARSED_LEMMA = 'plainText_parsed_lemma'
STR_DIALOG_TURNS_LIST = 'dialog_turns_list'
STR_MINI_DIALOG_TURN_LIST = 'mini_dialog_turn_list'
STR_PLAIN_TEXT = 'plainText'
STR_SPEAKER = 'speaker'
STR_CLIENT = 'Client'

# Extracting plain text
PLAIN_TEXT_FILE_PATH = '/tmp/plainText.txt'
PLAIN_TEXT_DETAILS_FILE_PATH = '/tmp/plainTextDetails.txt'
PLAIN_TEXT_PARSED_FILE_PATH = '/tmp/plainTextParsed.txt'
PLAIN_TEXT_WORD_SPLITED_FILE_PATH = '/tmp/plainTextWordSplited.txt'


def getOptions():
    if '--input-dir' in sys.argv:
        option_i = sys.argv.index('--input-dir')
        documents_dir = sys.argv[option_i + 1]
    else:
        documents_dir = TRANS_DIR

    if '--output' in sys.argv:
        option_i = sys.argv.index('--output')
        common_words_file_name = sys.argv[option_i + 1]
    else:
        common_words_file_name = RARE_WORDS_FILE_NAME

    if '--threshold' in sys.argv:
        option_i = sys.argv.index('--threshold')
        common_threshold = float(sys.argv[option_i + 1])
    else:
        common_threshold = WORD_FREQ_THRESHOLD

    if documents_dir == None or \
        common_threshold == None or \
        common_words_file_name == None: # or \
        print("Usage:\n"
              "python3 commonWords.py --input-dir $DIR --output $FILE_NAME --threshold $THRESHOLD \n"
              "Exiting.")
        sys.exit()

    return documents_dir, common_threshold, common_words_file_name


def iterate_dir(documents_dir, common_words_dict):
    directory = os.fsencode(documents_dir)
    dir_size = len(os.listdir(directory))
    file_i = 0
    for file in os.listdir(directory):
        file_i += 1
        file_name = os.fsdecode(file)
        doc_src_file_name = documents_dir + file_name
        ratio = file_i/len(os.listdir(directory)) * 100
        # print(str(ratio))
        if file_i % 1000 == 0:
            print(str(ratio) + '% docs were loaded')

        doc_data = []
        with open(doc_src_file_name) as f:
            for line in f:
                for word in line.split():
                    doc_data.append(word)

        #uniqe_doc_data = set(doc_data)

        for word in doc_data:
            common_words_dict[word] += 1

    return common_words_dict, dir_size


def write2File(common_words_file_name, common_words):
    with open(common_words_file_name, 'w') as f:
        for word in common_words:
            f.write(word)
            f.write('\n')


def processCommon(common_words_dict, common_threshold, dir_size):
    print("Processing ...")
    common_words = []
    for word, freq in common_words_dict.items():
        if freq >= common_threshold*dir_size:
            common_words.append(word)

    return common_words


if __name__ == '__main__':
    # That script extract words/lemmas that appeared more than $COMMON_THRESHOLD.
    # The documents here are in the same template that are imported into the Topic Modeling alg.
    # run without params for Usage print.
    # threshold between 0<=x<=1
    # The filter_by flag is not relevant, since the string counting is over the already created documents.
    # (We don't know if those documents created from words or lemmas)

    # initialization
    documents_dir, common_threshold, common_words_file_name = getOptions()
    common_words_dict = defaultdict(int)

    # get all words in the docs
    common_words_dict, dir_size = iterate_dir(documents_dir, common_words_dict)
    # get common words
    common_words = processCommon(common_words_dict, common_threshold, dir_size)

    # write all the anomalous words to file
    write2File(common_words_file_name, common_words)



