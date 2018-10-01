import madmom
import librosa
import sys
import numpy as np

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
  # path = argv[0]
  # print(get_beat_times(path))

  fountain = Fountain()
  print(fountain.turn_on_circuit(10, 5))
  print(fountain.turn_off_circuit(11, 5))
  print(fountain.make_command(7, 5, 'test', 6, 'test2'))

if __name__ == '__main__': main(sys.argv[1:])
