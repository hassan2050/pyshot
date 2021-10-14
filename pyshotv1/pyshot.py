#!/usr/bin/env python3

"""python program to solve the world problems..."""

import os, sys, string, time, logging, argparse

_version = "0.1"

import os, sys, math, time, random, glob
import pygame
import pygame.locals
import game
import config


try:
  import controls
except ImportError:
  controls = None

NORMAL = game.WHITE
SHINY = game.YELLOW

class SoundTheme:
  name = "None"
  
  def __init__(self):
    self.app = None

  def startMusic(self):
    pass

  def stopMusic(self):
    pass
  
  def stop(self):
    self.stopMusic()
    
  def start(self):
    if self.app.musicPlaying:
      self.startMusic()
      
  def countdown(self): pass
  def button(self): pass
  def gameover(self):  pass
  def basket(self):  pass
  def shoot(self): pass
  def skeet_left(self): pass
  def skeet_right(self): pass
  
  def startApp(self):
    if config.startAppSound:
      pass
  
class QuietTheme(SoundTheme):
  name = "quiet"
  def startApp(self):
    if config.startAppSound:
      pass

class DefaultSoundTheme(SoundTheme):
  name = "default"
  
  def startMusic(self):
    pass

  def stopMusic(self):
    try:
      pygame.mixer.music.stop()
    except pygame.error:
      pass
    
  def gameover(self):
    self.app.playSound('gameover')
  def basket(self):
    self.app.playSound('basket')
  def shoot(self): 
    self.app.playSound('shoot')
  def skeet_left(self):
    self.app.playSound('skeet_left')
  def skeet_right(self):
    self.app.playSound('skeet_right')
  def countdown(self):
    self.app.playSound('countdown')
  def button(self):
    self.app.playSound('button-20')
    

class SpaceJamTheme(DefaultSoundTheme):
  name = "spacejam"
  
  def startMusic(self):
    pygame.mixer.music.load("sounds/spacejam/spacejam.wav")
    pygame.mixer.music.play(loops=-1)

class PlayByPlayTheme(DefaultSoundTheme):
  name = "playbyplay"
  
  def startMusic(self):
    pygame.mixer.music.load("sounds/music1.wav")
    pygame.mixer.music.play(loops=-1)
    
  def startApp(self):
    if config.startAppSound:
      self.app.playSound('start')
    

class StartScreen(game.Screen):
    def __init__(self, app):
      super().__init__(app)
      
    def on_init(self):
      super().on_init()
      
      cx,cy = self.rect.center

      self.view.add(game.Text(self.app, game.Rect(cx, cy, self.rect.width, 200), "PyShot", 200, game.YELLOW))

    def on_keyup(self, event):
      if event.type == pygame.locals.KEYUP:
        if event.key == pygame.locals.K_q:
          self.app.stop_running()
        else:
          self.app.on_keyup(event)

    def on_switch(self):
      self.app.theme.startApp()
      self.timer = self.app.setTimer(time.time()+2, self.gameSelection, None)
                 
    def gameSelection(self, args):
      self.app.set_screen("gameselection")
      
class GameSelectionScreen(game.Screen):
    def __init__(self, app):
      super().__init__(app)
      
    def on_init(self):
      super().on_init()
      
      cx,cy = self.rect.center

      self.view.add(game.Text(self.app, game.Rect(cx, 80, 400, 100), "PyShot", 120, game.YELLOW))

      self.gameDescriptionView = game.Text(self.app, game.Rect(cx,cy+80, 500, 140), "", 30, game.WHITE)
      self.view.add(self.gameDescriptionView)

      self.app.gameMode.value = 0
      self.gameModeView = game.Text(self.app, game.Rect(cx,cy-30, self.rect.width, 80), "", 100, game.YELLOW)
      self.app.gameMode.add_observer(self.updateGameMode)
      self.view.add(self.gameModeView)

      self.view.add(game.TextButton(self.app, game.Rect(cx, cy+180, 80, 30), 'Start',
                                    font_size=60,
                                    func=self.start_game, color=NORMAL, shiny_color=SHINY))

    def updateGameMode(self, obj):
      self.gameModeView.set_text(self.app.theGames[self.app.gameMode.value].name)
      self.gameDescriptionView.set_text(self.app.theGames[self.app.gameMode.value].description)
      
    def on_keyup(self, event):
      if event.type == pygame.locals.KEYUP:
        #if event.key == ord("a"):
        if event.key == pygame.locals.K_RETURN:
          self.app.gameMode.value = (self.app.gameMode.value+1) % len(self.app.theGames)
          self.app.theme.button()
        #elif event.key == pygame.locals.K_RETURN:
        elif event.key == ord("a"):
          self.app.theme.countdown()
          self.start_game()
        elif event.key == pygame.locals.K_q:
          self.app.stop_running()
        else:
          self.app.on_keyup(event)

    def on_switch(self):
      self.app.startMusic()
                 
    def start_game(self):
      self.app.stopMusic()
      
      self.app.set_screen("ready")


