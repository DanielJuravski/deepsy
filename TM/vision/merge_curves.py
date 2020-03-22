import matplotlib.pyplot as plt
import os
import json
import numpy as np
import re

from visualizeTopics_curve import NEG_THREADLINE_FUNC, NEG_R2, POS_THREADLINE_FUNC, POS_R2


CURVE_FUNC_FILES = '/home/daniel/deepsy/TM/Dirs_of_Docs/c_sessions/results/Topic_Visualize/curve/'
OUTPUT_DIR = '/home/daniel/deepsy/TM/Dirs_of_Docs/c_sessions/results/Topic_Visualize/curve/avg/'
TOPICS = 'ORS'
CLIENTS = 'לב מב'
CLIENTS = 'לב מב כג ש עה'  # good
CLIENTS = 'עא ד ה יא ז'  # poor

PLT_SHOW = True
PLT_SAVE = True
DPI = 200


def load_funcs():
    client_funcs = dict()
    all_curve_files = os.listdir(CURVE_FUNC_FILES)
    for c in CLIENTS.split():
        func_file = c + '.func'
        # validate file exists
        if func_file not in all_curve_files:
            raise "[ERROR] There is not func file for {0} client!".format(c)
        func_file_path = CURVE_FUNC_FILES + func_file
        with open(func_file_path, 'r') as f:
            funcs = json.load(f)
            client_funcs[c] = funcs

    return client_funcs


def reverse(s):
    """
    reversed str
    abc --> cba
    :param s:
    :return:
    """
    return s[::-1]


def str_to_func_factors(neg_func):
    # extracts from y=2x+4 --> m=2, b=4
    p = re.compile("y=(.*)x(.*)")
    result = p.search(neg_func)
    try:
        m = float(result.group(1))
        b = float(result.group(2))
    except AttributeError as e:
        m = 0
        b = 0

    return m, b


def plot_funcs(client_funcs, func_name, func_c, avg_c):
    # init arrays
    line_size = 30
    x = np.linspace(1, line_size, num=line_size)
    y_sum = np.zeros(line_size)
    n_ys = 0

    for c in client_funcs.keys():
        # calc current func X,Y
        neg_func = client_funcs[c][func_name]
        m, b = str_to_func_factors(neg_func)
        y = m * x + b

        # plot current func
        plt.plot(x, y, func_c, linestyle='-', linewidth=1)
        plt.text(x[-1], y[-1], reverse(c))

        # calc avg
        y_sum += y
        n_ys += 1

    # plot avg curve
    y_avg = y_sum / n_ys
    z = np.polyfit(x, y_avg, 1)
    linear = f"y={z[0]:0.10f}x{z[1]:+0.10f}"
    plt.plot(x, y_avg, avg_c, linestyle='-', linewidth=2, label=linear)


def make_graph(client_funcs):
    if TOPICS == 'ORS':
        plot_funcs(client_funcs, NEG_THREADLINE_FUNC, func_c='#C26565', avg_c='r')
        plot_funcs(client_funcs, POS_THREADLINE_FUNC, func_c='#73C265', avg_c='g')

    # design plot
    plt.suptitle('Clients Names: \n{0}'.format(reverse(CLIENTS)), fontsize=15)
    plt.xlabel('Session number', fontsize=10)
    plt.ylabel('Topic signal', fontsize=10)
    plt.legend()
    if PLT_SAVE:
        out_str = OUTPUT_DIR + CLIENTS.replace(' ', '_') + '.png'
        plt.savefig(out_str, dpi=DPI)
    if PLT_SHOW:
        plt.show()
    plt.close()




if __name__ == '__main__':
    """
    ploting the CLIENTS' NEG_THREADLINE_FUNC and POS_THREADLINE_FUNC  and there mean curve"""
    client_funcs = load_funcs()
    make_graph(client_funcs)