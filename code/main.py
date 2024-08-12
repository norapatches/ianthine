from settings import *
from support import *
from debug import debug, debug_multiple, show_fps
from level import Level

from os.path import join
from pytmx.util_pygame import load_pygame

class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('stickman')
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        self.import_assets()
        
        self.tmx_maps = {
            0: load_pygame(join('.', 'data', 'levels', 'test.tmx'))
        }
        self.current_stage = Level(self.tmx_maps[0], self.level_frames)
    
    def import_assets(self):
        self.level_frames = {
            'player': import_sub_folders('.', 'assets', 'graphic', 'player'),
            'snail': import_folder('.', 'assets', 'graphic', 'enemy', 'snail'),
            'ghost': import_folder('.', 'assets', 'graphic', 'npc', 'ghost'),
            'spike': import_image('.', 'assets', 'graphic', 'level', 'spike')
        }
    
    def run(self) -> None:
        while True:
            dt = self.clock.tick(60)
            max_dt = 0.005
            dt = min(dt, max_dt)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.current_stage.run(dt)
            
            show_fps(self.clock.get_fps())
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()