class ReadyScreen(game.Screen):
    def __init__(self, app):
      super().__init__(app)

    def on_init(self):
      super().on_init()
      
      cx,cy = self.rect.center
      self.readyText = game.Text(self.app, game.Rect(cx,cy, 600, 250), "",  250, game.YELLOW)
      self.view.add(self.readyText)
      
      self.timers = []

    def on_switch(self):
      self.setMessage("Ready")
      self.timers = []
      for n,msg in enumerate(("3", "2", "1", "GO!")):
        self.timers.append(self.app.setTimer(time.time()+n+1, self.setMessage, msg))

      self.timers.append(self.app.setTimer(time.time()+5, self.start_game, ""))

    def on_keyup(self, event):
      if event.type == pygame.locals.KEYUP:
        if event.key == pygame.locals.K_s:
          self.start_game()
        elif event.key == pygame.locals.K_q:
          self.app.set_screen("gameselection")
        else:
          self.app.on_keyup(event)
        
    def setMessage(self, message):
      self.readyText.set_text(message)
        
    def start_game(self, arg=None):
      for timer in self.timers:
        self.app.removeTimer(timer)
      self.timers = []

      self.app.game = self.app.theGames[self.app.gameMode.value]
      self.app.set_screen("game%d" % self.app.gameMode.value)

class GameOverScreen(game.Screen):
    def on_init(self):
      super().on_init()
      
      self.message = ""

      cx,cy = self.rect.center

      self.messageText = game.Text(self.app, game.Rect(cx,cy-120, self.rect.width, 100), self.message,
                                   100, game.YELLOW)
      
      self.view.add(self.messageText)

      self.scoreViews = []
      self.scoreViews.append(game.Text(self.app, game.Rect(1*(cx/2),cy+120, 300, 250), "", 250, game.WHITE, font_family=self.app.bigFont))
      self.scoreViews.append(game.Text(self.app, game.Rect(3*(cx/2),cy+120, 300, 250), "", 250, game.WHITE, font_family=self.app.bigFont))
      
      for view in self.scoreViews:
        self.view.add(view)

      self.view.add(game.TextButton(self.app, game.Rect(cx, cy-10, 80, 25), 'Restart',
                                    font_size=60,
                                    func=self.restart_game, color=NORMAL, shiny_color=SHINY))

    def on_switch(self):
      self.app.theme.gameover()

    def setMessage(self, message):
      self.messageText.set_text(message)

      for n,p in enumerate(self.app.game.players):
        self.scoreViews[n].set_text(str(p.score.value))
        
    def on_keyup(self, event):
      if event.type == pygame.locals.KEYUP:
        if event.key == pygame.locals.K_q:
          self.app.set_screen("gameselection")
        elif event.key == pygame.locals.K_RETURN:
          self.restart_game()
        elif event.key == pygame.locals.K_a:
          self.app.set_screen("gameselection")
        else:
          self.app.on_keyup(event)

        
    def restart_game(self):
        self.app.set_screen("gameselection")

class Player:
  def __init__(self, num, name):
    self.num = num
    self.name = name
    self.score = game.Variable(0)
    self.scoreIncrement = 2
    self.max_time = 0
    self.view = None
    self.active = False
    self.show = True
    self.last_basket = 0
    
  def reset(self):
    self.score.value = 0
    self.scoreIncrement = 2
    self.max_time = 30
    self.active = True
    self.show = True
    self.last_basket = 0
        

