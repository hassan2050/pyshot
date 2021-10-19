#!/usr/bin/env python3

import os, sys, string, time, logging, math, argparse
from logging import debug,warning,info,error,fatal,critical; warn=warning

from panda3d.core import AudioManager

from ursina import *
from ursina import application

class Variable:
  def __init__(self, value=None):
    self._observers = []
    self.value = value

  def add_observer(self, observer, args=None):
    self._observers.append((observer, args))
    if args is not None:
      observer(self, args)
    else:
      observer(self)

  @property
  def value(self):
    return self._value
  
  @value.setter
  def value(self, value):
    self._value = value
    for (observer, args) in self._observers:
      if args is not None:
        observer(self, args)
      else:
        observer(self)
        
class DigitalText(Text):
  def __init__(self, **kwargs):
    grey_defaults = kwargs.copy()
    grey_defaults['color'] = (1, 1, 1, .02)
    
    self.grey = Text(**grey_defaults)
    
    super().__init__(**kwargs)

class MenuButton(Button):
  def __init__(self, text='', scale=(.65, .15), **kwargs):
    super().__init__(text, scale=scale, highlight_color=color.azure, **kwargs)

    self.clickSound = None
    for key, value in kwargs.items():
      setattr(self, key, value)

  def on_click(self):
    if self.clickSound:
      self.clickSound.play()
    super().on_click()

class GameScreen:
    def __init__(self, app):
      #super().__init__(app)
      self.app = app
      self.name = "NA"
  
      
class StandardGame(GameScreen):
    def __init__(self, app):
      super().__init__(app)
      self.name = "Standard"
      self.description = "2 Players\n:30 on clock\n\nBaskets are worth 2 points for the first 20 seconds, then 3 points for the final 10 seconds.\nBonus: Score at least 30 points during regulation and receive :15 of additional time\nReach at least 60 points during the first boinus round and receive a second bonus round of :10"

class SoloGame(GameScreen):
    def __init__(self, app):
      super().__init__(app)
      self.name = "Solo"
      self.description = "1 Player\n:30 on clock\n\nOnly one basket is active"

      self.player = None
      self.activeBasket = None

    def reset(self):
      super().reset()
      self.player = self.players[0]
      self.activeBasket = None
      
    def setupPlayers(self):
      self.players = []
      self.players.append(Player(0, "Player"))
      self.player = self.players[0]

      cx,cy = self.rect.center
      
      p = self.players[0]
      p.view = game.Text(self.app, game.Rect(1*(cx),cy+100, 300, 250), "", 250, game.WHITE, font_family=self.app.bigFont)
      p.score.add_observer(self.updateScore, p)
      self.view.add(p.view)
      
    def scoreBasket(self, basket_num):
      if self.activeBasket is None:
        self.activeBasket = basket_num
      
      if self.activeBasket == basket_num:
        self.score(self.player, 2)


class CrisscrossGame(GameScreen):
    def __init__(self, app):
      super().__init__(app)
      self.name = "Crisscross"
      self.description = "2 Player\n:30 on clock\n\nPlayers shoot at their opponent's basket\nScore is displayed on the shooter's side"
      
    def scoreBasket(self, basket_num):
      super().scoreBasket(int(not basket_num))
      
    def get_max_time(self):
      return 30

class DoubleNothingGame(GameScreen):
    def __init__(self, app):
      super().__init__(app)
      self.name = "Double or Nothing"
      self.description = "2 Players\n:30 on clock\n\nFirst basket counts for 2 points, then each subsequent basket counts for double\nIf no basket is made with :03, next basket is 2 points"
      
    def scoreBasket(self, player_num):
      p = self.players[player_num]
      if not p.active: return
      
      dt = self.get_timer()

      dtt = self.get_max_time() - dt
      if dtt <= 0: return

      last_dt = time.time() - p.last_basket
      
      if last_dt > 3:
        p.scoreIncrement = 2
        self.score(p, 2)
      else:
        p.scoreIncrement *= 2
        self.score(p, p.scoreIncrement)

      p.last_basket = time.time()
      
    def get_max_time(self):
      return 30
    
class OvertimeGame(GameScreen):
    def __init__(self, app):
      super().__init__(app)
      self.name = "Overtime"
      self.description = "2 Players\n1:00 on clock"
      
    def reset(self):
      super().reset()
      for p in self.players: p.max_time = 60
        
    def get_max_time(self):
      return 60

    def scoreBasket(self, player_num):
      p = self.players[player_num]
      if not p.active: return
      
      self.score(p, 2)
      
