import numpy as np
from scipy.signal import argrelextrema
import sys
import math

from fountain import *
from image import get_pixel_data
from track import track_duration_seconds
from pattern import Patterns

class Generator:

    def __init__(self, music_path, partitura_path):
        self.music_path = music_path
        self.partitura_path = partitura_path
        self.fountain = Fountain()

    def output(self, array):
        file = open(self.partitura_path, 'w')
        file.truncate(0)

        for e in array:
            file.write(e)

        file.close()


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

        for i in range(1, 6):
            commands.append(fountain.turn_on_pumps(0, i))
            commands.append(fountain.open_valves(0, i))

        pixels = get_pixel_data('../moonlight_spectrogram.png')
        height = len(pixels)
        width = len(pixels[0])

        elem_time = duration / len(pixels[0]) * 1000

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

        def smooth_map(x, in_min, in_max, out_min, out_max):
            return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

        for i in range(len(avg_strips)):
            small_avg.append([])
            for j in range(len(avg_strips[i]) - 5):
                avg = avg_strips[i][j] + avg_strips[i][j + 1] + avg_strips[i][j + 2] + avg_strips[i][j + 3] + avg_strips[i][j + 4]
                small_avg[i].append(avg / 5)

        for i in range(len(small_avg)):
            small_avg_min = min(small_avg[i]) + 1
            small_avg_max = max(small_avg[i])
            small_avg[i] = list(map(lambda x: smooth_map(x, small_avg_min, small_avg_max, 0, 100), small_avg[i]))

        for i in range(len(small_avg[0])):
            commands.append(fountain.combine(
                fountain.set_pumps_power(int(i * elem_time), 1, int(small_avg[0][i])),
                fountain.set_pumps_power(int(i * elem_time), 2, int(small_avg[1][i])),
                fountain.set_pumps_power(int(i * elem_time), 3, int(small_avg[2][i])),
                fountain.set_pumps_power(int(i * elem_time), 4, int(small_avg[3][i])),
                fountain.set_pumps_power(int(i * elem_time), 5, int(small_avg[4][i]))
            ))

        self.output(commands)

    def algorithm_1123(self):

        commands = []

        fountain = Fountain()
        duration = track_duration_seconds(self.music_path)

        for i in range(1, 6):
            commands.append(fountain.turn_on_pumps(0, i))
            commands.append(fountain.open_valves(0, i))

        pixels = get_pixel_data('../moonlight_spectrogram.png')
        height = len(pixels)
        width = len(pixels[0])

        elem_time = duration / len(pixels[0]) * 1000

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
            for j in range(len(strips[i][0])):
                avg_strips[i].append(average_column(strips[i], j))

        small_avg = []

        for i in range(len(avg_strips)):
            small_avg.append([])
            for j in range(int(len(avg_strips[i]) / 5)):
                avg = avg_strips[i][j] + avg_strips[i][j + 1] + avg_strips[i][j + 2] + avg_strips[i][j + 3] + avg_strips[i][j + 4]
                small_avg[i].append(avg / 5)

        def smooth_map(x, in_min, in_max, out_min, out_max):
            return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

        smooth_avg = []

        for i in range(len(small_avg)):
            min_v = min(small_avg[i])
            max_v = max(small_avg[i])
            smooth_avg.append(list(map(lambda x: smooth_map(x, min_v, max_v, 0, 100), small_avg[i])))

        for i in range(len(smooth_avg[0])):
            commands.append(fountain.combine(
                fountain.set_pumps_power(int(i * elem_time * 5), 1, int(smooth_avg[0][i])),
                fountain.set_pumps_power(int(i * elem_time * 5), 2, int(smooth_avg[1][i])),
                fountain.set_pumps_power(int(i * elem_time * 5), 3, int(smooth_avg[2][i])),
                fountain.set_pumps_power(int(i * elem_time * 5), 4, int(smooth_avg[3][i])),
                fountain.set_pumps_power(int(i * elem_time * 5), 5, int(smooth_avg[4][i]))
            ))

        self.output(commands)

    def algorithm_1124(self):

        commands = []

        plot_spectrogram(music_path, save = True, info = False)
        spectrogram_path = music_path[:len(music_path) - 3] + '_spectrogram.png'

        fountain = Fountain()
        duration = track_duration_seconds(self.music_path)

        conturs_number = 13

        for i in range(1, conturs_number):
            commands.append(fountain.turn_on_pumps(0, i))
            commands.append(fountain.open_valves(0, i))

        pixels = get_pixel_data(spectrogram_path)
        height = len(pixels)
        width = len(pixels[0])

        elem_time = duration / len(pixels[0]) * 1000

        strips = []
        for i in range(conturs_number): strips.append([])

        def get_percents(steps):
            percents = []
            value = 1 / steps
            for i in range(steps):
                percents.append(round(value * i, 2) * 100)
            percents = list(map(lambda x: math.floor(x + value * 100), percents))
            return percents

        def percentage(number, other_number): return (number * 100) / other_number

        percents = get_percents(conturs_number)

        for i in range(height):
            percent = percentage(i, height)
            for j in range(len(percents)):
                if percent < percents[j]:
                    strips[j].append(pixels[i])

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
            for j in range(len(strips[i][0])):
                avg_strips[i].append(average_column(strips[i], j))

        small_avg = []

        for i in range(len(avg_strips)):
            small_avg.append([])
            for j in range(int(len(avg_strips[i]) / 5)):
                avg = avg_strips[i][j] + avg_strips[i][j + 1] + avg_strips[i][j + 2] + avg_strips[i][j + 3] + avg_strips[i][j + 4]
                small_avg[i].append(avg / 5)

        def smooth_map(x, in_min, in_max, out_min, out_max):
            return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

        smooth_avg = []

        for i in range(len(small_avg)):
            min_v = min(small_avg[i])
            max_v = max(small_avg[i])
            smooth_avg.append(list(map(lambda x: smooth_map(x, min_v, max_v, 0, 100), small_avg[i])))

        for i in range(len(smooth_avg)):
            for j in range(len(smooth_avg[i]) - 1):
                first_val = 0
                second_val = 0
                if smooth_avg[i][j] > smooth_avg[i][j + 1]:
                    first_val = smooth_avg[i][j] * 1.1
                    second_val = smooth_avg[i][j + 1] * 0.9
                else:
                    first_val = smooth_avg[i][j] * 0.9
                    second_val = smooth_avg[i][j + 1] * 1.1
                if first_val > 100: first_val = 100   
                if first_val < 0: first_val = 0
                if second_val > 100: second_val = 100
                if second_val < 0: second_val = 0
                smooth_avg[i][j] = first_val
                smooth_avg[i][j + 1] = second_val
