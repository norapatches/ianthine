from settings import *
from gtimer import Timer
from random import choice

# BLUEPRINT CLASS TO INHERIT FROM
class Enemy(pygame.sprite.Sprite):
    '''Enemy types & states
        Chaser      [asleep, idle, charge, walk, *death]
        Crawler     [idle, walk, *death]
        Floater     [asleep, idle, walk, *death]
        Shooter     [asleep, idle, notice, shoot, *death]
        Skipper     [idle, jump, *death]
        Walker      [idle, walk, death]
    '''
    def __init__(self, position, frames, groups) -> None:
        self.enemy = True
        super().__init__(groups)
        
        self.frames, self.frame_index = frames, 0
        self.state, self.facing_right = 'idle', True
        self.image = self.frames[self.state][self.frame_index]
        
        self.mask = pygame.mask.from_surface(self.image)
        
        self.rect = self.image.get_frect(topleft= position)
        self.old_rect = self.rect.copy()
        self.z = Z_LAYERS['main']
        
        self.direction = vector()
        self.speed = 16
        self.animation_speed = ANIMATION_SPEED
    
    def take_hit(self) -> None:
        pass


# ENEMY TYPES
class Chaser(Enemy):
    '''Chaser enemy is asleep until player near, moves towards player if on level, stops near edges & walls'''
    def __init__(self, position, frames, groups, collision_sprites, player) -> None:
        super().__init__(position, frames, groups)
        self.hitbox_rect = self.rect.inflate(-4, 0)
        self.old_rect = self.hitbox_rect.copy()
        self.speed = 32
        
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        self.player = player
        
        self.player_near = {'x': False, 'y': False}
        
        self.timers = {'hit': Timer(400), 'edge': Timer(600)}
    
    def take_hit(self) -> None:
        '''Move backwards when hit by player'''
        if not self.timers['hit'].active:
            self.direction.x *= -1
            self.hitbox_rect.move_ip(-16, 0) if self.direction.x < 0 else self.hitbox_rect.move_ip(16, 0)
            self.timers['hit'].start()
    
    def check_player_near(self) -> None:
        '''Check if player is nearby'''
        player_pos, chaser_pos = vector(self.player.hitbox_rect.center), vector(self.hitbox_rect.center)
        
        self.player_near['x'] = chaser_pos.distance_to(player_pos) <= 64
        self.player_near['y'] = abs(chaser_pos.y - player_pos.y) <= 16
    
    def check_contact(self) -> None:
        '''Check contact with walls and edges'''
        floor_rect_right = pygame.FRect((self.hitbox_rect.bottomright), (2, 2))
        floor_rect_left = pygame.FRect((self.hitbox_rect.bottomleft + vector(-2, 0)), (2, 2))
        wall_rect = pygame.FRect((self.hitbox_rect.topleft + vector(-2, 0)), (self.hitbox_rect.width + 4, 2))
        
        if floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction.x > 0 or\
            floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction.x < 0 or\
            wall_rect.collidelist(self.collision_rects) != -1:
            self.timers['edge'].start()
            self.hitbox_rect.move_ip(-1, 0) if self.direction.x > 0 else self.hitbox_rect.move_ip(1, 0)
    
    def get_state(self) -> None:
        '''Get states for animation'''
        self.state = 'asleep'
        if self.player_near['x'] and not self.player_near['y'] and not self.player.crouch:
            self.state = 'idle'
        if self.player_near['x'] and self.player_near['y'] and not self.player.crouch:
            self.state = 'walk'
    
    def update_timers(self) -> None:
        '''Update all timers'''
        for timer in self.timers.values():
            timer.update()
    
    def move(self, dt) -> None:
        '''The movement method'''
        if not self.timers['edge'].active:
            if self.player_near['x'] and self.player_near['y'] and not self.player.crouch:
                self.direction.x = -1 if self.player.hitbox_rect.centerx <= self.hitbox_rect.centerx else 1
                self.direction.x = 0 if self.timers['hit'].active else self.direction.x
                self.hitbox_rect.x += self.direction.x * self.speed * dt
                self.check_contact()
            self.rect.center = self.hitbox_rect.center
    
    def animate(self, dt) -> None:
        '''The animation method'''
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        self.image = pygame.transform.flip(self.image, True, False) if self.direction.x < 0 else self.image
        
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self, dt) -> None:
        '''The update method'''
        self.old_rect = self.hitbox_rect.copy()
        
        self.update_timers()
        
        self.check_player_near()
        self.move(dt)
        
        self.get_state()
        self.animate(dt)

