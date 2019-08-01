import sys
import os
from datetime import datetime


########################## Params - Start ##########################
TRANS_JSON_DIR = '/home/daniel/Documents/parsed_trans_reut_v2/'
TRANS_DOCUMENTS_DIR = '/home/daniel/deepsy/TM/client_5_mini_turns/'
FILTER_BY = 'word'
WORD_FREQ_THRESHOLD = 9
COMMON_WORD_FREQ_THRESHOLD = 0.9
########################## Params - End   ##########################


def getOptions():
    if '--input-dir-json' in sys.argv:
        option_i = sys.argv.index('--input-dir-json')
        trans_dir_jsons = sys.argv[option_i + 1]
    else:
        trans_dir_jsons = TRANS_JSON_DIR

    if '--input-dir-docs' in sys.argv:
        option_i = sys.argv.index('--input-dir-docs')
        trans_dir_docs = sys.argv[option_i + 1]
    else:
        trans_dir_docs = TRANS_DOCUMENTS_DIR

    if '--filter-by' in sys.argv:
        option_i = sys.argv.index('--filter-by')
        filter_by = sys.argv[option_i + 1]
    else:
        filter_by = FILTER_BY

    if '--threshold' in sys.argv:
        option_i = sys.argv.index('--threshold')
        word_freq_threshold = int(sys.argv[option_i + 1])
    else:
        word_freq_threshold = WORD_FREQ_THRESHOLD

    if '--threshold-common' in sys.argv:
        option_i = sys.argv.index('--threshold-common')
        common_threshold = float(sys.argv[option_i + 1])
    else:
        common_threshold = COMMON_WORD_FREQ_THRESHOLD

    return trans_dir_jsons, trans_dir_docs, filter_by, word_freq_threshold, common_threshold


def runScripts(trans_dir_jsons, trans_dir_docs, filter_by, word_freq_threshold, common_threshold):
    # first check if there is not any .txt files in the current directory
    # run all stop words script and plot the .txt output to the current directory
    checkOnlyTxtFiles()

    os.system('python3 stopWords.py --input-dir {0} --filter-by {1}'.format(trans_dir_jsons, filter_by))
    os.system('python3 rareWords.py --input-dir {0} --filter-by {1} --threshold {2}'.format(trans_dir_jsons, filter_by, word_freq_threshold))
    os.system('python3 commonWords.py --input-dir {0} --threshold {1}'.format(trans_dir_docs, common_threshold))


def checkOnlyTxtFiles():
    f = os.listdir(path='.')
    if len(f) > 0:
        for i in os.listdir(path='.'):
            if i.endswith('.txt'):
                raise Exception('.txt files shouldn\'t be here')


def uniteTxts(directory, stop_file):
    # merge & mv *.txt all_stop_words_dir
    os.system('cat *.txt > {0}'.format(stop_file))
    os.system('mv *.txt {0}'. format(directory))

    # remove duplication of words
    #os.system('awk \'!a[$0]++\' {0}'.format(stop_file))


def generateOutputFiles():
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    directory = 'STOP_WORDS_DIRS/' + str(timestamp)

    if not os.path.exists(directory):
        os.makedirs(directory)

    info_file = directory + '/info.txt'
    stop_file = directory + '/ALL_STOP.txt'

    return info_file, stop_file, directory


def writeInfo(info_file, TRANS_JSON_DIR, TRANS_DOCUMENTS_DIR, FILTER_BY, WORD_FREQ_THRESHOLD, COMMON_WORD_FREQ_THRESHOLD):
    with open(info_file, 'w') as f:
        f.writelines('TRANS_JSON_DIR = {}'.format(TRANS_JSON_DIR))
        f.writelines('\nTRANS_DOCUMENTS_DIR = {}'.format(TRANS_DOCUMENTS_DIR))
        f.writelines('\nFILTER_BY = {}'.format(FILTER_BY))
        f.writelines('\nWORD_FREQ_THRESHOLD = {}'.format(WORD_FREQ_THRESHOLD))
        f.writelines('\nCOMMON_WORD_FREQ_THRESHOLD = {}'.format(COMMON_WORD_FREQ_THRESHOLD))



if __name__ == '__main__':
    info_file, stop_file, directory = generateOutputFiles()
    writeInfo(info_file, TRANS_JSON_DIR, TRANS_DOCUMENTS_DIR, FILTER_BY, WORD_FREQ_THRESHOLD, COMMON_WORD_FREQ_THRESHOLD)
    trans_dir_jsons, trans_dir_docs, filter_by, word_freq_threshold, common_threshold = getOptions()
    runScripts(trans_dir_jsons, trans_dir_docs, filter_by, word_freq_threshold, common_threshold)
    uniteTxts(directory, stop_file)
