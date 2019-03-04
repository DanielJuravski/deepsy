from configService import *


def initFiles():
    f_plain_text_parsed = open(PLAIN_TEXT_PARSED_FILE_PATH, 'r')
    f_plain_text_details = open(PLAIN_TEXT_DETAILS_FILE_PATH, 'r')
    logging.info('plain text parsed and details were loaded')
    return f_plain_text_parsed, f_plain_text_details


def addAttr2Json(src_json_data, all_word_sen, all_lemma_sen, all_pos_sen, f_plain_text_details):
    # set seek 0 because file was iterated already
    f_plain_text_details.seek(0)

    for word_sen, lemma_sen, pos_sen, details in zip(all_word_sen, all_lemma_sen, all_pos_sen, f_plain_text_details):
        details = details.split()
        dialog_turn_list_i = int(re.split(STR_DIALOG_TURNS_LIST+':', details[0])[1])
        mini_dialog_turn_list_i = int(re.split(STR_MINI_DIALOG_TURN_LIST+':', details[1])[1])

        src_json_data[STR_DIALOG_TURNS_LIST][dialog_turn_list_i] \
            [STR_MINI_DIALOG_TURN_LIST][mini_dialog_turn_list_i] \
            [PLAIN_TEXT_PARSED_WORD] = word_sen

        src_json_data[STR_DIALOG_TURNS_LIST][dialog_turn_list_i] \
            [STR_MINI_DIALOG_TURN_LIST][mini_dialog_turn_list_i] \
            [PLAIN_TEXT_PARSED_LEMMA] = lemma_sen

        src_json_data[STR_DIALOG_TURNS_LIST][dialog_turn_list_i] \
            [STR_MINI_DIALOG_TURN_LIST][mini_dialog_turn_list_i] \
            [PLAIN_TEXT_PARSED_POS] = pos_sen

    logging.info('New attributes were added to data')

    return src_json_data


def processPlainTextParsed(f_plain_text_parsed):
    '''
    get Word, Lemma and POS of the sentences
    :param f_plain_text_parsed:
    :return:
    '''
    all_word_sen = []
    all_lemma_sen = []
    all_pos_sen = []
    word_sen = []
    lemma_sen = []
    pos_sen = []

    for line in f_plain_text_parsed:
        s_line = line.split()
        # if not empty line
        if s_line:
            word = s_line[WORD_i]
            lemma = s_line[LEMMA_i]
            pos = s_line[POS_i]

            word_sen.append(word)
            lemma_sen.append(lemma)
            pos_sen.append(pos)
        else:
            # convert from list to str with join
            all_word_sen.append(' '.join(word_sen))
            all_lemma_sen.append(' '.join(lemma_sen))
            all_pos_sen.append(' '.join(pos_sen))
            word_sen = []
            lemma_sen = []
            pos_sen = []

    logging.info('New attributes were precessed')

    return all_word_sen, all_lemma_sen, all_pos_sen


def verifyLength(all_word_sen, all_lemma_sen, all_pos_sen, f_plain_text_details):
    f_plain_text_details_len = sum(1 for line in f_plain_text_details)

    all_word_sen_len = len(all_word_sen)
    all_lemma_sen_len = len(all_lemma_sen)
    all_pos_sen_len = len(all_pos_sen)

    if all_word_sen_len != f_plain_text_details_len:
        raise Exception('Word parsed lines and Details files are not equal !')

    if all_lemma_sen_len != f_plain_text_details_len:
        raise Exception('Lemma parsed lines and Details files are not equal !')

    if all_pos_sen_len != f_plain_text_details_len:
        raise Exception('POS parsed lines and Details files are not equal !')


def writeJson2File(target_json_data, json_target_file_name):
    with open(json_target_file_name, 'w') as outfile:
        json.dump(target_json_data, outfile, ensure_ascii=False)

    logging.info('Target json file was created')


def cleanWS(f_plain_text_parsed, f_plain_text_details):
    f_plain_text_parsed.close()
    f_plain_text_details.close()


if __name__ == '__main__':
    ##############################################################################
    # input: src_json, parsed_textPlain, details_file                            #
    # output: target_json that contains the src data plus:                       #
    #  - parsing by word                                                         #
    #  - parsing by lemma                                                        #
    #  - parsing by pos                                                          #
    ##############################################################################

    initLogger()

    if len(sys.argv) > 2:
        json_src_file_name = sys.argv[1]
        json_target_file_name = sys.argv[2]
    else:
        json_src_file_name = 'json_parse/trans_sample.json'
        json_target_file_name = 'json_parse/trans_parsed_sample.json'

    f_plain_text_parsed, f_plain_text_details = initFiles()

    all_word_sen, all_lemma_sen, all_pos_sen = processPlainTextParsed(f_plain_text_parsed)
    verifyLength(all_word_sen, all_lemma_sen, all_pos_sen, f_plain_text_details)

    with open(json_src_file_name) as f:
        src_json_data = json.load(f)
        logging.info('Source json file was loaded')

    target_json_data = addAttr2Json(src_json_data, all_word_sen, all_lemma_sen, all_pos_sen, f_plain_text_details)

    writeJson2File(target_json_data, json_target_file_name)

    cleanWS(f_plain_text_parsed, f_plain_text_details)

