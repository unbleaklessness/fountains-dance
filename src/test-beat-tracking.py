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
    
    print(fountain.turn_on_pumps(76643653, 5))
    print(fountain.turn_off_pumps(735672, 5))
    print(fountain.set_pumps_power(77546654, (3, 2), 87))
    print(fountain.set_pumps_power_fluently(2573475, (5, 12), 87, 3))
    print(fountain.pause_pumps(2745456, (5, 12), 87))
    print(fountain.open_valves(5546437, 3))
    print(fountain.valves_clockwise(123367, (9, 6), 14, 2))
    print(fountain.valves_counter_clockwise(86543, (7, 2), 3, 19))
    print(fountain.backlight_clockwise(2326274, (7, 2), 3, 19, Color.red))

    print(fountain.make_command(442321, Fountain.PUMPS, 5, 'test', 6, 'test2'))
    print(fountain.make_command(61523513, Fountain.PUMPS, (5, 3), 'aa', (2, 3), 'tasd'))
    print(fountain.make_command(5573644, Fountain.PUMPS, (5, 3), ('aa', [1, 2, 3]), (2, 3), 'tasd'))

if __name__ == '__main__': main(sys.argv[1:])
