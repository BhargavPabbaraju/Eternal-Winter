###IMPORTS
import pygame as pg
import pygame.locals
import time
import numpy as np
import random as rd
import shelve


saveData = shelve.open('savedata')

##SETTINGS

WIDTH,HEIGHT = 1024,640
optionPositions=[(300,150),(300,250),(300,350)]
options=['New Game','Load Save File','Quit']
pauseoptions = ['Continue','Inventory','Save','Quit']
invpos = [(192,64),(192,192),(192,320),(192,448),(448,64),(448,192),(448,320),(448,448)]
pausePositions = [(300,150),(300,250),(300,350),(300,450)]
MENUFONTSIZE = 44
BLOCKSIZE = 64
ORIGIN = (WIDTH/2-BLOCKSIZE,100)
FINALMAP = "007"
OVERMAP = "008"
TEXTSPEED = 2000
TEXTBOXPOSITIONS = {'sci':[1,475]}
CREDITS = ["CREDITS","Fonts Used",["Halo3","Will Turnbow"],["PowerClear","Peter O.,Mr. Gela"],"Code References",["Camera Class","KidsCanCode"],"Development and Assets","Bhargav"]
creditpos=[(256,192),(320,650),[(192,650),(512,650)],[(128,650),(512,650)],(320,650),[(64,650),(512,650)],(64,650),(256,650)]
intropos = [(64,128),(64,320),(320,256),(320,448),(192,192),(192,384),(190,288)]

####INITIALIZATION
window = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption('Eternal Winter')
pg.display.set_icon(pg.image.load('Images/snowball.png'))
clock = pg.time.Clock()
pg.init()


###COLORS
WHITE = (234,251,243)
GRAY = (123, 214, 215)
BLACK = (0,0,0)

COLORS = [
    (187, 179, 250), #Violet
    ( 180, 196, 244), #Indigo
    ( 172, 236, 252), #Blue
    (196, 244, 188), #Green
    (255, 225, 177), #Yellow
    (252, 224, 216), # Orange
    (252, 180, 196) #Red
]


###BGM
pg.mixer.music.load('Audio/menubgm.wav')



##Sounf Effects
warpfx = pygame.mixer.Sound('Audio/warpfx.wav')
warpfx.set_volume(0.1)
gemfx = pygame.mixer.Sound('Audio/gem.wav')
gemfx.set_volume(0.3)
portalfx = pygame.mixer.Sound('Audio/portal.wav')
portalfx.set_volume(0.1)
nextfx = pg.mixer.Sound('Audio/next.wav')
nextfx.set_volume(0.2)