import os


TRANSCRIPTIONS_DIR = '/home/daniel/Documents/pure_json_Transcriptions'


def main():
    client_he_names = set()

    # get all file names
    file_names = []
    for (dirpath, dirnames, filenames) in os.walk(TRANSCRIPTIONS_DIR):
        file_names.extend(filenames)

    # parse file names
    for file_name in file_names:
        file_name_date_name = file_name.split('.docx.json')[0].split('_')[0]

        # extracting patient name and drop if patient name option is given
        client_name = ''.join([i for i in file_name_date_name if not i.isdigit()])
        client_name_he = client_name
        client_he_names.add(client_name_he)

    # Save to file
    # you need saving rather then printing, since rlt-tlr issues.
    file_name = 'he_names.txt'
    # Write with quotes
    with open (file_name, 'w') as f:
        f.write(str(client_he_names))
        f.write('\n')
    # Write without quotes
    str_2_write = " ".join(name for name in client_he_names)
    with open (file_name, 'a') as f:
        f.write(str(str_2_write))
    print("HE names ere written to {}".format(file_name))




if __name__ == '__main__':
    # That script scans the TRANSCRIPTIONS_DIR directory,
    # gets all the HE letters prefixes of the documents,
    # and save them to a file.
    main()