class SkeetShootingGame(GameScreen):
    def __init__(self, app):
      super().__init__(app)
      self.name = "Skeet Shooting"
      self.description = "1 or 2 players\n\nAnnouncer says 'Shoot', then have :03 to make a basket"
      
    def reset(self):
      super().reset()

      self.mode = 0
      now = time.time()
      self.nextTime = now + random.randint(4,10)

      for p in self.players:
        p.shot = False
      
    def scoreBasket(self, player_num):
      p = self.players[player_num]
      if not p.active: return

      if self.mode == 1:
        if not p.shot:
          p.shot = True
          self.score(p, 2)
      
    def update(self):
      game.Screen.update(self)

      now = time.time()
      dt = self.nextTime - now

      if self.mode == 0:
        if dt <= 1:
          self.app.theme.shoot()

          self.mode = 1
          self.nextTime = now + 4
        else:
          self.timerView.set_text("--")

      elif self.mode == 1:
        if dt <= 1:
          for p in self.players:
            if p.shot == False:
              p.active = False
              p.view.color = game.GREY
              p.view.update_image()
              p.view.dirty = True
            else:
              p.shot = False
              
          self.mode = 0
          self.nextTime = now + random.randint(4,10)

        self.timerView.set_text("%s" % int(dt))

      done = True
      for p in self.players:
        if p.active: done = False
      if done:
        self.game_over()
      
class SharpShooterGame(GameScreen):
    def __init__(self, app):
      super().__init__(app)
      self.name = "Sharp Shooter"
      self.description = "1 Player\n\nAnnouncer says 'Left' or 'Right', then have :03 to make a shot in that basket"

    def setupPlayers(self):
      self.players = []
      self.players.append(Player(0, "Player"))

      cx,cy = self.rect.center

      p = self.players[0]
      p.view = game.Text(self.app, game.Rect(1*(cx),cy+100, 300, 250), "", 250, game.WHITE, font_family=self.app.bigFont)
      p.score.add_observer(self.updateScore, p)
      self.view.add(p.view)
      
    def reset(self):
      super().reset()

      self.mode = 0
      now = time.time()
      self.nextTime = now + random.randint(4,10)
      self.activeBasket = None

      for p in self.players: p.shot = False
      
    def scoreBasket(self, basket_num):
      p = self.players[0]
      if not p.active: return

      if self.mode == 1:
        if self.activeBasket == basket_num:
          if not p.shot:
            p.shot = True
            self.score(p, 2)
      
    def update(self):
      game.Screen.update(self)
      p = self.players[0]

      now = time.time()
      dt = self.nextTime - now

      if self.mode == 0:
        if dt <= 1:
          self.mode = 1
          self.nextTime = now + 4
          self.activeBasket = random.randint(0,1)
          if self.activeBasket == 0:
            self.app.theme.skeet_left()
          else:
            self.app.theme.skeet_right()
        else:
          self.activeBasket = None
          self.timerView.set_text("--")

      elif self.mode == 1:
        if dt <= 1:
          if p.shot == False:
            self.game_over()
            return
          p.shot = False
          self.mode = 0
          self.nextTime = now + random.randint(3,8)

        self.timerView.set_text("%s" % int(dt))
        
      
class SuddenDeathGame(GameScreen):
    def __init__(self, app):
      super().__init__(app)
      self.name = "Sudden Death"
      self.description = "2 Players\n:15 on clock"
      
    def reset(self):
      super().reset()
      for p in self.players: p.max_time = 60
      
    def get_max_time(self):
      return 15
      
class FreePlayGame(GameScreen):
    def __init__(self, app):
      super().__init__(app)
      self.name = "Free Play"
      self.description = "1-2 Players\nNo clock\n\nAll baskets count 2 points"

class TeamGame(GameScreen):
    def __init__(self, app):
      super().__init__(app)
      self.name = "Team"
      self.description = "2 players\n:30 on clock\n\nCombined score of players is shown only"
      
    def get_max_time(self):
      return 30
    
    def scoreBasket(self, player_num):
      p = self.players[0]
      if not p.active: return

      self.score(p, 2)

    def on_init(self):
      #super().on_init()
      game.Screen.on_init(self)
      
      cx,cy = self.rect.center
      
      self.timerView = game.Text(self.app, game.Rect(cx,cy/2, 200, 250), "", 250, game.YELLOW, font_family = self.app.bigFont)
      self.view.add(self.timerView)

      self.players = []
      self.players.append(Player(0, "Team"))

      p = self.players[0]
      p.view = game.Text(self.app, game.Rect(cx,cy+100, 200, 250), "", 300, game.WHITE, font_family=self.app.bigFont)
      p.score.add_observer(self.updateScore, p)
      self.view.add(p.view)

      self.reset()

