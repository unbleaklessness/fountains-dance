import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import sys
from pydub import AudioSegment

def stereo_to_mono(path):
    sound = AudioSegment.from_wav("/path/to/file.wav")
    sound = sound.set_channels(1)
    sound.export("/output/path.wav", format="wav")

def plot_spectrogram(path):
    sample_rate, samples = wavfile.read(path)
    frequencies, times, spectrogram = signal.spectrogram(samples.T[1], sample_rate)

    print(sample_rate)

    plt.pcolormesh(times, frequencies, spectrogram)
    plt.imshow(spectrogram)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()

def main(argv):
    path = argv[0]
    plot_spectrogram(path)

if __name__ == '__main__': main(sys.argv[1:])
