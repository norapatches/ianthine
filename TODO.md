# TODO
These are the currently open tasks on each topic

## TERRAIN LAYERS
All terrain layers are always *Tile Layers* in the **tmx_maps**
- [ ] **terrain**           *Floor class*
    - visible & static
    - appears on minimap
    - full collision
- [ ] **terrain_hidden**    *Floor(hidden=True) class*
    - invisible & static
    - doesn't appear on minimap
    - full collision
- [ ] **terrain_collapse**  *CollapseFloor class*
    - visible & static
    - falls down and disappears
    - doesn't appear on minimap
    - semi-collision
- [ ] **platform**          *Platform class*
    - visible & static
    - appears on minimap
    - semi-collision
- [ ] **spike**             *Sprite class*
    - visible & static
    - doesn't appear on minimap
    - death on collision

## OBJECT LAYERS
The object layers' layout is the following:
- [ ] bg_details
The naming convention is \<*objectname*> or \<*static*>
    - animated background elements
    - static background elements
    - no collision
- [ ] objects
    - player
    - animated static platforms
    - static objects
    - door
    - static traps
- [ ] moving_objects
    - moving platforms
    - moving traps
- [ ] items
    - potions
    - trade items
    - key
- [ ] enemies
    - moving enemy
    - shooting enemy
- [ ] npc
    - snails
    - traders
- [ ] data
    - level data

## PLAYER
### Abilities
- [x] movement
    - **move left** - LEFT ARROW
    - **move right** - RIGHT ARROW
- [x] jumping
    - **jump** - SPACEBAR
- [ ] double jump
    - **double jump** - SPACEBAR *(in mid-air)*
- [x] walljump
    - **walljump** - SPACEBAR *(when wallsliding)*
- [ ] dash
    - **horizontal dash** - X KEY
- [x] crouch / platform skip
    - **crouch** - DOWN ARROW *(skips semi-collison surfaces)*
- [ ] interaction
    - **interact** - UP ARROW