class Screen(Entity):
  def __init__(self, app, **kwargs):
    super().__init__(**kwargs)
    self.app = app
    self._event_mapping = {}
    
    self.on_init()

  def on_init(self):
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
  def on_init(self):
    defaults = {}
    defaults['parent'] = self
    defaults['clickSound'] = self.app.clickSound
    
    title = Text('PyShot', origin=(0, -1.3), size=.15, **defaults)

    self.gameModeText = Text('NA', origin=(0, 0.2), size=.1, **defaults)
    self.gameModeDescription = Text('NA', width=1,origin=(.5, 0.9), size=.05, **defaults)

    self.app.gameMode.add_observer(self.updateGameMode)

    self.startButton = MenuButton('Start',
                                  on_click=self.app.startGame,
                                  x=0,
                                  y=-.5,
                                  **defaults)
    
    self.optionsButton = MenuButton('Options',
                                    on_click=Func(self.app.showMenu, 'options'),
                                    scale=(.2, .1),
                                    text_size=.05,
                                    x=.7,
                                    y=-.5,
                                    **defaults)

    self.accept('a', self.changeGame)
    self.accept('enter', self.app.startGame)

  def changeGame(self):
    self.app.setGameMode((self.app.gameMode.value+1) % len(self.app.theGames))

  def updateGameMode(self, obj):
    if self.app.game:
      self.gameModeText.text = self.app.game.name
      self.gameModeDescription.text = self.app.game.description
    
  def on_change(self):
    if not self.app.music.status() == self.app.music.PLAYING:
      self.app.music.play()
  
class CountDownEntity(Screen):
  def on_init(self):
    red = (1,0,0,1)
    defaults = {}
    defaults['color'] = red
    defaults['parent'] = self
    defaults['font'] = self.app.digitfont

    self.timer = DigitalText(scale=10, text='0', origin=(-0.0, .3), **defaults)

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
  def on_init(self):
    defaults = {}
    defaults['parent'] = self
    defaults['clickSound'] = self.app.clickSound
    
    # options menu content
    review_text = Text(x=.275, y=.25, text='Preview text', origin=(-.5,0), **defaults)
    for t in [e for e in scene.entities if isinstance(e, Text)]:
      t.original_scale = t.scale

    menu_items = []
    if 1:
      text_scale_slider = Slider(0, 2, default=1, step=.1, dynamic=True, text='Text Size:',
                                 text_size=.05,
                                 x=-.25, **defaults)
      menu_items.append(text_scale_slider)

      def set_text_scale():
        review_text.scale = review_text.original_scale * text_scale_slider.value

      text_scale_slider.on_value_changed = set_text_scale

    if 1:
      volume_slider = Slider(0, 100, default=int(self.app.musicManager.getVolume()*100), step=1,
                             text='Master Volume:',
                             text_size=.05,
                             width=1.,
                             x=-.25, **defaults)
      menu_items.append(volume_slider)

      volume_slider.bg.x = 0.25

      def set_volume_multiplier():
        self.app.setVolume(volume_slider.value/100.)

      volume_slider.on_value_changed = set_volume_multiplier

    if 0:
      slider = Slider(-1, 1, default=volume_slider.bg.x, step=.025, dynamic=True, text='width:',
                      text_size=.05,
                      width=1.,
                      x=-.25, **defaults)
      menu_items.append(slider)
      slider.bg.x = 0.25

      def set_width():
        volume_slider.bg.x = slider.value

      slider.on_value_changed = set_width
    
    options_back = MenuButton(text='Back', x=-.25, origin_x=-.5,
                              on_click=Func(self.app.showMenu, 'main'), **defaults)
    menu_items.append(options_back)

    for i, e in enumerate(menu_items):
        e.y = -i * self.app.button_spacing
    
class LoadMenuEntity(Screen):
  def on_init(self):

    defaults = {}
    defaults['parent'] = self
    defaults['clickSound'] = self.app.clickSound
    
    # load menu content
    for i in range(3):
      MenuButton(text=f'Empty Slot {i}', y=-i * self.app.button_spacing+.1, **defaults)

    self.back_button = MenuButton(text='Back', y=((-i-1) * self.app.button_spacing),
                                  on_click=Func(self.app.showMenu, 'main'), **defaults)

    
