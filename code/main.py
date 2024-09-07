from settings import *
from support import *
from debug import debug_multiple, show_fps
from level import Level
from gdata import GameData
from ui import UI

class Game:
    def __init__(self) -> None:
        '''Game setup, load assets, load maps, init pygame library, define resolution'''
        pygame.init()
        pygame.display.set_caption('stickman')
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        self.import_assets()
        
        self.ui = UI(pygame.font.Font(None, 16), self.ui_frames)
        self.data = GameData(self.ui)
        
        self.tmx_maps = {
            0: load_pygame(join('.', 'data', 'levels', 'test.tmx'))
        }
        self.current_stage = Level(self.tmx_maps[0], self.level_frames, self.data)
    
    def import_assets(self) -> None:
        '''Import game assets'''
        self.level_frames = {
            'player': import_sub_folders('.', 'assets', 'graphic', 'player'),
            'snail': import_folder('.', 'assets', 'graphic', 'npc', 'snail'),
            'ghost': import_folder('.', 'assets', 'graphic', 'npc', 'ghost'),
            'particle': import_folder('.', 'assets', 'graphic', 'effects', 'particle'),
            'key': import_folder('.', 'assets', 'graphic', 'items', 'key'),
            'creature': import_sub_folders('.', 'assets', 'graphic', 'npc', 'creature'),
            'soldier': import_folder('.', 'assets', 'graphic', 'enemy', 'soldier'),
            'shadowman': import_sub_folders('.', 'assets', 'graphic', 'enemy', 'shadowman'),
            'horn': import_sub_folders('.', 'assets', 'graphic', 'enemy', 'horn'),
            'crawler': import_folder('.', 'assets', 'graphic', 'enemy', 'crawler'),
            'spike': import_image('.', 'assets', 'graphic', 'level', 'spike'),
            'moving_platform': import_folder('.', 'assets', 'graphic', 'level', 'moving_platform'),
            'items': import_sub_folders('.', 'assets', 'graphic', 'items')
        }
        self.sfx = {
            'jump': pygame.mixer.Sound(join('.', 'assets', 'sound', 'sfx', 'jump.wav')),
            'land': pygame.mixer.Sound(join('.', 'assets', 'sound', 'sfx', 'jump_land.wav')),
            'step': pygame.mixer.Sound(join('.', 'assets', 'sound', 'sfx', 'footstep.wav'))
        }
        self.ui_frames = {
            'heart': import_folder(join('.', 'assets', 'graphic', 'ui', 'heart'))
        }
        self.paused = False
    
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
            
            if not self.paused:
                # run current stage
                self.current_stage.run(dt)
            
            # DEBUG show fps & dt
            #show_fps(self.clock.get_fps())
            #debug_multiple((f'dt: {dt}',))
            
            # update display
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()