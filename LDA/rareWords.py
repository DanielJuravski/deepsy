import json
import os
import sys
from collections import defaultdict, Counter

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

TRANS_DIR = '/home/daniel/Documents/parsed_trans_reut_v2/'
WORD_FREQ_THRESHOLD = 10
RARE_WORDS_FILE_NAME = 'rare_words.txt'
FILTER_BY = 'word'


def getOptions():
    trans_dir = word_freq_threshold = rare_words_file_name = filter_by = None

    if '--input-dir' in sys.argv:
        option_i = sys.argv.index('--input-dir')
        trans_dir = sys.argv[option_i + 1]

    if '--output' in sys.argv:
        option_i = sys.argv.index('--output')
        rare_words_file_name = sys.argv[option_i + 1]

    if '--threshold' in sys.argv:
        option_i = sys.argv.index('--threshold')
        word_freq_threshold = int(sys.argv[option_i + 1])

    if '--filter-by' in sys.argv:
        option_i = sys.argv.index('--filter-by')
        filter_by = sys.argv[option_i + 1]

    if trans_dir == None or \
        word_freq_threshold == None or \
        rare_words_file_name == None or \
        filter_by == None:
        print("Usage:\n"
              "python3 rareWords.py --input-dir $DIR --output $FILE_NAME --threshold $THRESHOLD --filter-by <word/lemma>\n"
              "Exiting.")
        sys.exit()

    return trans_dir, word_freq_threshold, rare_words_file_name, filter_by


def extract(src_json_data, words_dict, filter_by):
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
            else:
                print("ERROR: filter_by value must be 'word' or 'lemma'.")
                print("Exiting.")
                sys.exit()
            words = plain_text.split()
            for word in words:
                words_dict[word] += 1

    return words_dict


def iterate_dir(trans_dir, words_dict, filter_by):
    directory = os.fsencode(trans_dir)
    for file in os.listdir(directory):

        file_name = os.fsdecode(file)
        json_src_file_name = trans_dir + file_name
        print('iterating over {0}'.format(json_src_file_name))

        with open(json_src_file_name) as f:
            src_json_data = json.load(f)
            words_dict = extract(src_json_data, words_dict, filter_by)

    return words_dict


def write2File(rare_words_file_name, words_dict, word_freq_threshold):
    with open(rare_words_file_name, 'w') as f:
        for word, freq in words_dict.items():
            if freq <= word_freq_threshold:
                f.write(word)
                f.write('\n')

if __name__ == '__main__':
    # That script extracts rare words/lemmas.
    # run for Usage print.

    trans_dir, word_freq_threshold, rare_words_file_name, filter_by = getOptions()
    words_dict = defaultdict(int)
    words_dict = iterate_dir(trans_dir, words_dict, filter_by)
    write2File(rare_words_file_name, words_dict, word_freq_threshold)



