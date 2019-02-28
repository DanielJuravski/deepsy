import json
import sys
import logging


# logger
LOG_LEVEL = 20  # INFO
LOG_FILE = 'myapp.log'

# transcription json file
STR_DIALOG_TURNS_LIST = 'dialog_turns_list'
STR_MINI_DIALOG_TURN_LIST = 'mini_dialog_turn_list'
STR_PLAIN_TEXT = 'plainText'

# extracting plain text
PLAIN_TEXT_FILE_PATH = '/tmp/plainText.txt'
PLAIN_TEXT_DETAILS_FILE_PATH = '/tmp/plainTextOrder.txt'



def usage():
    print("USAGE")


def initFiles():
    logging.FileHandler(filename=LOG_FILE, mode='w')
    f_plain_text = open(PLAIN_TEXT_FILE_PATH, 'w')
    f_plain_text_details = open(PLAIN_TEXT_DETAILS_FILE_PATH, 'w')

    return f_plain_text, f_plain_text_details


def initLogger():
    logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL)
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler(LOG_FILE)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)


def cleanWS(f_plain_text, f_plain_text_details):
    f_plain_text.close()
    f_plain_text_details.close()


def processText(plain_text):
    return plain_text


def write2files(dialog_turn_i, mini_dialog_turn_i, processed_plain_text, f_plain_text, f_plain_text_details):
    f_plain_text.write(processed_plain_text + '\n')
    details = "{0}:{1} {2}:{3}".format(STR_DIALOG_TURNS_LIST, dialog_turn_i, STR_MINI_DIALOG_TURN_LIST, mini_dialog_turn_i)
    f_plain_text_details.write(details + '\n')


def extractPlainTextDetails(src_json_data, f_plain_text, f_plain_text_details):
    '''
    extracting every plainText attr. (with its json location details) to appropriate files
    :param src_json_data:
    :param f_plain_text:
    :param f_plain_text_details:
    :return: NONE
    '''
    dialog_turns_list = src_json_data[STR_DIALOG_TURNS_LIST]
    dialog_turns_list_len = len(dialog_turns_list)
    for dialog_turn_i in range(dialog_turns_list_len):
        logging.info("Processing {0}/{1}".format(dialog_turn_i, dialog_turns_list_len-1))
        dialog_turn = dialog_turns_list[dialog_turn_i]
        mini_dialog_turn_list = dialog_turn[STR_MINI_DIALOG_TURN_LIST]
        mini_dialog_turn_list_len = len(mini_dialog_turn_list)
        for mini_dialog_turn_i in range(mini_dialog_turn_list_len):
            mini_dialog_turn = mini_dialog_turn_list[mini_dialog_turn_i]
            plain_text = mini_dialog_turn[STR_PLAIN_TEXT]
            processed_plain_text = processText(plain_text)
            write2files(dialog_turn_i, mini_dialog_turn_i, processed_plain_text, f_plain_text, f_plain_text_details)
    logging.info("All dialogs extracted")


if __name__ == '__main__':
    ##############################################################################
    # That script extracts:                                                      #
    # plain texts to PLAIN_TEXT_FILE_PATH and                                    #
    # plain texts details to PLAIN_TEXT_DETAILS_FILE_PATH                        #
    # each on those files are built of one plain text (and one details) per line #
    # line number of plain text is represented by line number of details         #
    ##############################################################################

    f_plain_text, f_plain_text_details = initFiles()
    initLogger()

    if len(sys.argv) > 1:
        json_src_file_name = sys.argv[1]
    else:
        json_src_file_name = 'trans_sample.json'

    with open(json_src_file_name) as f:
        src_json_data = json.load(f)
        logging.info('Source json file was loaded')

    extractPlainTextDetails(src_json_data, f_plain_text, f_plain_text_details)


    cleanWS(f_plain_text, f_plain_text_details)