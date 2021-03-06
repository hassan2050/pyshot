from ursina import *                    # this will import everything we need from ursina with just one line.
import random                           # Import the random library

random_generator = random.Random()      # Create a random number generator
texoffset = 0.0                         # define a variable that will keep the texture offset
texoffset2 = 0.0                        # define a variable that will keep the texture offset

def update():
    for entity in cubes:
        entity.rotation_y += time.dt * 5        # Rotate all the cubes every time update is called
    if held_keys['q']:                          # If q is pressed
        camera.position += (0, time.dt, 0)      # move up vertically
    if held_keys['a']:                          # If a is pressed
        camera.position -= (0, time.dt, 0)      # move down vertically

    global texoffset                            # Inform we are going to use the variable defined outside
    global texoffset2                           # Inform we are going to use the variable defined outside
    texoffset += time.dt * 0.2                  # Add a small number to this variable
    setattr(cube, "texture_offset", (0, texoffset))    # Assign as a texture offset
    texoffset2 += time.dt * 0.3                        # Add a small number to this variable
    setattr(cube2, "texture_offset", (0, texoffset2))  # Assign as a texture offset

    if mouse.hovered_entity == cube:
        info.visible = True
    else:
        info.visible = False


def input(key):
    if key == 'space':
        red = random_generator.random() * 255
        green = random_generator.random() * 255
        blue = random_generator.random() * 255
        cube.color = color.rgb(red, green, blue)

    if key == 'c':
        x = random_generator.random() * 10 - 5     # Value between -5 and 5
        y = random_generator.random() * 10 - 5     # Value between -5 and 5
        z = random_generator.random() * 10 - 5     # Value between -5 and 5
        s = random_generator.random() * 1          # Value between 0 and 1
        newcube = Entity(parent=cube, model='cube', color=color.white, position=(x, y, z), scale=(s,s,s), texture="crate")
        cubes.append(newcube)
        '''Create another child cube and add it to the list but using the newcube as the parent, keep the same colour, make it smaller'''
        childcube = Entity(parent=newcube, model='cube', color=color.white, position=(1, 0, 0), scale=(s/2, s/2, s/2), texture="crate")
        cubes.append(childcube)

if 1:
  window.title = 'My Game'                # The window title
  #window.size = (800,600)
  #window.size = (1920, 1080)
  #window.fullscreen_resolution = (1920, 1080)

  #window.borderless = False               # Show a border
  #window.fullscreen = False               # Go Fullscreen
  #window.exit_button.visible = False      # Show the in-game red X that loses the window
  #window.fps_counter.enabled = True       # Show the FPS (Frames per second) counter

  window.position = Vec2(0, 0)

  if 0:
    window.size = window.fullscreen_size
    window.position = Vec2(0, 0)
    window.fullscreen = True               # Go Fullscreen
    
    
app = Ursina()
window.update_aspect_ratio()

  
if 0:
  pass

cubes = []                              # Create the list
cube = Entity(model='cube', color=color.white, scale=(2,6,2), texture="waterfall", collider="box")
cube2 = Entity(model='cube', color=color.rgba(255,255,255,128), scale=(2.5,6,2.5), texture="waterfall")
cubes.append(cube)                      # Add the cube to the list
cubes.append(cube2)                     # Add the cube to the list

Text.size = 0.05
Text.default_resolution = 1080 * Text.size
info = Text(text="A powerful waterfall roaring on the mountains")
info.x = -0.5
info.y = 0.4
info.background = True
info.visible = False                    # Do not show this text

#win2 = app.open_window()

app.run()                               # opens a window and starts the game.

