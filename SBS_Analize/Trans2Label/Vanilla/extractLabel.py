import os
import pandas
import yaml
import re

# STATIC
TRANS_DIR_PATH = '/home/daniel/Documents/parsed_trans_reut_v2'
MAPPING_XLSX_PATH = '/home/daniel/Documents/SBS/Transcriptions_Questionnaire_Mapping.xlsx'

# ORS
MY_TRANS_ORS_XLSX_PATH = '/home/daniel/Documents/SBS/my/trans_ors.csv'
ORS_OUTPUT_FILE_NAME = 'trans_ors.yml'
# HSCL
MY_TRANS_HSCL_XLSX_PATH = '/home/daniel/Documents/SBS/my/trans_hscl.csv'
HSCL_OUTPUT_FILE_NAME = 'trans_hscl.yml'
# RUPTURE
MY_TRANS_RUPTURE_XLSX_PATH = '/home/daniel/Documents/SBS/my/trans_rupture.csv'
RUPTURE_OUTPUT_FILE_NAME = 'trans_rupture.yml'
# POMS
MY_TRANS_POMS_XLSX_PATH = '/home/daniel/Documents/SBS/my/trans_poms.csv'
POMS_OUTPUT_FILE_NAME = 'trans_poms.yml'

LABEL = 'poms'  # ors/hscl/rupture/poms


def getTransNames():
    # Return list of [DATE]_[SESSION_NUMBER][HE_CHAR]
    print('Loading {}'.format(TRANS_DIR_PATH))
    trans_names = []
    file_names = os.listdir(TRANS_DIR_PATH)
    for name in file_names:
        clear_name = name.split('.docx.json.parsed')[0]
        trans_names.append(clear_name)

    return trans_names


def loadXLSXs():
    print('Loading {}'.format(MAPPING_XLSX_PATH))
    mapping_df = pandas.read_excel(MAPPING_XLSX_PATH)
    mapping_format = ['client_name', 'c_id', 'c_init', 't_init']
    mapping_values = mapping_df[mapping_format]

    ### ORS ###
    if LABEL == 'ors':
        print('Loading {}'.format(MY_TRANS_ORS_XLSX_PATH))
        df = pandas.read_csv(MY_TRANS_ORS_XLSX_PATH)
        format = ['date', 't_init', 'c_init', 'c_id', 'ors1', 'ors2', 'ors3', 'ors4', 'ors_sum']
        label_values = df[format]

    ### HSCL ###
    elif LABEL == 'hscl':
        print('Loading {}'.format(MY_TRANS_HSCL_XLSX_PATH))
        df = pandas.read_csv(MY_TRANS_HSCL_XLSX_PATH)
        format = ['date', 't_init', 'c_init', 'c_id',
                  'c_b_hscl', 'c_b_hscl1', 'c_b_hscl2', 'c_b_hscl3',
                  'c_b_hscl4', 'c_b_hscl5', 'c_b_hscl6', 'c_b_hscl7',
                  'c_b_hscl8', 'c_b_hscl9', 'c_b_hscl10', 'c_b_hscl11']
        label_values = df[format]

    ### RUPTURE ###
    elif LABEL == 'rupture':
        print('Loading {}'.format(MY_TRANS_RUPTURE_XLSX_PATH))
        df = pandas.read_csv(MY_TRANS_RUPTURE_XLSX_PATH)
        format = ['date', 't_init', 'c_init', 'c_id',
                  'c_a_rupture1', 'c_a_rupture2', 't_a_rupture1', 't_a_rupture2']
        label_values = df[format]

    ### POMS ###
    elif LABEL == 'poms':
        print('Loading {}'.format(MY_TRANS_POMS_XLSX_PATH))
        df = pandas.read_csv(MY_TRANS_POMS_XLSX_PATH)
        format = ['date', 't_init', 'c_init', 'c_id',
                  'c_a_poms_calmness', 'c_a_poms_anger', 'c_a_poms_sad', 'c_a_poms_contentment', 'c_a_poms_anxiety', 'c_a_poms_vigor',
                  't_a_poms_anger', 't_a_poms_sad', 't_a_poms_contentment', 't_a_poms_anxiety', 't_a_poms_vigor',
                  'tc_a_poms_anger', 'tc_a_poms_sad', 'tc_a_poms_contentment', 'tc_a_poms_anxiety', 'tc_a_poms_vigor',
                  'c_a_poms_negative', 'c_a_poms_positive', 'tc_a_poms_negative', 'tc_a_poms_positive']
        label_values = df[format]

    else:
        raise exit("Unsupported label.")

    return mapping_values, label_values


def getCTDetails(mapping_df, he_char):
    c_id = c_init = t_init = None
    for line in mapping_df.values:
        if line[0] == he_char:
            c_id = line[1]
            c_init = line[2].lower()
            t_init = line[3].lower()

    if c_id == None or c_init == None or t_init == None:
        print('he_char:{0} not exist in {1}'.format(he_char, MAPPING_XLSX_PATH))
        print('c_id:{0} c_init:{1} t_init:{2}'.format(c_id, c_init, t_init))
        exit(1)

    return c_id, c_init, t_init


def getORS(ors_df, date, c_id, c_init, t_init):
    ors1 = ors2 = ors3 = ors4 = ors_sum = None
    null = None
    for line in ors_df.values:
        if line[0] == date and line[1] == t_init and line[2] == c_init and line[3] == c_id:
            try:
                ors1 = float(line[4])
            except:
                ors1 = null
            try:
                ors2 = float(line[5])
            except:
                ors2 = null
            try:
                ors3 = float(line[6])
            except:
                ors3 = null
            try:
                ors4 = float(line[7])
            except:
                ors4 = null
            try:
                ors_sum = float(line[8])
            except:
                ors_sum = null

    if ors1 == None or ors2 == None or ors3 == None or ors4 == None or ors_sum == None:
        print('date:{0} c_id:{1} c_init:{2} t_init:{3} not exist in {4}'.format(date, c_id, c_init, t_init, MY_TRANS_ORS_XLSX_PATH))
        print('ors1:{0} ors2:{1} ors3:{2} ors4:{3} ors_sum:{4}'.format(ors1, ors2, ors3, ors4, ors_sum))
        # exit(1)

    return ors1, ors2, ors3, ors4, ors_sum


def getHSCL(hscl_df, date, c_id, c_init, t_init):
    hscl1 = hscl2 = hscl3 = hscl4 = hscl5 = hscl6 = hscl7 = hscl8 = hscl9 = hscl10 = hscl11 = hscl_avg = None
    null = None
    for line in hscl_df.values:
        if line[0] == date and line[1] == t_init and line[2] == c_init and line[3] == c_id:
            try:
                hscl_avg = float(line[4])
            except:
                hscl_avg = null
            try:
                hscl1 = float(line[5])
            except:
                hscl1 = null
            try:
                hscl2 = float(line[6])
            except:
                hscl2 = null
            try:
                hscl3 = float(line[7])
            except:
                hscl3 = null
            try:
                hscl4 = float(line[8])
            except:
                hscl4 = null
            try:
                hscl5 = float(line[9])
            except:
                hscl5 = null
            try:
                hscl6 = float(line[10])
            except:
                hscl6 = null
            try:
                hscl7 = float(line[11])
            except:
                hscl7 = null
            try:
                hscl8 = float(line[12])
            except:
                hscl8 = null
            try:
                hscl9 = float(line[13])
            except:
                hscl9 = null
            try:
                hscl10 = float(line[14])
            except:
                hscl10 = null
            try:
                hscl11 = float(line[15])
            except:
                hscl11 = null

    if hscl1 == None or hscl2 == None or hscl3 == None or hscl4 == None or hscl5 == None or \
        hscl6 == None or hscl7 == None or hscl8 == None or hscl9 == None or hscl10 == None or \
        hscl11 == None or hscl_avg == None:
        print('date:{0} c_id:{1} c_init:{2} t_init:{3} not exist in {4}'.format(date, c_id, c_init, t_init, MY_TRANS_HSCL_XLSX_PATH))
        print('hscl1:{0} hscl2:{1} hscl3:{2} hscl4:{3} hscl5:{4} hscl6:{5} hscl7:{6} hscl8:{7} hscl9:{8} hscl10:{9} hscl11:{10} hscl_avg:{11}'
              .format(hscl1, hscl2, hscl3, hscl4, hscl5, hscl6, hscl7, hscl8, hscl9, hscl10, hscl11, hscl_avg))
        # exit(1)

    return hscl1, hscl2, hscl3, hscl4, hscl5, hscl6, hscl7, hscl8, hscl9, hscl10, hscl11, hscl_avg


