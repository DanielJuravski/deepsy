import numpy as np
np.random.seed(seed=1)
import yaml
from sklearn.utils import shuffle
import datetime
import json

from lib import smlr

### Data file params ###
INPUT_LABEL_YML = '/home/daniel/deepsy/SBS_Analize/Trans2Label/ProcessLabels/trans_poms_12/trans_poms.yml'
LABEL = "c_a_poms_positive"
INPUT_DIST_FILE = '/home/daniel/deepsy/TM/Dirs_of_Docs/c_sessions/results/inferencer_200-c_1turns_words_mini_small.txt'
### Data file params ###

### Model params ###
TRAIN_TEST_RATIO = 0.85  # this value ratio from the data will be train, the rest will be test.
### Model params ###

RESULTS_DIR = "/home/daniel/deepsy/Supervised/Topics2Labels/cand_results/"


def loadDists():
    nameDist = {}
    with open(INPUT_DIST_FILE, 'r') as f:
        for line in f:
            # handle comment lines
            if line[0] == '#':
                continue
            line_details = line.split()
            name = line_details[1].split('/')[-1].split('.docx.json.parsed')[0]
            dists = [float(i) for i in (line_details[2:])]
            nameDist[name] = dists

    return nameDist


def loadData():
    # load dists
    nameDist = loadDists()

    # load labels
    with open(INPUT_LABEL_YML, 'r') as stream:
        try:
            labels_data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # extract names and labels
    x = []
    y = []
    for item in labels_data:
        y_cand = labels_data[item][LABEL]
        # check if valid label
        if y_cand != -1:
            x_dist = nameDist[item]
            x.append(x_dist)
            y.append(y_cand)

    # list -> np array
    x = np.array(x)
    y = np.array(y)

    return x, y


def lenSafetyCompare(x_data_len, y_data_len):
    if x_data_len != y_data_len:
        raise exit("Data X's and Y's are not the same length.")

    return x_data_len


def splitData(x_data, y_data):
    x_data_len = len(x_data)
    y_data_len = len(y_data)
    # be sure it is the same length
    data_len = lenSafetyCompare(x_data_len, y_data_len)

    # shuffle
    x_data, y_data = shuffle(x_data, y_data)

    x_train_len = round(data_len * TRAIN_TEST_RATIO)
    x_test_len = data_len - x_train_len

    x_train = x_data[:x_train_len]
    y_train = y_data[:x_train_len]

    x_test = x_data[x_train_len:]
    y_test = y_data[x_train_len:]

    return x_train, y_train, x_test, y_test


def analyseYs(y_gold, y_cand, data_type):
    lenSafetyCompare(len(y_gold), len(y_cand))

    msg = "\n{0} results:\n".format(data_type)
    np.set_printoptions(linewidth=np.inf)
    msg += "gold:\t{0}\n".format(y_gold)
    msg += "hat:\t{0}\n".format(y_cand)

    correct = wrong = 0
    for (y, y_hat) in zip(y_gold, y_cand):
        if y == y_hat:
            correct += 1
        else:
            wrong += 1
    acc = round((correct/(correct+wrong)*100), 2)
    msg += "Correct: {0}/{3} | Wrong: {1}/{3} | Acc: {2}%\n".format(correct, wrong, acc, correct+wrong)
    print(msg)

    return msg


def getEffectiveFeat(model, c, f_num):
    """
    getting
    :param model:
    :param c: observe features of class c
           f_num: number of top and low features to get
    :return:
    """
    eff_pos = {}
    eff_neg = {}
    w = model.coef_[c, :]
    w_sorted = np.sort(w)
    most_effective = np.argsort(w)
    init_feat_size = len(w_sorted)

    # get bottom f_num features, start->middle
    for feat_i in range(f_num):
        eff_neg[most_effective[feat_i]] = w_sorted[feat_i]
    # get top f_num features, middle->end
    for feat_i in range(f_num):
        eff_pos[most_effective[init_feat_size-feat_i-1]] = w_sorted[init_feat_size-feat_i-1]

    # print("All weights: {0}".format(w))
    # print("All weights sorted: {0}".format(w_sorted))
    # print("Most effective topics: {0}".format(most_effective))
    msg = "Most positive effective: {0}\n" \
          "Most negative effective: {1}".format(eff_pos, eff_neg)

    print(msg)

    return eff_pos, eff_neg, msg


def printFile(out_msg_train, out_msg_test, effective_feat_msg, time_msg):
    time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
    file_name = RESULTS_DIR + time + '.txt'

    with open(file_name, 'w') as f:
        f.writelines("INPUT_LABEL_YML: {}\n".format(INPUT_LABEL_YML))
        f.writelines("LABEL: {}\n".format(LABEL))
        f.writelines("INPUT_DIST_FILE: {}\n".format(INPUT_DIST_FILE))
        f.writelines("TRAIN_TEST_RATIO: {}\n".format(TRAIN_TEST_RATIO))
        f.writelines(out_msg_train)
        f.writelines(out_msg_test + '\n')
        f.writelines(effective_feat_msg + '\n')
        f.writelines(time_msg)


if __name__ == '__main__':
    st = datetime.datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
    x_data, y_data = loadData()
    x_train, y_train, x_test, y_test = splitData(x_data, y_data)

    model = smlr.SMLR(max_iter=1000, tol=1e-4, verbose=1)
    model = model.fit(x_train, y_train)
    eff_pos, eff_neg, effective_feat_msg = getEffectiveFeat(model, c=0, f_num=10)

    y_hat_train = model.predict(x_train)
    out_msg_train = analyseYs(y_train, y_hat_train, data_type='Train')

    y_hat_test = model.predict(x_test)
    out_msg_test = analyseYs(y_test, y_hat_test, data_type='Test')

    et = datetime.datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
    time_msg = "\nStart time: {0}\n" \
          "End time: {1}".format(st, et)
    print(time_msg)

    printFile(out_msg_train, out_msg_test, effective_feat_msg, time_msg)

