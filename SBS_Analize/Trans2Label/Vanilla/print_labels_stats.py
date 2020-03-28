import yaml
import numpy as np

INPUT_LABELS_FILE = '/home/daniel/deepsy/SBS_Analize/Trans2Label/Vanilla/Rupture/trans_rupture.yml'
LABEL_NAME = 't_a_rupture1'


def loadLabelsFile():
    with open(INPUT_LABELS_FILE, 'r') as stream:
        try:
            labelsDict = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return labelsDict


def get_labels(data):
    labels = list()
    for sample in data:
        l = data[sample][LABEL_NAME]
        if l is not None:
            labels.append(float(l))

    return labels


if __name__ == '__main__':
    d = loadLabelsFile()
    d_lables = get_labels(d)  # list of labels values
    print("mean of labels: {0}".format(np.nanmean(np.asarray(d_lables))))
    print("sd of labels: {0}".format(np.nanstd(np.asarray(d_lables))))


    pass