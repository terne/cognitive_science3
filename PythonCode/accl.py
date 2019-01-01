from faceconstants import *
import numpy as np
from random import shuffle
import random

from random import shuffle
from pygaze.defaults import *
from pygaze import libtime
from pygaze import liblog
from pygaze.libscreen import Display, Screen
from pygaze.libinput import Keyboard
from pygaze import eyetracker
from constants import *
#from image_set_generation1 import make_image_set
from generate_image_sets_with_circles_squares import generate
import numpy as np
from pygaze.libgazecon import AOI
from faceconstants import *
from swap_images import swap
import random
import pygame
import time
from psychopy import data

def generate_trial_images():

    #Generate an array with half ones and zeroes, then shuffle it to get a random order
    #This array is twice as long as the number of females because we have twice as many images as people
    #this list determines which image is on the left/right for every pair of images
    lr_random_list = np.ones(len(facepairs_trial)*2, dtype=int)
    lr_random_list[:len(lr_random_list)/2] = 0
    np.random.shuffle(lr_random_list)#36 numbers long

    #18 females, 9 are happy that have circle, 9 that are sad that have circle
    #this list determines which happy/neutral pairs get a circle/square
    lr_random_sad_circle_list = np.ones(len(facepairs_trial), dtype=int)
    lr_random_sad_circle_list[:len(lr_random_sad_circle_list)/2] = 0
    np.random.shuffle(lr_random_sad_circle_list)

    #this list determines which sad/neutral pairs get a circle/square
    lr_random_happy_circle_list = np.ones(len(facepairs_trial), dtype=int)
    lr_random_happy_circle_list[:len(lr_random_happy_circle_list)/2] = 0
    np.random.shuffle(lr_random_happy_circle_list)

    count = 0

    #Every time through the list we use the random lists above to determine three things. The left-right order of each pair, and whether or not the pair should have a second pass with a circle/square
    all_image_set = []
    for i, image_prefix in enumerate(facepairs_trial):
        image_prefix = trial_folder + image_prefix

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
    return all_image_set


