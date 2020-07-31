import numpy
import PIL
from PIL import Image
import os

INPUT_DIR = "input_images"
OUTPUT_DIR = "output_images"

img_path = os.path.join(INPUT_DIR, "1_Sandia.jpg")

# TODO: turn images into numpy arrays then arrange the image to fit 4 by 4 in a larger image

class My_main:
    def __init__(self):
        pass

    def start(self):
        img_1 = Image.new('RGB', (800, 800))
        print("Hello world")
        im = Image.open(img_path)
        im = im.resize((200, 200))
        # img_1.show()
        # im.show()
        new_img = img_1.paste(im)



class Card:
    def __init__(self, name, number, image):
        self.name = name
        self.number = number
        self.image = image
        self.img_size = [200, 200]


m = My_main
m.start(m)