class GameScreen(game.Screen):
    def __init__(self, app):
      super().__init__(app)
      self.name = "NA"

    def on_init(self):
      super().on_init()
      
      cx,cy = self.rect.center
      
      self.timerView = game.Text(self.app, game.Rect(cx,cy/2, self.rect.width, 250), "", 250, game.YELLOW, font_family = self.app.bigFont)
      self.view.add(self.timerView)

      self.setupPlayers()
      
      self.reset()

    def setupPlayers(self):
      self.players = []
      self.players.append(Player(0, "Left"))
      self.players.append(Player(1, "Right"))

      cx,cy = self.rect.center
      
      p = self.players[0]
      p.view = game.Text(self.app, game.Rect(1*(cx/2),cy+100, 350, 250), "", 240, game.WHITE, font_family=self.app.bigFont)
      p.score.add_observer(self.updateScore, p)
      self.view.add(p.view)

      p = self.players[1]
      p.view = game.Text(self.app, game.Rect(3*(cx/2),cy+100, 350, 250), "", 240, game.WHITE, font_family = self.app.bigFont)
      p.score.add_observer(self.updateScore, p)
      self.view.add(p.view)
      
      
    def on_switch(self):
      self.reset()
      
    def reset(self):
      for p in self.players:
        p.reset()
        if not p.view: continue
        p.view.color = game.WHITE
        p.view.update_image()
        p.view.dirty = True
        p.view.show()
        
      self.startTime = time.time()
      
    def update(self):
      super().update()

      max_time = self.get_max_time()
      
      dt = self.get_timer()
      if dt <= max_time:
        dtt = max_time - dt
        self.timerView.set_text(str(dtt))
      else:
        self.game_over()
        self.timerView.set_text("NA")

      for p in self.players:
        pdt = p.max_time - dt

        if pdt < 0:
          p.active = False
          p.view.color = game.GREY
          p.view.update_image()
          p.view.dirty = True
      
    def updateScore(self, obj, player):
      player.view.set_text(str(player.score.value))

    def game_over(self):
      winner = None
      if len(self.players) == 2:
        if self.players[0].score.value > self.players[1].score.value:
          winner = self.players[0]
        elif self.players[0].score.value < self.players[1].score.value:
          winner = self.players[1]

        if winner:
          self.app.gameover.setMessage("%s player wins" % winner.name)
        else:
          self.app.gameover.setMessage("Tie Game")
          
      if len(self.players) == 1:
        self.app.gameover.setMessage("Game Over")
        
      self.app.set_screen("gameover")

    def get_timer(self):
      return int(time.time() - self.startTime)

    def get_max_time(self):
      dt = self.get_timer()
      
      for p in self.players:
        if not p.active: continue
        
        if dt >= 30+15 and p.score.value >= 60: p.max_time = 55
        elif dt >= 30 and p.score.value >= 30: p.max_time = 45
        else:
          p.max_time = 30
      max_time = max(p.max_time for p in self.players)
          
      return max_time
      
    def scoreBasket(self, player_num):
      p = self.players[player_num]
      if not p.active: return
      
      dt = self.get_timer()

      dtt = self.get_max_time() - dt
      if dtt <= 0: return

      pdt = p.max_time - dt

      if pdt < 0:
        logging.warning("no score")
        return
      
      if dtt >= 10:
        self.score(p, 2)
      else:
        self.score(p, 3)

    def score(self, p, val):
      p.score.value += val

      self.app.theme.basket()
        
    def on_keydown(self, event):
      if event.key == ord("z"):
        self.scoreBasket(0)
      elif event.key == ord("x"):
        self.scoreBasket(1)
        
    def on_keyup(self, event):
      if event.key == ord(" "):
        self.startTime -= 1
      elif event.key == pygame.locals.K_q:
        self.app.set_screen("gameselection")
      elif event.key == pygame.locals.K_a:
        self.app.set_screen("gameselection")
      else:
        self.app.on_keyup(event)
      
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
      
      
class App(game.App):
    def __init__(self):
      super().__init__()
      self.window_size = (800, 480)
      
      self.gameMode = game.Variable(0)
      self.game = None
      self.fullscreen = config.fullscreen

      self.volume = 5

      self.theme_num = 0
      self.theme = None
      self.themes = []
      
      self.musicPlaying = False

    def addTheme(self, theme):
      self.themes.append(theme)
      theme.app = self

    def getTheme(self, name):
      for theme in self.themes:
        if name == theme.name: return theme
      return None

    def setTheme(self, theme):
      if self.theme: self.theme.stop()
      try:
        theme_num = self.themes.index(theme)
      except ValueError:
        logging.error("no such theme")
        return
      self.theme = theme
      self.theme.start()
      
    def setThemeByName(self, name):
      if self.theme: self.theme.stop()
      theme = self.getTheme(name)
      self.setTheme(theme)

    def startMusic(self):
      self.musicPlaying = True
      self.theme.startMusic()
      
    def stopMusic(self):
      self.musicPlaying = False
      self.theme.stopMusic()

    def getSound(self, name):
      return self.app.sounds[name]
    
    def playSound(self, name):
      pygame.mixer.Channel(0).play(self.app.getSound(name))
      
    def init_display(self):
      super().init_display()
      pygame.mouse.set_visible(False)
    
    def on_init_fonts(self):
      self.bigFont = pygame.font.Font('fonts/DS-DIGI.TTF',250)
      self.smallFont = pygame.font.SysFont('fonts/DS-DIGI.TTF',30)
      
    def on_init(self):
      super().on_init()

      self.sounds = {}
      files = glob.glob("sounds/*.wav")
      for fn in files:
        path, f = os.path.split(fn)
        name, ext = os.path.splitext(f)

        self.sounds[name] = pygame.mixer.Sound(fn)

      
      pygame.display.set_caption('PyShot')

    def on_keyup(self, event):
      if event.type == pygame.locals.KEYUP:
        if event.key == pygame.locals.K_m:
          self.theme_num = (self.theme_num + 1) % len(self.themes)
          self.setTheme(self.themes[self.theme_num])
        elif event.key == pygame.locals.K_v:
          self.volume = (self.volume + 1) % 10
          pygame.mixer.music.set_volume(1.0 * self.volume / 10.)
          logging.warning("volume: %s" % self.volume)
          
