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
        
        self.speed = 64
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


class Crawler(pygame.sprite.Sprite):
    def __init__(self, position, frames, groups, collision_sprites) -> None:
        super().__init__(groups)
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(topleft= position)
        self.old_rect = self.rect.copy()
        self.z = Z_LAYERS['main']
        
        self.direction = vector(1, 0)
        self.speed = 4
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        
        self.on_surface = {'bottom': False, 'top': False, 'left': False, 'right': False}
        self.rotate = {'left': False, 'right': False}
        
    def check_contact(self) -> None:
        top_rect = pygame.FRect((self.rect.topleft + vector(0, -1)), (self.rect.width, 1))
        bottom_rect = pygame.FRect((self.rect.bottomleft), (self.rect.width, 1))
        left_rect = pygame.FRect((self.rect.topleft + vector(-1, 0)), (1, self.rect.height))
        right_rect = pygame.FRect((self.rect.topright), (1, self.rect.height))
        
        self.on_surface['bottom'] = True if bottom_rect.collidelist(self.collision_rects) >= 0 else False
        self.on_surface['top'] = True if top_rect.collidelist(self.collision_rects) >= 0 else False
        self.on_surface['left'] = True if left_rect.collidelist(self.collision_rects) >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(self.collision_rects) >= 0 else False
    
    def move(self, dt) -> None:
        self.rect.topleft += self.direction * self.speed * dt
    
    def change_move_dir(self) -> None:
        
        if self.on_surface['right']:
            self.rotate['left'] = True
        elif self.on_surface['left']:
            self.rotate['right'] = True
        else:
            self.rotate['left'], self.rotate['right'] = False, False
        
        if self.on_surface['bottom'] and self.on_surface['right']:
            self.direction.y = -1
            self.direction.x = 0
        
        if self.on_surface['top'] and self.on_surface['right']:
            self.direction.y = 0
            self.direction.x = -1
        
        if self.on_surface['top'] and self.on_surface['left']:
            self.direction.y = 1
            self.direction.x = 0
        
        if self.on_surface['left'] and self.on_surface['bottom']:
            self.direction.y = 0
            self.direction.x = 1
    
    def animate(self, dt) -> None:
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        
        self.image = pygame.transform.rotate(self.image, 90) if self.rotate['left'] else self.image
        self.image = pygame.transform.rotate(self.image, -90) if self.rotate['right'] else self.image
        self.image = pygame.transform.flip(self.image, False, True) if self.on_surface['top'] else self.image
    
    def update(self, dt) -> None:
        self.old_rect = self.rect.copy()
        self.check_contact()
        
        self.move(dt)
        self.change_move_dir()
        
        self.animate(dt)
