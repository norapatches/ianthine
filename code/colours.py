from settings import *

class ColourPalette:
    bubblegum = {'dark' : (41, 22, 29),     'light' : (250, 148, 149)}
    dust =      {'dark' : (37, 41, 50),     'light' : (203, 158, 106)}
    evening =   {'dark' : (29, 15, 68),     'light' : (244, 78, 56)}
    gato =      {'dark' : (54, 54, 54),     'light' : (236, 236, 236)}
    green =     {'dark' : (0, 0, 0),        'light' : (38, 195, 15)}
    ibm51 =     {'dark' : (50, 60, 57),     'light' : (211, 201, 161)}
    ibm8503 =   {'dark' : (46, 48, 55),     'light' : (235, 229, 206)}
    noire =     {'dark' : (30, 28, 50),     'light' : (198, 186, 172)}
    nokia =     {'dark' : (33, 44, 40),     'light' : (114, 164, 136)}
    orange =    {'dark' : (21, 29, 36),     'light' : (237, 132, 99)}
    port =      {'dark' : (16, 54, 143),    'light' : (255, 142, 66)}
    popart =    {'dark' : (214, 20, 6),     'light' : (0, 212, 255)}
    purple =    {'dark' : (23, 20, 28),     'light' : (166, 146, 176)}
    sand =      {'dark' : (37, 41, 50),     'light' : (203, 147, 97)}
    sangre =    {'dark' : (18, 6, 40),      'light' : (97, 14, 14)}
    sepia =     {'dark' : (111, 77, 61),    'light' : (203, 152, 103)}
    yellow =    {'dark' : (41, 43, 48),     'light' : (207, 171, 74)}

def change_colours(surfaces, palette, invert= False) -> None:
        # Convert surface to an array
        for surface in surfaces:
            pixel_array = pygame.surfarray.pixels3d(surface)

            # Define black and white as tuples (RGB)
            black = (0, 0, 0)
            white = (255, 255, 255)

            # Create masks for black and white pixels
            black_mask = np.all(pixel_array == black, axis=-1)
            white_mask = np.all(pixel_array == white, axis=-1)

            if invert:
                pixel_array[black_mask] = palette['light']
                pixel_array[white_mask] = palette['dark']
            else:
                pixel_array[black_mask] = palette['dark']
                pixel_array[white_mask] = palette['light']

            # Update the surface
            del pixel_array  # Unlock the surface from the array