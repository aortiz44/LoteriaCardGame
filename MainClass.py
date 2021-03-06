import numpy as np
from PIL import Image
import os
import cv2
from numpy.random._generator import default_rng
import random

# INPUT_DIR = "traditional_input_images"
# OUTPUT_DIR = "traditional_output_images"

INPUT_DIR = "my_input_images"
OUTPUT_DIR = "my_output_images"

img_path = os.path.join(INPUT_DIR, "01 el gallo.jpg")


def load_images_from_dir(data_dir, ext=".jpg", size=(180, 180)):
    imagesFiles = [f for f in os.listdir(data_dir) if f.endswith(ext)]
    # imagesFiles = []
    # for f in os.listdir(data_dir):
    #     if f.endswith(ext):
    #         imagesFiles.append(f)
    # print(len(imagesFiles))
    card_deck = []
    count = 0

    for f_name in imagesFiles:
        print(f_name)
        # get image
        get_image = cv2.imread(os.path.join(data_dir, f_name))
        # turn it into np array
        temp_np_img = np.array(get_image)
        # !!!!!!!!!!! This will error out
        # if the names of the cards have, accents like in the spanish language. !!!!!!!!!!!
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

class CardSheet:
    def __init__(self):
        # deck = The size of the images in the card
        # new_card_size the size of the Container Card Sheet
        # new_card_offset offset between cards
        # new_card_length
        # card_num_to_make Number of Container Card Sheets to make
        # num_pict_per_card Number of Images per Card Sheet
        self.deck = Deck((460, 460))
        self.new_card_size = 2000
        self.new_card_offset = 10
        self.new_card_length = 4
        self.cards_made = []
        self.card_made_values = []
        self.card_num_to_make = 5
        self.num_pict_per_card = 16
        self.list_cards_called = []
        pass

    def Start(self):
        # for elem in self.deck.card_list:
        #     print(np.shape(elem.image))
        #     print(str(elem.number), elem.name)
        #     # cv2.imshow(str(elem.number) + elem.name, elem.image)
        #     # cv2.waitKey(0)

        name_index = 0
        print(len(self.deck.card_list))
        num_choices = len(self.deck.card_list)
        if len(self.deck.card_list) >= self.num_pict_per_card:
            for i in range(self.card_num_to_make):
                # Pick 16 Random Cards
                rng = default_rng()
                random_array = rng.choice(num_choices, size=self.num_pict_per_card, replace=False)  # numbers 0 - 53
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

    def call_out_cards(self, time_to_wait=3000, call_range=5, show_img=True):
        deck_length = len(self.deck.card_list)
        # print(deck_length)
        list_remaining = [*range(0, deck_length)]
        self.list_cards_called = []
        print(list_remaining)
        random.shuffle(list_remaining)
        print(list_remaining)
        # Error check to see if the call range is greater than the deck length
        if call_range > deck_length:
            call_range = deck_length

        for i in range(call_range):
            # print("List of cards remaining")
            # print(list_remaining)
            card_picked = list_remaining[0]
            self.list_cards_called.append(card_picked)
            del list_remaining[0]
            # print("List of cards Used")
            # print(self.list_cards_called)
            print("Card Picked: ", card_picked)
            picked_card = sheet.deck.get_card_by_num(card_picked)
            window_name = str(picked_card.number) + picked_card.name

            if show_img:
                # -----------Swap Channels ------------------
                card_img = picked_card.image
                red = card_img[:, :, 2].copy()
                blue = card_img[:, :, 0].copy()

                card_img[:, :, 0] = red
                card_img[:, :, 2] = blue

                cv2.imshow(window_name, card_img)
                key = cv2.waitKey(time_to_wait)  # pauses for 3 seconds before fetching next image
                cv2.destroyWindow(window_name)
                if key == 27:  # if ESC is pressed, exit loop
                    cv2.destroyAllWindows()
                    break


class Deck:
    # Creates the Deck based on all the images in the input_images file
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

    def get_card_by_num(self, card_picked):
        for elem in self.card_list:
            if elem.number == card_picked:
                return elem
        pass


class Card:
    def __init__(self, name, number, image):
        self.name = name
        self.number = number
        self.image = image
        self.size = np.shape(image)


create_cards = True
call_out_cards = False
use_personal = True
# if use_personal:

sheet = CardSheet()
if create_cards:
    sheet.Start()
if call_out_cards:
    deck_length = len(sheet.deck.card_list)
    sheet.call_out_cards(3000, deck_length, False)
    print(sheet.list_cards_called)
