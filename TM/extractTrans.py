import json
import os
import numpy as np

########################## Params - Start ##########################
TURN_SPEAKER = 'Client'  # Client/Therapist/BOTH
TEXT_TYPE = 'plainText_parsed_word'  # plainText_parsed_word/plainText_parsed_lemma
NUM_OF_WORDS = 1000
GAUSSIAN_NUM_OF_WORDS = False  # True/False
NUM_OF_TURNS = 1
OUTPUT_DIR_NAME = 'cyh_sessions'
SPLIT_BY = 'session'  # turn/words/session
########################## Params - End   ##########################


# Transcription json file
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

# Extracting plain text
PLAIN_TEXT_FILE_PATH = '/tmp/plainText.txt'
PLAIN_TEXT_DETAILS_FILE_PATH = '/tmp/plainTextDetails.txt'
PLAIN_TEXT_PARSED_FILE_PATH = '/tmp/plainTextParsed.txt'
PLAIN_TEXT_WORD_SPLITED_FILE_PATH = '/tmp/plainTextWordSplited.txt'

TRANS_DIR = '/home/daniel/Documents/parsed_trans_reut_v2/'


def removeIdentifiers(text, client_identifier, therapist_identifier):
    """
    there are some turns that the transcripts made a mistake,
    and wrote the client/therapist identifier at the beginning of the turn text.
    That is bad because: (1) the client/therapist identifier appears a lot (~ as number of the mini turns) what brakes the topic-modeling
    (2): No additional information is added from those strings (words). So, they will be removed.
    :param text:
    :param client_identifier:
    :param therapist_identifier:
    :return: "text"
    """
    text = text.replace(client_identifier, '')
    text = text.replace(therapist_identifier, '')

    return text


def extract_by_speaker(src_json_data, json_src_file_name):
    # That method extracts all the json content (only the relevant speaker [client/therapist/BOTH] to one list by turns.
    text_list = []

    dialog_turns_list = src_json_data[STR_DIALOG_TURNS_LIST]
    client_identifier = src_json_data[STR_CLIENT_IDENTIFIER]
    therapist_identifier = src_json_data[STR_THERAPIST_IDENTIFIER]

    for dialog_turn_i, _ in enumerate(dialog_turns_list):
        dialog_turn_text = ''
        dialog_turn = dialog_turns_list[dialog_turn_i]
        dialog_turn_speaker = dialog_turn[STR_SPEAKER]

        # take only the TURN_SPEAKER text, the rest will not be written
        if dialog_turn_speaker == TURN_SPEAKER or \
            (TURN_SPEAKER == STR_BOTH and (dialog_turn_speaker == STR_CLIENT or dialog_turn_speaker == STR_THERAPIST)):
            mini_dialog_turn_list = dialog_turn[STR_MINI_DIALOG_TURN_LIST]
            for mini_dialog_turn_i, _ in enumerate(mini_dialog_turn_list):
                mini_dialog_turn = mini_dialog_turn_list[mini_dialog_turn_i]
                mini_dialog_turn_speaker = mini_dialog_turn[STR_SPEAKER]

                # take only the TURN_SPEAKER text, the rest will not be written
                if mini_dialog_turn_speaker == TURN_SPEAKER or \
                        (TURN_SPEAKER == STR_BOTH and (mini_dialog_turn_speaker == STR_CLIENT or mini_dialog_turn_speaker == STR_THERAPIST)):
                    text = mini_dialog_turn[TEXT_TYPE]
                    text = removeIdentifiers(text, client_identifier, therapist_identifier)
                    # handle blank mini_turns text
                    if text != "":
                        dialog_turn_text += ' '
                        dialog_turn_text += text
            # handle blank mini_turns text
            if dialog_turn_text != "":
                text_list.append(dialog_turn_text)
                # print("Doc:{0}\n line:{1}".format(json_src_file_name, dialog_turn_text))

    return text_list


def writeEntireSession2File(trans_file_name, text_list):
    # Write the whole session to single file.
    text_list_len = len(text_list)
    file_name = 'Dirs_of_Docs/{0}/Documents/{1}.txt'.format(OUTPUT_DIR_NAME, str(trans_file_name))

    with open(file_name, 'w') as f:
        for turn_i in range(text_list_len):
            turn = text_list[turn_i]
            f.write(turn + ' ')


