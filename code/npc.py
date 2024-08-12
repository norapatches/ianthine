from settings import *
from gtimer import Timer

class Ghost(pygame.sprite.Sprite):
    def __init__(self, position, frames, groups) -> None:
        super().__init__(groups)
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(topleft= position)
        
        self.map_image = pygame.Surface((1, 1))
        self.map_image.fill('white')
        self.map_rect = self.map_image.get_frect(topleft = (position[0] / TILE_SIZE, position[1] / TILE_SIZE))
        
        self.z = Z_LAYERS['main']
        
        self.direction = 1
        
        self.speed = 100
    
    def animate(self, dt) -> None:
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image
    
    def update(self, dt) -> None:
        
        self.animate(dt)


