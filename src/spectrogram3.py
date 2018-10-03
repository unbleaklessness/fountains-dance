import os
import wave
import pylab
import sys
from PIL import Image, ImageChops

def graph_spectrogram(wav_file):
    sound_info, frame_rate = get_wav_info(wav_file)
    pylab.figure(num = None, figsize = (19, 12))
    pylab.subplot(111)
    pylab.specgram(sound_info, Fs = frame_rate)
    pylab.show()

def trim_whitespace(path):
    im = Image.open(path)
    print("TES")
    bg = Image.new(im.mode, im.size, 'rgb(255,255,255)')
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox: return im.crop(bbox)
    im.save(path + '1')

def save_spectrogram(wav_file, spectrogram_path):
    sound_info, frame_rate = get_wav_info(wav_file)
    pylab.figure(num = None, figsize = (19, 12), frameon = False)
    pylab.subplot(111)
    pylab.specgram(sound_info, Fs = frame_rate)
    pylab.gca().get_yaxis().set_visible(False)
    pylab.gca().get_xaxis().set_visible(False)
    pylab.gca().set_yticklabels([])
    pylab.gca().set_xticklabels([])
    pylab.gca().set_axis_off()
    pylab.axis('off')
    pylab.autoscale(False)
    pylab.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
    # extent = pylab.gca().get_window_extent().transformed(pylab.gcf().dpi_scale_trans.inverted())
    pylab.savefig(spectrogram_path, bbox_inches = 'tight', pad_inches = -0.05)
    # pylab.savefig(spectrogram_path, bbox_inches='tight', pad_inches = -0.05)

def get_wav_info(wav_file):
    wav = wave.open(wav_file, 'r')
    frames = wav.readframes(-1)
    sound_info = pylab.fromstring(frames, 'int16')
    frame_rate = wav.getframerate()
    wav.close()
    return sound_info, frame_rate

def main(argv):
    wav_path = argv[0]
    spectrogram_path = argv[1]
    save_spectrogram(wav_path, spectrogram_path)
    trim_whitespace(spectrogram_path)

if __name__ == '__main__': main(sys.argv[1:])
