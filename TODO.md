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
- [ ] **spike**             *Spike class*
    - visible & static
    - doesn't appear on minimap
    - death on collision

## PLAYER
### Abilities
- [x] movement
- [x] jumping
- [x] walljump
- [ ] dash
- [x] crouch / platform skip
- [ ] interaction