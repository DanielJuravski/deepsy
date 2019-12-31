import yaml
import matplotlib.pyplot as plt

LABELS_DIR = "/home/daniel/deepsy/SBS_Analize/Trans2Label/Vanilla/ORS"  # change
INPUT_LABELS_FILE = LABELS_DIR + '/trans_ors.yml'  # change

LABEL_NAME = 'ors_sum'  # change


def loadLabelsFile():
    with open(INPUT_LABELS_FILE, 'r') as stream:
        try:
            labelsDict = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return labelsDict


def processLabels(labelsDict):
    label_values = []
    for item in labelsDict:
        val = labelsDict[item][LABEL_NAME]
        if val is not None and val != -1:
            label_values.append(val)

    return label_values


def makeGraph(label_values):
    print("Plotting ...")
    title = INPUT_LABELS_FILE.split('/')[-1] + ':' + LABEL_NAME

    N, bins, patches = plt.hist(label_values, bins=40)

    plt.ylabel('Count')
    plt.xlabel('ORS Value')
    # plt.title(title)
    plt.grid()

    for i in range(0, 24):
        patches[i].set_facecolor('r')
    for i in range(24, len(patches)):
        patches[i].set_facecolor('b')

    plt.savefig('ors_vanilla.png')
    # plt.show()


if __name__ == '__main__':
    """
    No output of -1 label
    bins=40

    """
    label_dict = loadLabelsFile()
    label_values = processLabels(label_dict)
    makeGraph(label_values)
