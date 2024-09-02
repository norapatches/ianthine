from settings import *
from os.path import join

class GameStateManager:
    def __init__(self) -> None:
        pass


class SoundManager:
    def __init__(self) -> None:
        self.sfx = {
            'jump': pygame.mixer.Sound(join('.', 'assets', 'sound', 'sfx', 'jump.wav')),
            'land': pygame.mixer.Sound(join('.', 'assets', 'sound', 'sfx', 'jump_land.wav')),
            'step': pygame.mixer.Sound(join('.', 'assets', 'sound', 'sfx', 'footstep.wav'))
        }
    
    def jump(self) -> None:
        self.sfx['jump'].play()
    
    def step(self) -> None:
        self.sfx['step'].play()