class Crawler(Enemy):
    '''Crawler enemy moves around on surfaces endlessly'''
    def __init__(self, position, frames, groups, collision_sprites) -> None:
        super().__init__(position, frames, groups)
        self.hitbox_rect = self.rect.inflate(0, 0)
        self.old_rect = self.hitbox_rect.copy()
        self.speed = 8
        self.direction = vector(1, 0)
        self.state = 'walk'
        
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        
        self.on_surface = {'bottom': False, 'top': False, 'left': False, 'right': False}
        self.rotate = {'left': False, 'right': False}
    
    def check_contact(self) -> None:
        '''Check contact with walss and edges'''
        top_rect = pygame.FRect((self.rect.topleft + vector(0, -1)), (self.rect.width, 1))
        bottom_rect = pygame.FRect((self.rect.bottomleft), (self.rect.width, 1))
        left_rect = pygame.FRect((self.rect.topleft + vector(-1, 0)), (1, self.rect.height))
        right_rect = pygame.FRect((self.rect.topright), (1, self.rect.height))
        
        self.on_surface['bottom'] = True if bottom_rect.collidelist(self.collision_rects) >= 0 else False
        self.on_surface['top'] = True if top_rect.collidelist(self.collision_rects) >= 0 else False
        self.on_surface['left'] = True if left_rect.collidelist(self.collision_rects) >= 0 else False
        self.on_surface['right'] = True if right_rect.collidelist(self.collision_rects) >= 0 else False
    
    def move(self, dt) -> None:
        '''The movement method'''
        self.rect.topleft += self.direction * self.speed * dt
    
    def change_move_dir(self) -> None:
        '''Detect collision with terrain and change move direction'''
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
        '''The animation method'''
        self.frame_index += (ANIMATION_SPEED + 3) * dt
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        
        self.image = pygame.transform.rotate(self.image, 90) if self.rotate['left'] else self.image
        self.image = pygame.transform.rotate(self.image, -90) if self.rotate['right'] else self.image
        self.image = pygame.transform.flip(self.image, True, True) if self.on_surface['top'] else self.image
        
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self, dt) -> None:
        '''The update method'''
        self.old_rect = self.rect.copy()
        self.check_contact()
        
        self.move(dt)
        self.change_move_dir()
        
        self.animate(dt)

