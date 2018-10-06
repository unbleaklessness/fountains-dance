import generator
from image import get_pixel_data
from PIL import *
from pychorus import find_and_output_chorus as faoc

def convert_to_millsec(sec):
	return sec * 100

spectr_path = '../../music/slow_vocal_spectrogram.png'
music_path  = '../../music/slow_vocal.wav'


image = Image.open(spectr_path)
image_data = get_pixel_data(spectr_path)
time_start_chorus = faoc(music_path, "../../music/tmp.wav", 15)
time_start_chorus = convert_to_millsec(time_start_chorus)

print(str(len(image_data) - int(time_start_chorus)))

print(' '.join([str(i[0]) for i in image_data[1]]))

#for index_x in range(len(image_data)):
#	for index_y in range(len(image_data[index_x])):