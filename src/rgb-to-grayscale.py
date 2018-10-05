from PIL import Image
import sys

def to_grayscale(from_path, out_path):
    image = Image.open(from_path)
    image = image.convert('RGB')
    pixels = image.load()
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            r, g, b = pixels[i, j]
            value = int(r * 0.8 + g * 0.2 + b * 0.0)
            pixels[i, j] = (value, value, value)
    image.save(out_path)

def main(argv):
    input_path = argv[0]
    output_path = argv[1]
    to_grayscale(input_path, output_path)

if __name__ == '__main__': main(sys.argv[1:])
