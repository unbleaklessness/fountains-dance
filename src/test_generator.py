from generator import *

def main():
    generator = Generator('../music/kill-the-universe.wav', '../partitura.txt')
    generator.algorithm_1()
    print('DONE!')

if __name__ == '__main__': main()
