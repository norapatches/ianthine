from settings import *
from support import *
from debug import debug_multiple, show_fps
from level import Level
from overworld import Overworld
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
        self.data = GameData()
        
        # load save file if any
        self.load_game()
        
        # level stages
        self.tmx_maps = {
            0: load_pygame(join('.', 'data', 'levels', 'test.tmx')),
            1: load_pygame(join('.', 'data', 'levels', 'boss.tmx'))
        }
        # game overworld
        self.tmx_overworld = load_pygame(join('.', 'data', 'overworld', 'overworld_test.tmx'))
        # main menu
        self.main_menu = load_pygame(join('.', 'data', 'overworld', 'main_menu.tmx'))
        # settings level stage
        ...
        
        # load stage
        #self.current_stage = Level(self.tmx_maps[0], self.level_frames, self.data, self.fonts, self.switch_stage)
        self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)
        
        self.debugging = False
    
    def switch_stage(self, target, unlock= 0) -> None:
        if target == 'level':
            self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.data, self.fonts, self.switch_stage)
        else:
            if unlock > 0:
                self.data.unlocked_level = unlock
            self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)
    
    def save_game(self) -> None:
        '''Save self.data as a serialised object'''
        with open(join('.', 'save', 'default.sav'), 'wb') as file:
            pickle.dump(self.data, file)
    
    def load_game(self) -> None:
        '''Load self.data from a serialised object'''
        try:
            # if the save file exists, load it
            with open(join('.', 'save', 'default.sav'), 'rb') as file:
                self.data = pickle.load(file)
                print(self.data.unlocked_level)
        except FileNotFoundError:
            # if file doesn't exist, carry on
            print('no save data found')
            pass
    
    def import_assets(self) -> None:
        '''Import game assets'''
        self.level_frames = {
            'player': import_sub_folders('.', 'assets', 'graphic', 'player'),
            'arrow': import_folder(join('.', 'assets', 'graphic', 'projectiles', 'arrow')),
            'door': import_folder('.', 'assets', 'graphic', 'level', 'door'),
            # INTERACTION
            'interact': import_folder('.', 'assets', 'graphic', 'level', 'interaction'),
            # NPC
            'snail': import_folder('.', 'assets', 'graphic', 'npc', 'snail'),
            'creature': import_sub_folders('.', 'assets', 'graphic', 'npc', 'creature'),
            # VFX
            'vfx': import_sub_folders('.', 'assets', 'graphic', 'vfx'),
            # ENEMY
            'plant': import_sub_folders('.', 'assets', 'graphic', 'enemy', 'plant'),
            'skeleton': import_sub_folders('.', 'assets', 'graphic', 'enemy', 'walker', 'skeleton'),
            'zombie': import_sub_folders('.', 'assets', 'graphic', 'enemy', 'walker', 'zombie'),
            'shadowman': import_sub_folders('.', 'assets', 'graphic', 'enemy', 'chaser', 'shadowman'),
            'horn': import_sub_folders('.', 'assets', 'graphic', 'enemy', 'chaser', 'horn'),
            'crawler': import_sub_folders('.', 'assets', 'graphic', 'enemy', 'crawler'),
            'ghost': import_sub_folders('.', 'assets', 'graphic', 'enemy', 'ghost'),
            # BOSS
            'golem': import_sub_folders('.', 'assets', 'graphic', 'boss', 'golem'),
            # TRAP
            'spike': import_image('.', 'assets', 'graphic', 'level', 'spike'),
            'boulder': import_image('.', 'assets', 'graphic', 'level', 'boulder'),
            # MOVING PLATFORM
            'elevator': import_folder('.', 'assets', 'graphic', 'level', 'elevator'),
            # ITEM
            'items': import_sub_folders('.', 'assets', 'graphic', 'items'),
            'chest': import_folder('.', 'assets', 'graphic', 'level', 'chest')
        }
        self.overworld_frames = {
            'path': import_folder_dict(join('.', 'assets', 'graphic', 'overworld', 'path')),
            'icon': import_sub_folders(join('.', 'assets', 'graphic', 'overworld', 'icon')),
            'water': import_folder(join('.', 'assets', 'graphic', 'overworld', 'water'))
        }
        self.bgm = {
            'overworld': pygame.mixer.Sound(join('.', 'assets', 'sound', 'bgm', 'overworld.wav'))
        }
        self.sfx = {
            'jump': pygame.mixer.Sound(join('.', 'assets', 'sound', 'sfx', 'jump.wav')),
            'land': pygame.mixer.Sound(join('.', 'assets', 'sound', 'sfx', 'jump_land.wav')),
            'step': pygame.mixer.Sound(join('.', 'assets', 'sound', 'sfx', 'footstep.wav'))
        }
        self.ui_frames = {
            'heart': import_folder(join('.', 'assets', 'graphic', 'ui', 'heart'))
        }
        self.fonts = {
            'regular': pygame.font.Font(join('.', 'assets', 'fonts', 'regular.ttf'), 16),
            'bold': pygame.font.Font(join('.', 'assets', 'fonts', 'bold.ttf'), 16),
            'large_regular': pygame.font.Font(join('.', 'assets', 'fonts', '8_regular.ttf'), 32),
            'large_bold': pygame.font.Font(join('.', 'assets', 'fonts', '8_bold.ttf'), 32)
        }
    
    def run(self) -> None:
        '''The game loop, runs current stage'''
        while True:
            # get delta time
            dt = self.clock.tick() / 1000
                        
            # check for pygame events
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    #self.save_game()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:                    
                    '''Show or hide debug surfaces'''
                    if event.key == pygame.K_TAB:
                        self.debugging = not self.debugging
            
            self.current_stage.run(dt)
            
            # DEBUG show fps & dt
            if self.debugging:
                show_fps(self.clock.get_fps())
                debug_multiple((f'dt: {dt}',))
            
            # update display
            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()