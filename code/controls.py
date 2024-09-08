from settings import *

class LevelControls:
    '''Control schemes to choose from'''
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
    def __init__(self, scheme= 0, gamepad=False) -> None:
        if gamepad:
            pass
        else:
            self.left = LevelControls.keyboard[scheme]['move_left']
            self.right = LevelControls.keyboard[scheme]['move_right']
            self.down = LevelControls.keyboard[scheme]['crouch']
            self.up = LevelControls.keyboard[scheme]['interact']
            
            self.melee = LevelControls.keyboard[scheme]['melee']
            self.ranged = LevelControls.keyboard[scheme]['ranged']
            self.jump = LevelControls.keyboard[scheme]['jump']
            self.map = LevelControls.keyboard[scheme]['map']
            
            self.menu = pygame.K_ESCAPE


class MenuControls:
    '''Control scheme for menu screens'''
    keyboard = [
        {
            'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN,
            'confirm': pygame.K_RETURN, 'cancel': pygame.K_ESCAPE
        },
        {
            'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s,
            'confirm': pygame.K_RETURN, 'cancel': pygame.K_ESCAPE
        }
    ]
    def __init__(self, scheme= 0, gamepad= False) -> None:
        if gamepad:
            pass
        else:
            self.left = MenuControls.keyboard[scheme]['left']
            self.right = MenuControls.keyboard[scheme]['right']
            self.up = MenuControls.keyboard[scheme]['up']
            self.down = MenuControls.keyboard[scheme]['down']
            
            self.confirm = MenuControls.keyboard[scheme]['confirm']
            self.cancel = MenuControls.keyboard[scheme]['cancel']