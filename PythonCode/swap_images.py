from faceconstants import *
import numpy as np
import random
from constants import DISPSIZE




def swap(face_pair_screen, image_pair, tracker):

    center_of_screen = (DISPSIZE[0]/2, DISPSIZE[1]/2)
    image_HW = 326

    neutral_image_index = 0
    if ("NE" in image_pair[1]):
        neutral_image_index = 1

    if ("Male" in image_pair[0]):
        new_suffix = "_result.jpg"
    else:
        new_suffix = circle_suffix
    if (random.choice([True, False]) == True):
        new_suffix = square_suffix

    image_pair[neutral_image_index] = image_pair[neutral_image_index].replace(regular_suffix, new_suffix)

    start_time, start_pos = tracker.wait_for_fixation_start()
    end_result = tracker.wait_for_fixation_end()

    if neutral_image_index == 0:
        # if fixation is started here... draw new images.
        if start_pos[0] >= center_of_screen[0]-300 and start_pos[0] <= center_of_screen[0]-300+image_HW and start_pos[1] >= center_of_screen[1] and start_pos[1] <= center_of_screen[1]+image_HW:
            face_pair_screen.clear()
            face_pair_screen.draw_image(image_pair[0], pos=(center_of_screen[0]-300,center_of_screen[1]), scale=None) #need screen width
            face_pair_screen.draw_image(image_pair[1], pos=(center_of_screen[0]+300,center_of_screen[1]), scale=None) #need screen width

            # then wait for fixation on position of image_pair[1], i.e. the opposite
    if neutral_image_index == 1:
        if start_pos[0] >= center_of_screen[0]+300 and start_pos[0] <= center_of_screen[0]+300+image_HW and start_pos[1] >= center_of_screen[1] and start_pos[1] <= center_of_screen[1]+image_HW:
            face_pair_screen.clear()
            face_pair_screen.draw_image(image_pair[0], pos=(center_of_screen[0]-300,center_of_screen[1]), scale=None) #need screen width
            face_pair_screen.draw_image(image_pair[1], pos=(center_of_screen[0]+300,center_of_screen[1]), scale=None) #need screen width

    return face_pair_screen
