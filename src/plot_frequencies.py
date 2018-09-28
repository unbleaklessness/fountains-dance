import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile

def plot_frequencies(path):

    fs, data = wavfile.read(path)
    a = data.T[0]

    b=[(ele / 2 ** 8.) * 2 - 1 for ele in a]
    c = fft(b)
    d = int(len(c)/2)

    plt.plot(abs(c[:(d - 1)]), 'r') 
    plt.show()