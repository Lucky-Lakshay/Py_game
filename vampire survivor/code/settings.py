import pygame 
from os.path import join 
from os import walk
from random import randint, choice
from pytmx.util_pygame import load_pygame
import math

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720 
TILE_SIZE = 64