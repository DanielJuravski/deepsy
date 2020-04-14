import pandas
import numpy as np

BQ_FILE_PATH = '/home/daniel/Documents/SBS/my/bq.csv'


# def int12(val):
#     # return int of 'str' only if it's 1 or 2
#     if val == 1 or val == 2:
#         return int(val)
#     else:
#         raise exit("c_questionnaire value is not 1 or 2.")


def processDataItem(date, start_treatment, c_init, c_id, oq_sum):
    # Process data item, otherwise return False
    isValid = True

    if date == "#NULL!":
        isValid = False
        return isValid

    if start_treatment == 1:  # 1 is True | 2 is False
        start_treatment = 'S'
    elif start_treatment == 2:
        start_treatment = 'E'
    else:
        isValid = False
        return isValid

    if c_init == "#NULL!":
        isValid = False
        return isValid

    if c_id == "#NULL!":
        isValid = False
        return isValid

    if oq_sum == "#NULL!":
        isValid = False
        return isValid
    else:
        oq_sum = float(oq_sum)

    return date, start_treatment, c_init, c_id, oq_sum


def loadFile():
    unfiltered_data = []
    df = pandas.read_csv(BQ_FILE_PATH)
    for i, row in df.iterrows():
        date = row['date']
        start_treatment = row['c_questionnaire']
        c_init = row['c_initials']
        c_id = row['c_id']
        oq_sum = row['SumOQ']

        client_data = processDataItem(date, start_treatment, c_init, c_id, oq_sum)
        if client_data is not False:
            print(client_data)
            unfiltered_data.append(client_data)

    return unfiltered_data


def arrange(unfiltered_data):
    clients = {}
    for item in unfiltered_data:
        date = item[0]
        start_treatment = item[1]
        c_init = item[2]
        c_id = item[3]
        oq_sum = item[4]
        c = {'c_id_' + str(start_treatment): c_id, 'date_' + str(start_treatment): date, 'oq_sum_' + str(start_treatment): oq_sum}
        if c_init not in clients:
            clients[c_init] = c
        else:
            clients[c_init].update(c)

    for c, c_info in clients.items():
        if 'oq_sum_S' in c_info and 'oq_sum_E' in c_info:
            oq_sum_diff = c_info['oq_sum_S'] - c_info['oq_sum_E']
            c_info['oq_sum_diff'] = oq_sum_diff

            if oq_sum_diff >= 14:
                c_info['change'] = 'Success'
            else:
                c_info['change'] = 'Failure'

            if c_info['oq_sum_S'] >= 64:
                c_info['oq_sum_S_H'] = 'True'
            else:
                c_info['oq_sum_S_H'] = 'False'

            if c_info['oq_sum_E'] < 64:
                c_info['oq_sum_E_L'] = 'True'
            else:
                c_info['oq_sum_E_L'] = 'False'

    print(clients)
    return clients


def write(clients):
    with open('bq_oq_sagnificant_change.txt', 'w') as f:
        for c, c_info in clients.items():
            f.write(c + '\t')
            f.write(str(c_info))
            f.write('\n')


def oq_stats(clients):
    oq_s_list = []
    oq_e_list = []
    for _, client_info in clients.items():
        if 'oq_sum_S' in client_info:
            oq_s_list.append(client_info['oq_sum_S'])
        if 'oq_sum_E' in client_info:
            oq_e_list.append(client_info['oq_sum_E'])

    oq_s_list = np.asarray(oq_s_list)
    oq_e_list = np.asarray(oq_e_list)

    print("OQ stat info ...")
    print("OQ Start Mean: {0}".format(oq_s_list.mean()))
    print("OQ Start STD: {0}".format(oq_s_list.std()))
    print("OQ End Mean: {0}".format(oq_e_list.mean()))
    print("OQ End STD: {0}".format(oq_e_list.std()))
    pass


if __name__ == '__main__':
    unfiltered_data = loadFile()
    clients = arrange(unfiltered_data)
    write(clients)
    oq_stats(clients)
