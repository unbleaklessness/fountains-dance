from PIL import Image
import sys

def get_pixel_data(image_path):
    image = Image.open(image_path)
    rgb_image = image.convert('RGB')
    height, width = rgb_image.size
    data = []
    for i in range(width):
        data.append([])
        for j in range(height):
            r, g, b = rgb_image.getpixel((j, i))
            v = int(r * 0.7 + g * 0.2 + b * 0.1)
            data[i].append((v, r, g, b))
    return data

def main(argv):
    path = argv[0]
    data = get_pixel_data(path)

if __name__ == '__main__': main(sys.argv[1:])
