import numpy as np
from scipy.signal import argrelextrema

from frequencies import *
from fountain import *

class Generator:

    def __init__(self, music_path, partitura_path):
        self.music_path = music_path
        self.partitura_path = partitura_path
        self.fountain = Fountain()

        freq_data = get_frequencies(music_path)
        self.freq_time = freq_data[0]
        self.freq_first = freq_data[1]
        self.freq_second = freq_data[2]

    def output(self, array):
        file = open(self.partitura_path, 'w')
        file.truncate(0)

        for e in array:
            file.write(e)

        file.close()

    def algorithm_1(self):

        commands = []

        counter_1 = 1
        counter_2 = 10
        counter_3 = 0

        for index in range(len(self.freq_first) - 1):
            if index % 10000 == 0:
                if counter_3 % 2 == 0:
                    commands.append(self.fountain.turn_off_pumps(self.freq_time[index], counter_1))
                    commands.append(self.fountain.close_valves(self.freq_time[index], counter_1))
                else:
                    commands.append(self.fountain.turn_on_pumps(self.freq_time[index], counter_2))
                    commands.append(self.fountain.open_valves(self.freq_time[index], counter_2))

                counter_1 += 1
                counter_2 -= 1
                counter_3 += 1

                if counter_1 > 10: counter_1 = 1
                if counter_2 < 1: counter_2 = 10

        self.output(commands)


    def algorithm_3742(self):

        commands = []

        # minimums = argrelextrema(self.freq_first, np.less)[0]
        maximums = argrelextrema(self.freq_first, np.greater)[0].tolist()[1::50]

        work_group = 8
        commands.append(self.fountain.turn_on_pumps(0, work_group))

        i = 0
        for e in maximums:
            if i % 2 == 0: del maximums[i]
            if i != len(maximums) and maximums[i] - maximums[i + 1] < 5000: del maximums[i]
            i += 1

        last_time = 0
        for e in maximums:
            if last_time > self.freq_time[e] - 500: continue
            commands.append(self.fountain.open_valves(self.freq_time[e], work_group))
            last_time = self.freq_time[e] + 1000
            commands.append(self.fountain.close_valves(last_time, work_group))

        self.output(commands)

    def algorithm_1122(self):

        commands = []

        

        self.output(commands)