import os
import json

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


def extract_identifiers(src_json_data):
    client_identifier = src_json_data[STR_CLIENT_IDENTIFIER]
    therapist_identifier = src_json_data[STR_THERAPIST_IDENTIFIER]

    return client_identifier, therapist_identifier


def main():
    ids = set()
    directory = os.fsencode(TRANS_DIR)
    for file in os.listdir(directory):
        file_name = os.fsdecode(file)
        json_src_file_name = TRANS_DIR + file_name
        with open(json_src_file_name) as f:
            src_json_data = json.load(f)

        client_identifier, therapist_identifier = extract_identifiers(src_json_data)
        ids.add(client_identifier)
        ids.add(therapist_identifier)

    print(ids)
    with open('identifiers.txt', 'w') as f:
        for id in ids:
            f.writelines(id)
            f.writelines('\n')


if __name__ == '__main__':
    # That script was made for:
    # extracting the client/therapist identifiers from the transcriptions json.
    # Then is they were added MANUALLY to the ALL_STOP.txt.
    # dropping the identifiers only from the 'extractTrans' script is not enough because at the HE parsing time,
    # the morphological parts as 'מ', 'ל', ה', ... are dropped and what remains is not identifier any more.
    main ()
