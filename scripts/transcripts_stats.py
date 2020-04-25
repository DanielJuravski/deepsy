import os
import json
import numpy as np

########################## Params - Start ##########################
TRANS_DIR = '/home/daniel/Documents/parsed_trans_reut_v2/'
########################## Params - End   ##########################

# Transcription json file
PLAIN_TEXT_PARSED_WORD = 'plainText_parsed_word'
PLAIN_TEXT_PARSED_LEMMA = 'plainText_parsed_lemma'
STR_DIALOG_TURNS_LIST = 'dialog_turns_list'
STR_MINI_DIALOG_TURN_LIST = 'mini_dialog_turn_list'
STR_PLAIN_TEXT = 'plainText'
STR_SPEAKER = 'speaker'
STR_CLIENT = 'Client'
STR_THERAPIST = 'Therapist'
STR_ANNOTATOR = 'Annotator'

# Extracting plain text
PLAIN_TEXT_FILE_PATH = '/tmp/plainText.txt'
PLAIN_TEXT_DETAILS_FILE_PATH = '/tmp/plainTextDetails.txt'
PLAIN_TEXT_PARSED_FILE_PATH = '/tmp/plainTextParsed.txt'
PLAIN_TEXT_WORD_SPLITED_FILE_PATH = '/tmp/plainTextWordSplited.txt'


def process(turns):
    words = 0
    num_turns = 0
    for t in turns:
        words += len(t.split())
        num_turns += 1

    return words, num_turns


def extract_turns():
    t_turns_words_count = list()
    t_turns_count = list()
    c_turns_words_count = list()
    c_turns_count = list()
    a_turns_words_count = list()
    a_turns_count = list()

    directory = os.fsencode(TRANS_DIR)
    for file in os.listdir(directory):

        file_name = os.fsdecode(file)
        json_src_file_name = TRANS_DIR + file_name

        with open(json_src_file_name) as f:
            src_json_data = json.load(f)
            local_t_turns, local_c_turns, local_a_turns = extract(src_json_data)

            words, num_turns = process(local_t_turns)
            t_turns_words_count.append(words)
            t_turns_count.append(num_turns)

            words, num_turns = process(local_c_turns)
            c_turns_words_count.append(words)
            c_turns_count.append(num_turns)

            words, num_turns = process(local_a_turns)
            a_turns_words_count.append(words)
            a_turns_count.append(num_turns)

    return t_turns_words_count, t_turns_count, c_turns_words_count, c_turns_count, a_turns_words_count, a_turns_count


def extract(src_json_data):
    c_turns = []
    t_turns = []
    a_turns = []
    dialog_turns_list = src_json_data[STR_DIALOG_TURNS_LIST]
    dialog_turns_list_len = len(dialog_turns_list)
    for dialog_turn_i in range(dialog_turns_list_len):
        dialog_turn = dialog_turns_list[dialog_turn_i]
        mini_dialog_turn_list = dialog_turn[STR_MINI_DIALOG_TURN_LIST]
        mini_dialog_turn_list_len = len(mini_dialog_turn_list)
        for mini_dialog_turn_i in range(mini_dialog_turn_list_len):
            mini_dialog_turn = mini_dialog_turn_list[mini_dialog_turn_i]
            if mini_dialog_turn[STR_SPEAKER] == STR_CLIENT:
                c_turns.append(mini_dialog_turn[STR_PLAIN_TEXT])
            if mini_dialog_turn[STR_SPEAKER] == STR_THERAPIST:
                t_turns.append(mini_dialog_turn[STR_PLAIN_TEXT])
            if mini_dialog_turn[STR_SPEAKER] == STR_ANNOTATOR:
                a_turns.append(mini_dialog_turn[STR_PLAIN_TEXT])

    return t_turns, c_turns, a_turns


def print_stats(t_turns_words_count, t_turns_count, c_turns_words_count, c_turns_count, a_turns_words_count, a_turns_count):
    print("number of total (patient + therapist) mini turns: {0}"
          .format(sum(t_turns_count) + sum(c_turns_count)))

    print("number of total (patient + therapist) words: {0}"
          .format(sum(t_turns_words_count) + sum(c_turns_words_count)))

    print("avg of words in trans by client: {0}"
          .format(np.average(np.asarray(c_turns_words_count))))
    print("sd of words in trans by client: {0}"
          .format(np.std(np.asarray(c_turns_words_count))))
    print(np.sort(np.asarray(c_turns_words_count))[:10])
    print("range words in trans by client: [{0}-{1}]"
          .format(np.min(np.asarray(c_turns_words_count)),
                  np.max(np.asarray(c_turns_words_count))))

    print("avg of words in trans by therapist: {0}"
          .format(np.average(np.asarray(t_turns_words_count))))
    print("sd of words in trans by therapist: {0}"
          .format(np.std(np.asarray(t_turns_words_count))))
    print(np.sort(np.asarray(t_turns_words_count))[:10])
    print("range words in trans by therapist: [{0}-{1}]"
          .format(np.min(np.asarray(t_turns_words_count)),
                  np.max(np.asarray(t_turns_words_count))))

    all_turns_count = [c+t for (c,t) in zip (c_turns_count, t_turns_count)]
    print("avg of turns in trans (therapist+patient): {0}"
          .format(np.average(all_turns_count)))
    print("sd of turns in trans (therapist+patient): {0}"
          .format(np.std(all_turns_count)))
    print("range turns in trans by therapist: [{0}-{1}]"
          .format(np.min(all_turns_count),
                  np.max(all_turns_count)))



if __name__ == '__main__':
    t_turns_words_count, t_turns_count, c_turns_words_count, c_turns_count, a_turns_words_count, a_turns_count = extract_turns()
    print_stats(t_turns_words_count, t_turns_count, c_turns_words_count, c_turns_count, a_turns_words_count, a_turns_count)
    pass