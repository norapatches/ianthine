from settings import *

class CameraGroup(pygame.sprite.Group):
    def __init__(self, width, height, data) -> None:
        '''The CameraGroup serves as a moving zoomed-in display surface that displays all sprites on level stages'''
        super().__init__()
        
        self.ui_sprites = [sprite for sprite in data.ui.sprites]
        
        self.display = pygame.display.get_surface()
        self.screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.offset = vector()
        self.width, self.height = width * TILE_SIZE, height * TILE_SIZE
        
        # minimap
        self.minimap = MiniMap(width, height)
        
        # camera boundaries
        self.borders = {
            'left': 0,
            'right': -self.width + SCREEN_WIDTH,
            'bottom': -self.height + SCREEN_HEIGHT,
            'top': 0
        }
    
    def camera_constraint(self) -> None:
        '''Don't allow camera movement when reaching level stage sides'''
        self.offset.x = self.offset.x if self.offset.x < self.borders['left'] else 0
        self.offset.x = self.offset.x if self.offset.x > self.borders['right'] else self.borders['right']
    
    def toggle_minimap(self) -> None:
        '''Show minimap while holding M key'''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            self.display.blit(self.minimap.scaled_surface, (10, WINDOW_HEIGHT - self.minimap.scaled_surface.height - 10))
    
    def draw(self, target_position, dt):
        '''The custom draw method for the CameraGroup that draws in Z layer order'''
        self.offset.x = -(target_position[0] - SCREEN_WIDTH / 2)
        self.offset.y = -(target_position[1] - SCREEN_HEIGHT / 2)
        self.camera_constraint()
        
        self.minimap.update(self.sprites())
        
        self.screen.fill('black')
        
        for sprite in sorted(self, key= lambda sprite: sprite.z):
            offset_pos = sprite.rect.topleft + self.offset
            self.screen.blit(sprite.image, offset_pos)
        
        #for sprite in self.ui_sprites:
        #    self.screen.blit(sprite.image, sprite.rect)
        
        pygame.transform.scale(self.screen, (WINDOW_WIDTH, WINDOW_HEIGHT), self.display)
        
        self.toggle_minimap()


class MiniMap:
    def __init__(self, width: int, height: int) -> None:
        '''A MiniMap surface that displays terrain and player position'''
        self.surface = pygame.Surface((width, height))
        self.scaled_surface = pygame.Surface((320, 240))
    
    def update(self, sprites) -> None:
        '''Update sprite positions'''
        self.scaled_surface.fill('black')
        self.surface.fill('black')
        
        for sprite in sprites:
            if hasattr(sprite, 'map_image'):
                self.surface.blit(sprite.map_image, (sprite.map_rect))
        
        scaled = pygame.transform.scale(self.surface, self.scaled_surface.size)
        self.scaled_surface.blit(scaled, (0, 0))

