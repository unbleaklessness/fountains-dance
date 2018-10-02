import fountain as fo

def main():
    fountain = fo.Fountain()

    commands = []

    iter = 1
    turn = False

    for i in range(0, 1000):
        if turn:
            commands.append(fountain.turn_on_pumps(i * 1000, iter))
            commands.append(fountain.open_valves(i * 1000, iter))
        else:
            commands.append(fountain.turn_off_pumps(i * 1000, iter))
            commands.append(fountain.close_valves(i * 1000, iter))

        iter += 1

        if iter == 10: iter = 1

        if i % 50 == 0:
            turn = not turn

    path = '../partitura.txt'
    file = open(path, 'w')
    for e in commands:
        file.write(e)

if __name__ == '__main__': main()
