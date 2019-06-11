import json
import os
import shutil

# Transcription json file
PLAIN_TEXT_PARSED_WORD = 'plainText_parsed_word'
PLAIN_TEXT_PARSED_LEMMA = 'plainText_parsed_lemma'
STR_DIALOG_TURNS_LIST = 'dialog_turns_list'
STR_MINI_DIALOG_TURN_LIST = 'mini_dialog_turn_list'
STR_PLAIN_TEXT = 'plainText'
STR_SPEAKER = 'speaker'
STR_CLIENT = 'Client'
STR_THERAPIST = 'Therapist'

# Extracting plain text
PLAIN_TEXT_FILE_PATH = '/tmp/plainText.txt'
PLAIN_TEXT_DETAILS_FILE_PATH = '/tmp/plainTextDetails.txt'
PLAIN_TEXT_PARSED_FILE_PATH = '/tmp/plainTextParsed.txt'
PLAIN_TEXT_WORD_SPLITED_FILE_PATH = '/tmp/plainTextWordSplited.txt'

TRANS_DIR = '/home/daniel/Documents/parsed_trans_reut_v2/'
# TRANS_DIR = 'first_client_parsed/'


def extract(src_json_data):
    client_text_list = []

    dialog_turns_list = src_json_data[STR_DIALOG_TURNS_LIST]
    dialog_turns_list_len = len(dialog_turns_list)
    for dialog_turn_i in range(dialog_turns_list_len):
        dialog_turn_client_text_list = []

        dialog_turn = dialog_turns_list[dialog_turn_i]
        dialog_turn_speaker = dialog_turn[STR_SPEAKER]
        # take only the Client turn, when therapist turn and the client answered -> it will not be written
        if dialog_turn_speaker == STR_CLIENT:
        # if dialog_turn_speaker == STR_THERAPIST:
            mini_dialog_turn_list = dialog_turn[STR_MINI_DIALOG_TURN_LIST]
            mini_dialog_turn_list_len = len(mini_dialog_turn_list)
            for mini_dialog_turn_i in range(mini_dialog_turn_list_len):
                mini_dialog_turn = mini_dialog_turn_list[mini_dialog_turn_i]
                mini_dialog_turn_speaker = mini_dialog_turn[STR_SPEAKER]
                if mini_dialog_turn_speaker == STR_CLIENT:
                # if mini_dialog_turn_speaker == STR_THERAPIST:
                #   plain_text = mini_dialog_turn[PLAIN_TEXT_PARSED_LEMMA]
                    plain_text = mini_dialog_turn[PLAIN_TEXT_PARSED_WORD]
                    dialog_turn_client_text_list.append(plain_text)
            client_text_list.append(dialog_turn_client_text_list)

    return client_text_list


def write2File(trans_file_name, client_text_list):
    #shutil.rmtree('/home/daniel/deepsy/LDA/client_mini_turns/')
    #os.makedirs('/home/daniel/deepsy/LDA/client_mini_turns/')
    client_text_list_len = len(client_text_list)
    for turn_i in range(client_text_list_len):
        turn = client_text_list[turn_i]
        file_name = 'client_mini_turns/' + str(trans_file_name) + str(turn_i) + '_turn.txt'
        with open(file_name, 'w') as f:
            for mini_turn in turn:
                f.write(mini_turn + ' ')


def write2File_client_to_file(trans_file_name, client_text_list):
    client_text_list_len = len(client_text_list)
    file_name = 'clients/' + str(trans_file_name) + '_all_turns.txt'
    with open(file_name, 'w') as f:
        for turn_i in range(client_text_list_len):
            turn = client_text_list[turn_i]
            for mini_turn in turn:
                f.write(mini_turn + ' ')


def write4turns2File(trans_file_name, client_text_list):
    #shutil.rmtree('/home/daniel/deepsy/LDA/client_4_mini_turns/')
    #os.makedirs('/home/daniel/deepsy/LDA/client_4_mini_turns/')
    file_i = 0
    client_text_list_len = len(client_text_list)
    for turn_i in range(client_text_list_len):
        if turn_i%4 == 0:
            file_i += 1
        turn = client_text_list[turn_i]
        file_name = 'v2_words_client_4_mini_turns/' + str(trans_file_name) + str(file_i) + '.txt'
        with open(file_name, 'a') as f:
            for mini_turn in turn:
                f.write(mini_turn + ' ')
            f.write('\n')


def writeDynamicTurns2File(trans_file_name, client_text_list):
    file_i = 1
    mini_turn_len_sum = 0
    client_text_list_len = len(client_text_list)
    for turn_i in range(client_text_list_len):
        turn = client_text_list[turn_i]
        for mini_turn in turn:
            mini_turn_len_sum += len(mini_turn.split())
            if mini_turn_len_sum > 500:
                file_i += 1
                mini_turn_len_sum = 0
            file_name = 'v2_therapist_dyn_mini_turns/' + str(trans_file_name) + str(file_i) + '.txt'
            with open(file_name, 'a') as f:
                f.write(mini_turn)
                f.write('\n')


    #write to file the final f



if __name__ == '__main__':
    # That script extracts the defined json transcriptions to pure text.
    # That for activating the MALLET LDA tool on the pure text.

    # TODO: fix main
    # TODO: output dir/file name as given parameter
    # TODO: think if there is a need to rm -rf the output dir content

    directory = os.fsencode(TRANS_DIR)
    for file in os.listdir(directory):
        file_name = os.fsdecode(file)
        #TRANS_FILE = 'א2_10.12.14.docx.json.parsed'
        json_src_file_name = TRANS_DIR + file_name
        with open(json_src_file_name) as f:
            src_json_data = json.load(f)

        client_text_list = extract(src_json_data)
        # write2File(file_name, client_text_list)
        # write2File_client_to_file(file_name, client_text_list)
        write4turns2File(file_name, client_text_list)
        # writeDynamicTurns2File(file_name, client_text_list)
    pass

