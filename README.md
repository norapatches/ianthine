- **Project Title** 'Stickman'
- **Project Version** *N/A*
- **Project Genre** platformer
- **Language** Python 3.12.2
- **Library** [pygame-ce](https://pyga.me) *2.5.1 (SDL 2.30.6)*
- Graphic Assets made with [Aseprite](https://aseprite.org) *1.3.8*
- Tilesets and Maps made with [Tiled](https://mapeditor.org) *1.11.0*
- [ClickUp](https://app.clickup.com/9012231275/home)

## Project Description
**'Stickman'** is a simple 2D *platformer* video game, where the player controls a stick figure. The game has an **overworld stage** and several individual **level stage**s. The player unlocks access to new levels on the overworld as progressing with finishing prior ones. The level stages have **checkpoints** where the player can respawn. The game has a **pause screen** both on the overworld and the level stages where the player can exit the game or resume gameplay.

### Overworld
There are **nodes** and **paths** on the overworld that represent **level stage**s and the progression between them. A new path only becomes available to traverse if a previous level stage has been finished.

### Levels
The player has to find a **key** that unlocks a door leading out of the level stage. The key can either be found somewhere on the level or another item can be found and **traded to an NPC**, who then either directly gives the key to the player in return, *or opens a new part of the level* to be discovered, where the key can be then located.

### Obstacles
There are **spikes** and **other traps** on the levels. Collision with said traps and spikes results in **death** and being respawned at a checkpoint on the level. If the player has not reached the first checkpoint yet, they *spawn back on the overworld*.

### Enemies
There are enemies on each level stage that damage the player if collision occurs between their sprites or hitboxes. The player can also take damage by colliding with one of the enemy projectiles. The player has five lives an each hit reduces their health by one.

### Checkpoints
There are checkpoints on longer levels. Shall the player lose all lives or collide with a spike or other trap, they don't spawn on the overworld but at the last checkpoint location.

### Items
The player can find items on the level stages that can be traded to NPCs, who then in return give either the key to the exit or open up a new area of the stage to discover the key in. The player can also find potions to heal with. Picking up the potion doesn't automatically heal the player, it can be used by pressing an action button.

### Key
The player can find the key on the level stage to open the door with and finish the level stage. This unlocks new Paths on the Overworld, to which the player is spawned the completing a level.