def start():
  theApp = App()
  theApp.add_screen("start", StartScreen(theApp))
  theApp.add_screen("gameselection", GameSelectionScreen(theApp))

  theApp.addTheme(SpaceJamTheme())
  theApp.addTheme(PlayByPlayTheme())
  theApp.addTheme(QuietTheme())

  logging.debug("Theme: %s" % config.startAppTheme)
  theme = theApp.getTheme(config.startAppTheme)
  theApp.theme_num = theApp.themes.index(theme)
  theApp.setTheme(theme)
  theApp.setThemeByName(config.startAppTheme)
  
  theGames = []
  theGames.append(StandardGame(theApp))
  theGames.append(SoloGame(theApp))
  theGames.append(CrisscrossGame(theApp))
  theGames.append(SkeetShootingGame(theApp))
  theGames.append(SharpShooterGame(theApp))
  theGames.append(DoubleNothingGame(theApp))
  theGames.append(OvertimeGame(theApp))
  theGames.append(SuddenDeathGame(theApp))
  theGames.append(FreePlayGame(theApp))
  theGames.append(TeamGame(theApp))
  
  theApp.theGames = theGames
  for i,game in enumerate(theGames):
    theApp.add_screen("game%d" % i, game)
  
  theApp.add_screen("ready", ReadyScreen(theApp))

  theApp.gameover = GameOverScreen(theApp)
  theApp.add_screen("gameover", theApp.gameover)

  theApp.set_screen("start")

  if controls:
    buttons = controls.setupButtons()

  while 1:
    logging.warning("starting pyshot mainloop")
    try:
      theApp.run()
    except:
      import traceback
      traceback.print_exc()
      time.sleep(1)

def test():
  logging.warning("Testing")

def parse_args(argv):
  parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description=__doc__)

  parser.add_argument("-t", "--test", dest="test_flag", 
                    default=False,
                    action="store_true",
                    help="Run test function")
  parser.add_argument("--log-level", type=str,
                      choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                      help="Desired console log level")
  parser.add_argument("-d", "--debug", dest="log_level", action="store_const",
                      const="DEBUG",
                      help="Activate debugging")
  parser.add_argument("-q", "--quiet", dest="log_level", action="store_const",
                      const="CRITICAL",
                      help="Quite mode")
  parser.add_argument("files", type=str, nargs='*')

  args = parser.parse_args(argv[1:])

  return parser, args

def main(argv, stdout, environ):
  if sys.version_info < (3, 0): reload(sys); sys.setdefaultencoding('utf8')

  parser, args = parse_args(argv)

  args.log_level = "DEBUG"

  logging.basicConfig(format="[%(asctime)s.%(msecs)03d] %(levelname)-8s %(message)s", 
                    datefmt="%m/%d %H:%M:%S", level=args.log_level)

  if args.test_flag:  test();   return

  try:
    start()
  finally:
    logging.warning("Exiting")
    time.sleep(4)

if __name__ == "__main__":
  main(sys.argv, sys.stdout, os.environ)
