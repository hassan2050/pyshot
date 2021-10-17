#!/usr/bin/env python3

import os, sys, string, time, logging, math, argparse
from logging import debug,warning,info,error,fatal,critical; warn=warning

from ursina import *
from ursina import application

class MenuButton(Button):
    def __init__(self, text='', **kwargs):
        super().__init__(text, scale=(.65, .15), highlight_color=color.azure, **kwargs)

        self.clickSound = None
        for key, value in kwargs.items():
          setattr(self, key, value)

    def on_click(self):
      if self.clickSound:
        self.clickSound.play()
      super().on_click()
      

class Screen(Entity):
  def __init__(self, app, **kwargs):
    super().__init__(**kwargs)
    self.app = app
    self._event_mapping = {}
    
    self.setup()

  def setup(self):
    pass

  def on_change(self):
    pass

  def accept(self, key, func):
    self._event_mapping[key] = func

  def input(self, key):
    handler = self._event_mapping.get(key)
    if handler:
      handler()
      return True
    return False
            
class MainMenuEntity(Screen):
  def setup(self):
    # main menu content
    self.buttons = [
        MenuButton('Start', on_click=self.app.startGame),
        MenuButton('Load game', on_click=Func(self.app.showMenu, 'load')),
        MenuButton('Options', on_click=Func(self.app.showMenu, 'options')),
        MenuButton('Quit', on_click=Sequence(Wait(.01), Func(self.app.quit))),
    ]
    for i, e in enumerate(self.buttons):
        e.parent = self
        e.clickSound = self.app.clickSound
        e.y = .1+ -i * self.app.button_spacing

  def on_change(self):
    if not self.app.music.status() == self.app.music.PLAYING:
      self.app.music.play()
  
class CountDownEntity(Screen):
  def setup(self):
    red = (1,0,0,1)
    defaults = {}
    defaults['color'] = red
    defaults['parent'] = self
    defaults['font'] = self.app.digitfont

    grey_defaults = defaults.copy()
    grey_defaults['color'] = (1, 1, 1, .2)

    Text(scale=10, text='0', origin=(-0.0, .3), **grey_defaults)
    self.timer = Text(scale=10, text='0', origin=(-0.0, .3), **defaults)

  def on_change(self):
    self.endTime = time.time() + 5

    self.app.music.stop()
    self.app.countdownSound.play()
    
  def updateTimer(self):
    dt = int(self.endTime - time.time())
    if dt == 4:
      self.timer.text = ""
    else:
      self.timer.text = "%d" % (dt)

    if dt <= 0:
      self.app.showMenu("game")
      
  def update(self):
    self.updateTimer()
  
class OptionsMenuEntity(Screen):
  def setup(self):
    defaults = {}
    defaults['parent'] = self
    defaults['clickSound'] = self.app.clickSound
    
    # options menu content
    review_text = Text(x=.275, y=.25, text='Preview text', origin=(-.5,0), **defaults)
    for t in [e for e in scene.entities if isinstance(e, Text)]:
      t.original_scale = t.scale

    text_scale_slider = Slider(0, 2, default=1, step=.1, dynamic=True, text='Text Size:',
                               x=-.25, **defaults)
    def set_text_scale():
      pass
    
    text_scale_slider.on_value_changed = set_text_scale

    volume_slider = Slider(0, 1, default=Audio.volume_multiplier, step=.1, text='Master Volume:',
                           x=-.25, **defaults)
    def set_volume_multiplier():
        Audio.volume_multiplier = volume_slider.value
    volume_slider.on_value_changed = set_volume_multiplier

    options_back = MenuButton(text='Back', x=-.25, origin_x=-.5,
                              on_click=Func(self.app.showMenu, 'main'), **defaults)

    for i, e in enumerate((text_scale_slider, volume_slider, options_back)):
        e.y = -i * self.app.button_spacing
    
class LoadMenuEntity(Screen):
  def setup(self):

    defaults = {}
    defaults['parent'] = self
    defaults['clickSound'] = self.app.clickSound
    
    # load menu content
    for i in range(3):
      MenuButton(text=f'Empty Slot {i}', y=-i * self.app.button_spacing+.1, **defaults)

    self.back_button = MenuButton(text='Back', y=((-i-1) * self.app.button_spacing),
                                  on_click=Func(self.app.showMenu, 'main'), **defaults)

    
class GameEntity(Screen):
  def setup(self):
    red = (1,0,0,1)
    defaults = {}
    defaults['color'] = red
    defaults['parent'] = self
    defaults['font'] = self.app.digitfont

    grey_defaults = defaults.copy()
    grey_defaults['color'] = (1, 1, 1, .2)

    Text(scale=6, text='00', origin=(-0.6, 0), **grey_defaults)
    self.score1 = Text(scale=6, text='00', origin=(-0.6, 0), **defaults)
    Text(scale=6, text='00', origin=(0.6, 0), **grey_defaults)
    self.score2 = Text(scale=6, text='00', origin=(0.6, 0), **defaults)
    Text(scale=4, text='00', origin=(0, 1.0), **grey_defaults)
    self.timer = Text(scale=4, text='00', origin=(0, 1.0), **defaults)

    self.updateScores()

    self.accept('z', self.app.leftBasket)
    self.accept('x', self.app.rightBasket)
    
  def on_change(self):
    self.app.scores = [0, 0]
    self.endTime = time.time() + 31

    self.app.audience.play()
    
  def updateScores(self):
    self.score1.text = "%02d" % self.app.scores[0]
    self.score2.text = "%02d" % self.app.scores[1]

  def updateTimer(self):
    dt = int(self.endTime - time.time())
    self.timer.text = "%02d" % dt

    if dt <= 0:
      self.app.audience.stop()
      self.app.showMenu("main")
      
  def update(self):
    self.updateScores()
    self.updateTimer()

