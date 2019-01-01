# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 20:04:06 2018

@author: ITLab
"""


#from moviepy.editor import *
#import moviepy
#clip = VideoFileClip("C:\\Users\\ITLab\\Desktop\\KaelaTerneProject\\WinPython-PyGaze-0.6.0\\neutral.mp4").rotate(180)
#clip.ipython_display(width=280)

#print(os.getenv('FFMPEG_BINARY', 'ffmpeg-imageio'))


#mov = visual.MovieStim3("C:\\Users\\ITLab\\Desktop\\KaelaTerneProject\\WinPython-PyGaze-0.6.0\\neutral.mp4")
#import moviepy
#clip = Movie("C:\\Users\\ITLab\\Desktop\\KaelaTerneProject\\WinPython-PyGaze-0.6.0\\neutral.mp4")
#mov.play()

from psychopy import visual, core, event

def video(vid):
    win = visual.Window((800, 600))
    mov = visual.MovieStim3(win, vid, size=(320, 240),
        flipVert=False, flipHoriz=False, loop=False)
    print('orig movie size=%s' % mov.size)
    print('duration=%.2fs' % mov.duration)
    globalClock = core.Clock()

    while mov.status != visual.FINISHED:
        mov.draw()
        win.flip()
        if event.getKeys():
            break

    win.close()
    core.quit()