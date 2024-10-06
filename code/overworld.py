from settings import *
from camera import OverworldCamera
from controls import MenuControls
from sprites import AnimatedSprite, Sprite, Icon, Node, PathSprite

class Overworld:
    def __init__(self, tmx_map, data, overworld_frames, switch_stage) -> None:
        self.display = pygame.display.get_surface()
        self.data = data
        self.switch_stage = switch_stage
        
        self.controls = MenuControls()
        
        # groups
        self.all_sprites = OverworldCamera(
            width= tmx_map.width,
            height= tmx_map.height,
            data= data
        )
        self.node_sprites = pygame.sprite.Group()
        
        self.setup(tmx_map, overworld_frames)
        
        self.current_node = [node for node in self.node_sprites if node.level == 0][0]
        
        self.path_frames = overworld_frames['path']
        self.create_path_sprites()
    
    def setup(self, tmx_map, overworld_frames) -> None:
        # tiles
        for layer in ['main', 'top']:
            for x, y, surface in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), surface, self.all_sprites, Z_LAYERS['bg_tiles'])
        
        # water
        for col in range(tmx_map.width):
            for row in range(tmx_map.height):
                AnimatedSprite((col * TILE_SIZE, row * TILE_SIZE), overworld_frames['water'], self.all_sprites, Z_LAYERS['bg'])
        
        # objects
        for obj in tmx_map.get_layer_by_name('objects'):
            Sprite((obj.x, obj.y), obj.image, self.all_sprites, Z_LAYERS['bg_details'])
        
        # paths
        self.paths = {}
        for obj in tmx_map.get_layer_by_name('paths'):
            position = [(int(p.x + TILE_SIZE / 2), int(p.y + TILE_SIZE / 2)) for p in obj.points]
            start = obj.properties['start']
            end = obj.properties['end']
            self.paths[end] = {'pos': position, 'start': start}
        
        # nodes and player
        for obj in tmx_map.get_layer_by_name('nodes'):
            
            # player
            if obj.name == 'node' and obj.properties['stage'] == self.data.current_level:
                self.icon = Icon((obj.x + TILE_SIZE / 2, obj.y + TILE_SIZE / 2), self.all_sprites, overworld_frames['icon'])
            
            # nodes
            if obj.name == 'node':
                available_paths = {k:v for k, v in obj.properties.items() if k in ('left', 'right', 'up', 'down')}
                Node(position= (obj.x, obj.y),
                     surface= overworld_frames['path']['node'],
                     groups= (self.all_sprites, self.node_sprites),
                     level= obj.properties['stage'],
                     data= self.data,
                     paths= available_paths)
    
    def create_path_sprites(self) -> None:
        # get tiles from path
        nodes = {node.level: vector(node.grid_position) for node in self.node_sprites}
        path_tiles = {}
        
        for path_id, data in self.paths.items():
            path = data['pos']
            start_node, end_node = nodes[data['start']], nodes[path_id]
            path_tiles[path_id] = [start_node]
            
            for idx, points in enumerate(path):
                if idx < len(path) - 1:
                    start, end = vector(points), vector(path[idx + 1])
                    path_dir = (end - start) / TILE_SIZE
                    start_tile = vector(int(start[0] / TILE_SIZE), int(start[1] / TILE_SIZE))
                    
                    if path_dir.y:
                        dir_y = 1 if path_dir.y > 0 else -1
                        for y in range(dir_y, int(path_dir.y) + dir_y, dir_y):
                            path_tiles[path_id].append(start_tile + vector(0, y))
                    
                    if path_dir.x:
                        dir_x = 1 if path_dir.x > 0 else -1
                        for x in range(dir_x, int(path_dir.x) + dir_x, dir_x):
                            path_tiles[path_id].append(start_tile + vector(x, 0))
            
            path_tiles[path_id].append(end_node)
        
        # create sprites
        for key, path in path_tiles.items():
            for idx, tile in enumerate(path):
                if idx > 0 and idx < len(path) - 1:
                    prev_tile = path[idx - 1] - tile
                    next_tile = path[idx + 1] - tile
                    
                    if prev_tile.x == next_tile.x:
                        surface = self.path_frames['vertical']
                    elif prev_tile.y == next_tile.y:
                        surface = self.path_frames['horizontal']
                    else:
                        if prev_tile.x == -1 and next_tile.y == -1 or prev_tile.y == -1 and next_tile.x == -1:
                            surface = self.path_frames['tl']
                        elif prev_tile.x == 1 and next_tile.y == 1 or prev_tile.y == 1 and next_tile.x == 1:
                            surface = self.path_frames['br']
                        elif prev_tile.x == -1 and next_tile.y == 1 or prev_tile.y == 1 and next_tile.x == -1:
                            surface = self.path_frames['bl']
                        elif prev_tile.x == 1 and next_tile.y == -1 or prev_tile.y == -1 and next_tile.x == 1:
                            surface = self.path_frames['tr']
                        else:
                            surface = self.path_frames['horizontal']
                
                    PathSprite(position= (tile.x * TILE_SIZE, tile.y * TILE_SIZE),
                            surface= surface,
                            groups= self.all_sprites,
                            level= key)
    
    def input(self) -> None:
        keys = pygame.key.get_pressed()
        if self.current_node and not self.icon.path:
            if keys[self.controls.down] and self.current_node.can_move('down'):
                self.move('down')
            if keys[self.controls.left] and self.current_node.can_move('left'):
                self.move('left')
            if keys[self.controls.right] and self.current_node.can_move('right'):
                self.move('right')
            if keys[self.controls.up] and self.current_node.can_move('up'):
                self.move('up')
            
            if keys[self.controls.confirm]:
                self.data.current_level = self.current_node.level
                self.switch_stage('level')
    
    def move(self, direction) -> None:
        path_key = int(self.current_node.paths[direction][0])
        path_reverse = True if self.current_node.paths[direction][-1] == 'r' else False
        path = self.paths[path_key]['pos'][:] if not path_reverse else self.paths[path_key]['pos'][::-1]
        self.icon.start_move(path)
    
    def get_current_node(self)-> None:
        nodes = pygame.sprite.spritecollide(self.icon, self.node_sprites, False)
        if nodes:
            self.current_node = nodes[0]
    
    def run(self, dt) -> None:
        self.display.fill('black')
        self.input()
        self.get_current_node()
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.icon.rect)