# GameEngine
This game engine was created for making Python 3d games easier!
You just need to install the game engine file into your project, that's easy! In this file, we already described all functions you need like ray casting, map generation, and more!
The game engine based on pygame, and the editing and adding something new is easy even for you!

Here is easy example of usage:

```
from game_engine import *

display, clock, player = init() # initialization game

txt_map = ["WWWWWWWWWWWW",
            "W..........W",
            "W..........W",
            "WWWWWWWWWWWW",
            "W..........W",
            "W..........W",
            "W..........W",
            "WWWWWWWWWWWW",
            ]
block_map = draw_map(txt_map, 0)

while True:
    quit_checking() # This fuction you use for check if user pressed a cross for close the window
    player.delta = delta_time() # getting delta time
    player.move() # checking if player moved
    display.fill((0, 0, 0)) # filling display in RGB
    draw_floor(display, 18,18,18, player) # drawing floor in the game
    draw_sky(display, 75, 153, 231, player) # drawing sky in the game
    ray_casting(display, player, block_map) # starting raycasting
    fps = str(int(clock.get_fps())) # fps
    show_fps(display, "corner", fps, clock) # showing fps
    pygame.display.flip() # showing all
```
