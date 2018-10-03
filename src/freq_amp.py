# Source: https://stackoverflow.com/questions/23377665/python-scipy-fft-wav-files

import scipy.io.wavfile as wavfile
import scipy
import scipy.fftpack
import numpy as np
from matplotlib import pyplot as plt
import sys

def plot_freq_amp(path):
    fs_rate, signal = wavfile.read(path)
    l_audio = len(signal.shape)

    if l_audio == 2:
        signal = signal.sum(axis = 1) / 2

    N = signal.shape[0]
    secs = N / float(fs_rate)
    Ts = 1.0 / fs_rate
    t = scipy.arange(0, secs, Ts)

    FFT = abs(scipy.fft(signal))
    FFT_side = FFT[range(N/2)]
    freqs = scipy.fftpack.fftfreq(signal.size, t[1]-t[0])

    fft_freqs = np.array(freqs)
    freqs_side = freqs[range(N/2)]
    fft_freqs_side = np.array(freqs_side)

    plt.subplot(311)
    p1 = plt.plot(t, signal, 'g')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')

    plt.subplot(312)
    p2 = plt.plot(freqs, FFT, 'r')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Count DBL-sided')

    plt.show()

def main(argv):
    path = argv[0]
    plot_freq_amp(path)

if __name__ == '__main__': main(sys.argv[1:])
