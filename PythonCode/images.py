
# coding: utf-8

# In[1]:


from pygaze.defaults import *
from pygaze import libtime
from pygaze import liblog
from pygaze.libscreen import Display, Screen
from pygaze.libinput import Keyboard
from pygaze import eyetracker
from constants import *
from faceconstants import *
import numpy as np


# In[2]:


#random shuffling
from random import shuffle
import random

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


shuffle(all_image_set)

#can check for shuffle
#for image in all_image_set:
    #print(image)


# In[3]:


#DUMMYMODE = True # set in constants.py
# To use your code with the new Tobii Pro SDK,
# set the TRACKERTYPE to 'tobii'

# start timing
libtime.expstart()

# create display object
disp = Display()

# create eyetracker object
tracker = eyetracker.EyeTracker(disp)

# create keyboard object
keyboard = Keyboard(keylist=['space',"q"],timeout=1)

center_of_screen = (DISPSIZE[0]/2, DISPSIZE[1]/2)

# create screen to draw things on
screen1 = Screen()
screen1.draw_fixation(fixtype='cross', pos=center_of_screen, colour=(255,255,255), pw=5, diameter=30)
screen2 = Screen()
#screen1.draw_image(base_path, pos=(center_of_screen[0]-300,center_of_screen[1]), scale=None) #need screen width
#screen2.draw_image(base_path1, pos=(center_of_screen[0]+300,center_of_screen[1]), scale=None) #need screen width
screen3 = Screen()


# Create a Screen to draw images on
#screen4 = Screen()

# calibrate eye tracker
tracker.calibrate()

#for female set
for image_pair in all_image_set:
    screen1.clear()

    #draws image pair
    screen1.draw_image(image_pair[0], pos=(center_of_screen[0]-300,center_of_screen[1]), scale=None) #need screen width
    screen1.draw_image(image_pair[1], pos=(center_of_screen[0]+300,center_of_screen[1]), scale=None) #need screen width

    #space (replace with 3 seconds)
    #current time
    pairstart = libtime.get_time()

    if (image_pair[2] == True):        # if we have the addition, wait for fixation. REPLACE THE NEXT LINE
        while keyboard.get_key()[0] == None: #Replace this with wait for fixation code
            disp.fill(screen1)
            disp.show()
    else:
        while libtime.get_time() - pairstart < 3000:
            disp.fill(screen1)
            disp.show()

    #image pair index 2 tells us if we need to draw a circle/square.
    if (image_pair[2] == True):

        neutral_image_index = 0
        if ("NE" in image_pair[1]):
            neutral_image_index = 1

        new_suffix = circle_suffix
        if (random.choice([True, False]) == True):
            new_suffix = square_suffix

        image_pair[neutral_image_index] = image_pair[neutral_image_index].replace(regular_suffix, new_suffix)

        #draws image pair
        screen1.clear()
        screen1.draw_image(image_pair[0], pos=(center_of_screen[0]-300,center_of_screen[1]), scale=None) #need screen width
        screen1.draw_image(image_pair[1], pos=(center_of_screen[0]+300,center_of_screen[1]), scale=None) #need screen width

        #space (Will be replaced by other code to wait for fixation)
        while keyboard.get_key()[0] == None: #REPLACE THIS LINE
            disp.fill(screen1)
            disp.show()

    #cross
    screen1.clear()
    screen1.draw_fixation(fixtype='cross', pos=center_of_screen, colour=(255,255,255), pw=5, diameter=30)


    #space
    while keyboard.get_key()[0] == None:
        disp.fill(screen1)
        disp.show()

    #if keyboard.get_key()[0] == "q":
     #   break


# start eye tracking
tracker.start_recording()
tracker.log("start_trial %d" %1)
trialstart = libtime.get_time()

#screen1.clear()
while libtime.get_time() - trialstart < 20000:
    disp.fill(screen2)
    disp.show()

# why is it pausing on the wrong screen???? solution: use psychopy instead of pygame for disptype
#libtime.pause(10000)
#tracker.stop_recording()
#tracker.close()
#disp.close()

# wait for eye movement
    t1, startpos = tracker.wait_for_fixation_start()
#endtime, startpos, endpos = tracker.wait_for_fixation_end()
#if startpos == center_of_screen:
    if ((startpos[0]-center_of_screen[0])**2 + (startpos[1]-center_of_screen[1])**2)**0.5 < 100/2:
        screen2.clear()
        disp.fill(screen3)
        disp.show()
        libtime.pause(2000)
        break
        # to make it not flicker?
    if keyboard.get_key()[0] == "space":
        break
# stop eye tracking
tracker.stop_recording()
tracker.close()
disp.close()
# remember to do some drift correction in each trial
# and to log data and so forth (check examples and guidelines)


# In[ ]:





# In[ ]:
