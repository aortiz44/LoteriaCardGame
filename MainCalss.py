import numpy as np
import PIL
from PIL import Image
import os
import cv2
from numpy.random._generator import default_rng

INPUT_DIR = "input_images"
OUTPUT_DIR = "output_images"

img_path = os.path.join(INPUT_DIR, "cake.jpg")


# TODO: turn images into numpy arrays then arrange the image to fit 4 by 4 in a larger image

def load_images_from_dir(data_dir, ext=".jpg", size=(180, 180)):
    imagesFiles = [f for f in os.listdir(data_dir) if f.endswith(ext)]

    card_deck = []
    # imgs = []
    count = 0

    for f_name in imagesFiles:
        temp_np_img = np.array(cv2.imread(os.path.join(data_dir, f_name)))
        resize_np_img = cv2.resize(temp_np_img, size)
        # imgs.append(temp_np_img)
        temp_card = Card(f_name, count, resize_np_img)
        card_deck.append(temp_card)
        count += 1

    # imgs = [np.array(cv2.imread(os.path.join(data_dir, f))) for f in imagesFiles]
    # resize_imgs = [cv2.resize(x, size) for x in imgs]
    return card_deck


class My_main:
    def __init__(self):
        Card_Deck = []
        pass

    def start(self):
        # Create 54 cards

        bg_size = 800
        offset = 20

        background_img = Image.new('RGB', (bg_size, bg_size))
        im = Image.open(img_path)

        img_size = int(bg_size / 4) - offset
        im = im.resize((img_size, img_size))
        top_range = bg_size + int(bg_size / 4) + int(offset / 2)
        for i in range(int(offset / 2), top_range, int(bg_size / 4)):
            for j in range(int(offset / 2), top_range, int(bg_size / 4)):
                background_img.paste(im, (i, j))

        background_img.show()
        save_path = os.path.join(OUTPUT_DIR, 'Loteria_card.jpg')
        background_img.save(save_path)

    def Create_Deck(self):
        # Read the images and resize them from directory
        c_d = load_images_from_dir(INPUT_DIR, ext=".jpg", size=(180, 180))
        for elem in c_d:
            print(np.shape(elem.image))
            print(str(elem.number), elem.name)
            # cv2.imshow(str(elem.number) + elem.name, elem.image)
            # cv2.waitKey(0)
        self.Card_Deck = c_d
        return

    def Create_Card(self, num_list):
        img_name_list = self.GetCardsFromList(num_list)
        # print(img_name_list)
        bg_size = 800
        offset = 20

        background_img = Image.new('RGB', (bg_size, bg_size))

        top_range = bg_size + int(bg_size / 4) + int(offset / 2)
        index = 0

        for i in range(int(offset / 2), top_range, int(bg_size / 4)):
            for j in range(int(offset / 2), top_range, int(bg_size / 4)):
                if index < len(img_name_list):

                    # img_p = os.path.join(INPUT_DIR, str(img_name_list[index]))
                    # im = Image.open(img_p)
                    # TODO images are coming out blue fix that issue probably during the conversion
                    im = Image.fromarray(img_name_list[index].astype('uint8'), 'RGB')
                    # img_list[index]
                    background_img.paste(im, (i, j))
                    index += 1

        background_img.show()
        save_path = os.path.join(OUTPUT_DIR, 'Loteria_card.jpg')
        background_img.save(save_path)

    def GetCardsFromList(self, num_list):
        img_name_list = []
        for i in num_list:
            for elem in self.Card_Deck:
                if elem.number == i:
                    img_name_list.append(elem.image)
                    print(elem.name)
            # print(elem.name)

        return img_name_list


class Card:
    def __init__(self, name, number, image):
        self.name = name
        self.number = number
        self.image = image
        self.size = np.shape(image)


cards_made = []

m = My_main()
m.start()
m.Create_Deck()

# Pick 16 Random Cards
rng = default_rng()
random_array = rng.choice(17, size=16, replace=False)  # numbers 0 - 53
# random_array = np.random.randint(low=1, high=54, size=16)
random_array = np.array(random_array)
print(random_array)

# Make sure that other Cards previously made don't have at least 4 of the Cards in common
# if len(cards_made) <= 0:
# Create a new card

m.Create_Card(random_array)

# else:
#     # pick new random array
#     rng = default_rng()
#     random_array = rng.choice(17, size=16, replace=False)  # numbers 0 - 53
#     print(random_array)