class GameEntity(Screen):
  def __init__(self, app, **kwargs):
    self.scores = [0, 0]
    self.endTime = 0

    super().__init__(app, **kwargs)
    
  def on_init(self):
    red = (1,0,0,1)
    defaults = {}
    defaults['color'] = red
    defaults['parent'] = self
    defaults['font'] = self.app.digitfont

    self.score1 = DigitalText(scale=6, text='00', origin=(-0.6, 0), **defaults)
    self.score2 = DigitalText(scale=6, text='00', origin=(0.6, 0), **defaults)
    self.timer = DigitalText(scale=4, text='00', origin=(0, 1.2), **defaults)

    self.updateScores()

    self.accept('z', self.leftBasket)
    self.accept('x', self.rightBasket)
    
  def on_change(self):
    self.scores = [0, 0]
    self.endTime = time.time() + 31

    self.app.audience.play()
    
  def updateScores(self):
    self.score1.text = "%02d" % self.scores[0]
    self.score2.text = "%02d" % self.scores[1]

  def updateTimer(self):
    dt = int(self.endTime - time.time())
    self.timer.text = "%02d" % dt

    if dt <= 0:
      self.app.audience.stop()
      self.app.showMenu("main")
      
  def update(self):
    self.updateScores()
    self.updateTimer()

  def leftBasket(self):
    self.scores[0] += 2
    self.app.basketSound.play()

  def rightBasket(self):
    self.scores[1] += 2
    self.app.basketSound.play()
    
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

    self.volume = 0.0
    self.theGames = []
    self.gameMode = Variable(None)

    application.setAssetFolder("Assets")
    
    Text.size = .075
    Text.default_resolution = 150
    
    # button_size = (.25, .075)
    self.button_spacing = .1 * 1.75
    self.menu_parent = Entity(parent=camera.ui, y=.15)

    if 1:
      self.digitfont = loader.loadFont("digital_counter_7.ttf")
      self.digitfont.setPixelsPerUnit(100)
      
    #self.setVolume(0.02)
    self.setVolume(0.0)
    
    self.music = loader.loadMusic("music/spacejam.wav")
    self.music.setLoop(True)
    #self.music.setVolume(0.075)

    self.clickSound = loader.loadSfx("sounds/UIClick.ogg")
    self.basketSound = loader.loadSfx("sounds/basket.wav")
    #self.basketSound.setVolume(0.075)
    self.countdownSound = loader.loadSfx("sounds/countdown.wav")

    self.audience = loader.loadMusic("sounds/audience.wav")
    self.audience.setLoop(True)
    #self.audience.setVolume(0.075)

    self.main_menu = self.addMenu('main', MainMenuEntity(self, parent=self.menu_parent))
    self.game_menu = self.addMenu('game', GameEntity(self, parent=self.menu_parent))
    self.load_menu = self.addMenu('load', LoadMenuEntity(self, parent=self.menu_parent))
    self.countdown_menu = self.addMenu('countdown', CountDownEntity(self, parent=self.menu_parent))
    self.options_menu = self.addMenu('options', OptionsMenuEntity(self, parent=self.menu_parent))
    
    self.state_handler = Animator(self.menus)

    if 0:
      self.background = Entity(model='quad', texture='shore', parent=camera.ui,
                               scale=(camera.aspect_ratio,1), color=color.white, z=1)

    

    self.showMenu("main")
    
    self.accept('v', self.changeVolume)
    self.accept('m', self.changeMusic)

  def setGameMode(self, gameMode):
    self.gameMode.value = gameMode

  @property
  def game(self):
    if self.gameMode.value == None: return None
    return self.theGames[self.gameMode.value]

  def changeVolume(self):
    self.setVolume(round((self.volume + .1) % 1, 1))
    
  def changeMusic(self):
    pass

  def setVolume(self, volume):
    self.volume = volume
    print(self.volume)
    self.musicManager.setVolume(volume)
    for sfx in self.sfxManagerList:
      sfx.setVolume(volume)
      
  def input(self, key):
    logging.debug("input %s" % key)
    
    if key == 'escape': self.quit()
    elif key == 'q':    self.showMenu("main")
    else:
      super().input(key)
    

  def quit(self):
    sys.exit(1)
      
  def startGame(self):
    logging.debug("startGame")
    self.showMenu("countdown")

  def animate_in_menu(self, menu):
    logging.debug("animate_in_menu %s" % menu)
    return
  
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
  
  theGames = []
  theGames.append(StandardGame(app))
  theGames.append(SoloGame(app))
  theGames.append(CrisscrossGame(app))
  theGames.append(SkeetShootingGame(app))
  theGames.append(SharpShooterGame(app))
  theGames.append(DoubleNothingGame(app))
  theGames.append(OvertimeGame(app))
  theGames.append(SuddenDeathGame(app))
  theGames.append(FreePlayGame(app))
  theGames.append(TeamGame(app))
  
  app.theGames = theGames
  app.setGameMode(0)

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
