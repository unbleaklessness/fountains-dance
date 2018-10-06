class Color:
    """ Colors available for fountain backlight. """

    none = '0'
    red = '1'
    green = '2'
    yellow = '3'
    blue = '4'
    magenta = '5'
    cyan = '6'
    white = '7'

class Fountain:

    color = Color.none # Current backlight color.
    power = 0 # 0 ... 100
    max_power = 100
    fluency = 1 # 1, 2, 3...
    time_delimiter = '\t' # Between time and commands.
    group_delimiter = ':' # Between target group and actions.
    command_delimiter = '|' # Between different commands.
    pumps_group_label = 'm' # Denotes pumps target group.
    valves_group_label = 'k' # Denotes valves target group.
    backlight_group_label = 'l' # Denotes backlight target group.
    circuit_label = 'x' # Placed between group number and circuit number.


    """ TARGET GROUPS: """
    PUMPS = 0
    VALVES = 1
    BACKLIGHT = 2

    def format_milliseconds(self, millis):
        """ Convert `time` in milliseconds to format: `{seconds}.{1/100 of second}`.

        Args:
            millis: Integer. Time in milliseconds.

        Returns:
            str: Converted time in the format: `{seconds}.{1/100 of second}`.
        """

        seconds = millis // 1000
        seconds_rest = int(round((millis % 1000) / 10, 0))
        if seconds_rest // 10 == 0: seconds_rest = str(seconds_rest) + '0'

        return str(seconds) + '.' + str(seconds_rest)

    # def remove_with_same_time(self, commands):
        # return filter(lambda e: len([x for x in commands if lambda n: n.startswith(e.split(self.time_delimiter)[0])]) == 1, commands)

    def make_command(self, time, group, *args):
        """ Method to construct fountain commands.

        Args:
            time: Command start time in milliseconds.
            group: What kind of group to target: pumps, valves or backlight group.
            args: Every even element is either:
                    + A pair-tuple of circuit number and pipe number.
                    + Circuit number only.
                Every odd element is one of the following:
                    + A pair-tuple of action and array of argument for the action.
                    + A pair-tuple of action and single argument for the action (not array).
                    + Just action, without argument (not tuple).
                You can pass multiple pairs to create complex commands.

        Returns:
            str: Constructed command.
        """

        if len(args) % 2 != 0 or len(args) < 2:
            print('Wrong number of arguments for `make_command` method of `Fountain` class!')
            return

        if group == self.PUMPS: current_group_label = self.pumps_group_label
        elif group == self.VALVES: current_group_label = self.valves_group_label
        elif group == self.BACKLIGHT: current_group_label = self.backlight_group_label
        else:
            print('Wrong `group` parameter passed to `make_command` method of `Fountain` class!')
            return

        command = self.format_milliseconds(time) + self.time_delimiter

        for n in map(lambda x: x * 2, range(int(len(args) / 2))):

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

            command += '\n'

        return command

    def combine(self, *args):
        """ Combine multiple commands. Start time of the combined command is a start
        time of the first passed command.
        Number of arguments should be minimum 2.

        Args:
            args: Commands returned from methods of this class. Minimum number: 2.

        Returns:
            str: Combined command.
        """

        if len(args) < 2:
            print('Wrong number of arguments for `combine` method of `Fountain` class!')

        command = ''
        command += args[0].split(self.time_delimiter)[0] + self.time_delimiter

        for e in args:
            part = e.split(self.time_delimiter)[1]
            command += part[:len(part) - 1] + '|'
        command = command[:len(command) - 1]

        return command

    def turn_on_pumps(self, time, target):
        """ Turn pumps off.

        Args:
            time: Start time in milliseconds.
            target: One of the following:
                1. Tuple-pair of group number and circuit number.
                2. Only group number.

        Returns:
            str: Constructed command.
        """

        return self.make_command(time, self.PUMPS, target, 'on')

    def turn_off_pumps(self, time, target):
        """ Sets pumps to maximum power (100).

        Args:
            time: Start time in milliseconds.
            target: One of the following:
                1. Tuple-pair of group number and circuit number.
                2. Only group number.

        Returns:
            str: Constructed command.
        """

        return self.make_command(time, self.PUMPS, target, 'off')

    def set_pumps_power(self, time, target, power):
        """ Sets power for the pumps between 0 and 100.

        Args:
            time: Start time in milliseconds.
            target: One of the following:
                1. Tuple-pair of group number and circuit number.
                2. Only group number.
            power: Power to set. Must be between 0 and 100.

        Returns:
            str: Constructed command.
        """

        if power > self.max_power:
            print('Unable to set power above %s'.format(self.max_power))
            return

        return self.make_command(time, self.PUMPS, target, ('sf', power))

    def set_pumps_power_fluently(self, time, target, power, fluency):
        """ Sets power for the pumps between 0 and 100 with given fluency (1, 2, 3...).

        Args:
            time: Start time in milliseconds.
            target: One of the following:
                1. Tuple-pair of group number and circuit number.
                2. Only group number.
            power: Power to set. Must be between 0 and 100.
            fluency: Fluency to set (1, 2, 3...).

        Returns:
            str: Constructed command.
        """

        if power > self.max_power:
            print('Unable to set power above %s'.format(self.max_power))
            return

        return self.make_command(time, self.PUMPS, target, ('pf', [power, fluency]))

    def pause_pumps(self, time, target, pause_time):
        """ Turn pumps off for a `time`, after that turn pumps on with previous power.

        Args:
            time: Start time in milliseconds.
            target: One of the following:
                1. Tuple-pair of group number and circuit number.
                2. Only group number.
            pause_time: Pause time for pumps  in milliseconds.

        Returns:
            str: Constructed command.
        """

        return self.make_command(time, self.PUMPS, target, ('flip', pause_time))

    def open_valves(self, time, target):
        """ Open valves...

        Args:
            time: Start time in milliseconds.
            target: One of the following:
                1. Tuple-pair of group number and circuit number.
                2. Only group number.

        Returns:
            str: Constructed command.
        """

        return self.make_command(time, self.VALVES, target, 'on')

    def close_valves(self, time, target):
        """ Close valves...

        Args:
            time: Start time in milliseconds.
            target: One of the following:
                1. Tuple-pair of group number and circuit number.
                2. Only group number.

        Returns:
            str: Constructed command.
        """

        return self.make_command(time, self.VALVES, target, 'off')

    def valves_clockwise(self, time, target, delta, count):
        """ Valves opens sequentially with interval `delta` and closes after `delta` * `count`.

        Args:
            time: Start time in milliseconds.
            target: One of the following:
                1. Tuple-pair of group number and circuit number.
                2. Only group number.
            delta: Time between valves switches in milliseconds.
            count: Number of valves that opens simultaneously.

        Returns:
            str: Constructed command.
        """

        return self.make_command(time, self.VALVES, target, ('cw', [delta, count]))

    def valves_counter_clockwise(self, time, target, delta, count):
        """ Valves opens sequentially with interval `delta` and closes after `delta` * `count`.

        Opens counter clockwise.

        Args:
            time: Start time in milliseconds.
            target: One of the following:
                1. Tuple-pair of group number and circuit number.
                2. Only group number.
            delta: Time between valves switches in milliseconds.
            count: Number of valves that opens simultaneously.

        Returns:
            str: Constructed command.
        """

        return self.make_command(time, self.VALVES, target, ('ccw', [delta, count]))

    def valves_chess(self, time, target, delta, count):
        """ Sequentially opens and closes even and odd valves.

        Args:
            time: Start time in milliseconds.
            target: One of the following:
                1. Tuple-pair of group number and circuit number.
                2. Only group number.
            delta: Time between valves switches in milliseconds.
            count: Number of valves in the group.

        Returns:
            str: Constructed command.
        """

        return self.make_command(time, self.VALVES, target, ('chess', [delta, count]))

    def backlight_clockwise(self, time, target, delta, count, color):
        """ Groups lights up sequentially with `color` and interval `delta` and after that
        returns to the original state.

        Args:
            time: Start time in milliseconds.
            target: One of the following:
                1. Tuple-pair of group number and circuit number.
                2. Only group number.
            delta: Time between lighting up of lamp groups in milliseconds.
            count: Number of groups.
            color: Color to enable.

        Returns:
            str: Constructed command.
        """

        return self.make_command(time, self.BACKLIGHT, target, ('cl', [delta, count, color]))

    def backlight_counter_clockwise(self, time, target, delta, count, color):
        """ Groups lights up sequentially with `color` and interval `delta` and after that
        returns to the original state.

        Light up counter clockwise.

        Args:
            time: Start time in milliseconds.
            target: One of the following:
                1. Tuple-pair of group number and circuit number.
                2. Only group number.
            delta: Time between lighting up of lamp groups in milliseconds.
            count: Number of groups.
            color: Color to enable.

        Returns:
            str: Constructed command.
        """

        return self.make_command(time, self.BACKLIGHT, target, ('ccl', [delta, count, color]))