class App(Ursina):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.menus = {}
    
  def addMenu(self, name, menu):
    self.menus[name] = menu
    return menu

  def showMenu(self, name):
    logging.debug("showMenu %s" % name)
    self.state_handler.state = name
    menu = self.menus[name]
    menu.on_change()
    self.animate_in_menu(menu)
  
  def input(self, key):
    entity = self.menus[self.state_handler.state]
    ret = entity.input(key)
    if not ret:
      super().input(key)

class PyShot(App):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    application.setAssetFolder("Assets")
    
    Text.size = .1
    Text.default_resolution = 150
    
    # button_size = (.25, .075)
    self.button_spacing = .1 * 1.75
    self.menu_parent = Entity(parent=camera.ui, y=.15)

    if 1:
      self.digitfont = loader.loadFont("digital_counter_7.ttf")
      self.digitfont.setPixelsPerUnit(100)
      
    self.scores = [0, 0]
    self.endTime = 0

    self.music = loader.loadMusic("music/spacejam.wav")
    self.music.setLoop(True)
    self.music.setVolume(0.075)

    self.clickSound = loader.loadSfx("sounds/UIClick.ogg")
    self.basketSound = loader.loadSfx("sounds/basket.wav")
    self.basketSound.setVolume(0.075)
    self.countdownSound = loader.loadSfx("sounds/countdown.wav")

    self.audience = loader.loadMusic("sounds/audience.wav")
    self.audience.setLoop(True)
    self.audience.setVolume(0.075)

    self.main_menu = self.addMenu('main', MainMenuEntity(self, parent=self.menu_parent))
    self.game_menu = self.addMenu('game', GameEntity(self, parent=self.menu_parent))
    self.load_menu = self.addMenu('load', LoadMenuEntity(self, parent=self.menu_parent))
    self.countdown_menu = self.addMenu('countdown', CountDownEntity(self, parent=self.menu_parent))
    self.options_menu = self.addMenu('options', OptionsMenuEntity(self, parent=self.menu_parent))
    
    self.state_handler = Animator(self.menus)

    self.background = Entity(model='quad', texture='shore', parent=camera.ui,
                             scale=(camera.aspect_ratio,1), color=color.white, z=1)

    

    self.showMenu("main")

  def input(self, key):
    logging.debug("input %s" % key)
    
    if key == 'escape': self.quit()
    elif key == 'q':    self.showMenu("main")
    else:
      super().input(key)
    
  def leftBasket(self):
    self.scores[0] += 2
    self.basketSound.play()

  def rightBasket(self):
    self.scores[1] += 2
    self.basketSound.play()

  def quit(self):
    sys.exit(1)
      
  def startGame(self):
    logging.debug("startGame")
    self.showMenu("countdown")

  def animate_in_menu(self, menu):
    logging.debug("animate_in_menu %s" % menu)
    for i, e in enumerate(menu.children):
      if 0:
        e.original_x = e.x
        e.x += .1
        e.animate_x(e.original_x, delay=i*.05, duration=.1, curve=curve.out_quad)
      if 1:
        e.alpha = 0
        e.animate('alpha', .7, delay=i*.05, duration=.1, curve=curve.out_quad)

        if hasattr(e, 'text_entity'):
            e.text_entity.alpha = 0
            e.text_entity.animate('alpha', 1, delay=i*.05, duration=.1)
    

def start(args):
  app = PyShot(title="PyShot",
               size=(800,600),
               fullscreen=False,
               position=(0,0),
               development_mode=True,
               vsync=True)

  window.update_aspect_ratio()
  logging.debug("screen_resolution=%s" % repr(window.screen_resolution))
  logging.debug("Text.default_resolution=%s" % repr(Text.default_resolution))

  app.run()

def test():
  logging.warn("Testing")

def parse_args(argv):
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, description=__doc__)

  parser.add_argument("-t", "--test", dest="test_flag", default=False, action="store_true", help="Run test function")
  parser.add_argument("--log-level", type=str, choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Desired console log level")
  parser.add_argument("-d", "--debug", dest="log_level", action="store_const", const="DEBUG", help="Activate debugging")
  parser.add_argument("-q", "--quiet", dest="log_level", action="store_const", const="CRITICAL", help="Quite mode")
  parser.add_argument("files", type=str, nargs='*')

  args = parser.parse_args(argv[1:])

  return parser, args

def main(argv, stdout, environ):
  if sys.version_info < (3, 0): reload(sys); sys.setdefaultencoding('utf8')

  parser, args = parse_args(argv)

  logging.basicConfig(format="[%(asctime)s] %(levelname)-6s %(message)s (%(filename)s:%(lineno)d)", 
                      datefmt="%m/%d %H:%M:%S", level=args.log_level)

  if args.test_flag:  test();   return

  start(args)

if __name__ == "__main__":
  main(sys.argv, sys.stdout, os.environ)
