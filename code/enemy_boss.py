from settings import *
from gtimer import Timer
from random import choice, choices

class Golem(pygame.sprite.Sprite):
    def __init__(self, position, frames, groups, boulder_func, spike_func, player) -> None:
        self.enemy = True
        super().__init__(groups)
        
        self.frames, self.frame_index = frames, 0
        self.state, self.facing_right = 'idle', True
        self.image = self.frames[self.state][self.frame_index]
        
        self.rect = self.image.get_frect(topleft= position)
        self.hitbox_rect = pygame.FRect((self.rect.topleft + vector(10, 20)), (41, 41))
        self.old_rect = self.hitbox_rect.copy()
        self.z = Z_LAYERS['main']
        
        self.direction = vector()
        self.speed = 64
        self.init_position = position
        
        self.has_fired = False
        self.create_boulder = boulder_func
        self.create_spike = spike_func
        
        self.player = player
        
        self.timers = {
            'change_state' : Timer(5000)
        }
        self.timers['change_state'].start()
    
    def change_direction(self) -> None:
        self.facing_right = True if self.hitbox_rect.centerx <= self.player.hitbox_rect.centerx else False
        
        if self.state == 'right_punch':
            if int(self.frame_index) == 1:
                self.direction.x = 1 if self.facing_right else -1
            if int(self.frame_index) == 3:
                self.direction.x = -1 if self.facing_right else 1
        
        if self.state == 'left_hammer':
            if int(self.frame_index) == 1:
                self.direction.x = 1 if self.facing_right else -1
                self.direction.y = -1
            if int(self.frame_index) == 3:
                self.direction.x = 1 if self.facing_right else -1
                self.direction.y = 1
            if int(self.frame_index) == 4:
                self.direction.x = -1 if self.facing_right else 1
                self.direction.y = -1
            if int(self.frame_index) == 5:
                self.hitbox_rect.topleft = self.init_position + vector(10, 20)
        
        if self.state == 'ground_pound':
            chosen = choice(('boulder', 'spike'))
            
            if int(self.frame_index) == 1:
                self.direction.y = -1
            if int(self.frame_index) == 3:
                self.direction.y = 1
            if int(self.frame_index) == 5:
                if chosen == 'boulder':
                    self.hitbox_rect.topleft = self.init_position + vector(10, 20)
                    self.create_boulder(self.player.rect.midtop + vector(-4, -48), 1)
                    self.state = 'idle'
                
                if chosen == 'spike':
                    self.hitbox_rect.topleft = self.init_position + vector(10, 20)
                    self.create_spike(self.rect.bottomright + vector(0, -8), 1)
                    self.state = 'idle'
        
        if self.state == 'idle':
            self.hitbox_rect.topleft = self.init_position + vector(10, 20)
            self.direction.x, self.direction.y = 0, 0
    
    def move(self, dt) -> None:
        self.hitbox_rect.topleft += self.direction * self.speed * dt
        self.rect.topleft = self.hitbox_rect.topleft + vector(-10, -20)
    
    def change_state(self) -> None:
        if not self.timers['change_state'].active:
            #self.state = choices(('idle', 'left_hammer', 'ground_pound', 'right_punch'), (0, 0, 1, 0))[0]
            self.state = choices(('idle', 'left_hammer', 'ground_pound', 'right_punch'), (0.01, 0.33, 0.33, 0.33))[0]
            self.frame_index = 0
            self.timers['change_state'].start()
    
    def animate(self, dt) -> None:
        animation_speed = ANIMATION_SPEED - 2 if self.state == 'idle' else ANIMATION_SPEED + 3
                
        self.frame_index += animation_speed * dt
        
        if self.state in ('left_hammer', 'right_punch','ground_pound') and int(self.frame_index) > len(self.frames[self.state]) -1:
            self.state = 'idle'
        
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
        self.image = pygame.transform.flip(self.image, True, False) if not self.facing_right else self.image
    
    def update_timers(self) -> None:
        for timer in self.timers.values():
            timer.update()
    
    def update(self, dt) -> None:
        self.old_rect = self.hitbox_rect.copy()
        self.update_timers()
        self.change_state()
        
        self.change_direction()
        self.move(dt)
        
        self.animate(dt)

class Boulder(pygame.sprite.Sprite):
    def __init__(self, position, surface, groups, direction, speed) -> None:
        self.boss_projectile = True
        super().__init__(groups)
        
        self.image = surface
        self.rect = self.image.get_frect(topleft= position)
        self.direction = direction
        self.speed = speed
        self.z = Z_LAYERS['main']
        
        self.timers = {
            'lifetime': Timer(1500),
            'rotate': Timer(200, self.rotate, repeat=True)
        }
        self.timers['lifetime'].start()
    
    def rotate(self) -> None:
        self.image = pygame.transform.rotate(self.image, 90)
    
    def update(self, dt) -> None:
        for timer in self.timers.values():
            timer.update()
        
        self.rect.y += self.direction * self.speed * dt
        
        if not self.timers['lifetime'].active:
            self.kill()

class Spike(pygame.sprite.Sprite):
    def __init__(self, position, surface, groups, direction, speed) -> None:
        self.boss_projectile = True
        super().__init__(groups)
        
        self.image = surface
        self.image.fill('white')
        self.rect = self.image.get_frect(topleft= position)
        self.direction = direction
        self.speed = speed
        self.z = Z_LAYERS['main']
        
        self.timers = {
            'lifetime': Timer(1500)
        }
        self.timers['lifetime'].start()
    
    def update(self, dt) -> None:
        for timer in self.timers.values():
            timer.update()
        self.rect.x += self.direction * self.speed * dt
        
        if not self.timers['lifetime'].active:
            self.kill()
    