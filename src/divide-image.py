from PIL import Image
import sys

def divide_image(path, percents):
    image = Image.open(path)
    pixels = image.load()
    image_width, image_height = image.size
    for i in range(image_height):
        pixels[i, ]
    print('true')

def main(argv):
    path = argv[0]
    divide_image(path, 10)

if __name__ == '__main__': main(sys.argv[1:])
