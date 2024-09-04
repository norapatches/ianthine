from settings import *
from support import *
from debug import debug, show_fps
from level import Level

from os.path import join
from pytmx.util_pygame import load_pygame   

class Game:
    def __init__(self) -> None:
        '''Game setup, load assets, load maps, init pygame library, define resolution'''
        pygame.init()
        pygame.display.set_caption('stickman')
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        self.import_assets()
        
        self.tmx_maps = {
            0: load_pygame(join('.', 'data', 'levels', 'test.tmx'))
        }
        self.current_stage = Level(self.tmx_maps[0], self.level_frames)
        
        self.paused = False
    
    def import_assets(self) -> None:
        '''Import game assets'''
        self.level_frames = {
            'player': import_sub_folders('.', 'assets', 'graphic', 'player'),
            'snail': import_folder('.', 'assets', 'graphic', 'npc', 'snail'),
            'ghost': import_folder('.', 'assets', 'graphic', 'npc', 'ghost'),
            'key': import_folder('.', 'assets', 'graphic', 'items', 'key'),
            'creature': import_sub_folders('.', 'assets', 'graphic', 'npc', 'creature'),
            'soldier': import_folder('.', 'assets', 'graphic', 'enemy', 'soldier'),
            'crawler': import_folder('.', 'assets', 'graphic', 'enemy', 'crawler'),
            'spike': import_image('.', 'assets', 'graphic', 'level', 'spike'),
            'moving_platform': import_folder('.', 'assets', 'graphic', 'level', 'moving_platform')
        }
        self.sfx = {
            'jump': pygame.mixer.Sound(join('.', 'assets', 'sound', 'sfx', 'jump.wav')),
            'land': pygame.mixer.Sound(join('.', 'assets', 'sound', 'sfx', 'jump_land.wav')),
            'step': pygame.mixer.Sound(join('.', 'assets', 'sound', 'sfx', 'footstep.wav'))
        }
    
    def run(self) -> None:        
        '''The game loop, runs current stage'''
        while True:
            # get delta time
            dt = self.clock.tick() / 1000
            
            # limit delta time
            max_dt = 0.007
            dt = min(dt, max_dt)
            
            # check for pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # run current stage
            self.current_stage.run(dt)
            
            # DEBUG show fps & dt
            show_fps(self.clock.get_fps())
            debug(f'dt: {dt}')
            
            # update display
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()