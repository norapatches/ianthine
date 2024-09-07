from settings import *
from gtimer import Timer
from random import choice

'''Enemy types:
    Chaser      img=frames[state][idx]     is idle until player near, moves towards player if on level, turns around on edges & walls
    Crawler     img=frames[idx]            walks on surfaces, changes direction in corners
    Floater     img=frames[state][idx]     moves around on level towards player if near, ignores collision and physics
    *Shooter    img=frames[state][idx]     stationary, shoots projectiles at player if near
    *Skipper    img=frames[idx]            jumps around on level endlessly
    *Walker     img=frames[idx]            walks left-right, turns around on edges & walls

Using these enemy archetypes we can use different assets and have more enemies in total.
'''

class Chaser(pygame.sprite.Sprite):
    def __init__(self, position, frames, groups, collision_sprites, player) -> None:
        super().__init__(groups)
        self.frames, self.frame_index = frames, 0
        self.state, self.facing_right = 'asleep', True
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_frect(topleft= position)
        self.hitbox_rect = self.rect.inflate(-6, 0)
        self.old_rect = self.hitbox_rect.copy()
        self.z = Z_LAYERS['main']
        
        self.direction = vector()
        self.speed = 36
        
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        self.player = player
        
        self.player_near = {'x': False, 'y': False}
        
        self.timers = {'hit': Timer(400), 'edge': Timer(600)}
    
    def take_hit(self) -> None:
        if not self.timers['hit'].active:
            self.direction.x *= -1
            self.hitbox_rect.move_ip(-16, 0) if self.direction.x < 0 else self.hitbox_rect.move_ip(16, 0)
            self.timers['hit'].start()
    
    def check_player_near(self) -> None:
        player_pos, chaser_pos = vector(self.player.hitbox_rect.center), vector(self.hitbox_rect.center)
        self.player_near['x'] = chaser_pos.distance_to(player_pos) <= 64
        self.player_near['y'] = abs(chaser_pos.y - player_pos.y) <= 16
    
    def check_contact(self) -> None:
        floor_rect_right = pygame.FRect((self.hitbox_rect.bottomright), (2, 2))
        floor_rect_left = pygame.FRect((self.hitbox_rect.bottomleft + vector(-2, 0)), (2, 2))
        wall_rect = pygame.FRect((self.hitbox_rect.topleft + vector(-2, 0)), (self.hitbox_rect.width + 4, 2))
        
        if floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction.x > 0 or\
            floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction.x < 0 or\
            wall_rect.collidelist(self.collision_rects) != -1:
            self.timers['edge'].start()
            self.hitbox_rect.move_ip(-1, 0) if self.direction.x > 0 else self.hitbox_rect.move_ip(1, 0)
    
    def move(self, dt) -> None:
        if not self.timers['edge'].active:
            if self.player_near['x'] and self.player_near['y'] and not self.player.crouch:
                self.direction.x = -1 if self.player.hitbox_rect.centerx <= self.hitbox_rect.centerx else 1
                self.direction.x = 0 if self.timers['hit'].active else self.direction.x
                self.hitbox_rect.x += self.direction.x * self.speed * dt
                self.check_contact()
            self.rect.center = self.hitbox_rect.center
    
    def get_state(self) -> None:
        self.state = 'asleep'
        if self.player_near['x'] and not self.player_near['y'] and not self.player.crouch:
            self.state = 'idle'
        if self.player_near['x'] and self.player_near['y'] and not self.player.crouch:
            self.state = 'walk'
    
    def animate(self, dt) -> None:
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        self.image = pygame.transform.flip(self.image, True, False) if self.direction.x < 0 else self.image
    
    def update_timers(self) -> None:
        for timer in self.timers.values():
            timer.update()
    
    def update(self, dt) -> None:
        self.old_rect = self.hitbox_rect.copy()
        
        self.update_timers()
        self.check_player_near()
        
        self.move(dt)
        
        self.get_state()
        self.animate(dt)

class Crawler(pygame.sprite.Sprite):
    '''The Crawler can move on any surface endlessly'''
    def __init__(self, position, frames, groups, collision_sprites) -> None:
        super().__init__(groups)
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(topleft= position)
        self.old_rect = self.rect.copy()
        self.z = Z_LAYERS['main']
        
        self.direction = vector(1, 0)
        self.speed = 8
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
        self.image = pygame.transform.flip(self.image, True, True) if self.on_surface['top'] else self.image
    
    def update(self, dt) -> None:
        self.old_rect = self.rect.copy()
        self.check_contact()
        
        self.move(dt)
        self.change_move_dir()
        
        self.animate(dt)

class Floater(pygame.sprite.Sprite): pass

class Shooter(pygame.sprite.Sprite): pass

class Skipper(pygame.sprite.Sprite): pass

class Walker(pygame.sprite.Sprite):
    def __init__(self, position, frames, groups, collision_sprites) -> None:
        super().__init__(groups)
        self.enemy = True
        
        self.frames, self.frame_index = frames, 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(topleft= position)
        self.hitbox_rect = self.rect.inflate(-6, 0)
        self.z = Z_LAYERS['main']
        
        self.direction = choice((-1, 1))
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        
        self.speed = 32
        self.hit_timer = Timer(250)
    
    def take_hit(self) -> None:
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
        self.hitbox_rect.x += self.direction * self.speed * dt
        self.rect.center = self.hitbox_rect.center
        
        # reverse direction
        floor_rect_right = pygame.FRect(self.hitbox_rect.bottomright, (1, 1))
        floor_rect_left = pygame.FRect(self.hitbox_rect.bottomleft, (-1, 1))
        wall_rect = pygame.FRect(self.hitbox_rect.topleft + vector(-1, 0), (self.hitbox_rect.width + 2, 1))
        
        if floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction > 0 or\
            floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0 or\
            wall_rect.collidelist(self.collision_rects) != -1:
            self.direction *= -1
