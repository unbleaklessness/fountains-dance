import wave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import sys

types = {
    1: np.int8,
    2: np.int16,
    4: np.int32
}

def get_amplitudes(path):

    wav = wave.open(path, mode = 'r')
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()

    w, h = 800, 300
    k = int(nframes / w / 32)
    peak = 256 ** sampwidth / 2

    content = wav.readframes(nframes)
    samples = np.frombuffer(content, dtype = types[sampwidth])

    combined = []

    for n in range(nchannels):
        channel = samples[n::nchannels]

        channel = channel[0::k]
        if nchannels == 1:
            channel = channel - peak

        combined.append(channel)

    return combined

def plot_amplitudes(path):

    wav = wave.open(path, mode = 'r')
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()

    duration = nframes / framerate
    w, h = 800, 300
    k = int(nframes / w / 32)
    DPI = 72
    peak = 256 ** sampwidth / 2

    content = wav.readframes(nframes)
    samples = np.frombuffer(content, dtype = types[sampwidth])

    def format_time(x, pos = None):
        progress = int(x / float(nframes) * duration * k)
        mins, secs = divmod(progress, 60)
        hours, mins = divmod(mins, 60)
        out = '%d:%02d' % (mins, secs)
        if hours > 0:
            out = '%d:' % hours
        return out

    def format_data(x, pos = None):
        if pos == 0: return ''
        if x == 0: return '-inf'
        data = 20 * math.log10(abs(x) / float(peak))
        return int(data)

    plt.figure(1, figsize = (float(w) / DPI, float(h) / DPI), dpi = DPI)
    plt.subplots_adjust(wspace = 0, hspace = 0)

    for n in range(nchannels):
        channel = samples[n::nchannels]

        channel = channel[0::k]
        if nchannels == 1:
            channel = channel - peak

        axis = plt.subplot(2, 1, n + 1)
        axis.plot(channel, 'g')
        axis.yaxis.set_major_formatter(ticker.FuncFormatter(format_data))
        plt.grid(True, color = 'w')
        axis.xaxis.set_major_formatter(ticker.NullFormatter())

    axis.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
    plt.show()

def main(argv):
    path = argv[0]
    plot_amplitudes(path)
    print(get_amplitudes(path))

if __name__ == '__main__': main(sys.argv[1:])
