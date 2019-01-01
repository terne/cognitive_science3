# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 15:05:18 2018

@author: Kaela DeAngelis and Terne Thorn Jakobsen
"""
#from pygame import display,movie
#from psychopy import visual, core
#from psychopy.visual import MovieStim
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

center_of_screen = (DISPSIZE[0]/2, DISPSIZE[1]/2)
image_HW = 326

# create display object
disp = Display()

# create eyetracker object
tracker = eyetracker.EyeTracker(disp)

# create keyboard object
keyboard = Keyboard(keylist=['space', "q", "escape"],timeout=1)

# create logfile (txt file that is tab seperated, I think)
# write "headlines" to log file

# calibrate the eye-tracker
tracker.calibrate()

# make the sets of images
image_set = generate()
#shuffle our image sets
shuffle(image_set)

# give pre-trial instuctions first
#instruction_screen = Screen()
#instruction_screen.draw_text(text="Trial session", pos=center_of_screen, colour=(255,255,255), fontsize=22)
#while keyboard.get_key()[0] != "space":
	#disp.fill(instruction_screen)
	#disp.show()

#draw image pair 
#face_pair_screen.draw_image(image_pair[0], pos=(center_of_screen[0]-300,center_of_screen[1]), scale=None) #need screen width
#face_pair_screen.draw_image(image_pair[1], pos=(center_of_screen[0]+300,center_of_screen[1]), scale=None) 

#call movie function - will need to switch betwwen neutral and sad 
#INSERT CODE HERE 			
				
# start trials

#create excel sheet columns for data output 
trial_indices = []
for i in range(len(image_set)):
	trial_indices.append(i)
trials = data.TrialHandler(trial_indices, 1, method='random')
trials.data.addDataType('Left Image')
trials.data.addDataType('Right Image')
trials.data.addDataType('Fixation Frequency on Emotional')
trials.data.addDataType('Fixation Duration on Emotional')
trials.data.addDataType('Disengage')
trials.data.addDataType('Disengagement Time')
trials.data.addDataType('First Fixation')

#define AOI
AOI_left = AOI(aoitype="rectangle", pos=(center_of_screen[0]-300-163, center_of_screen[1]-163), size=[326,326])
AOI_right = AOI(aoitype="rectangle", pos=(center_of_screen[0]+300-163, center_of_screen[1]-163), size=[326,326])

pressed_key = None

# give trial instuctions first
instruction_screen = Screen()
instruction_screen.draw_text(text="The practice trials will now begin. \n You will see a white cross followed by a white number. Please say the number out loud. \n You will see a pair of faces. Please watch them naturally. \n You may see a square of circle appear around an image. If you see either, please look at the image with the shape. \n Left click if it is a sqaure. Right click if it is a circle", pos=center_of_screen, colour=(255,255,255), fontsize=22)
while keyboard.get_key()[0] != "space":
	disp.fill(instruction_screen)
	disp.show()
				
instruction_screen.clear()
pygame.display.update()
from accl import acclimation
acclimation(center_of_screen, tracker, disp, keyboard, AOI_left, AOI_right)

#from vidtest import video
#vid_screen = Screen()
#vid_screen.draw_image(video('neutral.mp4'), pos=(center_of_screen[0]-300,center_of_screen[1]), scale=None)
#disp.fill(vid_screen)
#disp.show()
#import pygame
#from pygame import display,movie
#movie = pygame.movie.Movie('neutral.mp4')
#screen = pygame.display.set_mode(movie.get_size())
#movie_screen = pygame.Surface(movie.get_size()).convert()
#movie.set_display(movie_screen)
#movie.play()

# give test instuctions
instruction_screen = Screen()
instruction_screen.draw_text(text="The testing trials will now begin. \n You will see a white cross followed by a white number. Please say the number out loud. \n After, you will see a pair of faces. Please watch them naturally. \n You may see a square of circle appear around an image. If you see either, please look at the image with the shape. \n Left click if it is a sqaure. Right click if it is a circle.", pos=center_of_screen, colour=(255,255,255), fontsize=22)
while keyboard.get_key()[0] != "space":
	disp.fill(instruction_screen)
	disp.show()
				
instruction_screen.clear()
#start trials  q
for trialnr in trials: 
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
	tracker.log("start_trial %d" %trialnr)
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
	image_pair = image_set[trialnr]
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

	#Add basic data
	trials.data.add('Left Image', image_pair[0])
	trials.data.add('Right Image', image_pair[1])
	trials.data.add('Disengage', image_pair[2])

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
				
			#Check first fixation
			if (first_image == 0):
				if neutral_image_index == 0:
					trials.data.add('First Fixation', 'Emotional')
				else:
					trials.data.add('First Fixation', 'Neutral')
				first_image = 1

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

			#Check first fixation
			if (first_image == 0):
				if neutral_image_index == 0:
					trials.data.add('First Fixation', 'Neutral')
				else:
					trials.data.add('First Fixation', 'Emotional')
				first_image = 2
		else:
			last_fixation_on_emotional = False


		last_pass_time_taken = (time.time() * 1000) - last_pass_time_stamp
		last_pass_time_stamp = (time.time() * 1000)
		total_time_taken = (time.time() * 1000) - start_time_taken

	print("Total time taken " + str(total_time_taken))
	print("Neutral time " + str(time_neutral))
	print("Emotional time " + str(time_emotional))

	trials.data.add('Fixation Frequency on Emotional', count_fixation_on_emotional)
	trials.data.add('Fixation Duration on Emotional', time_emotional)

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
							trials.data.add('Disengagement Time', disengagement_end_time - disengagement_start_time)
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

		# space (Will be replaced by other code to wait for fixation)
	# while keyboard.get_key()[0] == None: #REPLACE THIS LINE
	# 	pressed_key = keyboard.get_key()[0]
	# 	if (pressed_key == 'q'):
	# 		break

	# 	disp.fill(face_pair_screen)
	# 	disp.show()

	# height and width of images = 326 × 326
	# height and width of square and circle images = 426 x 426

	# disengagement task

	# wait for fixation start on emotional
	# wait for fixation start on neutral
	# save times
	# wait for key-press as well
	disengagement = "add in the disengagement time (diff between fixation start 1 and 2)"
	# end trial
	trialend = libtime.get_time()
	tracker.stop_recording()
	tracker.log("stop trial %d" % trialnr)


	# log information in the end
	# add a way out (quit if pressing q)
	if keyboard.get_key()[0] == "q":
		break

trials.saveAsExcel(fileName='data.csv',
                  sheetName = 'rawData',
                  stimOut=[], 
                  dataOut=['all_raw'])


# close experiemnt
tracker.close()
disp.close()
libtime.expend()

# we should probabaly remember to remove the previous logfile for each experiment