def getRUPTURE(rupture_df, date, c_id, c_init, t_init):
    c_a_rupture1 = c_a_rupture2 = t_a_rupture1 = t_a_rupture2 = None
    null = None
    for line in rupture_df.values:
        if line[0] == date and line[1] == t_init and line[2] == c_init and line[3] == c_id:
            try:
                c_a_rupture1 = float(line[4])
            except:
                c_a_rupture1 = null
            try:
                c_a_rupture2 = float(line[5])
            except:
                c_a_rupture2 = null
            try:
                t_a_rupture1 = float(line[6])
            except:
                t_a_rupture1 = null
            try:
                t_a_rupture2 = float(line[7])
            except:
                t_a_rupture2 = null

    if c_a_rupture1 == None or c_a_rupture2 == None or t_a_rupture1 == None or t_a_rupture2 == None:
        print('date:{0} c_id:{1} c_init:{2} t_init:{3} not exist in {4}'.format(date, c_id, c_init, t_init, MY_TRANS_RUPTURE_XLSX_PATH))
        print('c_a_rupture1:{0} c_a_rupture2:{1} t_a_rupture1:{2} t_a_rupture2:{3} '.format(c_a_rupture1, c_a_rupture2, t_a_rupture1, t_a_rupture2))
        # exit(1)

    return c_a_rupture1, c_a_rupture2, t_a_rupture1, t_a_rupture2


def getPOMS(poms_df, date, c_id, c_init, t_init):
    c_a_poms_calmness = c_a_poms_anger = c_a_poms_sad = c_a_poms_contentment = c_a_poms_anxiety = c_a_poms_vigor = \
    t_a_poms_anger = t_a_poms_sad = t_a_poms_contentment = t_a_poms_anxiety = t_a_poms_vigor = \
    tc_a_poms_anger = tc_a_poms_sad = tc_a_poms_contentment = tc_a_poms_anxiety = tc_a_poms_vigor = \
    c_a_poms_negative = c_a_poms_positive = tc_a_poms_negative = tc_a_poms_positive = None
    null = None
    for line in poms_df.values:
        if line[0] == date and line[1] == t_init and line[2] == c_init and line[3] == c_id:
            # c_a
            try:
                c_a_poms_calmness = float(line[4])
            except:
                c_a_poms_calmness = null
            try:
                c_a_poms_anger = float(line[5])
            except:
                c_a_poms_anger = null
            try:
                c_a_poms_sad = float(line[6])
            except:
                c_a_poms_sad = null
            try:
                c_a_poms_contentment = float(line[7])
            except:
                c_a_poms_contentment = null
            try:
                c_a_poms_anxiety = float(line[8])
            except:
                c_a_poms_anxiety = null
            try:
                c_a_poms_vigor = float(line[9])
            except:
                c_a_poms_vigor = null
            # t_a
            try:
                t_a_poms_anger = float(line[10])
            except:
                t_a_poms_anger = null
            try:
                t_a_poms_sad = float(line[11])
            except:
                t_a_poms_sad = null
            try:
                t_a_poms_contentment = float(line[12])
            except:
                t_a_poms_contentment = null
            try:
                t_a_poms_anxiety = float(line[13])
            except:
                t_a_poms_anxiety = null
            try:
                t_a_poms_vigor = float(line[14])
            except:
                t_a_poms_vigor = null
            # tc_a
            try:
                tc_a_poms_anger = float(line[15])
            except:
                tc_a_poms_anger = null
            try:
                tc_a_poms_sad = float(line[16])
            except:
                tc_a_poms_sad = null
            try:
                tc_a_poms_contentment = float(line[17])
            except:
                tc_a_poms_contentment = null
            try:
                tc_a_poms_anxiety = float(line[18])
            except:
                tc_a_poms_anxiety = null
            try:
                tc_a_poms_vigor = float(line[19])
            except:
                tc_a_poms_vigor = null
            try:
                c_a_poms_negative = float(line[20])
            except:
                c_a_poms_negative = null
            try:
                c_a_poms_positive = float(line[21])
            except:
                c_a_poms_positive = null
            try:
                tc_a_poms_negative = float(line[22])
            except:
                tc_a_poms_negative = null
            try:
                tc_a_poms_positive = float(line[23])
            except:
                tc_a_poms_positive = null

    if c_a_poms_calmness == None or c_a_poms_anger == None or c_a_poms_sad == None or c_a_poms_contentment == None or c_a_poms_anxiety == None or \
        c_a_poms_vigor == None or t_a_poms_anger == None or t_a_poms_sad == None or t_a_poms_contentment == None or t_a_poms_anxiety == None or \
        t_a_poms_vigor == None or tc_a_poms_anger == None or tc_a_poms_sad == None or tc_a_poms_contentment == None or tc_a_poms_anxiety == None or \
        tc_a_poms_vigor == None or c_a_poms_negative == None or c_a_poms_positive == None or tc_a_poms_negative == None or tc_a_poms_positive == None:
        print('date:{0} c_id:{1} c_init:{2} t_init:{3} not exist in {4}'.format(date, c_id, c_init, t_init, MY_TRANS_POMS_XLSX_PATH))
        print('c_a_poms_calmness:{0} c_a_poms_anger:{1} c_a_poms_sad:{2} c_a_poms_contentment:{3} c_a_poms_anxiety:{4} c_a_poms_vigor:{5} '
              't_a_poms_anger:{6} t_a_poms_sad:{7} t_a_poms_contentment:{8} t_a_poms_anxiety:{9} t_a_poms_vigor:{10} tc_a_poms_anger:{11} '
              'tc_a_poms_sad:{12} tc_a_poms_contentment:{13} tc_a_poms_anxiety:{14} tc_a_poms_vigor:{15} c_a_poms_negative:{16} c_a_poms_positive:{17} '
              'tc_a_poms_negative: {18} tc_a_poms_positive: {19}'
              .format(c_a_poms_calmness, c_a_poms_anger, c_a_poms_sad, c_a_poms_contentment, c_a_poms_anxiety, c_a_poms_vigor,
                      t_a_poms_anger, t_a_poms_sad, t_a_poms_contentment, t_a_poms_anxiety, t_a_poms_vigor,
                      tc_a_poms_anger, tc_a_poms_sad, tc_a_poms_contentment, tc_a_poms_anxiety, tc_a_poms_vigor,
                      c_a_poms_negative, c_a_poms_positive, tc_a_poms_negative, tc_a_poms_positive))

    return c_a_poms_calmness, c_a_poms_anger, c_a_poms_sad, c_a_poms_contentment, c_a_poms_anxiety, c_a_poms_vigor, \
                        t_a_poms_anger, t_a_poms_sad, t_a_poms_contentment, t_a_poms_anxiety, t_a_poms_vigor, \
                        tc_a_poms_anger, tc_a_poms_sad, tc_a_poms_contentment, tc_a_poms_anxiety, tc_a_poms_vigor, \
                        c_a_poms_negative, c_a_poms_positive, tc_a_poms_negative, tc_a_poms_positive


