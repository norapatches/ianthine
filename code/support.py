from settings import *
from os import walk
from os.path import join
import pygame

def import_image(*path, alpha=True, format='png') -> pygame.Surface:
    '''Import a single image from a file path'''
    full_path = join(*path) + f'.{format}'
    return pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()

def import_folder(*path) -> list:
    '''Import images from a folder and store them in a list'''
    frames = []
    for folder_path, _, image_names in walk(join(*path)):
        for image_name in sorted(image_names):
            try:
                int(image_name.split('.')[0])
                full_path = join(folder_path, image_name)
                frames.append(pygame.image.load(full_path).convert_alpha())
            except ValueError:
                # Skip files that cannot be converted to an integer
                continue
    return frames

def import_folder_dict(*path) -> dict:
    '''Import images from a folder and store them in a dictionary'''
    frame_dict = {}
    for folder_path, _, image_names in walk(join(*path)):
        for image_name in image_names:
            try:
                key = int(image_name.split('.')[0])
                full_path = join(folder_path, image_name)
                surface = pygame.image.load(full_path).convert_alpha()
                frame_dict[key] = surface
            except ValueError:
                # Skip files that cannot be converted to an integer
                continue
    return frame_dict

def import_sub_folders(*path) -> dict:
    '''Import assets from a folder and store them in a dictionary where the keys are the subfolder names'''
    frame_dict = {}
    for _, sub_folders, __ in walk(join(*path)):
        if sub_folders:
            for sub_folder in sub_folders:
                frame_dict[sub_folder] = import_folder(*path, sub_folder)
    return frame_dict
