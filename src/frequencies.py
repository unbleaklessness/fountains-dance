import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile

def frequencies(path):

    fs, data = wavfile.read(path)

    a = data.T[0]
    b = [(e / 2 ** 8.) * 2 - 1 for e in a]
    c = fft(b)
    d = int(len(c) / 2)

    return abs(c[:(d - 1)])


def plot_frequencies(path):
    f = frequencies(path)

    plt.plot(f, 'r')
    plt.show()

def frequencies_to_file(source, to):
    f = frequencies(source)

    file = open(to, 'w')
    for e in f:
        file.write(str(e) + '\n')
    file.close()
    