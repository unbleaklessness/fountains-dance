import numpy as np
from scipy.signal import argrelextrema
import sys
import math

from fountain import *
from image import get_pixel_data
from track import track_duration_seconds
from spectrogram import output_spectrogram

def output_commands(commands, partitura_path):
    ''' Вывести комманды фонтана в файл партитуры. '''
    
    file = open(partitura_path, 'w')
    file.truncate(0)

    for e in commands:
        file.write(e)

    file.close()

def create_partiture(music_path, partitura_path):

    commands = [] # Комманды фонтана

    fountain = Fountain() # Объект для создания комманд фонтана
    duration = track_duration_seconds(music_path) # Длительност трека в секундах

    output_spectrogram(music_path) # Создание спектрограммы
    part_path = music_path[:len(music_path) - 3]
    spectrogram_path = part_path[:len(part_path) - 1] + '_spectrogram.png' # Путь до созданной спектрограммы

    conturs_number = 13 # Количество контуров

    for i in range(1, conturs_number): # Включить насосы на полную мощность и открыть все клапаны
        commands.append(fountain.turn_on_pumps(0, i))
        commands.append(fountain.open_valves(0, i))

    pixels = get_pixel_data(spectrogram_path) # Обработать спектрограмму: извлечь 2D массив пикселей
    height = len(pixels) # Высота спектрограммы
    width = len(pixels[0]) # Ширина спектрограммы

    # track-duration / spectrogram-width
    pixel_time = duration / len(pixels[0]) * 1000 # Сколько один пиксель в ширину вырожает времени

    # Список, который хранит в себе разбитие спектрограммы на 12 частей (разбитие сверху вниз).
    strips = []
    for i in range(conturs_number): strips.append([])

    def get_percents(steps): # Разбить 100% на `steps` частей и записать части в список
        # Пример: `get_percents(3)` => [33, 66, 99]
        percents = []
        value = 1 / steps
        for i in range(steps):
            percents.append(round(value * i, 2) * 100)
        percents = list(map(lambda x: math.floor(x + value * 100), percents))
        return percents

    # Сколько процентов составляет число `number` от числа `other_number`
    def percentage(number, other_number): return (number * 100) / other_number

    percents = get_percents(conturs_number)

    # Разбитие массива спектрограммы на 12 частей по процентам: от 0 до 12%, от 12% до 24%...
    for i in range(height):
        percent = percentage(i, height)
        for j in range(len(percents)):
            if percent < percents[j]:
                strips[j].append(pixels[i])

    # Массив в котором будет хранится средние значения по колонкам из списка `strips`
    avg_strips = []

    def average_column(table, column_number): # Вычислить среднее значение колонки под номером `column_number` из 2D списка
        avg = 0
        for e in table:
            v, r, g, b = e[column_number]
            avg += v
        avg /= len(table)
        return avg

    # Создать список из средних значений по колонкам из списка `strips`
    for i in range(len(strips)):
        avg_strips.append([])
        for j in range(len(strips[i][0])):
            avg_strips[i].append(average_column(strips[i], j))

    small_avg = [] # Уменьщенная версия `avg_strips`, берутся средние значения элементов от i до i + 5 => список в 5 раз меньше чем `avg_strips`

    for i in range(len(avg_strips)):
        small_avg.append([])
        for j in range(int(len(avg_strips[i]) / 5)):
            avg = 0
            for a in range(1, 4):
                avg += avg_strips[i][j + a]
            small_avg[i].append(avg / 5)

    # Берет значение `x` из диапозона от `in_min` до `in_max` и переводит в диапозон `out_min` до `out_max`
    # Пример: `smooth_map(3, 1, 10, 1, 20)` => 6
    def smooth_map(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    smooth_avg = [] # Список `small_avg` с примененным `smooth_map` к каждому элементу

    for i in range(len(small_avg)):
        min_v = min(small_avg[i])
        max_v = max(small_avg[i])
        smooth_avg.append(list(map(lambda x: smooth_map(x, min_v, max_v, 0, 100), small_avg[i])))

    # Увеличить разброс значений в списке `smooth_avg`, чтобы были лучше видны колебания, аналогия: умножение sin на 2
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
    colors = Color.all # Список из всех цветов фонтана

    for i in range(len(smooth_avg[0])):
        coms = []
        for j in range(len(smooth_avg)):
            # Задать можность струи по элементам `smooth_avg`
            coms.append(fountain.set_pumps_power(int(i * pixel_time * 5), j + 1, int(smooth_avg[j][i])))
            # Задать цвета для фонтана
            coms.append(fountain.make_command(int(i * pixel_time * 5), Fountain.BACKLIGHT, j + 1, colors[color_counter]))
            if i % 10: color_counter += 1
            if color_counter >= len(colors): color_counter = 0
        commands.append(fountain.combine(*coms))

    # Удалить комманды, которые выполняются в одну секунду
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

    # Выключить насосы и закрыть клапаны
    for i in range(1, conturs_number):
        commands.append(fountain.turn_off_pumps(duration * 1000, i))
        commands.append(fountain.close_valves(duration * 1000, i))

    # Вывести комманды в партитуру
    output_commands(commands, partitura_path)

def main(argv):
    music_path = argv[0]
    partitura_path = argv[1]
    create_partiture(music_path, partitura_path)

if __name__ == '__main__': main(sys.argv[1:])