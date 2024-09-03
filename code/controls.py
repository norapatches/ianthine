from settings import *

class LevelControls:
    '''Three keyboard control schemes to choose from'''
    keyboard = [
        {
            'move_left': pygame.K_LEFT, 'move_right': pygame.K_RIGHT, 'crouch': pygame.K_DOWN, 'interact': pygame.K_UP,
            'jump': pygame.K_SPACE, 'melee': pygame.K_x, 'ranged': pygame.K_c, 'map': pygame.K_TAB
        },
        {
            'move_left': pygame.K_LEFT, 'move_right': pygame.K_RIGHT, 'crouch': pygame.K_DOWN, 'interact': pygame.K_UP,
            'jump': pygame.K_KP2, 'melee': pygame.K_KP4, 'ranged': pygame.K_KP8, 'map': pygame.K_KP6
        },
        {
            'move_left': pygame.K_a, 'move_right': pygame.K_d, 'crouch': pygame.K_s, 'interact': pygame.K_w,
            'jump': pygame.K_SPACE, 'melee': pygame.K_j, 'ranged': pygame.K_i, 'map': pygame.K_TAB
        }
    ]
    def __init__(self, scheme= 0) -> None:
        self.left = LevelControls.keyboard[scheme]['move_left']
        self.right = LevelControls.keyboard[scheme]['move_right']
        self.down = LevelControls.keyboard[scheme]['crouch']
        self.up = LevelControls.keyboard[scheme]['interact']
        
        self.melee = LevelControls.keyboard[scheme]['melee']
        self.ranged = LevelControls.keyboard[scheme]['ranged']
        self.jump = LevelControls.keyboard[scheme]['jump']
        self.map = LevelControls.keyboard[scheme]['map']
        
        self.menu = pygame.K_ESCAPE