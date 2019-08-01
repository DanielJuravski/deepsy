import sys
import os
import json

########################## Params - Start ##########################
TRANS_DIR = '/home/daniel/Documents/parsed_trans_reut_v2/'
FILTER_BY = 'word'
STOPWORDS_FILE_NAME = 'stop.txt'
########################## Params - End   ##########################

# Transcription json file
PLAIN_TEXT_PARSED_WORD = 'plainText_parsed_word'
PLAIN_TEXT_PARSED_LEMMA = 'plainText_parsed_lemma'
PLAIN_TEXT_PARSED_POS = 'plainText_parsed_pos'

STR_DIALOG_TURNS_LIST = 'dialog_turns_list'
STR_MINI_DIALOG_TURN_LIST = 'mini_dialog_turn_list'
STR_PLAIN_TEXT = 'plainText'
STR_SPEAKER = 'speaker'
STR_CLIENT = 'Client'

NON_STOP_POS = ["ADVERB", "BN", "BNT", "JJ", "JJT", "NN", "NNP", "NNT", "VB"]

def getOptions():
    if '--input-dir' in sys.argv:
        option_i = sys.argv.index('--input-dir')
        trans_dir = sys.argv[option_i + 1]
    else:
        trans_dir = TRANS_DIR

    if '--output' in sys.argv:
        option_i = sys.argv.index('--output')
        stop_words_file_name = sys.argv[option_i + 1]
    else:
        stop_words_file_name = STOPWORDS_FILE_NAME

    if '--filter-by' in sys.argv:
        option_i = sys.argv.index('--filter-by')
        filter_by = sys.argv[option_i + 1]
    else:
        filter_by = FILTER_BY

    if trans_dir == None or \
        stop_words_file_name == None or \
        filter_by == None:
        print("Usage:\n"
              "python3 rareWords.py --input-dir $DIR --output $FILE_NAME --filter-by <word/lemma>\n"
              "Exiting.")
        sys.exit()

    return trans_dir, stop_words_file_name, filter_by


def findStopWords(src_json_data, filter_by):
    trans_stop_words = set([])

    dialog_turns_list = src_json_data[STR_DIALOG_TURNS_LIST]
    dialog_turns_list_len = len(dialog_turns_list)
    for dialog_turn_i in range(dialog_turns_list_len):
        dialog_turn = dialog_turns_list[dialog_turn_i]
        mini_dialog_turn_list = dialog_turn[STR_MINI_DIALOG_TURN_LIST]
        mini_dialog_turn_list_len = len(mini_dialog_turn_list)
        for mini_dialog_turn_i in range(mini_dialog_turn_list_len):
            mini_dialog_turn = mini_dialog_turn_list[mini_dialog_turn_i]
            if filter_by == 'word':
                plain_text = mini_dialog_turn[PLAIN_TEXT_PARSED_WORD].split()
            elif filter_by == 'lemma':
                plain_text = mini_dialog_turn[PLAIN_TEXT_PARSED_LEMMA].split()
            plain_text_pos = mini_dialog_turn[PLAIN_TEXT_PARSED_POS].split()
            plain_text_len = len(plain_text)
            for word_i in range(plain_text_len):
                word_pos = plain_text_pos[word_i]
                word = plain_text[word_i]
                if word_pos not in NON_STOP_POS:
                    trans_stop_words.add(word)

    return trans_stop_words


def iterateTrans(trans_dir, filter_by):
    all_stop_words = set()
    directory = os.fsencode(trans_dir)
    for file in os.listdir(directory):
        file_name = os.fsdecode(file)
        json_src_file_name = trans_dir + file_name
        print('iterating over {0}'.format(json_src_file_name))
        with open(json_src_file_name) as f:
            src_json_data = json.load(f)
            trans_stop_words = findStopWords(src_json_data, filter_by)
            all_stop_words = all_stop_words.union(trans_stop_words)

    return all_stop_words


def write2Files(stop_words, stopwords_file_name):
    with open(stopwords_file_name, 'w') as f:
        for word in stop_words:
            f.write(word)
            f.write('\n')


def getMaualStopWords():
    words = set()
    words.add('X')
    words.add('XX')
    words.add('XXX')
    words.add('XXXX')
    words.add('XXXXX')
    words.add('XXXXXX')
    words.add('x')
    words.add('xx')
    words.add('xxx')
    words.add('xxxx')
    words.add('xxxxx')
    words.add('xxxxxx')
    words.add('אמ')
    words.add('אממ')
    words.add('אמממ')
    words.add('מ')
    words.add('ממ')
    words.add('מממ')
    words.add('ממממ')
    words.add('אה')
    words.add('אהה')
    words.add('אההה')

    return words


if __name__ == '__main__':
    # get stopwords/lemmas from all the transcriptions files
    # stop word/lemma is any word/lemma that its POS is not noun, verb, adverb, adj

    trans_dir, stop_words_file_name, filter_by = getOptions()
    stop_words = iterateTrans(trans_dir,filter_by)

    stop_words = stop_words.union(getMaualStopWords())
    write2Files(stop_words, stop_words_file_name)

