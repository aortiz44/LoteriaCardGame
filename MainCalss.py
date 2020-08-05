import numpy as np
import PIL
from PIL import Image
import os
import cv2
from numpy.random._generator import default_rng

INPUT_DIR = "input_images"
OUTPUT_DIR = "output_images"

img_path = os.path.join(INPUT_DIR, "cake.jpg")


def load_images_from_dir(data_dir, ext=".jpg", size=(180, 180)):
    imagesFiles = [f for f in os.listdir(data_dir) if f.endswith(ext)]

    card_deck = []
    count = 0

    for f_name in imagesFiles:
        temp_np_img = np.array(cv2.imread(os.path.join(data_dir, f_name)))
        RGB_img = cv2.cvtColor(temp_np_img, cv2.COLOR_BGR2RGB)
        resize_np_img = cv2.resize(RGB_img, size)
        # imgs.append(temp_np_img)
        temp_card = Card(f_name, count, resize_np_img)
        card_deck.append(temp_card)
        count += 1

    # imgs = [np.array(cv2.imread(os.path.join(data_dir, f))) for f in imagesFiles]
    # resize_imgs = [cv2.resize(x, size) for x in imgs]
    return card_deck

# TODO fix the size so that it can work with a rectangle instead of a square
# change width to 2250 pixels by height 3000, that's the max of a 8.5 by 11 paper

class My_main:
    def __init__(self):
        self.deck = Deck((230, 230))
        self.new_card_size = 1000
        self.new_card_offset = 10
        self.new_card_length = 4
        self.cards_made = []
        self.card_made_values = []
        self.card_num_to_make = 2
        pass

    def Start(self):
        # for elem in self.deck.card_list:
        #     print(np.shape(elem.image))
        #     print(str(elem.number), elem.name)
        #     # cv2.imshow(str(elem.number) + elem.name, elem.image)
        #     # cv2.waitKey(0)

        name_index = 0
        for i in range(self.card_num_to_make):
            # Pick 16 Random Cards
            rng = default_rng()
            random_array = rng.choice(19, size=16, replace=False)  # numbers 0 - 53
            # random_array = np.random.randint(low=1, high=54, size=16)
            random_array = np.array(random_array)
            print(random_array)
            # Make sure that other Cards previously made don't have at least 4 of the Cards in common
            # if len(self.cards_made) <= 0:
            # Create a new card
            self.card_made_values.append(random_array)
            card_lis = self.deck.search_deck(random_array)
            self.Create_Card(card_lis, name_index)
            # print(len(self.cards_made))
            # print(self.cards_made)
            name_index += 1

    def Create_Card(self, card_list, name_index):
        background_img = Image.new('RGB', (self.new_card_size, self.new_card_size), (255, 255, 255))
        top_range = self.new_card_size + int(self.new_card_offset)
        index = 0
        for i in range(int(self.new_card_offset), top_range, int(self.new_card_size / self.new_card_length)):
            for j in range(int(self.new_card_offset), top_range, int(self.new_card_size / self.new_card_length)):
                if index < len(card_list):
                    # print(card_list[index].name)
                    im = Image.fromarray(card_list[index].image.astype('uint8'), 'RGB')
                    background_img.paste(im, (j, i))
                    index += 1

        # background_img.show()
        card_name = "Loteria card " + str(name_index) + " .jpg"
        save_path = os.path.join(OUTPUT_DIR, card_name)
        background_img.save(save_path)
        self.cards_made.append(background_img)

    # def compare_list_made(self, cur_ran_list):
    #     same_v_count = 0
    #     for elem in self.card_made_values:
    #         print(elem)
    #         for i in cur_ran_list:
    #             if i in elem:
    #                 # print(i, "is in ", elem)
    #                 same_v_count += 1
    #         # if the same count is high enough return and pick a new random list
    #         if same_v_count >= 15:
    #             return same_v_count
    #         #
    #         else:
    #             same_v_count = 0
    #     print(same_v_count)
    #     return 0


class Deck:
    def __init__(self, img_size):
        self.card_list = load_images_from_dir(INPUT_DIR, ext=".jpg", size=img_size)
        pass

    def search_deck(self, list_want):
        card_list = []
        for i in list_want:
            for elem in self.card_list:
                if elem.number == i:
                    card_list.append(elem)
            # print(elem.name)
        return card_list


class Card:
    def __init__(self, name, number, image):
        self.name = name
        self.number = number
        self.image = image
        self.size = np.shape(image)


m = My_main()
m.Start()
