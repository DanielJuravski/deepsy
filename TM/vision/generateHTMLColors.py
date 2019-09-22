import numpy as np
import yaml
import matplotlib.pyplot as plt
from matplotlib import colors

TOPICS_NUM = 100
FILE_NAME = str(TOPICS_NUM) + '_HMTL_colors.yml'


def plotColors(i_colors):
    # TODO: which colors were generated
    pass


def generateColors(num_topics):
    print('Generating {} colors ...'.format(num_topics))
    topic_color = {}
    colors = list()
    for t in range(num_topics):
        color = np.random.choice(range(256), size=3)
        colors.append(color)
        color_format = "rgb({0} {1} {2})".format(color[0], color[1], color[2])
        topic_color[str(t)] = color_format

    plotColors(colors)

    return topic_color


def write2File(topic_color):
    print('Exporting to {} file ...'.format(FILE_NAME))
    with open(FILE_NAME, 'w') as f:
        yaml.dump(topic_color, f, default_flow_style=False)


def main():
    topic_color = generateColors(TOPICS_NUM)
    write2File(topic_color)


if __name__ == '__main__':
    main()
