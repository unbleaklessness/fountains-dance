from generator import *

def main():
    generator = Generator('../kill-the-universe.wav', '../partitura.txt')
    generator.algorithm_3742()
    print('DONE!')

if __name__ == '__main__': main()
