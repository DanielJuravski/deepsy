import os
import json
from collections import defaultdict
import collections
import csv
import operator


# Datasets location
HE_FACEBOOK_DATASET = "../Reut/data/token_train.tsv"
PSY_DATASET = "/home/daniel/Documents/parsed_trans_reut_v2/"
FILTER_BY = "word"

# Transcription json file
PLAIN_TEXT_PARSED_WORD = 'plainText_parsed_word'
PLAIN_TEXT_PARSED_LEMMA = 'plainText_parsed_lemma'
STR_DIALOG_TURNS_LIST = 'dialog_turns_list'
STR_MINI_DIALOG_TURN_LIST = 'mini_dialog_turn_list'
STR_PLAIN_TEXT = 'plainText'
STR_SPEAKER = 'speaker'
STR_CLIENT = 'Client'


def loadPData():
    tokens = defaultdict(int)
    directory = os.fsencode(PSY_DATASET)
    psy_file_i = 1
    num_mini_turns = 0
    for file in os.listdir(directory):
        file_name = os.fsdecode(file)
        json_src_file_name = PSY_DATASET + file_name
        print('iterating on file {0}/{1}'.format(psy_file_i, len(os.listdir(directory))))

        with open(json_src_file_name) as f:
            src_json_data = json.load(f)
            tokens, num_mini_turns_i = extract(src_json_data, tokens)

        psy_file_i += 1
        num_mini_turns += num_mini_turns_i

    print("Num of mini turns: {0}".format(num_mini_turns))

    return tokens


def extract(src_json_data, tokens):
    dialog_turns_list = src_json_data[STR_DIALOG_TURNS_LIST]
    dialog_turns_list_len = len(dialog_turns_list)
    num_mini_turns = 0
    for dialog_turn_i in range(dialog_turns_list_len):
        dialog_turn = dialog_turns_list[dialog_turn_i]
        mini_dialog_turn_list = dialog_turn[STR_MINI_DIALOG_TURN_LIST]
        mini_dialog_turn_list_len = len(mini_dialog_turn_list)
        for mini_dialog_turn_i in range(mini_dialog_turn_list_len):
            num_mini_turns += 1
            mini_dialog_turn = mini_dialog_turn_list[mini_dialog_turn_i]
            if FILTER_BY == 'word':
                plain_text = mini_dialog_turn[PLAIN_TEXT_PARSED_WORD]
            elif FILTER_BY == 'lemma':
                plain_text = mini_dialog_turn[PLAIN_TEXT_PARSED_LEMMA]
            words = plain_text.split()
            for word in words:
                tokens[word] += 1

    return tokens, num_mini_turns


def loadFData():
    tokens = defaultdict(int)
    with open(HE_FACEBOOK_DATASET, 'r') as f:
        lines = csv.reader(f, delimiter="\t")
        for line in lines:
            sentence = line[0].split()
            for word in sentence:
                tokens[word] += 1

    return tokens


def loadData():
    # make 2 dicts with tokens
    p_data = loadPData()
    f_data = loadFData()

    return p_data, f_data


def compare(p_tokens, f_tokens):
    OOF = defaultdict(int)
    for p_token in p_tokens:
        if p_token not in f_tokens:
            OOF[p_token] = p_tokens[p_token]

    sorted_OOF = sorted(OOF.items(), key=operator.itemgetter(1), reverse=True)
    sorted_OOF = collections.OrderedDict(sorted_OOF)

    return sorted_OOF


def printStat(p_tokens, f_tokens, oof):
    num_p_tokens = float(len(p_tokens))
    sum_p_appearances = float(sum(p_tokens.values()))
    num_f_tokens = float(len(oof))
    sum_f_appearances = float(sum(oof.values()))
    print("Original num of psy tokens: {0}".format(num_p_tokens))
    print("Original num of psy tokens' appearances: {0}".format(sum_p_appearances))
    print("Num of un-founded facebook tokens: {0}".format(num_f_tokens))
    print("Num of un-founded facebook tokens' appearances: {0}".format(sum_f_appearances))
    tokens_prop = round(num_f_tokens/num_p_tokens * 100, 2)
    appearances_prop = round(sum_f_appearances/sum_p_appearances * 100, 2)
    print("Unfounded tokens: {0}%".format(tokens_prop))
    print("Unfounded appearances: {0}%".format(appearances_prop))
    print("tokens details in where_tokens.txt")

    with open('OutputTXT/where_tokens.txt', 'w') as f:
        for key, val in oof.items():
            f.write("token not founded: {0} number of appearances: {1}\n".format(key, val))


if __name__ == '__main__':
    """
    run over all the tokens in the 873 sessions (p_data),
    check the number of tokens that exist/non exist in the HE Facebook dataset (f_data)
    """
    p_tokens, f_tokens = loadData()
    oof = compare(p_tokens, f_tokens)
    printStat(p_tokens, f_tokens, oof)


    pass