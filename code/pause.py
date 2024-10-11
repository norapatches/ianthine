from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gdata import GameData

from settings import *
from colours import ColourPalette, change_colours
from controls import MenuControls
from sprites import AnimatedSprite, Sprite

class PauseScreen:
    '''When the game is paused a screen is displayed with two buttons and info about current stage'''
    def __init__(self, frames: dict, fonts: dict, data: GameData) -> None:
        self.screen = data.screen
        
        self.frames = frames
        
        self.controls = MenuControls()
        
        self.sprites = pygame.sprite.Group()
        self.coin = AnimatedSprite(((self.screen.get_width() / 3) * 2, self.screen.get_height() / 2), self.frames['coin'], self.sprites)
        
        self.fonts = fonts
        self.data = data
        
        self.selected = 0
        
        # adjust filters
        self.filters = [
            None,
            ColourPalette.bubblegum,
            ColourPalette.dust,
            ColourPalette.evening,
            ColourPalette.gato,
            ColourPalette.green,
            ColourPalette.evening,
            ColourPalette.ibm51,
            ColourPalette.ibm8503,
            ColourPalette.noire,
            ColourPalette.nokia,
            ColourPalette.orange,
            ColourPalette.port,
            ColourPalette.popart,
            ColourPalette.purple,
            ColourPalette.sand,
            ColourPalette.sangre,
            ColourPalette.sepia,
            ColourPalette.yellow
        ]
        self.filter = 0
        self.invert = 0
    
    def input(self) -> None:
        '''Check keyboard input'''
        keys = pygame.key.get_just_pressed()
        
        if keys[self.controls.left]:
            self.selected -= 1
            if self.selected < 0: self.selected = 0
        if keys[self.controls.right]:
            self.selected += 1
            if self.selected > 1: self.selected = 1
        if keys[self.controls.confirm]:
            if self.selected == 1:
                pygame.quit()
                sys.exit()
            else:
                self.data.paused = False
        
        if keys[pygame.K_BACKSPACE]:
            self.filter += 1
            self.filter = 0 if self.filter > 16 else self.filter
        
        if keys[pygame.K_RSHIFT]:
            self.invert += 1
            self.invert = 0 if self.invert > 1 else self.invert
    
    def show_pause_text(self) -> None:
        '''Display paused label'''
        text = self.fonts['large_bold'].render('PAUSED', False, 'white')
        rect = pygame.Rect(self.screen.get_width() / 2 - text.get_width() / 2,
                           16,
                           text.get_width(), text.get_height())
        self.screen.blit(text, rect)
    
    def show_coin_text(self) -> None:
        '''Display coins label'''
        text = self.fonts['regular'].render('coins', False, 'white')
        rect = pygame.Rect(int(self.coin.rect.x) - 2 * text.get_width(),
                           int(self.coin.rect.y) - 5,
                           text.get_width(), text.get_height())
        coins = self.fonts['bold'].render(f'{self.data.coins}', False, 'white')
        coin_rect = pygame.Rect(self.coin.rect.x - 1.5 * coins.get_width(),
                                rect.top,
                                coins.get_width(), coins.get_height())
        self.screen.blit(text, rect)
        self.screen.blit(coins, coin_rect)
    
    def show_key(self) -> None:
        '''Display the key if in possession of it'''
        if self.data.key:
            Sprite((self.screen.get_width() / 2, self.screen.get_height() / 2 + 16), self.frames['key'][0], self.sprites)
    
    def show_buttons(self) -> None:
        '''Display resume and quit buttons and draw rectangle around selected one'''
        resume = self.fonts['bold'].render('RESUME', False, 'white')
        quit = self.fonts['bold'].render('QUIT', False, 'white')
        resume_rect = pygame.Rect(self.screen.get_width() / 2 - resume.get_width(),
                                  (self.screen.get_height() / 4) * 3,
                                  resume.get_width(), resume.get_height())
        quit_rect = pygame.Rect(resume_rect.right + 16,
                                resume_rect.top,
                                quit.get_width(), quit.get_height())
        
        self.screen.blit(resume, resume_rect)
        self.screen.blit(quit, quit_rect)
        
        buttons = [resume_rect.inflate(8, 8), quit_rect.inflate(8, 8)]
        
        pygame.draw.rect(self.screen, 'white', buttons[self.selected], 1)
    
    def run(self, dt) -> None:
        '''The run method'''
        self.screen.fill('black')
        
        self.show_pause_text()
        
        self.input()
        
        self.show_coin_text()
        self.show_key()
        self.show_buttons()
        
        self.sprites.update(dt)
        self.sprites.draw(self.screen)
        
        change_colours((self.screen, ), self.filters[self.filter], self.invert)
        #scaled = pygame.transform.scale(self.screen, (PAUSE_WIDTH, PAUSE_HEIGHT))
        #self.display.blit(scaled, (171, 0))
        