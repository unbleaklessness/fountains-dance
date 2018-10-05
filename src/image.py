from PIL import Image
import sys
import os

CROP_NAME = 'crop'
CROP_EXT = 'png'

def pixel_strips(image_path, output_directory):
    """ Crop image on strips with width 1 and height of the image. """

    image = Image.open(image_path)
    image_width, image_height = image.size
    for i in range(image_width):
        box = (i, 0, i + 1, image_height)
        crop = image.crop(box)
        crop.save(output_directory + CROP_NAME + str(i) + '.' + CROP_EXT)

def count_files_in_directory(directory_path):
    path, dirs, files = next(os.walk(directory_path))
    return len(files)

def crop_name(index):
    """ Get crop name with index. """
    return CROP_NAME + str(index) + '.' + CROP_EXT

def crops_size(crops_path):
    """ Get crops size in the directory. """
    image = Image.open(os.path.join(crops_path, crop_name(0)))
    return image.size

def crops_pixel_data(crops_path):
    """ Returns 2D array with size: N * M, N - image width, M - image height.
    Every element of outer array is N-th crop RGB data.
    Every element of inner array is (R, G, B) tuple of N x M pixel.
    """
    crops_number = count_files_in_directory(crops_path)
    crops_width, crops_height = crops_size(crops_path)
    data = []
    for i in range(crops_number):
        data.append([])
        image = Image.open(os.path.join(crops_path, crop_name(i)))
        rgb_image = image.convert('RGB')
        for j in range(crops_height):
            rgb = rgb_image.getpixel((0, j))
            data[i].append(rgb)
    return data

def main(argv):
    # image_path = argv[0]
    # output_directory = argv[1]
    # pixel_strips(image_path, output_directory)

    crops_path = argv[0]
    data = crops_pixel_data(crops_path)
    print(data[1498])

if __name__ == '__main__': main(sys.argv[1:])
