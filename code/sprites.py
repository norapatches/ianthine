from settings import *
from gtimer import Timer

class Sprite(pygame.sprite.Sprite):
    def __init__(self, position, surface= pygame.Surface((TILE_SIZE, TILE_SIZE)), groups= None, z= Z_LAYERS['main']) -> None:
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(topleft= position)
        self.old_rect = self.rect.copy()
        self.z = z


class AnimatedSprite(Sprite):
    def __init__(self, position, frames, groups, z= Z_LAYERS['main'], animation_speed = ANIMATION_SPEED) -> None:
        self.frames, self.frame_index = frames, 0
        super().__init__(position, self.frames[self.frame_index], groups, z)
        self.animation_speed = animation_speed
    
    def animate(self, dt) -> None:
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
    
    def update(self, dt) -> None:
        self.animate(dt)


class Floor(Sprite):
    def __init__(self, position, surface, groups) -> None:
        super().__init__(position, surface, groups)
        
        # minimap
        self.map_image = pygame.Surface((1, 1))
        self.map_image.fill('white')
        self.map_rect = self.map_image.get_frect(topleft = (position[0] / TILE_SIZE, position[1] / TILE_SIZE))


class Door(Sprite):
    def __init__(self, position, surface, groups):
        super().__init__(position, surface, groups)
        self.old_rect = self.rect.copy()
        
        # minimap
        self.map_image = pygame.Surface((1, 1))
        self.map_image.fill('gray')
        self.map_rect = self.map_image.get_frect(topleft = (position[0] / TILE_SIZE, position[1] / TILE_SIZE))
    
    def update(self, dt) -> None:
        self.old_rect = self.rect.copy()