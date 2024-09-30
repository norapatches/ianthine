from settings import *
from os import walk
from os.path import join

def import_image(*path, alpha=True, format='png') -> pygame.Surface:
    '''Imports a single image from the specified file path and returns it as a Pygame Surface object.'''
    full_path = join(*path) + f'.{format}'
    return pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()

def import_folder(*path) -> list:
    '''Imports all images from a specified folder and returns them as a list of Pygame Surface objects.'''
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

def import_folder_dict(*path):
    frame_dict = {}
    for folder_path, _, image_names in walk(join(*path)):
        for image_name in image_names:
            full_path = join(folder_path, image_name)
            surface = pygame.image.load(full_path).convert_alpha()
            frame_dict[image_name.split('.')[0]] = surface
    return frame_dict

def import_sub_folders(*path) -> dict:
    '''Imports assets from all subfolders within a specified folder and returns them as a dictionary.
    The keys are the subfolder names, and the values are lists of Pygame Surface objects representing the images within each subfolder.'''
    frame_dict = {}
    for _, sub_folders, __ in walk(join(*path)):
        if sub_folders:
            for sub_folder in sub_folders:
                frame_dict[sub_folder] = import_folder(*path, sub_folder)
    return frame_dict
