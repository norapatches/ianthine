from settings import *
from sprites import Heart

class UI:
    def __init__(self, font, frames) -> None:
        self.display = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        self.font = font
        
        # health
        self.heart_frames = frames['heart']
        self.heart_surface_width = self.heart_frames[0].get_width()
        self.heart_padding = 8
    
    def create_hearts(self, amount) -> None:
        for sprite in self.sprites:
            sprite.kill()
        
        for heart in range(amount):
            x = 16 + heart * (self.heart_surface_width + self.heart_padding)
            y = 16
            Heart((x, y), self.heart_frames, self.sprites)
    
    def update(self, dt) -> None:
        self.sprites.update(dt)
        self.sprites.draw(self.display)