class Floater(Enemy):
    '''Floater enemy is asleep until player is near, moves towards player ignoring collisions if player is near and facing away'''
    def __init__(self, position, frames, groups, player) -> None:
        super().__init__(position, frames, groups)
        self.hitbox_rect = self.rect.inflate(-6, -2)
        self.old_rect = self.hitbox_rect.copy()
        
        self.facing_right = True
        self.speed = 36
        
        self.player = player
        self.player_near = {'x': False, 'y': False, 'facing_away': False}
    
    def check_player_near(self) -> None:
        '''Check if player is nearby'''
        player_pos, floater_pos = vector(self.player.hitbox_rect.center), vector(self.hitbox_rect.center)
        self.player_near['x'] = floater_pos.distance_to(player_pos) <= 80
        self.player_near['y'] = abs(floater_pos.y - player_pos.y) <= 80
        
        self.facing_right = True if self.hitbox_rect.centerx < self.player.hitbox_rect.centerx else False
        self.player_near['facing_away'] = True if \
            all((self.player_near['x'], self.player_near['y'])) and \
            ((self.hitbox_rect.centerx < self.player.hitbox_rect.centerx and all((self.facing_right, self.player.facing_right))) or\
            (self.hitbox_rect.centerx > self.player.hitbox_rect.centerx and not self.facing_right and not self.player.facing_right)) else False
    
    def get_state(self) -> None:
        '''Get states for animation'''
        self.state = 'asleep'
        if all((self.player_near['x'], self.player_near['y'])) and not self.player_near['facing_away']:
            self.state = 'idle'
        if self.player_near['facing_away']:
            self.state = 'move'

    def move(self, dt) -> None:
        '''The movement method'''
        if self.state == 'move':
            self.direction.x = 1 if self.hitbox_rect.centerx <= self.player.hitbox_rect.centerx else -1
            self.direction.y = 1 if self.hitbox_rect.centery <= self.player.hitbox_rect.centery else -1
            
            self.hitbox_rect.center += self.direction.normalize() * self.speed * dt if self.direction.x != 0 and self.direction.y != 0 else self.direction * self.speed * dt
            self.rect.center = self.hitbox_rect.center
    
    def animate(self, dt) -> None:
        '''The animation method'''
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        self.image = pygame.transform.flip(self.image, True, False) if not self.facing_right else self.image
        
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self, dt) -> None:
        '''The update method'''
        self.old_rect = self.hitbox_rect.copy()
        
        self.check_player_near()
        self.get_state()
        
        self.move(dt)
        self.animate(dt)

class Shooter(Enemy):
    '''Shooter enemy is stationary and asleep until player is near, turns towards player and shoots projectile is player is near'''
    def __init__(self, position, frames, groups, player, create_projectile) -> None:
        super().__init__(position, frames, groups)
        self.state = 'asleep'
        self.facing_right = True
        
        self.hitbox_rect = self.rect.inflate(0, 0)
        self.old_rect = self.hitbox_rect.copy()
        
        self.player = player
        
        self.timers = {'shoot': Timer(3000)}
        self.has_fired = False
        self.create_projectile = create_projectile
    
    def check_player_near(self) -> None:
        '''Check is playeris nearby'''
        player_pos, shooter_pos = vector(self.player.hitbox_rect.center), vector(self.rect.center)
        player_near = shooter_pos.distance_to(player_pos) < 64
        player_level = abs(shooter_pos.y - player_pos.y) < 32
        
        if player_near and player_level and not self.timers['shoot'].active:
            self.state = 'shoot'
            self.frame_index = 0
            self.timers['shoot'].start()
            self.facing_right = False if shooter_pos.x > player_pos.x else True
    
    def animate(self, dt) -> None:
        '''The animation method'''
        self.frame_index += (ANIMATION_SPEED + 2) * dt
        if self.frame_index < len(self.frames[self.state]):
            self.image = self.frames[self.state][int(self.frame_index)]
            self.image = pygame.transform.flip(self.image, True, False) if not self.facing_right else self.image
            self.mask = pygame.mask.from_surface(self.image)
            # fire
            if self.state == 'shoot' and int(self.frame_index) == len(self.frames[self.state]) - 1 and not self.has_fired:
                self.create_projectile(self.rect.topright, 1 if self.facing_right else -1)
                self.has_fired = True
        
        else:
            self.frame_index = 0
            if self.state == 'shoot':
                self.state = 'asleep'
                self.has_fired = False
    
    def update(self, dt) -> None:
        '''The update method'''
        self.old_rect = self.hitbox_rect.copy()
        
        self.timers['shoot'].update()
        
        self.check_player_near()
        
        self.animate(dt)

class Skipper(Enemy):
    '''Skipper enemy is jumping around the level endlessly, has full collision with all surfaces'''
    def __init__(self, position, frames, groups, collision_sprites) -> None:
        super().__init__(position, frames, groups)
    
    def update(self, dt) -> None:
        pass