#                new_value = smooth_avg[i][j] * 1.0
#                if new_value > 100: new_value = 100
#                smooth_avg[i][j] = new_value                

        for i in range(len(smooth_avg[0])):
            coms = []
            for j in range(len(smooth_avg)):
                coms.append(fountain.set_pumps_power(int(i * elem_time * 5), j + 1, int(smooth_avg[j][i])))
            commands.append(fountain.combine(*coms))

        def filter_commands(commands):
            remove_indexes = []
            last = -1
            for i in range(len(commands)):
                current = int(commands[i].split('.')[0])
                if current == last: remove_indexes.append(i)
                last = current
            for e in reversed(remove_indexes):
                del commands[e]

        filter_commands(commands)

#        def eloquentify_commands(commands):
#            for i in range(len(commands)):
#                commands[i] = map
                

#        eloquentify_commands(commands)

        self.output(commands)

    def algorithm_1125(self):

        commands = []

        fountain = Fountain()
        duration = track_duration_seconds(self.music_path)

        conturs_number = 12

        for i in range(1, conturs_number):
            commands.append(fountain.turn_on_pumps(0, i))
            commands.append(fountain.open_valves(0, i))

        pixels = get_pixel_data('../moonlight_spectrogram.png')
        height = len(pixels)
        width = len(pixels[0])

        elem_time = duration / len(pixels[0]) * 1000

        strips = []
        for i in range(conturs_number): strips.append([])

        def get_percents(steps):
            percents = []
            value = 1 / steps
            for i in range(steps):
                percents.append(round(value * i, 2) * 100)
            percents = list(map(lambda x: math.floor(x + value * 100), percents))
            return percents

        def percentage(number, other_number): return (number * 100) / other_number

        percents = get_percents(conturs_number)

        for i in range(height):
            percent = percentage(i, height)
            for j in range(len(percents)):
                if percent < percents[j]:
                    strips[j].append(pixels[i])

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
            for j in range(len(strips[i][0])):
                avg_strips[i].append(average_column(strips[i], j))

        small_avg = []

        for i in range(len(avg_strips)):
            small_avg.append([])
            for j in range(int(len(avg_strips[i]) / 5)):
                avg = avg_strips[i][j] + avg_strips[i][j + 1] + avg_strips[i][j + 2] + avg_strips[i][j + 3] + avg_strips[i][j + 4]
                small_avg[i].append(avg / 5)

        def smooth_map(x, in_min, in_max, out_min, out_max):
            return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;

        smooth_avg = []

        for i in range(len(small_avg)):
            min_v = min(small_avg[i])
            max_v = max(small_avg[i])
            smooth_avg.append(list(map(lambda x: smooth_map(x, min_v, max_v, 0, 100), small_avg[i])))

        for i in range(5, 12):
            for j in range(len(smooth_avg[i]) - 1):
                first_val = 0
                second_val = 0
                if smooth_avg[i][j] > smooth_avg[i][j + 1]:
                    first_val = smooth_avg[i][j] * 1
                    second_val = smooth_avg[i][j + 1] * 0.7
                else:
                    first_val = smooth_avg[i][j] * 0.7
                    second_val = smooth_avg[i][j + 1] * 1
                if first_val > 100: first_val = 100   
                if first_val < 0: first_val = 0
                if second_val > 100: second_val = 100
                if second_val < 0: second_val = 0
                smooth_avg[i][j] = first_val
                smooth_avg[i][j + 1] = second_val         

        for i in range(0, 4):
            for j in range(len(smooth_avg[i]) - 1):
                first_val = 0
                second_val = 0
                if smooth_avg[i][j] > smooth_avg[i][j + 1]:
                    first_val = smooth_avg[i][j] * 1
                    second_val = smooth_avg[i][j + 1] * 0.5
                else:
                    first_val = smooth_avg[i][j] * 0.5
                    second_val = smooth_avg[i][j + 1] * 1
                if first_val > 100: first_val = 100   
                if first_val < 0: first_val = 0
                if second_val > 100: second_val = 100
                if second_val < 0: second_val = 0
                smooth_avg[i][j] = first_val
                smooth_avg[i][j + 1] = second_val         

        patterns = Patterns()

        for i in range(len(smooth_avg[0])):
            coms = []
            for j in range(len(smooth_avg)):
                coms.append(fountain.set_pumps_power(int(i * elem_time * 5) + 1000, j + 1, int(smooth_avg[j][i])))
            commands.append(fountain.combine(*coms))

        def filter_commands(commands):
            remove_indexes = []
            last = -1
            for i in range(len(commands)):
                current = int(commands[i].split('.')[0])
                if current == last: remove_indexes.append(i)
                last = current
            for e in reversed(remove_indexes):
                del commands[e]

        filter_commands(commands)

#        for i in range(len(smooth_avg[0])):
#            avg = 0
#            for j in range(len(smooth_avg)):
#                avg += smooth_avg[j][i]
#            if avg < 600:
#                pats = patterns.get_pattern(int(i * elem_time * 5) + 1000, 3 * 1000, 1)
#                for e in pats: commands.append(e)

        for i in range(1, conturs_number):
            commands.append(fountain.turn_off_pumps(duration * 1000, i))
            commands.append(fountain.close_valves(duration * 1000, i))

        self.output(commands)


    def _algorithm_(self):
        command = []
        fountain = Fountain()
        duration = track_duration_seconds(self.music_path)


        commands.append(fountain.turn_on_pumps(0, 1))
        commands.append(fountain.open_valves(0, 1))

        pixels = get_pixel_data('../moonlight_spectrogram.png')
        height = len(pixels)
        width = len(pixels[0])

        elem_time = duration / len(pixels[0]) * 1000

        strips = []


def main(argv):
    music_path = argv[0]
    partitura_path = argv[1]
    generator = Generator(music_path, partitura_path)
    generator.algorithm_1125()

if __name__ == '__main__': main(sys.argv[1:])