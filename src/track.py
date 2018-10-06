import sys
import wave

def track_duration_seconds(path):
    file = wave.open(path)
    frames = file.getnframes()
    rate = file.getframerate()
    duration = frames / float(rate)
    return int(duration)

def main(argv):
    path = argv[0]
    duration = track_duration_seconds(path)
    print(duration)

if __name__ == '__main__': main(sys.argv[1:])