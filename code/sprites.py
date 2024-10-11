from settings import *
from gtimer import Timer

# BLUEPRINTS
class Sprite(pygame.sprite.Sprite):
    '''A regular static sprite'''
    def __init__(self, position, surface= pygame.Surface((TILE_SIZE, TILE_SIZE)), groups= None, z= Z_LAYERS['main']) -> None:
        super().__init__(groups)
        
        self.image = surface
        self.rect = self.image.get_frect(topleft= position)
        self.old_rect = self.rect.copy()
        
        self.z = z

class AnimatedSprite(Sprite):
    '''A static but animated sprite'''
    def __init__(self, position, frames, groups, z= Z_LAYERS['main'], animation_speed = ANIMATION_SPEED) -> None:
        self.frames, self.frame_index = frames, 0
        super().__init__(position, self.frames[self.frame_index], groups, z)
        self.animation_speed = animation_speed
    
    def animate(self, dt) -> None:
        '''Animate through sprite frames'''
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
    
    def update(self, dt) -> None:
        '''The update method'''
        self.animate(dt)

class MovingSprite(AnimatedSprite):
    '''A moving animated sprite'''
    def __init__(self, frames, groups, start_pos, end_pos, move_dir, speed, flip= False) -> None:
        super().__init__(start_pos, frames, groups)
        
        if move_dir == 'x':
            self.rect.midleft = start_pos
        else:
            self.rect.midtop = start_pos
        
        self.start_pos = start_pos
        self.end_pos = end_pos
        
        # movement
        self.moving = True
        self.speed = speed
        self.direction = vector(1, 0) if move_dir == 'x' else vector(0, 1)
        self.move_dir = move_dir
        
        self.flip = flip
        self.reverse = {'x': False, 'y': False}
    
    def check_border(self) -> None:
        if self.move_dir == 'x':
            if self.rect.right >= self.end_pos[0] and self.direction.x == 1:
                self.direction.x = -1
                self.rect.right = self.end_pos[0]
            if self.rect.left <= self.start_pos[0] and self.direction.x == -1:
                self.direction.x = 1
                self.rect.left = self.start_pos[0]
            self.reverse['x'] = True if self.direction.x < 0 else False
        else:
            if self.rect.bottom >= self.end_pos[1] and self.direction.y == 1:
                self.direction.y = -1
                self.rect.bottom = self.end_pos[1]
            if self.rect.top <= self.start_pos[1] and self.direction.y == -1:
                self.direction.y = 1
                self.rect.top = self.start_pos[1]
            self.reverse['y'] = True if self.direction.y > 0 else False
    
    def update(self, dt) -> None:
        self.old_rect = self.rect.copy()
        self.rect.topleft += self.direction * self.speed * dt
        self.check_border()
        
        self.animate(dt)
        if self.flip:
            self.image = pygame.transform.flip(self.image, self.reverse['x'], self.reverse['y'])

# LEVEL
class Item(AnimatedSprite):
    '''An item that can be picked up by player'''
    def __init__(self, item_type, position, frames, groups, data):
        self.data = data
        super().__init__(position, frames, groups)
        self.rect.center = position
        self.item_type = item_type
        self.animation_speed = ANIMATION_SPEED * 1.5
    
    def activate(self) -> None:
        if self.item_type == 'coin':
            self.data.coins += 1
        if self.item_type == 'key':
            self.data.key = True
        self.kill()

class VFX(AnimatedSprite):
    '''A visual effect used for projectile collisions'''
    def __init__(self, position, frames, groups) -> None:
        super().__init__(position, frames, groups)
        self.rect.center = position
        self.z = Z_LAYERS['fg']
        self.animation_speed = 16
    
    def animate(self, dt) -> None:
        self.frame_index += self.animation_speed * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

class ExprBubble(Sprite):
    marks = {
        '?': 0,
        '!': 1,
        'key': 2
    }
    def __init__(self, position, frames, groups, mark) -> None:
        self.image = frames[ExprBubble.marks[mark]]
        super().__init__(position, self.image, groups)
        
        self.timer = Timer(10)
        self.timer.start()
    
    def update(self, dt) -> None:
        self.timer.update()
        if not self.timer.active:
            self.kill()

# UI
class Heart(AnimatedSprite):
    '''A heart for the ui'''
    def __init__(self, position, frames, groups) -> None:
        super().__init__(position, frames, groups)
        self.z = Z_LAYERS['main']
    
    def update(self, dt) -> None:
        self.animate(dt)