def writeDynamicTurns2File(trans_file_name, text_list):
    # Write words to file by the number of turns.
    # HERE THERE IS A PROBLEM,
    # ORIGINALLY WAS CREATED FOR MINI-TURNS, BUT NOW TEXT LIST IS 1 SINGLE TURN
    # IS WRITING TURN IS NOT TOO MUCH?
    file_i = 1
    text_to_print = ''
    for turn_i, _ in enumerate(text_list):
        turn = text_list[turn_i]
        text_to_print += turn
        text_to_print += ' '

        if turn_i % NUM_OF_TURNS == 0 and turn_i != 0:
            file_name = 'Dirs_of_Docs/{0}/Documents/{1}{2}.txt'.format(OUTPUT_DIR_NAME, str(trans_file_name), str(file_i))

            with open(file_name, 'w') as f:
                f.write(text_to_print)

            file_i += 1
            text_to_print = ''

    # Write the last section to file. because we exited from the for loop.
    file_name = 'Dirs_of_Docs/{0}/Documents/{1}{2}.txt'.format(OUTPUT_DIR_NAME, str(trans_file_name), str(file_i))

    # with open(file_name, 'w') as f:
    #     f.write(text_to_print)


def list2str(text_list):
    text_str = ''
    for i in text_list:
        text_str += i

    return text_str


def writeDynamicWords2File(trans_file_name, text_list):
    # Push words to buffer, until it contain NUM_OF_WORDS words.
    # Then write that content to file.

    text_str = list2str(text_list)
    num_of_words_buffer = np.random.normal(NUM_OF_WORDS, 50, 1) if GAUSSIAN_NUM_OF_WORDS is True else NUM_OF_WORDS
    file_i = 1
    turn_len_sum = 0
    text_to_print = ''
    for word in text_str.split():

        turn_len_sum += 1
        text_to_print += word
        text_to_print += ' '

        if turn_len_sum >= num_of_words_buffer:
            file_name = 'Dirs_of_Docs/{0}/Documents/{1}{2}.txt'.format(OUTPUT_DIR_NAME, str(trans_file_name), str(file_i))

            with open(file_name, 'w') as f:
                f.write(text_to_print)

            file_i += 1
            turn_len_sum = 0
            text_to_print = ''

    # write last file (where certainty turn_len_sum < num_of_words_buffer)
    file_name = 'Dirs_of_Docs/{0}/Documents/{1}{2}.txt'.format(OUTPUT_DIR_NAME, str(trans_file_name), str(file_i))
    with open(file_name, 'w') as f:
        f.write(text_to_print)


def createOutputDir():
    print('Create output Documents dir ...')
    output_dir = 'Dirs_of_Docs/{0}/Documents'.format(OUTPUT_DIR_NAME)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        num_of_files = len(os.listdir(output_dir))
        print('[WARNING] dir already exist with {0} files in it.'.format(num_of_files))


if __name__ == '__main__':
    # That script extracts the defined json transcriptions to pure text.
    # That for activating the MALLET TM tool on the pure text.

    # create the dir where the created documents will be plotted to
    createOutputDir()

    print('Processing ...')
    directory = os.fsencode(TRANS_DIR)
    for file in os.listdir(directory):
        file_name = os.fsdecode(file)
        json_src_file_name = TRANS_DIR + file_name
        with open(json_src_file_name) as f:
            src_json_data = json.load(f)

        # 'text_list' contains all the string content of the current json
        text_list = extract_by_speaker(src_json_data, json_src_file_name)

        if SPLIT_BY == 'words':
            writeDynamicWords2File(file_name, text_list)
        elif SPLIT_BY == 'turn':
            writeDynamicTurns2File(file_name, text_list)
        elif SPLIT_BY == 'session':
            writeEntireSession2File(file_name, text_list)
        else:
            print('[ERROR]: Invalid SPLIT_BY value.')
            exit(1)

    print("Done.")


