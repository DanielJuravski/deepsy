import sys
import os
import json
from collections import defaultdict, Counter


# Transcription json file
STR_DIALOG_TURNS_LIST = 'dialog_turns_list'
STR_MINI_DIALOG_TURN_LIST = 'mini_dialog_turn_list'
STR_PLAIN_TEXT = 'plainText'

# Json
PLAIN_TEXT_PARSED_WORD = 'plainText_parsed_word'
PLAIN_TEXT_PARSED_LEMMA = 'plainText_parsed_lemma'
PLAIN_TEXT_PARSED_POS = 'plainText_parsed_pos'
PLAIN_TEXT_PARSED_MORPH = 'plainText_parsed_morphological'


def analizeSentence(plain_text_word, emb_dict_file, words_in_dict, words_not_in_dict):
    words = plain_text_word.split()

    with open(emb_dict_file, 'r') as dict_f:
        dict = dict_f.read().splitlines()
        for word in words:
            if word in dict:
                words_in_dict[word] += 1
                print('in dict: {0}'.format(word))

            else:
                words_not_in_dict[word] += 1
                print('not in dict: {0}'.format(word))

    return words_in_dict, words_not_in_dict


def openFile(transcriptions_dir, filename, emb_dict_file, words_in_dict, words_not_in_dict):
    file_path = transcriptions_dir + filename
    with open(file_path, 'r') as transcription_file:
        transcription_json = json.load(transcription_file)
        print('Scanning: {0}'.format(filename))

        dialog_turns_list = transcription_json[STR_DIALOG_TURNS_LIST]
        dialog_turns_list_len = len(dialog_turns_list)
        for dialog_turn_i in range(dialog_turns_list_len):
            dialog_turn = dialog_turns_list[dialog_turn_i]
            mini_dialog_turn_list = dialog_turn[STR_MINI_DIALOG_TURN_LIST]
            mini_dialog_turn_list_len = len(mini_dialog_turn_list)
            for mini_dialog_turn_i in range(mini_dialog_turn_list_len):
                mini_dialog_turn = mini_dialog_turn_list[mini_dialog_turn_i]
                plain_text_word = mini_dialog_turn[PLAIN_TEXT_PARSED_WORD]
                #plain_text = mini_dialog_turn[STR_PLAIN_TEXT]
                words_in_dict, words_not_in_dict = analizeSentence(plain_text_word, emb_dict_file, words_in_dict, words_not_in_dict)


    return words_in_dict, words_not_in_dict



def analizeDir(emb_dict_file, transcriptions_dir):
    directory = os.fsencode(transcriptions_dir)
    words_in_dict = defaultdict(int)
    words_not_in_dict = defaultdict(int)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".parsed"):
            words_in_dict, words_not_in_dict = openFile(transcriptions_dir, filename, emb_dict_file, words_in_dict, words_not_in_dict)

    return words_in_dict, words_not_in_dict


if __name__ == '__main__':
    # check how many words in the transcription files exist in the embedding representation

    emb_dict_file = '/home/daniel/Documents/he_emb/ron_shemesh/words_list.txt'
    transcriptions_dir = '/home/daniel/Documents/parsed_trans_reut_test/'

    print('Searching parsed files in {0}'.format(transcriptions_dir))
    print('Embedding dictionary: {0}'.format(emb_dict_file))

    words_in_dict, words_not_in_dict = analizeDir(emb_dict_file, transcriptions_dir)

    print('Total words in dict: {0}'.format(len(words_in_dict)))
    print('Total words not in dict: {0}'.format(len(words_not_in_dict)))
