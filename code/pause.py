from settings import *
from sprites import AnimatedSprite

class PauseScreen:
    def __init__(self, coin_frames, fonts, data) -> None:
        self.display = pygame.display.get_surface()
        self.pause_box = pygame.Surface((200, 150))
        self.pause_box.fill('black')
        
        self.sprites = pygame.sprite.Group()
        self.coin = AnimatedSprite(((self.pause_box.get_width() / 3) * 2, self.pause_box.get_height() / 2), coin_frames, self.sprites)
        
        self.fonts = fonts
        self.data = data
    
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
        coin_rect = pygame.Rect(self.coin.rect.x - 2 * coins.get_width(), rect.top, coins.get_width(), coins.get_height())
        self.pause_box.blit(text, rect)
        self.pause_box.blit(coins, coin_rect)
        
    def run(self, dt) -> None:
        self.show_pause_text()
        
        self.show_coin_text()
        
        self.sprites.update(dt)
        self.sprites.draw(self.pause_box)
        
        scaled = pygame.transform.scale(self.pause_box, (PAUSE_WIDTH, PAUSE_HEIGHT))
        self.display.blit(scaled, (320, 240))