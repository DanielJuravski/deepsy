import sys
from operator import itemgetter


def getOptions():
    if '--input' in sys.argv:
        input_option_i = sys.argv.index('--input')
        file_name = sys.argv[input_option_i + 1]
    else:
        file_name = 'client_5/topics_100.txt'

    if '--output' in sys.argv:
        output_option_i = sys.argv.index('--output')
        output_name = sys.argv[output_option_i + 1]
    else:
        output_name = file_name + '.sorted'

    if '--descent' in sys.argv:
        sort_reverse = True
    else:
        sort_reverse = False

    return file_name, output_name, sort_reverse


def sortTopicsFile(file_name, sort_reverse):
    all_topics = []
    with open(file_name, 'r') as f:
        for line in f:
            line_details = line.split()
            topic_number = line_details[0]
            topic_dist = float(line_details[1])
            topic_words = line_details[2:]
            topic_i_details = (topic_number, topic_dist, topic_words)
            all_topics.append(topic_i_details)

    all_topics.sort(key=itemgetter(1), reverse=sort_reverse)

    return all_topics


def saveTopics(sortedTopics, output_name):
    with open(output_name, 'w') as f:
        for topic in sortedTopics:
            f.write("{0}\t{1}\t".format(topic[0], topic[1]))
            for i in topic[2]:
                f.write("{0} ".format(i))
            f.write("\n")


if __name__ == '__main__':
    '''
    Sorting MALLET --output-topic-keys output.
    The trigger for that script was that the topics' dist is messy,
    I would like to see it in ascend/descend order.
    '''

    input_file_name, output_name, sort_reverse = getOptions()
    sortedTopics = sortTopicsFile(input_file_name, sort_reverse)
    saveTopics(sortedTopics, output_name)

