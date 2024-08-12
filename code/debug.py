import pygame
pygame.init()
font = pygame.font.Font(None, 30)

def debug(info, x: int= 10, y: int= 40):
    display_surface = pygame.display.get_surface()
    debug_text = font.render(str(info), True, 'white')
    debug_rect = debug_text.get_rect(topleft= (x, y))
    pygame.draw.rect(display_surface, 'black', debug_rect)
    display_surface.blit(debug_text, debug_rect)

def debug_multiple(items: list, x: int= 10, y: int= 40) -> None:
    display_surface = pygame.display.get_surface()
    for idx, item in enumerate(items):
        debug_text = font.render(str(item), True, 'White')
        debug_rect = debug_text.get_rect(topleft = (x, y + (idx * 30)))
        pygame.draw.rect(display_surface, 'Black', debug_rect)
        display_surface.blit(debug_text, debug_rect)

def show_fps(info, x: int= 10, y: int= 10):
    display_surface = pygame.display.get_surface()
    debug_text = font.render(f'FPS: {info:.2f}', True, 'white')
    debug_rect = debug_text.get_rect(topleft= (x, y))
    pygame.draw.rect(display_surface, 'black', debug_rect)
    display_surface.blit(debug_text, debug_rect)