import os


#######################################################################################
# That script iterates over giver dir, and make every file in it to a virtual sentence.
# As a result, each all those sentences will be as a single file.
#######################################################################################



sens = []

documents_dir_name = '/home/daniel/deepsy/TM/client_5_mini_turns/'
dir = os.fsencode(documents_dir_name)
for doc in os.listdir(dir):
    doc_name = os.fsdecode(doc)
    doc_full_path = documents_dir_name + str(doc_name)
    # print('loading document: {0}'.format(doc_name))

    with open(doc_full_path, 'r') as f:
        doc_words = f.read().split()
        sens.append(doc_words)

with open('sentences.txt', 'w') as f:
    for s in sens:
        for w in s:
            f.write(w + ' ')
        f.write('\n')

