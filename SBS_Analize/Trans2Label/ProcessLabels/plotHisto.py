import yaml
import matplotlib.pyplot as plt

LABELS_DIR = "/home/daniel/deepsy/SBS_Analize/Trans2Label/ProcessLabels/trans_poms_14"  # change
INPUT_LABELS_FILE = LABELS_DIR + '/trans_poms.yml'  # change
LABEL_NAME = 'tc_a_poms_positive'  # change


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
        if val == None:
            val = -1
        label_values.append(val)

    return label_values


def makeGraph(label_values):
    print("Plotting ...")
    title = INPUT_LABELS_FILE.split('/')[-1] + ':' + LABEL_NAME
    save_path = LABELS_DIR + '/' + title + '.png'
    plt.hist(label_values, bins=30)
    plt.ylabel('Count')
    plt.xlabel('Value')
    plt.title(title)
    plt.grid()

    plt.savefig(save_path)
    plt.show()


if __name__ == '__main__':
    label_dict = loadLabelsFile()
    label_values = processLabels(label_dict)
    makeGraph(label_values)
