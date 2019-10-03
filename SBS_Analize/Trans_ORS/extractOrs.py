import os
import pandas
import yaml

MAPPING_XLSX_PATH = '/home/daniel/Documents/SBS/Transcriptions_Questionnaire_Mapping.xlsx'
MY_TRANS_ORS_XLSX_PATH = '/home/daniel/Documents/SBS/my/trans_ors.csv'
TRANS_DIR_PATH = '/home/daniel/Documents/parsed_trans_reut_v2'

OUTPUT_FILE_NAME = 'trans_ors.yml'


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

    print('Loading {}'.format(MY_TRANS_ORS_XLSX_PATH))
    ors_df = pandas.read_csv(MY_TRANS_ORS_XLSX_PATH)
    ors_format = ['date', 't_init', 'c_init', 'c_id', 'ors1', 'ors2', 'ors3', 'ors4', 'ors_sum']
    ors_values = ors_df[ors_format]

    return mapping_values, ors_values


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


def generate(trans_names, mapping_df, ors_df):
    print("Generating ...")
    trans_info = {}

    for trans_name in trans_names:
        he_char_sessionNumber, date = trans_name.split('_')
        he_char = ''.join([i for i in he_char_sessionNumber if not i.isdigit()])
        c_id, c_init, t_init = getCTDetails(mapping_df, he_char)
        ors1, ors2, ors3, ors4, ors_sum = getORS(ors_df, date, c_id, c_init, t_init)

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
                                  }
    
    return trans_info


def write2File(trans_info):
    with open(OUTPUT_FILE_NAME, 'w') as f:
        yaml.dump(trans_info, f, default_flow_style=False, allow_unicode=True)


if __name__ == '__main__':
    trans_names = getTransNames()
    mapping_df, ors_df = loadXLSXs()
    trans_info = generate(trans_names, mapping_df, ors_df)
    write2File(trans_info)

    pass