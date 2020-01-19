import yaml
import os

INPUT_LABELS_FILE = '/home/daniel/deepsy/SBS_Analize/Trans2Label/Vanilla/POMS/trans_poms.yml'  # change
LABEL_NAME = 'tc_a_poms_positive'  # change
OUTPUT_DIR_NAME = 'trans_poms_14'  # change
MANIPULATION_TYPE = 'C'  # (C)ontinuous/(D)iscrete  # change
# Discrete values mapping, SRC_val:TARGET_val.
DISCRETE_LABEL_MANIPULATION = {  # change if D
    1:0,
    2:1,
    3:1,
    4:1,
    5:1
}
CONTINUOUS_LABEL_MANIPULATION = {  # change if C
    'lower_then':3.0,  # will be 0
    'higher_then':3.0  # will be 1
}


def loadVanillaLabels():
    with open(INPUT_LABELS_FILE, 'r') as stream:
        try:
            vanilla_labels = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    return vanilla_labels


def isfloat(value):
    try:
        f_val = float(value)
        return f_val
    except:
        return False


def manipulateLabels(labels):
    for item in labels:
        # get old val
        old_val = labels[item][LABEL_NAME]
        if MANIPULATION_TYPE == 'D':
            if old_val in DISCRETE_LABEL_MANIPULATION:
                new_val = DISCRETE_LABEL_MANIPULATION[old_val]
            else:
                new_val = -1
        elif MANIPULATION_TYPE == 'C':
            if isfloat(old_val):
                if old_val <= CONTINUOUS_LABEL_MANIPULATION['lower_then']:
                    new_val = 0
                elif old_val > CONTINUOUS_LABEL_MANIPULATION['higher_then']:
                    new_val = 1
                else:
                    new_val = -1
            else:
                new_val = -1

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
                     "LABEL_NAME = {1}\n".format(INPUT_LABELS_FILE, LABEL_NAME))
        if MANIPULATION_TYPE == 'C':
            f.writelines("CONTINUOUS_LABEL_MANIPULATION = {0}".format(CONTINUOUS_LABEL_MANIPULATION))
        elif MANIPULATION_TYPE == 'D':
            f.writelines("DISCRETE_LABEL_MANIPULATION = {0}".format(DISCRETE_LABEL_MANIPULATION))


if __name__ == '__main__':
    vanilla_labels = loadVanillaLabels()
    manipulated_values = manipulateLabels(vanilla_labels)
    writeFile(manipulated_values)

    pass


