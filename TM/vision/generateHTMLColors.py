import numpy as np
import yaml
import matplotlib.pyplot as plt
from matplotlib import colors

TOPICS_NUM = 100
FILE_NAME = str(TOPICS_NUM) + '_HMTL_colors.yml'


def plotColors(i_colors):
    # TODO: which colors were generated
    pass


def generateColors():
    print('Generating {} colors ...'.format(TOPICS_NUM))
    topic_color = {}
    colors = list()
    generated_colors = 0
    while generated_colors < TOPICS_NUM:
        color = (np.random.choice(range(256), size=3)).tolist()
        if color in colors:
            continue
        colors.append(color)
        color_format = "rgb({0} {1} {2})".format(color[0], color[1], color[2])
        topic_color[str(generated_colors)] = color_format
        generated_colors += 1

    plotColors(colors)

    return topic_color


def write2File(topic_color):
    print('Exporting to {} file ...'.format(FILE_NAME))
    with open(FILE_NAME, 'w') as f:
        yaml.dump(topic_color, f, default_flow_style=False)


def main():
    topic_color = generateColors()
    write2File(topic_color)


if __name__ == '__main__':
    main()
