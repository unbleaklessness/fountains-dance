import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.fftpack import fft
from scipy.io import wavfile
import numpy as np
import sys

def get_frequencies(path):

    rate, data = wavfile.read(path)

    a1 = data.T[0]
    # b1 = [(e / 2 ** 15.) * 2 - 1 for e in a1]
    # c1 = fft(b1)
    c1 = fft(a1)
    d1 = int(len(c1) / 2)

    time = []
    for index in range(len(c1[:(d1 - 1)])):
        time.append(int((1000.0 / rate) * index))

    a2 = data.T[1]
    # b2 = [(e / 2 ** 15.) * 2 - 1 for e in a2]
    # c2 = fft(b2)
    c2 = fft(a2)
    d2 = int(len(c2) / 2)

    return [time, abs(c1[:(d1 - 1)]), abs(c2[:(d2 - 1)])]

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

def main(argv):
    path = argv[0]
    plot_frequencies(path)

if __name__ == '__main__': main(sys.argv[1:])
