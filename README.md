# VIDEO GAME PROJECT
    Project Title: 'Stickman'
    Language: Python 3.12.2
    Library: pygame-ce 2.5.1 (SDL 2.30.6)
    Graphic Assets made with Aseprite 1.3.8
    Tilesets and Maps made with Tiled 1.11.0

## Project Description
'Stickman' is a simple 2D platformer video game, where the player controls a stick figure. The game has an overworld stage and several individual level stages. The player unlocks access to new levels on the overworld as progressing with finishing prior ones.

### Overworld
There are Nodes and Paths on the Overworld that represent level stages and the progression between them. A new path only becomes available to traverse if a previous level stage has been finished.

### Levels
The player has to find a key that unlocks a door leading out of the level stage. The key can either be found somewhere on the level or another item can be found and traded to an NPC, who then either directly gives the key to the player in return, or opens a new part of the level to be discovered where the key can be located.

### Obstacles
There are spikes and other traps on the levels. Collision with said traps and spikes results in death and being respawned at a checkpoint on the level. If the player has not reached the first checkpoint yet, they spawn back on the overworld.

### Enemies
There are enemies on each level stage that damage the player if collision occurs between their sprites or hitboxes. The player can also take damage by colliding with one of the enemy projectiles.

### Checkpoints
There are checkpoints on longer levels. Shall the player lose all lives or collide with a spike or other trap, they don't spawn on the overworld but at the last checkpoint location.