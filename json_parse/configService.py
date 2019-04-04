import json
import sys
import logging
import re
import string

from loggerService import initLogger
from loggerService import LOG_FILE


# Transcription json file
STR_DIALOG_TURNS_LIST = 'dialog_turns_list'
STR_MINI_DIALOG_TURN_LIST = 'mini_dialog_turn_list'
STR_PLAIN_TEXT = 'plainText'

# Extracting plain text
PLAIN_TEXT_FILE_PATH = '/tmp/plainText.txt'
PLAIN_TEXT_DETAILS_FILE_PATH = '/tmp/plainTextDetails.txt'
PLAIN_TEXT_PARSED_FILE_PATH = '/tmp/plainTextParsed.txt'
PLAIN_TEXT_WORD_SPLITED_FILE_PATH = '/tmp/plainTextWordSplited.txt'

# Json
PLAIN_TEXT_PARSED_WORD = 'plainText_parsed_word'
PLAIN_TEXT_PARSED_LEMMA = 'plainText_parsed_lemma'
PLAIN_TEXT_PARSED_POS = 'plainText_parsed_pos'
PLAIN_TEXT_PARSED_MORPH = 'plainText_parsed_morphological'

# Conll
WORD_i = 1
LEMMA_i = 2
POS_i = 3
MORPHOLOGICAL_i = 5
