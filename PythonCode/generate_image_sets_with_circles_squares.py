from faceconstants import *
import numpy as np
from random import shuffle
import random

def generate():

    #Generate an array with half ones and zeroes, then shuffle it to get a random order
    #This array is twice as long as the number of females because we have twice as many images as people
    #this list determines which image is on the left/right for every pair of images
    lr_random_list = np.ones(len(facepairs_female)*2, dtype=int)
    lr_random_list[:len(lr_random_list)/2] = 0
    np.random.shuffle(lr_random_list)#36 numbers long

    #18 females, 9 are happy that have circle, 9 that are sad that have circle
    #this list determines which happy/neutral pairs get a circle/square
    lr_random_sad_circle_list = np.ones(len(facepairs_female), dtype=int)
    lr_random_sad_circle_list[:len(lr_random_sad_circle_list)/2] = 0
    np.random.shuffle(lr_random_sad_circle_list)

    #this list determines which sad/neutral pairs get a circle/square
    lr_random_happy_circle_list = np.ones(len(facepairs_female), dtype=int)
    lr_random_happy_circle_list[:len(lr_random_happy_circle_list)/2] = 0
    np.random.shuffle(lr_random_happy_circle_list)

    count = 0

    #Every time through the list we use the random lists above to determine three things. The left-right order of each pair, and whether or not the pair should have a second pass with a circle/square
    all_image_set = []
    for i, image_prefix in enumerate(facepairs_female):
        image_prefix = female_folder + image_prefix

        happy_path = image_prefix + happy_suffix + regular_suffix
        sad_path = image_prefix + sad_suffix + regular_suffix
        neutral_path = image_prefix + neutral_suffix + regular_suffix

        #Since our random number array is for every image and not just every person we multiply i by 2
        #Picking neutral for left or for right using the random number list
        if (lr_random_list[i*2] == 0):
            happy_pair = [neutral_path, happy_path]
        else:
            happy_pair = [happy_path, neutral_path]

        #1 = add circle/square
        if (lr_random_happy_circle_list[i] == 1):
            happy_pair.append(True)
        else:
            happy_pair.append(False)

        if (lr_random_list[i*2+1] == 0):
            sad_pair = [neutral_path, sad_path]
        else:
            sad_pair = [sad_path, neutral_path]

        if (lr_random_sad_circle_list[i] == 1):
            sad_pair.append(True)
        else:
            sad_pair.append(False)

        all_image_set.append(happy_pair)
        all_image_set.append(sad_pair)

    #add males
    np.random.shuffle(lr_random_list)
    np.random.shuffle(lr_random_happy_circle_list)
    np.random.shuffle(lr_random_sad_circle_list)
    for i, image_prefix in enumerate(facepairs_male):
        image_prefix = male_folder + image_prefix

        happy_path = image_prefix + happy_suffix + regular_suffix
        sad_path = image_prefix + sad_suffix + regular_suffix
        neutral_path = image_prefix + neutral_suffix + regular_suffix

        #Since our random number array is for every image and not just every person we multiply i by 2
        if (lr_random_list[i*2] == 0):
            happy_pair = [neutral_path, happy_path]
        else:
            happy_pair = [happy_path, neutral_path]

        if (lr_random_happy_circle_list[i] == 1):
            happy_pair.append(True)
        else:
            happy_pair.append(False)

        if (lr_random_list[i*2+1] == 0):
            sad_pair = [neutral_path, sad_path]
        else:
            sad_pair = [sad_path, neutral_path]

        if (lr_random_sad_circle_list[i] == 1):
            sad_pair.append(True)
        else:
            sad_pair.append(False)

        all_image_set.append(happy_pair)
        all_image_set.append(sad_pair)

    return all_image_set
