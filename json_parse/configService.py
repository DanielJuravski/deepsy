import json
import sys
import logging
import re

from json_parse.loggerService import initLogger
from json_parse.loggerService import LOG_FILE


# Transcription json file
STR_DIALOG_TURNS_LIST = 'dialog_turns_list'
STR_MINI_DIALOG_TURN_LIST = 'mini_dialog_turn_list'
STR_PLAIN_TEXT = 'plainText'

# Extracting plain text
PLAIN_TEXT_FILE_PATH = '/tmp/plainText.txt'
PLAIN_TEXT_DETAILS_FILE_PATH = '/tmp/plainTextOrder.txt'
PLAIN_TEXT_PARSED_FILE_PATH = '/tmp/plainTextParsed.txt'

# Json
PLAIN_TEXT_PARSED_WORD = 'plainText_parsed_word'
PLAIN_TEXT_PARSED_LEMMA = 'plainText_parsed_lemma'
PLAIN_TEXT_PARSED_POS = 'plainText_parsed_pos'

# Conll
WORD_i = 1
LEMMA_i = 2
POS_i = 3
