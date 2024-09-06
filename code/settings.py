from os.path import join
import pygame, sys
from pygame.math import Vector2 as vector
from pytmx.util_pygame import load_pygame
import pickle

# Game Settings
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 960     # the game window
SCREEN_WIDTH, SCREEN_HEIGHT = 200, 160      # resolution - will be upscaled to window
TILE_SIZE = 16                              # tile size in tmx_map

ANIMATION_SPEED = 4

Z_LAYERS = {
    'bg': 0,
    'bg_details': 1,
    'bg_tiles': 2,
    'main': 3,
    'fg': 4
}