def generate(trans_names, mapping_df, labels_df):
    trans_info = {}

    ### ORS ###
    if LABEL == 'ors':
        print("Generating {0} labels ...".format(LABEL))
        for trans_name in trans_names:
            he_char_sessionNumber, date = trans_name.split('_')
            he_char = ''.join([i for i in he_char_sessionNumber if not i.isdigit()])
            session_number = int(re.sub("[^0-9]", "", he_char_sessionNumber))
            c_id, c_init, t_init = getCTDetails(mapping_df, he_char)
            ors1, ors2, ors3, ors4, ors_sum = getORS(labels_df, date, c_id, c_init, t_init)

            trans_info[trans_name] = {'date': date,
                                      'he_char': he_char,
                                      'c_id': c_id,
                                      'c_init': c_init,
                                      't_init': t_init,
                                      'ors1': ors1,
                                      'ors2': ors2,
                                      'ors3': ors3,
                                      'ors4': ors4,
                                      'ors_sum': ors_sum,
                                      'session_number': session_number,
                                      }
    ### HSCL ###
    elif LABEL == 'hscl':
        print("Generating {0} labels ...".format(LABEL))
        for trans_name in trans_names:
            he_char_sessionNumber, date = trans_name.split('_')
            he_char = ''.join([i for i in he_char_sessionNumber if not i.isdigit()])
            session_number = int(re.sub("[^0-9]", "", he_char_sessionNumber))
            c_id, c_init, t_init = getCTDetails(mapping_df, he_char)
            hscl1, hscl2, hscl3, hscl4, hscl5, hscl6, hscl7, hscl8, hscl9, hscl10, hscl11, hscl_avg = getHSCL(labels_df, date, c_id, c_init, t_init)

            trans_info[trans_name] = {'date': date,
                                      'he_char': he_char,
                                      'c_id': c_id,
                                      'c_init': c_init,
                                      't_init': t_init,
                                      'hscl1': hscl1,
                                      'hscl2': hscl2,
                                      'hscl3': hscl3,
                                      'hscl4': hscl4,
                                      'hscl5': hscl5,
                                      'hscl6': hscl6,
                                      'hscl7': hscl7,
                                      'hscl8': hscl8,
                                      'hscl9': hscl9,
                                      'hscl10': hscl10,
                                      'hscl11': hscl11,
                                      'hscl_avg': hscl_avg,
                                      'session_number': session_number,
                                      }

    ### RUPTURE ###
    if LABEL == 'rupture':
        print("Generating {0} labels ...".format(LABEL))
        for trans_name in trans_names:
            he_char_sessionNumber, date = trans_name.split('_')
            he_char = ''.join([i for i in he_char_sessionNumber if not i.isdigit()])
            session_number = int(re.sub("[^0-9]", "", he_char_sessionNumber))
            c_id, c_init, t_init = getCTDetails(mapping_df, he_char)
            c_a_rupture1, c_a_rupture2, t_a_rupture1, t_a_rupture2 = getRUPTURE(labels_df, date, c_id, c_init, t_init)

            trans_info[trans_name] = {'date': date,
                                      'he_char': he_char,
                                      'c_id': c_id,
                                      'c_init': c_init,
                                      't_init': t_init,
                                      'c_a_rupture1': c_a_rupture1,
                                      'c_a_rupture2': c_a_rupture2,
                                      't_a_rupture1': t_a_rupture1,
                                      't_a_rupture2': t_a_rupture2,
                                      'session_number': session_number,
                                      }

    ### POMS ###
    if LABEL == 'poms':
        print("Generating {0} labels ...".format(LABEL))
        for trans_name in trans_names:
            he_char_sessionNumber, date = trans_name.split('_')
            he_char = ''.join([i for i in he_char_sessionNumber if not i.isdigit()])
            session_number = int(re.sub("[^0-9]", "", he_char_sessionNumber))
            c_id, c_init, t_init = getCTDetails(mapping_df, he_char)
            c_a_poms_calmness, c_a_poms_anger, c_a_poms_sad, c_a_poms_contentment, c_a_poms_anxiety, c_a_poms_vigor, \
            t_a_poms_anger, t_a_poms_sad, t_a_poms_contentment, t_a_poms_anxiety, t_a_poms_vigor, \
            tc_a_poms_anger, tc_a_poms_sad, tc_a_poms_contentment, tc_a_poms_anxiety, tc_a_poms_vigor, \
            c_a_poms_negative, c_a_poms_positive, tc_a_poms_negative, tc_a_poms_positive = getPOMS(labels_df, date, c_id, c_init,t_init)

            trans_info[trans_name] = {'date': date,
                                      'he_char': he_char,
                                      'c_id': c_id,
                                      'c_init': c_init,
                                      't_init': t_init,
                                      'c_a_poms_calmness': c_a_poms_calmness,
                                      'c_a_poms_anger': c_a_poms_anger,
                                      'c_a_poms_sad': c_a_poms_sad,
                                      'c_a_poms_contentment': c_a_poms_contentment,
                                      'c_a_poms_anxiety': c_a_poms_anxiety,
                                      'c_a_poms_vigor': c_a_poms_vigor,
                                      't_a_poms_anger': t_a_poms_anger,
                                      't_a_poms_sad': t_a_poms_sad,
                                      't_a_poms_contentment': t_a_poms_contentment,
                                      't_a_poms_anxiety': t_a_poms_anxiety,
                                      't_a_poms_vigor': t_a_poms_vigor,
                                      'tc_a_poms_anger': tc_a_poms_anger,
                                      'tc_a_poms_sad': tc_a_poms_sad,
                                      'tc_a_poms_contentment': tc_a_poms_contentment,
                                      'tc_a_poms_anxiety': tc_a_poms_anxiety,
                                      'tc_a_poms_vigor': tc_a_poms_vigor,
                                      'c_a_poms_negative': c_a_poms_negative,
                                      'c_a_poms_positive': c_a_poms_positive,
                                      'tc_a_poms_negative': tc_a_poms_negative,
                                      'tc_a_poms_positive': tc_a_poms_positive,
                                      'session_number': session_number,
                                      }
    else:
        raise exit("Unsupported label.")

    return trans_info


def write2File(trans_info):
    if LABEL == 'ors':
        out_name = ORS_OUTPUT_FILE_NAME
    elif LABEL == 'hscl':
        out_name = HSCL_OUTPUT_FILE_NAME
    elif LABEL == 'rupture':
        out_name = RUPTURE_OUTPUT_FILE_NAME
    elif LABEL == 'poms':
        out_name = POMS_OUTPUT_FILE_NAME
    else:
        raise exit("Unsupported label.")

    with open(out_name, 'w') as f:
        yaml.dump(trans_info, f, default_flow_style=False, allow_unicode=True)


if __name__ == '__main__':
    # Map the trans file names to theirs labels.
    # For creating vanilla yml files.
    trans_names = getTransNames()
    mapping_values, label_values = loadXLSXs()
    trans_info = generate(trans_names, mapping_values, label_values)
    write2File(trans_info)

