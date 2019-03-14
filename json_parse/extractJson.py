from configService import *

def usage():
    print("USAGE")


def initFiles():
    f_plain_text = open(PLAIN_TEXT_FILE_PATH, 'w')
    f_plain_text_details = open(PLAIN_TEXT_DETAILS_FILE_PATH, 'w')
    f_plain_text_word_splited = open(PLAIN_TEXT_WORD_SPLITED_FILE_PATH, 'w')

    return f_plain_text, f_plain_text_details, f_plain_text_word_splited


def cleanWS(f_plain_text, f_plain_text_details, f_plain_text_word_splited):
    f_plain_text.close()
    f_plain_text_details.close()
    f_plain_text_word_splited.close()


def processText(plain_text):
    return plain_text


def removePunc(item):
    # that method removes punctuation (partially) from the end of each word, for Reut's parser
    # extracting long punc (...) need to be before short punc (.)
    # insure that there is a word near that punc (not just punc with spaces). do this to avoid spliting single punc to 2 items.
    no_punc_word_list = []

    # remove '...'
    if (item[-3:] == '...') and len(item)>3:
        word = item[:-3]
        punc = item[-3:]
        no_punc_word_list.append(word)
        no_punc_word_list.append(punc)

    # remove '..'
    elif (item[-2:] == '..') and len(item)>2:
        word = item[:-2]
        punc = item[-2:]
        no_punc_word_list.append(word)
        no_punc_word_list.append(punc)

    # remove .,?!
    elif (item[-1] == '.' or item[-1] == ',' or item[-1] == '?' or item[-1] == '!') and len(item)>1:
        word = item[:-1]
        punc = item[-1]
        no_punc_word_list.append(word)
        no_punc_word_list.append(punc)

    else:
        no_punc_word_list.append(item)

    return no_punc_word_list


def write2files(dialog_turn_i, mini_dialog_turn_i, processed_plain_text, f_plain_text, f_plain_text_details, f_plain_text_word_splited):
    # write plain text
    f_plain_text.write(processed_plain_text + '\n')

    # write plain text details
    details = "{0}:{1} {2}:{3}".format(STR_DIALOG_TURNS_LIST, dialog_turn_i, STR_MINI_DIALOG_TURN_LIST, mini_dialog_turn_i)
    f_plain_text_details.write(details + '\n')

    # write plain text splited
    processed_plain_text_list = processed_plain_text.split()
    for word in processed_plain_text_list:
        no_punc_word_list = removePunc(word)
        for processed_word in no_punc_word_list:
            f_plain_text_word_splited.write("%s\n" % processed_word)
    f_plain_text_word_splited.write('\n')


def extractPlainTextDetails(src_json_data, f_plain_text, f_plain_text_details, f_plain_text_word_splited):
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
        logging.debug("Processing {0}/{1}".format(dialog_turn_i, dialog_turns_list_len-1))
        dialog_turn = dialog_turns_list[dialog_turn_i]
        mini_dialog_turn_list = dialog_turn[STR_MINI_DIALOG_TURN_LIST]
        mini_dialog_turn_list_len = len(mini_dialog_turn_list)
        for mini_dialog_turn_i in range(mini_dialog_turn_list_len):
            mini_dialog_turn = mini_dialog_turn_list[mini_dialog_turn_i]
            plain_text = mini_dialog_turn[STR_PLAIN_TEXT]
            processed_plain_text = processText(plain_text)
            write2files(dialog_turn_i, mini_dialog_turn_i, processed_plain_text, f_plain_text, f_plain_text_details, f_plain_text_word_splited)
    logging.info("All dialogs extracted")


if __name__ == '__main__':
    ##############################################################################
    # That script extracts:                                                      #
    # plain texts to PLAIN_TEXT_FILE_PATH and                                    #
    # plain texts details to PLAIN_TEXT_DETAILS_FILE_PATH                        #
    # plain texts (each word on a new line) to PLAIN_TEXT_WORD_SPLITED_FILE_PATH #
    # each on those files are built of one plain text (and one details) per line #
    # line number of plain text is represented by line number of details         #
    ##############################################################################

    f_plain_text, f_plain_text_details, f_plain_text_word_splited = initFiles()
    initLogger()

    if len(sys.argv) > 1:
        json_src_file_name = sys.argv[1]
    else:
        json_src_file_name = 'json_parse/trans_sample.json'

    with open(json_src_file_name) as f:
        src_json_data = json.load(f)
        logging.info('Source json file was loaded')

    extractPlainTextDetails(src_json_data, f_plain_text, f_plain_text_details, f_plain_text_word_splited)

    cleanWS(f_plain_text, f_plain_text_details, f_plain_text_word_splited)
