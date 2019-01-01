# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 14:47:44 2018

@author: Kaela DeAngelis and Terne Thorn Jakobsen
"""

from faceconstants import *
import numpy as np

from random import shuffle

#Generate an array with half ones and zeroes, then shuffle it to get a random order
#This array is twice as long as the number of females because we have twice as many images as people
def make_image_set():
	lr_random_list = np.ones(len(facepairs_female)*2, dtype=int)
	lr_random_list[:len(lr_random_list)/2] = 0
	np.random.shuffle(lr_random_list)

	all_image_set = []
	for i, image_prefix in enumerate(facepairs_female):
	    image_prefix = female_folder + image_prefix
	
	    happy_path = image_prefix + happy_suffix + regular_suffix
	    sad_path = image_prefix + sad_suffix + regular_suffix
	    neutral_path = image_prefix + neutral_suffix + regular_suffix
	
	    #Since our random number array is for every image and not just every person we multiply i by 2
	    if (lr_random_list[i*2] == 0):
	        happy_pair = (neutral_path, happy_path)
	    else:
	        happy_pair = (happy_path, neutral_path)
	
	    if (lr_random_list[i*2+1] == 0):
	        sad_pair = (neutral_path, sad_path)
	    else:
	        sad_pair = (sad_path, neutral_path)
	
	    all_image_set.append(happy_pair)
	    all_image_set.append(sad_pair)
	
	#add males
	np.random.shuffle(lr_random_list)
	for i, image_prefix in enumerate(facepairs_male):
	    image_prefix = male_folder + image_prefix
	
	    happy_path = image_prefix + happy_suffix + regular_suffix
	    sad_path = image_prefix + sad_suffix + regular_suffix
	    neutral_path = image_prefix + neutral_suffix + regular_suffix
	
	    #Since our random number array is for every image and not just every person we multiply i by 2
	    if (lr_random_list[i*2] == 0):
	        happy_pair = (neutral_path, happy_path)
	    else:
	        happy_pair = (happy_path, neutral_path)
	
	    if (lr_random_list[i*2+1] == 0):
	        sad_pair = (neutral_path, sad_path)
	    else:
	        sad_pair = (sad_path, neutral_path)
	
	    all_image_set.append(happy_pair)
	    all_image_set.append(sad_pair)
	
	return all_image_set