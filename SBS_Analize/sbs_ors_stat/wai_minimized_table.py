import pandas as pd
import xlrd
import sys

# SBS columns names
CID = 'c_id'  # 'dyad'
CINIT = 'c_init'
TINIT = 't_init'
SESSION_N = 'session_n'
C_A_WAI = 'c_a_wai'
T_A_WAI = 't_a_wai'

NUM_OF_SESSIONS = 3
# RCI_MARGIN = 5


def getOptions():
    if '--file' in sys.argv:
        file_option_i = sys.argv.index('--file')
        file_name = sys.argv[file_option_i + 1]
    else:
        file_name = '/home/daniel/Documents/SBS/my/trans_wai.csv'

    if '--sheet' in sys.argv:
        sheet_option_i = sys.argv.index('--sheet')
        sheet_name = sys.argv[sheet_option_i + 1]
    else:
        sheet_name = 'trans_wai'

    if '--output' in sys.argv:
        output_option_i = sys.argv.index('--output')
        output_name = sys.argv[output_option_i + 1]
    else:
        output_name = 'my_wai_composition_stat_01.txt'

    return file_name, sheet_name, output_name


def loadData():
    df = pd.read_csv(xlsx_file_name)
    dyad_list = []
    session_n_list = []
    c_a_wai_list = []
    t_a_wai_list = []
    for i, row in df.iterrows():
        c_id = row[CID]
        c_init = row[CINIT]
        t_init = row[TINIT]
        dyad = c_init.lower() + str(c_id) + t_init.lower()
        session_n = row[SESSION_N]
        c_a_wai = row[C_A_WAI]
        t_a_wai = row[T_A_WAI]
        try:
            c_a_wai_num = float(c_a_wai)
            t_a_wai_num = float(t_a_wai)
            dyad_list.append(dyad)
            session_n_list.append(session_n)
            c_a_wai_list.append(c_a_wai_num)
            t_a_wai_list.append(t_a_wai_num)
        except ValueError:
            pass

    return dyad_list, session_n_list, c_a_wai_list, t_a_wai_list


def getStat(c_dict):
    c_stat = {}
    for c in c_dict:
        first_session_n = []
        last_session_n = []
        first_3_c_wai = []
        last_3_c_wai = []
        first_3_t_wai = []
        last_3_t_wai = []
        first_c_avg = 0
        last_c_avg = 0
        first_t_avg = 0
        last_t_avg = 0

        if len(c_dict[c][0]) < NUM_OF_SESSIONS:
            first_session_n = c_dict[c][0]
            last_session_n = c_dict[c][0]
            first_3_hscl = c_dict[c][1]
            last_3_hscl = c_dict[c][1]
            first_c_avg = 'N/A'
            last_c_avg = 'N/A'
            first_t_avg = 'N/A'
            last_t_avg = 'N/A'
            rci = 'N/A'
            success = 'N/A'
        else:
            for session in range(NUM_OF_SESSIONS):
                # c_dict is {client} = {(c_seesion, c_ors)}
                first_session_n.append(c_dict[c][0][session])
                last_session_n.append(c_dict[c][0][-session-1])
                first_3_c_wai.append(round(float(c_dict[c][1][session]), 2))
                last_3_c_wai.append(round(float(c_dict[c][1][-session-1]), 2))
                first_3_t_wai.append(round(float(c_dict[c][2][session]), 2))
                last_3_t_wai.append(round(float(c_dict[c][2][-session-1]), 2))
                first_c_avg += float(c_dict[c][1][session])
                last_c_avg += float(c_dict[c][1][-session-1])
                first_t_avg += float(c_dict[c][2][session])
                last_t_avg += float(c_dict[c][2][-session-1])
            # how many times ors == 0.0 (the sum value is null)
            # if 1,2 - make the avg costumly, if 3 - set the success to N/A
            first_c_zero_val_count = first_3_c_wai.count(0.0)
            last_c_zero_val_count = last_3_c_wai.count(0.0)
            first_t_zero_val_count = first_3_t_wai.count(0.0)
            last_t_zero_val_count = last_3_t_wai.count(0.0)

            # client (c)
            if first_c_zero_val_count != 3 and last_c_zero_val_count != 3:
                first_c_avg = round(first_c_avg / ((NUM_OF_SESSIONS - first_c_zero_val_count) * 1.0), 2)
                last_c_avg = round(last_c_avg / ((NUM_OF_SESSIONS - last_c_zero_val_count) * 1.0), 2)

                rci = round(last_c_avg - first_c_avg, 2)
                # success = 'N/A' if rci > RCI_MARGIN else 'poor'
                success = 'N/A'
            elif first_c_zero_val_count == 3:
                first_c_avg = 'N/A'
                rci = 'N/A'
                success = 'N/A'
                if last_c_zero_val_count == 3:
                    last_c_avg = 'N/A'
                    rci = 'N/A'
                    success = 'N/A'
                else:
                    last_c_avg = round(last_c_avg / ((NUM_OF_SESSIONS - last_c_zero_val_count) * 1.0), 2)
            else:
                first_c_avg = round(first_c_avg / ((NUM_OF_SESSIONS - first_c_zero_val_count) * 1.0), 2)

            # therapist (t)
            if first_t_zero_val_count != 3 and last_t_zero_val_count != 3:
                first_t_avg = round(first_t_avg / ((NUM_OF_SESSIONS - first_t_zero_val_count) * 1.0), 2)
                last_t_avg = round(last_t_avg / ((NUM_OF_SESSIONS - last_t_zero_val_count) * 1.0), 2)

                rci = round(last_t_avg - first_t_avg, 2)
                # success = 'N/A' if rci > RCI_MARGIN else 'poor'
                success = 'N/A'
            elif first_t_zero_val_count == 3:
                first_t_avg = 'N/A'
                rci = 'N/A'
                success = 'N/A'
                if last_t_zero_val_count == 3:
                    last_c_avg = 'N/A'
                    rci = 'N/A'
                    success = 'N/A'
                else:
                    last_t_avg = round(last_t_avg / ((NUM_OF_SESSIONS - last_t_zero_val_count) * 1.0), 2)
            else:
                first_t_avg = round(first_t_avg / ((NUM_OF_SESSIONS - first_t_zero_val_count) * 1.0), 2)

        c_stat[c] = (first_session_n, last_session_n, first_3_c_wai, last_3_c_wai, first_c_avg, last_c_avg, first_3_t_wai, last_3_t_wai, first_t_avg, last_t_avg)

    return c_stat