class Walker(Enemy):
    '''Walker enemy walks around left and right and turns around on edges and walls'''
    def __init__(self, position, frames, groups, collision_sprites) -> None:
        super().__init__(position, frames, groups)
        
        self.hitbox_rect = self.rect.inflate(-6, 0)
        self.old_rect = self.hitbox_rect.copy()
        self.speed = 16
        self.direction = vector(choice((-1, 1)), 0)
        self.state = 'walk'
        self.collision_rects = [sprite.rect for sprite in collision_sprites]
        
        self.health = 3
        
        self.timers = {'hit': Timer(400), 'wait': Timer(1000), 'dir_change': Timer(5000, self.change_direction, True)}
        self.hit_timer = Timer(400)
    
    def take_hit(self) -> None:
        '''Take hit from player attack and die on third hit'''
        if not self.timers['hit'].active:
            self.health -= 1
            if self.health <= 0:
                self.state, self.frame_index = 'death', 0
                self.animation_speed = 1.5 * self.animation_speed
                self.direction.x, self.direction.y = 0, 0
            else:
                self.direction.x *= -1
            self.timers['hit'].start()
    
    def check_contact(self) -> None:
        '''Turn around on edges and walls'''
        floor_rect_right = pygame.FRect(self.hitbox_rect.bottomright, (1, 1))
        floor_rect_left = pygame.FRect(self.hitbox_rect.bottomleft, (-1, 1))
        wall_rect = pygame.FRect(self.hitbox_rect.topleft + vector(-1, 0), (self.hitbox_rect.width + 2, 1))
        
        if floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction.x > 0 or\
            floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction.x < 0 or\
            wall_rect.collidelist(self.collision_rects) != -1:
            self.direction.x *= -1
    
    def change_direction(self) -> None:
        self.state, self.frame_index = 'idle', 0
        self.timers['wait'].start()
        self.direction.x = choice((-1, 1))
    
    def move(self, dt) -> None:
        '''The mobve method'''
        if not self.timers['wait'].active and not self.state == 'death':
            self.state = 'walk'
            self.hitbox_rect.x += self.direction.x * self.speed * dt
            self.rect.center = self.hitbox_rect.center
    
    def animate(self, dt) -> None:
        '''Animate movement'''
        self.frame_index += self.animation_speed * dt
        
        if self.state == 'death' and int(self.frame_index) > len(self.frames[self.state]) - 1:
            self.kill()
        
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        self.image = pygame.transform.flip(self.image, True, False) if self.direction.x < 0 else self.image
        
        self.mask = pygame.mask.from_surface(self.image)
    
    def update_timers(self) -> None:
        for timer in self.timers.values():
            timer.update()
    
    def update(self, dt) -> None:
        self.old_rect= self.hitbox_rect.copy()
        self.update_timers()
        
        self.check_contact()
        self.move(dt)
        self.animate(dt)  


# ENEMY PROJECTILES
class Thorn(pygame.sprite.Sprite):
    right = np.array([
        [255, 0, 255],
        [255, 255, 255],
        [0, 255, 0]
    ], dtype=np.uint8)
    left = np.array([
        [0, 255, 0],
        [255, 255, 255],
        [255, 0, 255]
    ], dtype=np.uint8)
    def __init__(self, position, groups, direction, speed) -> None:
        self.enemy_projectile = True
        super().__init__(groups)
        
        self.image = pygame.surfarray.make_surface(Thorn.right if direction > 0 else Thorn.left)
        
        self.rect = self.image.get_frect(center= position + vector(-4, 4) if direction > 0 else position + vector(-12, 4))
        self.direction = direction
        self.speed = speed
        self.z = Z_LAYERS['main']
        
        self.timers = {'lifetime': Timer(5000)}
        self.timers['lifetime'].start()
    
    def update_timers(self) -> None:
        for timer in self.timers.values():
            timer.update()
    
    def update(self, dt) -> None:
        self.update_timers()
        
        self.rect.x += self.direction * self.speed * dt
        
        if not self.timers['lifetime'].active:
            self.kill()

