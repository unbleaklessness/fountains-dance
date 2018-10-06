import sys

from final import *

def main(argv):
  music_path = argv[0]
  partitura_path = argv[1]
  create_partiture(music_path, partitura_path)

if __name__ == '__main__': main(sys.argv[1:])