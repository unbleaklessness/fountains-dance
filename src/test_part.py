from fountain import *
from image import get_pixel_data
import sys
'''
f = Fountain()
c = []
c.append(f.turn_on_pumps(1000, (2, 10)))
c.append(f.turn_off_pumps(2000, (2,10)))
c.append(f.set_pumps_power(3421, (1,8), 20))
c.append(f.set_pumps_power_fluently(5041, (3,12), 40,4))
c.append(f.pause_pumps(7810,2, 5000))
c.append(f.open_valves(8912, (3,1)))
c.append(f.close_valves(1241,(3,1)))
c.append(f.valves_clockwise(1523,(1,12),3,8))
c.append(f.valves_counter_clockwise(1791,(3),5,7))
c.append(f.valves_chess(1902,1,5,7))
c.append(f.backlight_clockwise(2141, (1,12),5,7,1))
c.append(f.backlight_counter_clockwise(2141, (1,12),5,7,1))
'''
def main(argv):
	#music_path = argv[0]
	image_path = argv[0]
	data = get_pixel_data(image_path)
	for i in range(len(data)):
		red = 0
		for j in range(len(data[i])):
			if data[i][j][1] >= 200 and data[i][j][2] <= 100 and data[i][j][3] == 0:
				red += 1
		print(red)
	print("Mass: " + str(len(data)))

if __name__ == '__main__': main(sys.argv[1:])
#for i in range(len(c)):
#	print(c[i])