import pandas as pd
import xlrd
import sys

# SBS columns names
C_INIT = 'c_init'
SESSION_N = 'session_n'
C_B_ORS = 'c_b_ors'

NUM_OF_SESSIONS = 3
RCI_MARGIN = 5


def getOptions():
    if '--file' in sys.argv:
        file_option_i = sys.argv.index('--file')
        file_name = sys.argv[file_option_i + 1]
    else:
        file_name = 'sbs_orig_data/SBS_x_1000Transcriptions.xlsx'

    if '--sheet' in sys.argv:
        sheet_option_i = sys.argv.index('--sheet')
        sheet_name = sys.argv[sheet_option_i + 1]
    else:
        sheet_name = 'Sheet1'

    if '--output' in sys.argv:
        output_option_i = sys.argv.index('--output')
        output_name = sys.argv[output_option_i + 1]
    else:
        output_name = 'sbs_stat/1000_stat.txt'

    return file_name, sheet_name, output_name


def loadData():
    df = pd.read_excel(io=xlsx_file_name, sheet_name=sheet_name)
    c_init_list = []
    session_n_list = []
    c_b_ors_list = []
    for i, row in df.iterrows():
        c_init = row[C_INIT]
        session_n = row[SESSION_N]
        c_b_ors = row[C_B_ORS]
        try:
            c_b_ors_num = float(c_b_ors)
            c_init_list.append(c_init)
            session_n_list.append(session_n)
            c_b_ors_list.append(c_b_ors_num)
        except ValueError:
            pass

    return c_init_list, session_n_list, c_b_ors_list


def getStat(c_dict):
    c_stat = {}
    for c in c_dict:
        first_session_n = []
        last_session_n = []
        first_3_ors = []
        last_3_ors = []
        first_avg = 0
        last_avg = 0

        if len(c_dict[c][0]) < NUM_OF_SESSIONS:
            first_session_n = c_dict[c][0]
            last_session_n = c_dict[c][0]
            first_3_ors = c_dict[c][1]
            last_3_ors = c_dict[c][1]
            first_avg = 'N/A'
            last_avg = 'N/A'
            rci = 'N/A'
            success = 'failure'
        else:
            for session in range(NUM_OF_SESSIONS):
                # c_dict is {client} = {(c_seesion, c_ors)}
                first_session_n.append(c_dict[c][0][session])
                last_session_n.append(c_dict[c][0][-session-1])
                first_3_ors.append(round(float(c_dict[c][1][session]), 2))
                last_3_ors.append(round(float(c_dict[c][1][-session-1]), 2))
                first_avg += float(c_dict[c][1][session])
                last_avg += float(c_dict[c][1][-session-1])
            first_avg = round(first_avg/(NUM_OF_SESSIONS*1.0), 2)
            last_avg = round(last_avg/(NUM_OF_SESSIONS*1.0), 2)

            rci = round(last_avg - first_avg, 2)
            success = 'success' if rci > RCI_MARGIN else 'failure'

        c_stat[c] = (first_session_n, last_session_n, first_3_ors, last_3_ors, first_avg, last_avg, rci, success)

    return c_stat


def calcORS(c_init_list, session_n_list, c_b_ors_list):
    c_name = c_init_list[0]
    c_seesion = []
    c_ors = []
    c_dict = {}
    for c_index in range(len(c_init_list)):
        c = c_init_list[c_index]
        if c != c_name:
            c_dict[c_name] = (c_seesion, c_ors)
            c_name = c
            c_seesion = []
            c_ors = []
        c_seesion.append(session_n_list[c_index])
        c_ors.append(c_b_ors_list[c_index])
    c_dict[c] = (c_seesion, c_ors)

    c_stat = getStat(c_dict)

    return c_stat


def print2file(c_stat, output_name):
    # c_stat is (first_session_n, last_session_n, first_3_ors, last_3_ors, first_avg, last_avg, rci, success)
    with open(output_name, 'w') as f:
        for c in c_stat:
            string = 'c_init:{0}    ' \
                     '{1} first sessions:{2}  ' \
                     '{1} last sessions:{3}  ' \
                     '{1} first ORS:{4}  ' \
                     '{1} last ORS:{5}  ' \
                     '{1} first ORS avg:{6}  ' \
                     '{1} last ORS avg:{7}  ' \
                     'RCI={8}  ' \
                     'Change:{9}' \
                     '\n'.format(c, NUM_OF_SESSIONS, c_stat[c][0], c_stat[c][1], c_stat[c][2], c_stat[c][3], c_stat[c][4], c_stat[c][5], c_stat[c][6], c_stat[c][7])
            f.write(string)


if __name__ == '__main__':
    xlsx_file_name, sheet_name, output_name = getOptions()
    c_init_list, session_n_list, c_b_ors_list = loadData()
    c_stat = calcORS(c_init_list, session_n_list, c_b_ors_list)
    print2file(c_stat, output_name)


