import numpy as np
from scipy.signal import argrelextrema
import sys

from frequencies import *
from fountain import *
from image import get_pixel_data
from track import track_duration_seconds

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

        fountain = Fountain()
        duration = track_duration_seconds(self.music_path)
        print(duration)

        commands.append(fountain.turn_on_pumps(0, 8))

        pixels = get_pixel_data('../moonlight_spectrogram.png')
        height = len(pixels)
        width = len(pixels[0])

        strips = []
        for i in range(5): strips.append([])

        def get_percents(steps):
            percents = []
            value = 1 / steps
            for i in range(steps):
                percents.append(round(value * i, 2))
            return percents


        def percentage(number, other_number): return (number * 100) / other_number

        for i in range(height):
            percent = percentage(i, height)
            if percent < 10: strips[0].append(pixels[i])
            elif percent < 40: strips[1].append(pixels[i])
            elif percent < 60: strips[2].append(pixels[i])
            elif percent < 80: strips[3].append(pixels[i])
            else: strips[4].append(pixels[i])

        avg_strips = []

        def average_column(table, column_number):
            avg = 0
            for e in table:
                v, r, g, b = e[column_number]
                avg += v
            avg /= len(table)
            return avg

        for i in range(len(strips)):
            avg_strips.append([])
            for j in range(len(strips[i])):
                avg_strips[i].append(average_column(strips[i], j))

        small_avg = []

        for i in range(len(avg_strips[1]) - 5):
            small_avg.append(avg_strips[1][i] + avg_strips[1][i + 1] + avg_strips[1][i + 2] + avg_strips[1][i + 3] + avg_strips[1][i + 4])

        print(len(small_avg))

#        for i in range(len(small_avg)):
#            commands.append(fountain.open_valves()

        self.output(commands)

def main(argv):
    music_path = argv[0]
    partitura_path = argv[1]
    generator = Generator(music_path, partitura_path)
    generator.algorithm_1122()

if __name__ == '__main__': main(sys.argv[1:])