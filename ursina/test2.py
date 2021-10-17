from ursina import *


app = Ursina()

window.title = 'My Game'                # The window title
#window.borderless = False               # Show a border
#window.borderless = True               # Show a border
window.fullscreen = False               # Do not go Fullscreen
#window.exit_button.visible = False      # Do not show the in-game red X that loses the window
#window.fps_counter.enabled = True       # Show the FPS (Frames per second) counter
window.update_aspect_ratio()

player = Entity(model='cube', color=color.orange, scale_y=2)

def update():
    player.x += held_keys['d'] * time.dt
    player.x -= held_keys['a'] * time.dt

def input(key):
    if key == 'space':
        player.y += 1
        invoke(setattr, player, 'y', player.y-1, delay=.25)


# start running the game
app.run()


