import numpy as np
from matplotlib import pyplot as plt
import scipy.io.wavfile as wav
from numpy.lib import stride_tricks
import sys

''' Short time fourier transform of audio signal: '''
def stft(samples, frame_size, overlap_factor = 0.5, window = np.hanning):
    win = window(frame_size)
    hopSize = int(frame_size - np.floor(overlap_factor * frame_size))

    # Zeros at beginning (thus center of 1st window should be for sample nr. 0)
    samples = np.append(np.zeros(int(np.floor(frame_size / 2.0))), samples)
    # Cols for windowing
    cols = np.ceil((len(samples) - frame_size) / float(hopSize)) + 1
    # Zeros at end (thus samples can be fully covered by frames)
    samples = np.append(samples, np.zeros(frame_size))

    frames = stride_tricks.as_strided(samples, shape = (int(cols), frame_size), strides = (samples.strides[0] * hopSize, samples.strides[0])).copy()
    frames *= win

    return np.fft.rfft(frames)

''' Scale frequency axis logarithmically: '''
def logscale_spec(spec, sample_rate = 44100, factor = 20.):
    timebins, freqbins = np.shape(spec)

    scale = np.linspace(0, 1, freqbins) ** factor
    scale *= (freqbins - 1) / max(scale)
    scale = np.unique(np.round(scale))

    # Create spectrogram with new freq bins
    newspec = np.complex128(np.zeros([timebins, len(scale)]))
    for i in range(0, len(scale)):
        if i == len(scale) - 1:
            newspec[:,i] = np.sum(spec[:,int(scale[i]):], axis = 1)
        else:
            newspec[:,i] = np.sum(spec[:,int(scale[i]):int(scale[i + 1])], axis = 1)

    # List center freq of bins
    allfreqs = np.abs(np.fft.fftfreq(freqbins * 2, 1.0 / sample_rate)[:freqbins + 1])
    freqs = []
    for i in range(0, len(scale)):
        if i == len(scale) - 1:
            freqs += [np.mean(allfreqs[int(scale[i]):])]
        else:
            freqs += [np.mean(allfreqs[int(scale[i]):int(scale[i + 1])])]

    return newspec, freqs

''' Plot spectrogram: '''
def plotstft(audiopath, binsize = 2 ** 10, plotpath = None, colormap = 'jet'):
    samplerate, samples = wav.read(audiopath)

    s = stft(samples, binsize)

    sshow, freq = logscale_spec(s, factor = 1.0, sample_rate = samplerate)

    ims = 20.0 * np.log10(np.abs(sshow) / 10e-6) # Amplitude to decibel

    timebins, freqbins = np.shape(ims)

    print('Timebins: ', timebins)
    print('Freqbins: ', freqbins)

    plt.figure(figsize=(15, 7.5))
    plt.imshow(np.transpose(ims), origin = 'lower', aspect = 'auto', cmap = colormap, interpolation = 'none')
    plt.colorbar()

    plt.xlabel('Time (s)')
    plt.ylabel('Frequency (Hz)')
    plt.xlim([0, timebins - 1])
    plt.ylim([0, freqbins])

    xlocs = np.float32(np.linspace(0, timebins - 1, 5))
    plt.xticks(xlocs, ['%.02f' % l for l in ((xlocs * len(samples) / timebins) + (0.5 * binsize)) / samplerate])
    ylocs = np.int16(np.round(np.linspace(0, freqbins - 1, 10)))
    plt.yticks(ylocs, ['%.02f' % freq[i] for i in ylocs])

    if plotpath:
        plt.savefig(plotpath, bbox_inches = 'tight')
    else:
        plt.show()

    plt.clf()

    return ims

def plot_spectrogram(path):
    plotstft('../classic_no_vocal.wav')

def main(argv):
    wav_path = argv[0]
    spectrogram_path = argv[1]
    plot_spectrogram(path)

if __name__ == '__main__': main(sys.argv[1:])
