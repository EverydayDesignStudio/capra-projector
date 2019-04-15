#!/usr/bin/env python

import math
import time
import pygame
import csv
import sh       # contains global variables
from PIL import Image
# from envirophat import motion
# from meth import *

# General variables
# ========================
sh.init()

select = 0 # variable for choosing hike folder
tolerance = 45 # threshold amount of degrees to turn viewpointer before switching to other hike folder
buffersize = 5
heading = [] # array to store heading values in and calculate average.
overlay = False # for toggling overlay on/off
lowres = False # for toggling lowres mode
photo = True # for toggling photo
for i in range(buffersize):
    heading.append(0)
heady = 0 # index to count location in array 'heading'
headcount = 0
print(heading)

# for i in range(buffersize - 1):
#     heading[i] = motion.heading()

image = Image.open('hike4/1.jpg') # initialise
pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((1280, 720))
sh.width, sh.height = pygame.display.get_surface().get_size()

# prepare semitransparent black screen
photolayer = pygame.Surface((sh.width, sh.height))
bfade = pygame.Surface((sh.width, sh.height))
bfade.fill((0, 0, 0, 3))
bfade.set_alpha(3)
background = pygame.Rect(0, 0, sh.width, sh.height)

font = pygame.font.SysFont("monospace", 15)
largefont = pygame.font.SysFont("monospace", 70)

# Arrange sh.hikes on ring, Count hikes
metaAlt = 0
hikes = 0
for file in listdir('..'):
    print file
    if file.startswith('Hike'):
        print '=============='
        print 'file says hike'
        print '=============='
        hikes += 1
        print hikes
print str(hikes) + ' hikes counted!'
alts = [0] * hikes
start = int(raw_input('start? '))
progress = [start] * hikes # variable for displaying correct hike photo

sh.hikes = hikes

#pass alts data to shared
initialisehikes(alts)

# draw indication of angles corresponding with hikes
indication = pygame.Surface((sh.width, sh.height))

while (1):
    #draw image 
    if photo:
        if select is not -1:
            print 'select: ' + str(select + 1)
            folder = 'Hike' + str(13) # str(select + 1)
            file = folder +'-' + "{:04}".format(progress[select]) +'.jpg'
            if lowres:
                folder = folder + '/405/'
            folder = '../' + folder
            image = pygame.image.load(folder + '/' + file)
            #image = pygame.transform.scale(image, (1280, 720))
            fadeimagein(image, photolayer)
            progress[select] = progress[select] + 1
            if (progress[select] > len(listdir(folder)) - 1):
                print '+- RESET HIKE -+'
                print folder + ' contains ' + str(len(listdir(folder))) + 'files,'
                print 'progress[' + str(select) + '] @ ' + str(progress[select])
                progress[select] = 0
        else:
            photolayer.blit(bfade, (0,0))
        screen.blit(photolayer, (0,0))

    # Jordan White - commented out
    # if overlay:
    #     screen.blit(indication, (0,0))
    #     label = largefont.render(str(select), 1, (255, 255, 255))
    #     screen.blit(label, (sh.width/2, sh.height/2))
    #     r = sh.height/2
    #     x1, y1 = polar(0, 0)
    #     x2, y2 = polar(headcount, r)
    #     x3, y3 = polar(motion.heading(), r)
    #     pygame.draw.line(screen, (255, 0, 0), (x1, y1), (x2, y2), 10)
    #     pygame.draw.line(screen, (0, 0, 255), (x1, y1), (x3, y3), 10)

    # print program info to screen
    """
    #rectangle = pygame.Rect(80, 80, 200, 100)
    pygame.draw.rect(screen, (0, 0, 0), rectangle)
    label = font.render('compass: ' + str(motion.heading()), 1, (255, 255, 255))
    screen.blit(label, (100, 100))
    label = font.render('headingdiff: ' + str(headingdiff), 1, (255, 255, 255))
    screen.blit(label, (100, 120))
    label = font.render('folder: ' + str(select), 1, (255, 255, 255))
    screen.blit(label, (100, 140))
    label = font.render('photo: ' + str(progress), 1, (255, 255, 255))
    screen.blit(label, (100, 160))
    """

    pygame.display.flip() # update screen


# ============================================================================
#     __            __                    __                                 =
#    / /_____ __ __/ /  ___  ___ ________/ /                                 =
#   /  '_/ -_) // / _ \/ _ \/ _ `/ __/ _  /                                  =
#  /_/\_\\__/\_, /_.__/\___/\_,_/_/  \_,_/                                   =
#           /___/                                                            =
# ============================================================================
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                pygame.display.set_mode(1280, 720)
            elif event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()
            elif event.key == pygame.K_o:
                overlay = not overlay
            elif event.key == pygame.K_i:
                photo = not photo
            elif event.key == pygame.K_l:
                lowres = not lowres
