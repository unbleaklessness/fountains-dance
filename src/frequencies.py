import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.io import wavfile
import numpy as np
import sys

def get_frequencies(path):

    rate, data = wavfile.read(path)

    time = []
    for index in range(len(data.T[0])):
        time.append(int((1000.0 / rate) * index))

    return [time, data.T[0], data.T[1]]

def plot_frequencies(path):
    frequencies = get_frequencies(path)

    def format_time(x, pos = None):
        seconds = x / 1000
        minutes = seconds // 60
        seconds = seconds % 60
        out = '%d:%d' % (minutes, seconds)
        return out

    figure, axis = plt.subplots()
    axis.plot(frequencies[0], frequencies[1], 'b-', frequencies[0], frequencies[2], 'g-', alpha = 0.5)
    axis.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))

    plt.show()

def frequencies_to_file(source, to):
    frequencies = frequencies(source)

    file = open(to, 'w')
    for index in range(len(frequencies) - 1):
        file.write(str(frequencies[1][index]) + '    ' + frequencies[2][index] + '\n')

    file.close()

def main(argv):
    path = argv[0]

    plot_frequencies(path)
    print(get_frequencies(path))

if __name__ == '__main__': main(sys.argv[1:])
