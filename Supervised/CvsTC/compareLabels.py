import yaml

C_LABELS_FILE = '/home/daniel/deepsy/SBS_Analize/Trans2Label/ProcessLabels/trans_poms_08/trans_poms.yml'
TC_LABELS_FILE = '/home/daniel/deepsy/SBS_Analize/Trans2Label/ProcessLabels/trans_poms_14/trans_poms.yml'
C_LABEL = 'c_a_poms_positive'
TC_LABEL = 'tc_a_poms_positive'


def loadFiles():
    with open(C_LABELS_FILE, 'r') as stream:
        try:
            c_labels = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    with open(TC_LABELS_FILE, 'r') as stream:
        try:
            tc_labels = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return c_labels, tc_labels


def compare(c_labels, tc_labels):
    correct = wrong = 0
    for c_item in c_labels:
        c_value = c_labels[c_item][C_LABEL]
        tc_value = tc_labels[c_item][TC_LABEL]
        if c_value == -1:
            continue
        if c_value == tc_value:
            correct += 1
        else:
            wrong += 1

    return correct, wrong


def printResult(correct, wrong):
    total = correct + wrong
    acc = round((correct / total * 100), 2)
    print("Correct: {0}/{2} | Wrong:{1}/{2} | Acc: {3}%".format(correct, wrong, total, acc))


if __name__ == '__main__':
    c_labels, tc_labels = loadFiles()
    correct, wrong = compare(c_labels, tc_labels)
    printResult(correct, wrong)
