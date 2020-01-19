
FILE_PATH = "/home/daniel/Documents/Data_Sets/HarryPotter/full.txt"
TARGET_DIR = "/home/daniel/Documents/Data_Sets/HarryPotter/docs/"


def parse():
    docs = []
    with open(FILE_PATH, 'r') as f:
        for line in f:
            if line != '\n':
                line = line[:-2]
                line = line.translate({ord(i):None for i in '!@#$!@#$%^&*())_+-=\][/.,;`~"'})
                docs.append(line)

    for i, doc in enumerate(docs):
        file_name = TARGET_DIR + 'doc' + str(i) + ".txt"
        with open(file_name, 'w') as f:
            f.writelines(doc)
    pass




if __name__ == '__main__':
    parse()