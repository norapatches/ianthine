from math import sin
import numpy as np
from os.path import join
import pickle
import pygame, sys
from pygame.math import Vector2 as vector
from pytmx.util_pygame import load_pygame
from random import choice, randint

# Game Settings
WINDOW_WIDTH, WINDOW_HEIGHT = 1366, 768     # the game window
SCREEN_WIDTH, SCREEN_HEIGHT = 256, 144      # resolution
TILE_SIZE = 16                              # tile size in tmx_map
ANIMATION_SPEED = 5                         # global animation speed

Z_LAYERS = {
    'bg': 0,
    'sky': 1,
    'bg_tiles': 2,
    'path': 3,
    'bg_details': 4,
    'main': 5,
    'water': 6,
    'fg': 7
}