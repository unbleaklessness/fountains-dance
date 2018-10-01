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


    # NAMING EXPLANATION:
    #
    # 0.10  m3x2:pf(70,3)|l3:b
    #
    # WHERE:
    # 0.10 - Time.
    # ' ' - time_delimiter.
    # m - pumps_group_label.
    # 3 - Group number
    # x - circuit_label.
    # 2 - Circuit number.
    # : - group_delimiter.
    # pf - Action name.
    # (70,3) - Action arguments.
    # | - command_delimiterv.
    # ETC...

    color = Colors.none
    power = 0 # 0 ... 100
    max_power = 100
    fluency = 1 # 1, 2, 3...
    time_delimiter = '\t' # Between time and commands.
    group_delimiter = ':' # Between circuit and action.
    command_delimiter = '|' # Between different commands.
    pumps_group_label = 'm'
    valves_group_label = 'k'
    backlight_group_label = 'l'
    circuit_label = 'x'

    PUMPS = 0
    VALVES = 1
    BACKLIGHT = 2

    # Method to construct fountain commands.
    #
    # `time` - Command start time.
    # `group` - What kind of group to target: pumps, valves or backlight group.
    # `args` - Every even element is either:
    #            + A pair-tuple of circuit number and pipe number.
    #            + Circuit number only.
    #          Every odd element is either:
    #            + A pair-tuple of action and array of argument for the action.
    #            + A pair-tuple of action and single argument for the action (not array).
    #            + Just action, without argument (not tuple).
    #          You can pass multiple pairs to create complex commands.
    def make_command(self, time, group, *args):
        if len(args) % 2 != 0 or len(args) < 2:
            print('Wrong number of arguments for `make_command` method!')
            return

        if group == self.PUMPS: current_group_label = self.pumps_group_label
        elif group == self.VALVES: current_group_label = self.valves_group_label
        elif group == self.BACKLIGHT: current_group_label = self.backlight_group_label

        command = str(time) + self.time_delimiter

        for n in map(lambda x: x * 2, range(len(args) / 2)):

            if type(args[n]) is tuple:
                group, circuit = args[n]
                command += current_group_label +  str(group) + self.circuit_label +  str(circuit)
            else:
                command += current_group_label +  str(args[n])

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

    # Turn on pumps with maximum power.
    def turn_on_pumps(self, time, circuit):
        return self.make_command(time, self.PUMPS, circuit, 'on')

    def turn_off_pumps(self, time, circuit):
        return self.make_command(time, self.PUMPS, circuit, 'off')

    # Set power for the pumps between 0 and 100.
    #
    # `pipe` - Tuple. First element - circuit group number, second - circuit number.
    # `power`
    def set_pumps_power(self, time, circuit, power):
        if power > self.max_power:
            print('Unable to set power above %s'.format(self.max_power))
            return
        return self.make_command(time, self.PUMPS, circuit, ('sf', power))

    def set_pumps_power_fluently(self, time, circuit, power, fluency):
        if power > self.max_power:
            print('Unable to set power above %s'.format(self.max_power))
            return
        return self.make_command(time, self.PUMPS, circuit, ('pf', [power, fluency]))

    def pause_pumps(self, time, circuit, pause_time):
        return self.make_command(time, self.PUMPS, circuit, ('flip', pause_time))
