import madmom
import librosa
import sys
import numpy as np
import matplotlib.pyplot as plt

from fountain import *

np.seterr(invalid='ignore')

def get_beat_times(path):
    x, sr = librosa.load(path)

    proc = madmom.features.beats.DBNBeatTrackingProcessor(fps=100)
    act = madmom.features.beats.RNNBeatProcessor()(path)

    beat_times = proc(act)

    return beat_times

def beat_times_to_sequence(beat_times):
  sequence = []
  sequence.append('0.00\t')

def main(argv):
    path = argv[0]

    fountain = Fountain()
    beat_times = get_beat_times(path)

    print(beat_times)

    plt.plot(beat_times, range(106))
    plt.show()


if __name__ == '__main__': main(sys.argv[1:])
