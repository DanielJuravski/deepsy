import yaml
import os

INPUT_LABELS_FILE = '/home/daniel/deepsy/SBS_Analize/Trans2Label/Vanilla/Rupture/trans_rupture.yml'
LABEL_NAME = 't_a_rupture1'
OUTPUT_DIR_NAME = 'trans_rupture_01'
# Discrete values mapping, SRC_val:TARGET_val.
LABEL_MANIPULATION = {
    1:0,
    4:1,
    5:1
}


def loadVanillaLabels():
    with open(INPUT_LABELS_FILE, 'r') as stream:
        try:
            vanilla_labels = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return vanilla_labels


def manipulateLabels(labels):
    for item in labels:
        # get old val
        old_val = labels[item][LABEL_NAME]
        if old_val in LABEL_MANIPULATION:
            new_val = LABEL_MANIPULATION[old_val]
        else:
            new_val = -1

        # set new val
        labels[item][LABEL_NAME] = new_val

    return labels


def writeFile(manipulated_values):
    if not os.path.exists(OUTPUT_DIR_NAME):
        os.makedirs(OUTPUT_DIR_NAME)
    else:
        raise exit("Dir already exist. Change Dir name.")

    # drop values yml
    out_name = OUTPUT_DIR_NAME + '/' + INPUT_LABELS_FILE.split('/')[-1]
    with open(out_name, 'w') as f:
        yaml.dump(manipulated_values, f, default_flow_style=False, allow_unicode=True)

    # drop info file
    out_name = OUTPUT_DIR_NAME + '/' + "info.txt"
    with open(out_name, 'w') as f:
        f.writelines("INPUT_LABELS_FILE = {0}\n"
                     "LABEL_NAME = {1}\n"
                     "LABEL_MANIPULATION = {2}".format(INPUT_LABELS_FILE, LABEL_NAME, LABEL_MANIPULATION))


if __name__ == '__main__':
    vanilla_labels = loadVanillaLabels()
    manipulated_values = manipulateLabels(vanilla_labels)
    writeFile(manipulated_values)

    pass