def acclimation(center_of_screen, tracker, disp, keyboard, AOI_left, AOI_right):
    image_set = generate_trial_images()

    #start trials
    for index in range(0,len(image_set)):
        # make trial screens
        fixation_cross_screen = Screen()
        fixation_cross_screen.draw_fixation(fixtype='cross', pos=center_of_screen, colour=(255,255,255), pw=5, diameter=30)
        number_screen = Screen()
        number_screen.draw_text(text=str(np.random.randint(1,10)),pos = center_of_screen, colour=(255,255,255), fontsize=40)
        face_pair_screen = Screen()
        disengagement_screen = Screen()

        # start with blank screen	 for 500 ms and start recording
        disp.fill()
        disp.show()
        tracker.start_recording()
        tracker.log("start_trial %d" %index)
        trialstart = libtime.get_time()
        libtime.pause(500)

        # fixation	cross screen
        disp.fill(fixation_cross_screen)
        disp.show()
        libtime.pause(500)
        fixation_cross_screen.clear()

        # number screen
        disp.fill(number_screen)
        disp.show()
        libtime.pause(1000)
        number_screen.clear()

        #draws image pair
        image_pair = image_set[index]
        face_pair_screen.draw_image(image_pair[0], pos=(center_of_screen[0]-300,center_of_screen[1]), scale=None) #need screen width
        face_pair_screen.draw_image(image_pair[1], pos=(center_of_screen[0]+300,center_of_screen[1]), scale=None) #need screen width
        disp.fill(face_pair_screen)
        disp.show()
        
        neutral_image_index = 0
        if ("NE" in image_pair[1]):
            neutral_image_index = 1
        
        #NEED WHILE LOOP TO CAPTURE FIXATIONS AND TIME
        start_time_taken = time.time() * 1000
        total_time_taken = 0
        time_neutral = 0
        time_emotional = 0
        last_pass_time_stamp = (time.time() * 1000) - start_time_taken
        last_pass_time_taken = 0

        first_image = 0

        count_fixation_on_emotional = 0
        last_fixation_on_emotional = False
        while total_time_taken < 3000:
            pressed_key = keyboard.get_key()[0]
            if (pressed_key == 'q'):
                break

            tracker_pos = tracker.sample()
            
            if AOI_right.contains(tracker_pos):
                #Add time
                if neutral_image_index == 0:
                    time_emotional = time_emotional + last_pass_time_taken
                    if not last_fixation_on_emotional:
                        count_fixation_on_emotional = count_fixation_on_emotional + 1
                    last_fixation_on_emotional = True
                else:
                    time_neutral = time_neutral + last_pass_time_taken
                    last_fixation_on_emotional = False
                    
            elif AOI_left.contains(tracker_pos):
                #Add time
                if neutral_image_index == 0:
                    time_neutral = time_neutral + last_pass_time_taken
                    last_fixation_on_emotional = False
                else:
                    time_emotional = time_emotional + last_pass_time_taken
                    if not last_fixation_on_emotional:
                        count_fixation_on_emotional = count_fixation_on_emotional + 1
                    last_fixation_on_emotional = True


            last_pass_time_taken = (time.time() * 1000) - last_pass_time_stamp
            last_pass_time_stamp = (time.time() * 1000)
            total_time_taken = (time.time() * 1000) - start_time_taken

        if (pressed_key == 'q'):
            break

        #libtime.pause(3000) # 3000 ms of free viewing
        #image pair index 2 tells us if we need to draw a circle/square.

        #myRect_ontheleft = (center_of_screen[0]-300-163, center_of_screen[0]-300+163, center_of_screen[1]+163, center_of_screen[1]-163)
        #myRect_ontheright = (center_of_screen[0]+300-163, center_of_screen[0]+300+163, center_of_screen[1]+163, center_of_screen[1]-163)

        if (image_pair[2] == True):
            # new_face_pair_screen = swap(face_pair_screen, image_pair, tracker)

            #if ("Male" in image_pair[0]):
                #new_suffix = "_result.jpg"
            #else:
            new_suffix = circle_suffix
            if (random.choice([True, False]) == True):
                new_suffix = square_suffix

            image_pair[neutral_image_index] = image_pair[neutral_image_index].replace(regular_suffix, new_suffix)

            disengagement_screen.draw_image(image_pair[0], pos=(center_of_screen[0]-300,center_of_screen[1]), scale=None) #need screen width
            disengagement_screen.draw_image(image_pair[1], pos=(center_of_screen[0]+300,center_of_screen[1]), scale=None) #need screen width

            while keyboard.get_key()[0] == None:
                start_pos = tracker.sample()
                #face_pair_screen.draw_circle(colour=(255,255,255), pos=((start_pos[0]-center_of_screen[0]+300)**2,(start_pos[1]-center_of_screen[1])**2, 326/2))
                #disp.fill(face_pair_screen)
                #disp.show()
                if neutral_image_index == 0:
                    #area = pygame.Rect(myRect_ontheleft)
                    #pygame.draw.rect(face_pair_screen, (100, 200, 70), area)
                    #pygame.display.flip()
                    #if ((start_pos[0]-center_of_screen[0]+300)**2 + (start_pos[1]-center_of_screen[1])**2)**0.5 < 100/2:
                    if AOI_right.contains(start_pos):
                        #face_pair_screen.draw_circle(color=(255,255,255), pos=(start_pos[0]-center_of_screen[0]+300)**2,start_pos[1]-center_of_screen[1])**2), 326/2)

                        #print("you fixated on the right image:))")
                        disengagement_start_time = libtime.get_time()


                        # if fixation is started here... draw new images.
                        #if (start_pos[0] >= center_of_screen[0]-300 and start_pos[0] <= center_of_screen[0]-300+image_HW and start_pos[1] >= center_of_screen[1] and start_pos[1] <= center_of_screen[1]+image_HW):
                        face_pair_screen.clear()
                        #disengagement_screen.draw_text(text="yep", pos=center_of_screen)
                        #while keyboard.get_key()[0] == None:
                        disp.fill(disengagement_screen)
                        disp.show()
                        
                        while True:
                            start_pos = tracker.sample()
                            if AOI_left.contains(start_pos):			
                                print("you fixated on the right image:))")
                                disengagement_end_time = libtime.get_time()
                                break
                        break

                    # then wait for fixation on position of image_pair[1], i.e. the opposite
                if neutral_image_index == 1:
                    #area = pygame.Rect(myRect_ontheright)
                    #pygame.draw.rect(face_pair_screen, (100, 200, 70), area)
                    #pygame.display.flip()
                    #if ((start_pos[0]-center_of_screen[0]-300)**2 + (start_pos[1]-center_of_screen[1])**2)**0.5 < 326/2:
                    if AOI_left.contains(start_pos):
                        disengagement_start_time = libtime.get_time()
                                                                                    #if (start_pos[0] >= center_of_screen[0]+300 and start_pos[0] <= center_of_screen[0]+300+image_HW and start_pos[1] >= center_of_screen[1] and start_pos[1] <= center_of_screen[1]+image_HW):
                        face_pair_screen.clear()
                        #disengagement_screen.draw_image(image_pair[0], pos=(center_of_screen[0]-300,center_of_screen[1]), scale=None) #need screen width
                        #disengagement_screen.draw_image(image_pair[1], pos=(center_of_screen[0]+300,center_of_screen[1]), scale=None) #need screen width
                        disp.fill(disengagement_screen)
                        disp.show()
                        
                        while True:
                            start_pos = tracker.sample()
                            if AOI_right.contains(start_pos):			
                                disengagement_end_time = libtime.get_time()
                                print("Total time taken" + str(disengagement_end_time - disengagement_start_time))
                                break
                        break
        else:
            continue

        if (pressed_key == 'q'):
            break

        # end trial
        trialend = libtime.get_time()
        tracker.stop_recording()
        tracker.log("stop trial %d" % index)


        # log information in the end
        # add a way out (quit if pressing q)
        if keyboard.get_key()[0] == "q":
            break