def calcWAI(dyad_list, session_n_list, c_a_wai_list, t_a_wai_list):
    c_name = dyad_list[0]
    c_seesion = []
    c_wai = []
    t_wai = []
    c_dict = {}
    for c_index in range(len(dyad_list)):
        c = dyad_list[c_index]
        if c != c_name:
            c_dict[c_name] = (c_seesion, c_wai, t_wai)
            c_name = c
            c_seesion = []
            c_wai = []
            t_wai = []
        c_seesion.append(session_n_list[c_index])
        c_wai.append(c_a_wai_list[c_index])
        t_wai.append(t_a_wai_list[c_index])
    c_dict[c] = (c_seesion, c_wai, t_wai)

    c_stat = getStat(c_dict)

    return c_stat


def print2file(c_stat, output_name, cid2dyad):
    # c_stat is (first_session_n, last_session_n, first_3_ors, last_3_ors, first_avg, last_avg, rci, success)
    with open(output_name, 'w') as f:
        for c in c_stat:
            # if is_float_number(c_stat[c][4]) and is_float_number(c_stat[c][5]) and str(c_stat[c][4]) != 'nan' and str(c_stat[c][5]) != 'nan':
            #     pre_ors_avg_under = "T" if float(c_stat[c][4]) < 24.0 else "F"
            #     post_ors_avg_over = "T" if float(c_stat[c][5]) >= 24.0 else "F"
            # else:
            #     pre_ors_avg_under = "N/A"
            #     post_ors_avg_over = "N/A"
            pre_ors_avg_under = "N/A"
            post_ors_avg_over = "N/A"
            try:
                dyad = cid2dyad[str(c)]
            except KeyError:
                dyad = "N/A"
            string = 'c_id:{0}\t' \
                     '{1}_first_sessions:{2}\t' \
                     '{1}_last_sessions:{3}\t' \
                     '{1}_first_c_WAI:{4}\t' \
                     '{1}_last_c_WAI:{5}\t' \
                     '{1}_first_c_WAI_avg:{6}\t' \
                     '{1}_last_c_WAI_avg:{7}\t' \
                     '{1}_first_t_WAI:{8}\t' \
                     '{1}_last_t_WAI:{9}\t' \
                     '{1}_first_t_WAI_avg:{10}\t' \
                     '{1}_last_t_WAI_avg:{11}\t' \
                     'dyad:{12}\n'.format(c, NUM_OF_SESSIONS, c_stat[c][0], c_stat[c][1], c_stat[c][2], c_stat[c][3], c_stat[c][4], c_stat[c][5], c_stat[c][6], c_stat[c][7], c_stat[c][8], c_stat[c][9], dyad)
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
    dyad_list, session_n_list, c_a_wai_list, t_a_wai_list = loadData()
    c_stat = calcWAI(dyad_list, session_n_list, c_a_wai_list, t_a_wai_list)
    cid2dyad, dyad2cid = load_ciddyad_mapping()
    print2file(c_stat, output_name, cid2dyad)


