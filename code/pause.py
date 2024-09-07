from settings import *
from sprites import AnimatedSprite, Sprite

class PauseScreen:
    def __init__(self, frames, fonts, data) -> None:
        self.display = pygame.display.get_surface()
        self.pause_box = pygame.Surface((200, 150))
        
        self.frames = frames
        
        self.sprites = pygame.sprite.Group()
        self.coin = AnimatedSprite(((self.pause_box.get_width() / 3) * 2, self.pause_box.get_height() / 2), self.frames['coin'], self.sprites)
        
        self.fonts = fonts
        self.data = data
        
        self.selected = 0
    
    def input(self) -> None:
        keys = pygame.key.get_just_pressed()
        
        if keys[pygame.K_LEFT]:
            self.selected -= 1
            if self.selected < 0: self.selected = 0
        if keys[pygame.K_RIGHT]:
            self.selected += 1
            if self.selected > 1: self.selected = 1
        if keys[pygame.K_RETURN]:
            if self.selected == 1:
                pygame.quit()
                sys.exit()
            else:
                self.data.paused = False
    
    def show_pause_text(self) -> None:
        text = self.fonts['large_bold'].render('PAUSED', False, 'white')
        rect = pygame.Rect(self.pause_box.get_width() / 2 - text.get_width() / 2,
                           16,
                           text.get_width(), text.get_height())
        self.pause_box.blit(text, rect)
    
    def show_coin_text(self) -> None:
        text = self.fonts['regular'].render('coins', False, 'white')
        rect = pygame.Rect(int(self.coin.rect.x) - 2 * text.get_width(),
                           int(self.coin.rect.y) - 5,
                           text.get_width(), text.get_height())
        coins = self.fonts['bold'].render(f'{self.data.coins}', False, 'white')
        coin_rect = pygame.Rect(self.coin.rect.x - 1.5 * coins.get_width(),
                                rect.top,
                                coins.get_width(), coins.get_height())
        self.pause_box.blit(text, rect)
        self.pause_box.blit(coins, coin_rect)
    
    def show_key(self) -> None:
        if self.data.key:
            Sprite((self.pause_box.get_width() / 2, self.pause_box.get_height() / 2 + 16), self.frames['key'][0], self.sprites)
    
    def show_buttons(self) -> None:
        resume = self.fonts['bold'].render('RESUME', False, 'white')
        quit = self.fonts['bold'].render('QUIT', False, 'white')
        resume_rect = pygame.Rect(self.pause_box.get_width() / 2 - resume.get_width(),
                                  (self.pause_box.get_height() / 4) * 3,
                                  resume.get_width(), resume.get_height())
        quit_rect = pygame.Rect(resume_rect.right + 16,
                                resume_rect.top,
                                quit.get_width(), quit.get_height())
        
        self.pause_box.blit(resume, resume_rect)
        self.pause_box.blit(quit, quit_rect)
        
        buttons = [resume_rect.inflate(8, 8), quit_rect.inflate(8, 8)]
        
        pygame.draw.rect(self.pause_box, 'white', buttons[self.selected], 1)
    
    def run(self, dt) -> None:
        self.pause_box.fill('black')
        
        self.input()
        
        self.show_pause_text()
        self.show_coin_text()
        self.show_key()
        self.show_buttons()
        
        self.sprites.update(dt)
        self.sprites.draw(self.pause_box)
        
        self.display.blit(pygame.transform.scale(self.pause_box, (PAUSE_WIDTH, PAUSE_HEIGHT)), (320, 240))