class Colors:
    none = '0'
    red = '1'
    green = '2'
    yellow = '3'
    blue = '4'
    magenta = '5'
    cyan = '6'
    white = '7'

class Fountain:

    color = Colors.none
    power = 0 # 0 ... 100
    fluency = 1 # 1, 2, 3...
    time_delimiter = '\t' # Between time and commands.
    part_delimiter = ':' # Between circuit and action.
    command_delimiter = '|' # Between different commands.
    circuit_label = 'm'
    pipe_label = 'x'

    # Method to construct fountain commands.
    #
    # `time` - Command start time.
    # `args` - Every even element is either a pair of circuit number and pipe number or
    #          circuit number only. Every odd element is an action.
    #          You can pass multiple circuit-action pairs to create a complex command.
    def make_command(self, time, *args):
        if (len(args) % 2 != 0 or len(args) < 2):
            print('Wrong arguments for `make_command` method!')
            return

        command = str(time) + self.time_delimiter

        for n in map(lambda x: x * 2, range(len(args) / 2)):
            if isinstance(args[0], tuple):
                circuit, pipe = args[n]
                command += self.circuit_label + str(circuit) + self.pipe_label + str(pipe) + self.part_delimiter + str(args[n + 1])
            else:
                command += self.circuit_label + str(args[n]) + self.part_delimiter + str(args[n + 1])
            if n != len(args) - 2:
                command += self.command_delimiter

        return command

    # Turn on circuit with maximum power.
    def turn_on_circuit(self, time, circuit):
        return self.make_command(time, circuit, 'on')

    def turn_off_circuit(self, time, circuit):
        return self.make_command(time, circuit, 'off')
