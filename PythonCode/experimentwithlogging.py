# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 19:08:10 2018

@author: ITLab
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 15:05:18 2018

@author: Kaela DeAngelis and Terne Thorn Jakobsen
"""
#from pygame import display,movie
#from psychopy import visual, core
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

# make the sets of images
image_set = generate()

trial_indices = []
for i in range(len(image_set)):
    trial_indices.append(i)

#shuffle our image sets
shuffle(image_set)

trials = data.TrialHandler(trial_indices, 1, method='random')
trials.data.addDataType('Left Image')
trials.data.addDataType('Right Image')
trials.data.addDataType('Initial Orientation')
trials.data.addDataType('Fixation Frequency on Emotional')
trials.data.addDataType('Fixation Duration on Emotional')
trials.data.addDataType('Fixation')

for trial in trials:
    print(image_set[trial])
    trials.data.add('Left Image', image_set[trial][0])
    trials.data.add('Right Image', image_set[trial][1])
    trials.data.add('Fixation', image_set[trial][2])

trials.saveAsExcel(fileName='data.csv',
                  sheetName = 'rawData',
                  stimOut=[], 
                  dataOut=['all_raw'])