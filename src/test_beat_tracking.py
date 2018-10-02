import madmom
import librosa
import sys
import numpy as np
import matplotlib.pyplot as plt

from fountain import *
import amplitude as amp

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

    # track_time = 106
    # time_range = []
    # for i in range(106 * 100)
    #     time_range.append(i / 100)
    # t = np.linspace(0, 106, 106 * 100)

    # plt.plot(t, np.array(beat_times))
    # plt.show()


if __name__ == '__main__': main(sys.argv[1:])
