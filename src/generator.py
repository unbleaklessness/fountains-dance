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

        # freq_first = filter(lambda x: x % 2 == 0, self.freq_first)
        # freq_second = filter(lambda x: x % 2 == 0, self.freq_first)

        for index in range(len(self.freq_first) - 1):
            if index % 1000 == 0:
                commands.append(self.fountain.turn_off_pumps(self.freq_time[index], (counter_1, counter_2)))
                commands.append(self.fountain.close_valves(self.freq_time[index], (counter_1, counter_2)))
            else:
                commands.append(self.fountain.turn_on_pumps(self.freq_time[index], (counter_1, counter_2)))
                commands.append(self.fountain.open_valves(self.freq_time[index], (counter_1, counter_2)))

            counter_1 += 1
            counter_2 -= 1

            if counter_1 > 10: counter_1 = 1
            if counter_2 < 1: counter_2 = 10

        self.output(commands)
