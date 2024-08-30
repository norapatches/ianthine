from settings import *
from random import choice

class Creature(pygame.sprite.Sprite):
    '''Creature is a neutral NPC that can get angry and chomp'''
    def __init__(self, position, frames, groups) -> None:
        super().__init__(groups)
        self.state = 'chomp'
        self.facing_right = True
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_frect(topleft= position)
        
        self.z = Z_LAYERS['main']
        
        self.direction = 1
        
    def animate(self, dt) -> None:
        self.frame_index += ANIMATION_SPEED * dt
                
        self.image = self.frames[self.state][int(self.frame_index) % len(self.frames[self.state])]
        self.image = self.image if self.facing_right else pygame.transform.flip(self.image, True, False)
    
    def update(self, dt) -> None:
        
        self.animate(dt)


class Ghost(pygame.sprite.Sprite):
    '''Ghost is a friendly NPC that appears on some levels and trades with the player'''
    def __init__(self, position, frames, groups) -> None:
        super().__init__(groups)
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(topleft= position)
        
        self.z = Z_LAYERS['main']
        
        self.direction = 1
    
    def animate(self, dt) -> None:
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image
    
    def update(self, dt) -> None:
        
        self.animate(dt)


class Snail(pygame.sprite.Sprite):
    '''Snail is a friendly NPC that moves left and right. The player can ride on it to avoid spike damage'''
    def __init__(self, position, frames, groups, collision_sprites) -> None:
        super().__init__(groups)
        self.moving = True
        
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(topleft= position)
        
        self.hitbox_rect = pygame.FRect((self.rect.topleft + vector(4, 1)), (7, 7))
        self.old_rect = self.hitbox_rect.copy()
        
        self.z = Z_LAYERS['main']
        
        dir = choice((-1, 1))
        self.direction = vector(dir, 0)
        
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
                
        self.speed = 8
    
    def reverse(self) -> None:
        floor_rect_right = pygame.FRect(self.hitbox_rect.bottomright, (1, 1))
        floor_rect_left = pygame.FRect(self.hitbox_rect.bottomleft + vector(-1, 0), (1, 1))
        wall_rect = pygame.FRect(self.hitbox_rect.topleft + vector(-1, 0), (self.hitbox_rect.width + 2, 2))
        
        if floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction.x > 0 or\
            floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction.x < 0 or\
            wall_rect.collidelist(self.collision_rects) != -1:
            self.direction.x *= -1
    
    def move(self, dt) -> None:
        self.hitbox_rect.x += self.direction.x * self.speed * dt
        
        self.rect.topleft = self.hitbox_rect.topleft + vector(-4, -1)
        self.map_rect.x, self.map_rect.y = (self.hitbox_rect.x / TILE_SIZE), self.hitbox_rect.y / TILE_SIZE
    
    def animate(self, dt) -> None:
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
        self.image = pygame.transform.flip(self.image, True, False) if self.direction.x < 0 else self.image
    
    def show_hitbox(self):
        '''Display a colourful hitbox for debug purposes'''
        surf = pygame.Surface(self.hitbox_rect.size)
        surf.fill('yellow')
        self.image.blit(surf, (4, 1))
    
    def update(self, dt) -> None:
        self.old_rect = self.hitbox_rect.copy()
        
        self.move(dt)
        self.reverse()
        
        self.animate(dt)
        #self.show_hitbox()