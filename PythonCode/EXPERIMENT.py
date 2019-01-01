# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 15:05:18 2018

@author: Kaela DeAngelis and Terne Thorn Jakobsen
"""
#from pygame import display,movie
#from psychopy import visual, core
from psychopy.visual import MovieStim
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

center_of_screen = (DISPSIZE[0]/2, DISPSIZE[1]/2)
image_HW = 326

# create display object
disp = Display()

# create eyetracker object
tracker = eyetracker.EyeTracker(disp)

# create keyboard object
keyboard = Keyboard(keylist=['space', "q", "escape"],timeout=1)

# create logfile (txt file that is tab seperated, I think)
our_log = liblog.Logfile()
# write "headlines" to log file
our_log.write(["trialnr", "trialstart", "trialend", "disengagementtime", "imagepair"]) # fill in with the neccecary headlines

# calibrate the eye-tracker
tracker.calibrate()

# make the sets of images
image_set = generate()
#shuffle our image sets
shuffle(image_set)


# give instuctions first
instruction_screen = Screen()
instruction_screen.draw_text(text="You will watch a short clip. After, the trials will begin. \n Press space to continue", pos=center_of_screen, colour=(255,255,255), fontsize=22)
while keyboard.get_key()[0] != "space":
	disp.fill(instruction_screen)
	disp.show()
				
instruction_screen.clear()

#call movie function - will need to switch betwwen neutral and sad 
#INSERT CODE HERE 			
				
# start trials
for trialnr in range(len(image_set)):
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
	AOI_left = AOI(aoitype="rectangle", pos=(center_of_screen[0]-300,center_of_screen[1]), size=[326,326])
	AOI_right = AOI(aoitype="rectangle", pos=(center_of_screen[0]+300, center_of_screen[1]), size=[326,326])
	disp.fill(face_pair_screen)
	disp.show()
	
	neutral_image_index = 0
	if ("NE" in image_pair[1]):
		neutral_image_index = 1
	
	#NEED WHILE LOOP TO CAPTURE FIXATIONS AND TIME
	start_time_taken = time.time() * 1000
	time_taken = 0
	while time_taken < 3000:
		start_time, start_pos = tracker.wait_for_fixation_start()
		end_time, start_pos = tracker.wait_for_fixation_end()
		
		if AOI_right.contains(start_pos):
			if neutral_image_index == 0:
				print("fixed emotional")
			else:
				print("Fixed neutral")
				
		if AOI_right.contains(start_pos):
			if neutral_image_index == 0:
				print("fixed neutral")
			else:
				print("Fixed emotional")

		time_taken = (time.time() * 1000) - start_time_taken
	
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
			start_time, start_pos = tracker.wait_for_fixation_start()
			end_time, start_pos = tracker.wait_for_fixation_end()
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
					
					while keyboard.get_key()[0] == None:
						start_time, start_pos = tracker.wait_for_fixation_start()
						end_time, start_pos = tracker.wait_for_fixation_end()
						if AOI_left.contains(start_pos):			
							print("you fixated on the right image:))")
							disengagement_end_time = libtime.get_time()
							print("Total time taken" + str(disengagement_end_time - disengagement_start_time))
							break
					break

				# then wait for fixation on position of image_pair[1], i.e. the opposite
			if neutral_image_index == 1:
				#area = pygame.Rect(myRect_ontheright)
				#pygame.draw.rect(face_pair_screen, (100, 200, 70), area)
				#pygame.display.flip()
				#if ((start_pos[0]-center_of_screen[0]-300)**2 + (start_pos[1]-center_of_screen[1])**2)**0.5 < 326/2:
				if AOI_left.contains(start_pos):
					print("you fixated on the left image :))")
					
					disengagement_start_time = libtime.get_time()
																				#if (start_pos[0] >= center_of_screen[0]+300 and start_pos[0] <= center_of_screen[0]+300+image_HW and start_pos[1] >= center_of_screen[1] and start_pos[1] <= center_of_screen[1]+image_HW):
					face_pair_screen.clear()
					#disengagement_screen.draw_image(image_pair[0], pos=(center_of_screen[0]-300,center_of_screen[1]), scale=None) #need screen width
					#disengagement_screen.draw_image(image_pair[1], pos=(center_of_screen[0]+300,center_of_screen[1]), scale=None) #need screen width
					disp.fill(disengagement_screen)
					disp.show()
					
					while keyboard.get_key()[0] == None:
						start_time, start_pos = tracker.wait_for_fixation_start()
						end_time, start_pos = tracker.wait_for_fixation_end()
						if AOI_right.contains(start_pos):			
							print("you fixated on the right image:))")
							disengagement_end_time = libtime.get_time()
							print("Total time taken" + str(disengagement_end_time - disengagement_start_time))
							break
					break
		#space (Will be replaced by other code to wait for fixation)
		#while keyboard.get_key()[0] == None: #REPLACE THIS LINE
			#disp.fill(face_pair_screen)
			#disp.show()

	# height and width of images = 326 × 326
	# height and width of square and circle images = 426 x 426

	else:
		continue

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
	our_log.write([trialnr, trialstart, trialend, disengagement, image_pair])
	# add a way out (quit if pressing q)
	if keyboard.get_key()[0] == "q":
		break

# close experiemnt
our_log.close()
tracker.close()
disp.close()
libtime.expend()

# we should probabaly remember to remove the previous logfile for each experiment