# TERRAIN
class Floor(Sprite):
    '''Regular static terrain, the minimap visibility can be toggled as an argument'''
    def __init__(self, position, surface, groups, hidden=False) -> None:
        super().__init__(position, surface, groups)
        
        if not hidden:
            # minimap
            self.map_image = pygame.Surface((1, 1))
            self.map_image.fill('white')
            self.map_rect = self.map_image.get_frect(topleft = (position[0] / TILE_SIZE, position[1] / TILE_SIZE))

class Platform(Floor):
    '''Regular static platform'''
    def __init__(self, position, surface, groups) -> None:
        super().__init__(position, surface, groups)
        self.map_image.fill('gray')

# INTERACTIBLES
class Door(Sprite):
    def __init__(self, position, frames, groups) -> None:
        super().__init__(position, frames[0], groups, Z_LAYERS['bg_tiles'])
        self.frames, self.frame_index = frames, 0
        self.unlocked = False
    
    def animate(self, dt) -> None:
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[int(self.frame_index % len(self.frames))]
    
    def update(self, dt) -> None:
        if self.unlocked:
            self.animate(dt)

class Lever(Sprite):
    def __init__(self, position, surface, groups, linked_object) -> None:
        super().__init__(position, surface, groups, Z_LAYERS['bg_tiles'])
        self.activated_surface = pygame.transform.flip(self.image, True, False)
        self.activated = False
        self.linked_object = linked_object
    
    def update(self, dt) -> None:
        self.image = self.activated_surface if self.activated else self.image

# OVERWORLD
class Node(pygame.sprite.Sprite):
    def __init__(self, position, surface, groups, level, data, paths) -> None:
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_frect(center= (position[0] + TILE_SIZE / 2, position[1] + TILE_SIZE / 2))
        self.z = Z_LAYERS['path']
        self.level = level
        self.data = data
        self.paths = paths
        self.grid_position = (int(position[0] / TILE_SIZE), int(position[1] / TILE_SIZE))
    
    def can_move(self, direction) -> bool:
        if direction in list(self.paths.keys()) and int(self.paths[direction][0][0]) <= self.data.unlocked_level:
            return True

class Icon(pygame.sprite.Sprite):
    def __init__(self, position, groups, frames) -> None:
        super().__init__(groups)
        self.icon = True
        self.path = None
        self.direction = vector()
        self.speed = 48
        
        # image
        self.frames, self.frame_index = frames, 0
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]
        self.z = Z_LAYERS['main']
        self.rect = self.image.get_frect(center = position)
    
    def start_move(self, path) -> None:
        self.rect.center = path[0]
        self.path = path[1:]
        self.find_path()
    
    def find_path(self) -> None:
        if self.path:
            # VERTICAL
            if self.rect.centerx == self.path[0][0]:
                self.direction = vector(0, 1 if self.path[0][1] > self.rect.centery else -1)
            # HORIZONTAL
            else:
                self.direction = vector(1 if self.path[0][0] > self.rect.centerx else -1, 0)
        else:
            self.direction = vector(0, 0)
    
    def point_collision(self) -> None:
        if self.direction.y == 1 and self.rect.centery >= self.path[0][1] or \
            self.direction.y == -1 and self.rect.centery <= self.path[0][1]:
            self.rect.centery = self.path[0][1]
            del self.path[0]
            self.find_path()
        
        if self.direction.x == 1 and self.rect.centerx >= self.path[0][0] or \
            self.direction.x == -1 and self.rect.centerx <= self.path[0][0]:
            self.rect.centerx = self.path[0][0]
            del self.path[0]
            self.find_path()
    
    def get_state(self) -> None:
        self.state = 'idle'
        if self.direction == vector(1, 0):
            self.state = 'right'
        if self.direction == vector(-1, 0):
            self.state = 'left'
        if self.direction == vector(0, 1):
            self.state = 'down'
        if self.direction == vector(0, -1):
            self.state = 'up'
    
    def animate(self, dt) -> None:
        self.frame_index += ANIMATION_SPEED * dt
        self.image = self.frames[self.state][int(self.frame_index % len(self.frames[self.state]))]
    
    def update(self, dt) -> None:
        if self.path:
            self.point_collision()
            self.rect.center += self.direction * self.speed * dt
        self.get_state()
        self.animate(dt)

class PathSprite(Sprite):
    def __init__(self, position, surface, groups, level) -> None:
        super().__init__(position, surface, groups, Z_LAYERS['path'])
        self.level = level