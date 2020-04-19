import pandas as pd
import xlrd
import sys

# SBS columns names
CID = 'c_id'  # 'dyad'
CINIT = 'c_init'
TINIT = 't_init'
SESSION_N = 'session_n'
C_B_ORS = 'ors_sum'

NUM_OF_SESSIONS = 3
RCI_MARGIN = 5


def getOptions():
    if '--file' in sys.argv:
        file_option_i = sys.argv.index('--file')
        file_name = sys.argv[file_option_i + 1]
    else:
        file_name = '/home/daniel/Documents/SBS/my/trans_ors.csv'

    if '--sheet' in sys.argv:
        sheet_option_i = sys.argv.index('--sheet')
        sheet_name = sys.argv[sheet_option_i + 1]
    else:
        sheet_name = 'trans_ors'

    if '--output' in sys.argv:
        output_option_i = sys.argv.index('--output')
        output_name = sys.argv[output_option_i + 1]
    else:
        output_name = 'my_ors_composition_stat_02.txt'

    return file_name, sheet_name, output_name


def loadData():
    df = pd.read_csv(xlsx_file_name)
    dyad_list = []
    session_n_list = []
    c_b_ors_list = []
    for i, row in df.iterrows():
        c_id = row[CID]
        c_init = row[CINIT]
        t_init = row[TINIT]
        dyad = c_init.lower() + str(c_id) + t_init.lower()
        session_n = row[SESSION_N]
        c_b_ors = row[C_B_ORS]
        try:
            c_b_ors_num = float(c_b_ors)
            dyad_list.append(dyad)
            session_n_list.append(session_n)
            c_b_ors_list.append(c_b_ors_num)
        except ValueError:
            pass

    return dyad_list, session_n_list, c_b_ors_list


def getStat(c_dict):
    c_stat = {}
    for c in c_dict:
        first_session_n = []
        last_session_n = []
        first_3_ors = []
        last_3_ors = []
        first_avg = 0
        last_avg = 0
        all_ors = c_dict[c][1]

        if len(c_dict[c][0]) < NUM_OF_SESSIONS:
            first_session_n = c_dict[c][0]
            last_session_n = c_dict[c][0]
            first_3_ors = c_dict[c][1]
            last_3_ors = c_dict[c][1]
            first_avg = 'N/A'
            last_avg = 'N/A'
            rci = 'N/A'
            success = 'N/A'
        else:
            for session in range(NUM_OF_SESSIONS):
                # c_dict is {client} = {(c_seesion, c_ors)}
                first_session_n.append(c_dict[c][0][session])
                last_session_n.append(c_dict[c][0][-session-1])
                first_3_ors.append(round(float(c_dict[c][1][session]), 2))
                last_3_ors.append(round(float(c_dict[c][1][-session-1]), 2))
                first_avg += float(c_dict[c][1][session])
                last_avg += float(c_dict[c][1][-session-1])
            # how many times ors == 0.0 (the sum value is null)
            # if 1,2 - make the avg costumly, if 3 - set the success to N/A
            first_zero_val_count = first_3_ors.count(0.0)
            last_zero_val_count = last_3_ors.count(0.0)

            if first_zero_val_count != 3 and last_zero_val_count != 3:
                first_avg = round(first_avg / ((NUM_OF_SESSIONS - first_zero_val_count) * 1.0), 2)
                last_avg = round(last_avg / ((NUM_OF_SESSIONS - last_zero_val_count) * 1.0), 2)

                rci = round(last_avg - first_avg, 2)
                success = 'good' if rci > RCI_MARGIN else 'poor'
            elif first_zero_val_count == 3:
                first_avg = 'N/A'
                rci = 'N/A'
                success = 'N/A'
                if last_zero_val_count == 3:
                    last_avg = 'N/A'
                    rci = 'N/A'
                    success = 'N/A'
                else:
                    last_avg = round(last_avg / ((NUM_OF_SESSIONS - last_zero_val_count) * 1.0), 2)
            else:
                first_avg = round(first_avg / ((NUM_OF_SESSIONS - first_zero_val_count) * 1.0), 2)

        c_stat[c] = (first_session_n, last_session_n, first_3_ors, last_3_ors, first_avg, last_avg, rci, success, all_ors)

    return c_stat


def calcORS(dyad_list, session_n_list, c_b_ors_list):
    c_name = dyad_list[0]
    c_seesion = []
    c_ors = []
    c_dict = {}
    for c_index in range(len(dyad_list)):
        c = dyad_list[c_index]
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


def print2file(c_stat, output_name, cid2dyad):
    # c_stat is (first_session_n, last_session_n, first_3_ors, last_3_ors, first_avg, last_avg, rci, success)
    with open(output_name, 'w') as f:
        for c in c_stat:
            if is_float_number(c_stat[c][4]) and is_float_number(c_stat[c][5]) and str(c_stat[c][4]) != 'nan' and str(c_stat[c][5]) != 'nan':
                pre_ors_avg_under = "T" if float(c_stat[c][4]) < 24.0 else "F"
                post_ors_avg_over = "T" if float(c_stat[c][5]) >= 24.0 else "F"
            else:
                pre_ors_avg_under = "N/A"
                post_ors_avg_over = "N/A"
            try:
                dyad = cid2dyad[str(c)]
            except KeyError:
                dyad = "N/A"
            string = 'c_id:{0}\t' \
                     '{1}_first_sessions:{2}\t' \
                     '{1}_last_sessions:{3}\t' \
                     '{1}_first_ORS:{4}\t' \
                     '{1}_last_ORS:{5}\t' \
                     '{1}_first_ORS_avg:{6}\t' \
                     '{1}_last_ORS_avg:{7}\t' \
                     'RCI:{8}\t' \
                     '{1}_first_ors_avg_under_24:{10}\t' \
                     '{1}_last_ors_avg_over_24:{11}\t' \
                     'Change:{9}\t' \
                     'dyad:{12}\t' \
                     'all_ORS:{13}\n'.format(c, NUM_OF_SESSIONS, c_stat[c][0], c_stat[c][1], c_stat[c][2], c_stat[c][3], c_stat[c][4], c_stat[c][5], c_stat[c][6], c_stat[c][7], pre_ors_avg_under, post_ors_avg_over, dyad, c_stat[c][8])
            f.write(string)


def is_float_number(s):
    try:
        float(s) # for int, long, float and complex
    except ValueError:
        return False

    return True


def load_ciddyad_mapping():
    dyad2cid = {}
    with open('dyay2cid.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            (dyay, cid, cinit, tinit) = line.split('\t')
            tinit = tinit.split()[0]  # remove \n
            ccode = cinit.lower() + str(cid) + tinit.lower()
            dyad2cid[dyay] = ccode
    cid2dyad = {v: k for k, v in dyad2cid.items()}

    return cid2dyad, dyad2cid


if __name__ == '__main__':
    xlsx_file_name, sheet_name, output_name = getOptions()
    dyad_list, session_n_list, c_b_ors_list = loadData()
    c_stat = calcORS(dyad_list, session_n_list, c_b_ors_list)
    cid2dyad, dyad2cid = load_ciddyad_mapping()
    print2file(c_stat, output_name, cid2dyad)


