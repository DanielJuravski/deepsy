import json
import os
import sys
from collections import defaultdict, Counter

########################## Params - Start ##########################
TRANS_DIR = '/home/daniel/Documents/parsed_trans_reut_v2/'
WORD_FREQ_THRESHOLD = 9
FILTER_BY = 'lemma'
RARE_WORDS_FILE_NAME = 'rare.txt'
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
        trans_dir = sys.argv[option_i + 1]
    else:
        trans_dir = TRANS_DIR

    if '--output' in sys.argv:
        option_i = sys.argv.index('--output')
        rare_words_file_name = sys.argv[option_i + 1]
    else:
        rare_words_file_name = RARE_WORDS_FILE_NAME

    if '--threshold' in sys.argv:
        option_i = sys.argv.index('--threshold')
        word_freq_threshold = int(sys.argv[option_i + 1])
    else:
        word_freq_threshold = WORD_FREQ_THRESHOLD

    if '--filter-by' in sys.argv:
        option_i = sys.argv.index('--filter-by')
        filter_by = sys.argv[option_i + 1]
        if filter_by != 'word' and filter_by != 'lemma':
            print("ERROR: filter_by value must be 'word' or 'lemma'.")
            print("Exiting.")
    else:
        filter_by = FILTER_BY

    if trans_dir == None or \
        word_freq_threshold == None or \
        rare_words_file_name == None or \
        filter_by == None:
        print("Usage:\n"
              "python3 rareWords.py --input-dir $DIR --output $FILE_NAME --threshold $THRESHOLD --filter-by <word/lemma>\n"
              "Exiting.")
        sys.exit()

    return trans_dir, word_freq_threshold, rare_words_file_name, filter_by


def extract(src_json_data, rare_words_dict, filter_by):
    dialog_turns_list = src_json_data[STR_DIALOG_TURNS_LIST]
    dialog_turns_list_len = len(dialog_turns_list)
    for dialog_turn_i in range(dialog_turns_list_len):
        dialog_turn = dialog_turns_list[dialog_turn_i]
        mini_dialog_turn_list = dialog_turn[STR_MINI_DIALOG_TURN_LIST]
        mini_dialog_turn_list_len = len(mini_dialog_turn_list)
        for mini_dialog_turn_i in range(mini_dialog_turn_list_len):
            mini_dialog_turn = mini_dialog_turn_list[mini_dialog_turn_i]
            if filter_by == 'word':
                plain_text = mini_dialog_turn[PLAIN_TEXT_PARSED_WORD]
            elif filter_by == 'lemma':
                plain_text = mini_dialog_turn[PLAIN_TEXT_PARSED_LEMMA]
            words = plain_text.split()
            for word in words:
                rare_words_dict[word] += 1

    return rare_words_dict


def iterate_dir(trans_dir, rare_words_dict, filter_by):
    directory = os.fsencode(trans_dir)
    for file in os.listdir(directory):

        file_name = os.fsdecode(file)
        json_src_file_name = trans_dir + file_name
        print('iterating over {0}'.format(json_src_file_name))

        with open(json_src_file_name) as f:
            src_json_data = json.load(f)
            rare_words_dict = extract(src_json_data, rare_words_dict, filter_by)

    return rare_words_dict


def write2File(rare_words_file_name, rare_words):
    with open(rare_words_file_name, 'w') as f:
        for word in rare_words:
            f.write(word)
            f.write('\n')


def processRare(words_dict, word_freq_threshold):
    rare_words = []
    for word, freq in words_dict.items():
        if freq <= word_freq_threshold:
            rare_words.append(word)

    return rare_words


if __name__ == '__main__':
    # That script extracts rare words/lemmas.
    # run without params for Usage print.

    # initialization
    trans_dir, word_freq_threshold, rare_words_file_name, filter_by = getOptions()
    rare_words_dict = defaultdict(int)

    # get all words in the docs
    rare_words_dict = iterate_dir(trans_dir, rare_words_dict, filter_by)
    # get rare words
    rare_words = processRare(rare_words_dict, word_freq_threshold)

    # write all the anomalous words to file
    write2File(rare_words_file_name, rare_words)



