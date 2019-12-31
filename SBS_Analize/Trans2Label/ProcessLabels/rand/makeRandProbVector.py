import yaml
import numpy as np
from random import random


with open('/home/daniel/deepsy/TM/Dirs_of_Docs/c_sessions/results/inferencer_200-c_1turns_words_mini_small.txt', 'r') as f_i:
    new_file = []
    for line in f_i:
        new_line = []
        # handle comment lines
        if line[0] == '#':
            intro_line = line
            continue
        line_details = line.split()
        new_line.append(line_details[0])
        new_line.append(line_details[1])

        # vector
        rand_prob = np.empty([200])
        for i in range(200):
            rand_prob[i] = (random())
        sum_rand = rand_prob.sum()
        rand_prob = rand_prob/sum_rand
        new_line.append(rand_prob)


        new_file.append(new_line)


    pass

with open ('rand.txt', 'w') as f_o:
    f_o.writelines(intro_line)
    for line in new_file:
        f_o.writelines(line[0] + '\t')
        f_o.writelines(line[1] + '\t')
        for prob in line[2]:
            f_o.writelines(str(float(prob)) + '\t')

        f_o.writelines('\n')
