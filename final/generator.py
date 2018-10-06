import numpy as np
from scipy.signal import argrelextrema
import sys
import math

from fountain import *
from image import get_pixel_data
from track import track_duration_seconds
from spectrogram import output_spectrogram

def output_commands(commands, partitura_path):
    
    file = open(partitura_path, 'w')
    file.truncate(0)

    for e in commands:
        file.write(e)

    file.close()

def create_partiture(music_path, partitura_path):

    commands = []

    fountain = Fountain()
    duration = track_duration_seconds(music_path)

    output_spectrogram(music_path)
    part_path = music_path[:len(music_path) - 3]
    spectrogram_path = part_path[:len(part_path) - 1] + '_spectrogram.png'

    conturs_number = 12

    for i in range(1, conturs_number):
        commands.append(fountain.turn_on_pumps(0, i))
        commands.append(fountain.open_valves(0, i))

    pixels = get_pixel_data(spectrogram_path)
    height = len(pixels)
    width = len(pixels[0])

    pixel_time = duration / len(pixels[0]) * 1000

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
            avg = 0
            for a in range(1, 4):
                avg += avg_strips[i][j + a]
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

    color_counter = 0
    colors = Color.all

    for i in range(len(smooth_avg[0])):
        coms = []
        for j in range(len(smooth_avg)):
            coms.append(fountain.set_pumps_power(int(i * pixel_time * 5) + 1000, j + 1, int(smooth_avg[j][i])))
            coms.append(fountain.make_command(int(i * pixel_time * 5) + 1000, Fountain.BACKLIGHT, j + 1, colors[color_counter]))
            color_counter += 1
            if color_counter >= len(colors): color_counter = 0
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

    for i in range(1, conturs_number):
        commands.append(fountain.turn_off_pumps(duration * 1000, i))
        commands.append(fountain.close_valves(duration * 1000, i))

    output_commands(commands, partitura_path)

def main(argv):
    music_path = argv[0]
    partitura_path = argv[1]
    create_partiture(music_path, partitura_path)

if __name__ == '__main__': main(sys.argv[1:])