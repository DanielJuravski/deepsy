import json
import os

########################## Params - Start ##########################
TURN_SPEAKER = 'Client'
TEXT_TYPE = 'plainText_parsed_word'
NUM_OF_WORDS = 1000
OUTPUT_DIR_NAME = 'c_sessions'
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

# Extracting plain text
PLAIN_TEXT_FILE_PATH = '/tmp/plainText.txt'
PLAIN_TEXT_DETAILS_FILE_PATH = '/tmp/plainTextDetails.txt'
PLAIN_TEXT_PARSED_FILE_PATH = '/tmp/plainTextParsed.txt'
PLAIN_TEXT_WORD_SPLITED_FILE_PATH = '/tmp/plainTextWordSplited.txt'

TRANS_DIR = '/home/daniel/Documents/parsed_trans_reut_v2/'


def extract_by_speaker(src_json_data):
    # That method extracts all the json content (only the relevant speaker [client/therapist] to one list by turns.
    text_list = []

    dialog_turns_list = src_json_data[STR_DIALOG_TURNS_LIST]
    for dialog_turn_i, _ in enumerate(dialog_turns_list):
        dialog_turn_text = ''
        dialog_turn = dialog_turns_list[dialog_turn_i]
        dialog_turn_speaker = dialog_turn[STR_SPEAKER]

        # take only the TURN_SPEAKER text, the rest will not be written
        if dialog_turn_speaker == TURN_SPEAKER:
            mini_dialog_turn_list = dialog_turn[STR_MINI_DIALOG_TURN_LIST]
            for mini_dialog_turn_i, _ in enumerate(mini_dialog_turn_list):
                mini_dialog_turn = mini_dialog_turn_list[mini_dialog_turn_i]
                mini_dialog_turn_speaker = mini_dialog_turn[STR_SPEAKER]

                # take only the TURN_SPEAKER text, the rest will not be written
                if mini_dialog_turn_speaker == TURN_SPEAKER:
                    text = mini_dialog_turn[TEXT_TYPE]
                    dialog_turn_text += ' '
                    dialog_turn_text += text
            text_list.append(dialog_turn_text)

    return text_list


def write2File(trans_file_name, client_text_list):

    client_text_list_len = len(client_text_list)
    for turn_i in range(client_text_list_len):
        turn = client_text_list[turn_i]
        file_name = 'client_mini_turns/' + str(trans_file_name) + str(turn_i) + '_turn.txt'
        with open(file_name, 'w') as f:
            for mini_turn in turn:
                f.write(mini_turn + ' ')


def writeEntireSession2File(trans_file_name, text_list):
    # Write the whole session to single file.
    text_list_len = len(text_list)
    file_name = 'Dirs_of_Docs/{0}/Documents/{1}.txt'.format(OUTPUT_DIR_NAME, str(trans_file_name))

    with open(file_name, 'w') as f:
        for turn_i in range(text_list_len):
            turn = text_list[turn_i]
            f.write(turn + ' ')


def writeTurns2File(trans_file_name, text_list, num_of_turns):
    # THERE IS HERE A PROBLEM,
    # WAS CREATED FOR MINI-TURNS, BUT NOW TEXT LIST IS 1 SINGLE TURN
    # IS WRITING TURN IS NOT TOO MUCH?
    file_i = 0
    text_to_print = ''
    text_list_len = len(text_list)
    for turn_i in range(text_list_len):
        turn = text_list[turn_i]
        text_to_print += turn
        text_to_print += ' '

        if turn_i%num_of_turns == 0:
            file_i += 1

        file_name = 'v2_words_client_4_mini_turns/' + str(trans_file_name) + str(file_i) + '.txt'
        with open(file_name, 'w') as f:
            for mini_turn in turn:
                f.write(mini_turn + ' ')
            f.write('\n')


def writeDynamicWords2File(trans_file_name, text_list):
    # Push words to buffer, until it contain NUM_OF_WORDS words.
    # Then write that content to file.
    file_i = 1
    turn_len_sum = 0
    text_to_print = ''
    for turn_i, _ in enumerate(text_list):
        turn = text_list[turn_i]
        # get number of words
        turn_len_sum += len(turn.split())
        text_to_print += turn
        text_to_print += ' '

        if turn_len_sum > NUM_OF_WORDS:
            file_name = 'Dirs_of_Docs/{0}/Documents/{1}{2}.txt'.format(OUTPUT_DIR_NAME, str(trans_file_name), str(file_i))

            with open(file_name, 'w') as f:
                f.write(text_to_print)

            file_i += 1
            turn_len_sum = 0
            text_to_print = ''


def createOutputDir():
    output_dir = 'Dirs_of_Docs/{0}/Documents'.format(OUTPUT_DIR_NAME)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


if __name__ == '__main__':
    # That script extracts the defined json transcriptions to pure text.
    # That for activating the MALLET TM tool on the pure text.

    # create the dir where the created documents will be plotted to
    createOutputDir()

    directory = os.fsencode(TRANS_DIR)
    for file in os.listdir(directory):
        file_name = os.fsdecode(file)
        json_src_file_name = TRANS_DIR + file_name
        with open(json_src_file_name) as f:
            src_json_data = json.load(f)

        # 'text_list' contains all the string content of the current json
        text_list = extract_by_speaker(src_json_data)

        # write2File(file_name, client_text_list)
        # write4turns2File(file_name, client_text_list)

        # Supported:
        writeEntireSession2File(file_name, text_list)
        # writeDynamicWords2File(file_name, text_list)


