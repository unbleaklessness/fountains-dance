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
    max_power = 100
    fluency = 1 # 1, 2, 3...
    time_delimiter = '\t' # Between time and commands.
    group_delimiter = ':' # Between circuit and action.
    command_delimiter = '|' # Between different commands.
    circuit_group_label = 'm'
    circuit_label = 'x'

    # Method to construct fountain commands.
    #
    # `time` - Command start time.
    # `args` - Every even element is either a pair of circuit number and pipe number or
    #          circuit number only.
    #          Every odd element is either:
    #          + A pair-tuple of action and array of argument for the action.
    #          + A pair-tuple of action and single argument for the action (not array).
    #          + Just action, without argument (not tuple).
    #          You can pass multiple pairs to create a complex commands.
    def make_command(self, time, *args):
        if len(args) % 2 != 0 or len(args) < 2:
            print('Wrong arguments for `make_command` method!')
            return

        command = str(time) + self.time_delimiter

        for n in map(lambda x: x * 2, range(len(args) / 2)):

            if type(args[n]) is tuple:
                group, circuit = args[n]
                command += self.circuit_group_label +  str(group) + self.circuit_label +  str(circuit)
            else:
                command += self.circuit_group_label +  str(args[n])

            command += self.group_delimiter

            if type(args[n + 1]) is tuple:
                action, arguments = args[n + 1]
                command += action + '('

                if type(arguments) is list:
                    for i in range(len(arguments)):
                        command += str(arguments[i])
                        if i < len(arguments) - 1: command += ','
                else:
                    command += str(arguments)

                command += ')'
            else:
                command += args[n + 1]

            if n != len(args) - 2:
                command += self.command_delimiter

        return command

    # Turn on circuit with maximum power.
    def turn_on_circuit(self, time, circuit):
        return self.make_command(time, circuit, 'on')

    def turn_off_circuit(self, time, circuit):
        return self.make_command(time, circuit, 'off')

    # Set power for the pipe between 0 and 100.
    #
    # `pipe` - Tuple. First element - circuit group number, second - circuit number.
    # `power`
    def set_circuit_power(self, time, circuit, power):
        if power > self.max_power:
            print('Unable to set power above %s'.format(self.max_power))
            return
        return self.make_command(time, circuit, ('sf', power))
