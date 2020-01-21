import os
import json
import random


PSY_DATASET = "/home/daniel/Documents/parsed_trans_reut_v2/"
FILTER_BY = "orig"
MINI_TURNS_FILE = "all_mini_turns.txt"
TURN_SPEAKER = 'Client'  # Client/Therapist/BOTH
NUM_TURNS_PRINT = 10

# Transcription json file
PLAIN_TEXT = 'plainText'
PLAIN_TEXT_PARSED_WORD = 'plainText_parsed_word'
PLAIN_TEXT_PARSED_LEMMA = 'plainText_parsed_lemma'
STR_DIALOG_TURNS_LIST = 'dialog_turns_list'
STR_MINI_DIALOG_TURN_LIST = 'mini_dialog_turn_list'
STR_CLIENT_IDENTIFIER = 'client_identifier'
STR_THERAPIST_IDENTIFIER = 'therapist_identifier'
STR_PLAIN_TEXT = 'plainText'
STR_SPEAKER = 'speaker'
STR_CLIENT = 'Client'
STR_THERAPIST = 'Therapist'
STR_BOTH = 'BOTH'


def extract(src_json_data):
    dialog_turns_list = src_json_data[STR_DIALOG_TURNS_LIST]
    dialog_turns_list_len = len(dialog_turns_list)
    mini_turns = []

    for dialog_turn_i in range(dialog_turns_list_len):
        dialog_turn = dialog_turns_list[dialog_turn_i]
        dialog_turn_speaker = dialog_turn[STR_SPEAKER]
        # take only the TURN_SPEAKER text
        if dialog_turn_speaker == TURN_SPEAKER or \
                (TURN_SPEAKER == STR_BOTH and
                        (dialog_turn_speaker == STR_CLIENT or dialog_turn_speaker == STR_THERAPIST)):
            mini_dialog_turn_list = dialog_turn[STR_MINI_DIALOG_TURN_LIST]
            mini_dialog_turn_list_len = len(mini_dialog_turn_list)
            for mini_dialog_turn_i in range(mini_dialog_turn_list_len):
                mini_dialog_turn = mini_dialog_turn_list[mini_dialog_turn_i]
                mini_dialog_turn_speaker = mini_dialog_turn[STR_SPEAKER]

                # take only the TURN_SPEAKER text
                if mini_dialog_turn_speaker == TURN_SPEAKER or \
                        (TURN_SPEAKER == STR_BOTH and (
                                mini_dialog_turn_speaker == STR_CLIENT or mini_dialog_turn_speaker == STR_THERAPIST)):
                    if FILTER_BY == 'word':
                        plain_text = mini_dialog_turn[PLAIN_TEXT_PARSED_WORD]
                    elif FILTER_BY == 'lemma':
                        plain_text = mini_dialog_turn[PLAIN_TEXT_PARSED_LEMMA]
                    elif FILTER_BY == 'orig':
                        plain_text = mini_dialog_turn[PLAIN_TEXT]
                    mini_turns.append(plain_text)

    return mini_turns


def loadData():
    directory = os.fsencode(PSY_DATASET)
    psy_file_i = 1
    mini_turns = []
    for file in os.listdir(directory):
        file_name = os.fsdecode(file)
        json_src_file_name = PSY_DATASET + file_name
        if psy_file_i % 100 == 0:
            print('iterating on file {0}/{1}'.format(psy_file_i, len(os.listdir(directory))))

        with open(json_src_file_name) as f:
            src_json_data = json.load(f)
            mini_turns_i = extract(src_json_data)
        mini_turns += mini_turns_i
        psy_file_i += 1

    return mini_turns


def outputMiniTurns(mini_turns):
    num_mini_turns = len(mini_turns)
    print("Number of mini_turns: {0}".format(num_mini_turns))

    with open(MINI_TURNS_FILE, 'w') as f:
        for mt in mini_turns:
            f.write(mt)
            f.write('\n')

    for _ in range(NUM_TURNS_PRINT):
        val = random.randint(0,num_mini_turns)
        print(mini_turns[val])


if __name__ == '__main__':
    """
    That script iterate all the 873 trans, and 
    1. write to MINI_TURNS_FILE all the TURN_SPEAKER mini turns
    2. print randomly NUM_TURNS_PRINT of them
    """
    mini_turns = loadData()
    outputMiniTurns(mini_turns)
