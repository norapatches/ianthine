import pygame, sys
from pygame.math import Vector2 as vector

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 960
SCREEN_WIDTH, SCREEN_HEIGHT = 160, 120
TILE_SIZE = 16

ANIMATION_SPEED = 10

Z_LAYERS = {
    'bg': 0,
    'bg_details': 1,
    'bg_tiles': 2,
    'main': 3,
    'fg': 4
}