from settings import *
from gtimer import Timer
from random import choice

class Soldier(pygame.sprite.Sprite):
    def __init__(self, position, frames, groups, collision_sprites) -> None:
        super().__init__(groups)
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(topleft= position)
        self.z = Z_LAYERS['main']
        
        self.direction = choice((-1, 1))
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        
        self.speed = 128
        self.hit_timer = Timer(250)
    
    def reverse(self) -> None:
        if not self.hit_timer.active:
            self.direction *= -1
            self.hit_timer.start()
    
    def update(self, dt) -> None:
        self.hit_timer.update()
        
        # animation
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image
        
        # movement
        self.rect.x += self.direction * self.speed * dt
        
        # reverse direction
        floor_rect_right = pygame.FRect(self.rect.bottomright, (1, 1))
        floor_rect_left = pygame.FRect(self.rect.bottomleft, (-1, 1))
        wall_rect = pygame.FRect(self.rect.topleft + vector(-1, 0), (self.rect.width + 2, 1))
        
        if floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction > 0 or\
            floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0 or\
            wall_rect.collidelist(self.collision_rects) != -1:
            self.direction *= -1