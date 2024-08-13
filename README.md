# STICKMAN

*v0.0.1*

*pygame-ce v2.5.1 | Python 3.12.2*

Stickman is a 2d platformer game that uses the [pygame-ce](http://pyga.me) library. The player character is a stick figure who can move left and right and is affected by gravity but can overcome it by jumping. The main goal of the game is exploring the given level, finding the key to the door, avoiding obstacles and/or enemies and finding the door.

## PLAYER

### Player abilities
**movement**
    - pressing the *LEFT* and *RIGHT* arrows

**jumping**
    - pressing the *SPACEBAR*
    - holding *SPACEBAR* increases jump length

**dashing**
    - pressing *X* key

**wall sliding**
    - when colliding with a wall, the gravity is reduced

**wall jumping**
    - when wall sliding is active the player can jump once

**crouching**
    - holding the *DOWN* arrow makes the character crouch
    - walking while crouching halves movement speed

**platform skip**
    - pressing the *DOWN* arrow key on semi-collidable platforms allows the player to fall downwards

### Snail
- they keep moving in a direction as long as not colliding with a wall or if there is no more surface to walk on
- they can move on spikes as if it was standard terrain
- the player is able to stand on the snail's shell and thus be carried over spikes

### Ghost
- they can be interacted with and they help with saving progress