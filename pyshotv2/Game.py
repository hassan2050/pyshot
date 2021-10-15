import os, sys, time

from direct.showbase.ShowBase import ShowBase

from direct.actor.Actor import Actor
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionTube, CollisionNode
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import Vec4, Vec3
from panda3d.core import WindowProperties

from direct.gui.DirectGui import *

from panda3d.core import *

#from GameObject import *

import random

class Screen:
  def __init__(self, app):
    self.app = app
    self.screen = None
    self.mapping = {}

  def accept(self, name, func):
    self.mapping[name] = func
    self.app.setupAccept(name, self)

  def event(self, name):
    f = self.mapping.get(name)
    if f:
      f()
      
  def on_change(self):
    pass

  def update(self):
    pass
  
  def setup(self):
    pass

  def hide(self):
    self.screen.hide()
    
  def show(self):
    self.screen.show()

class GameOverDialog(Screen):
  def setup(self):
        self.screen = DirectDialog(frameSize = (-0.7, 0.7, -0.7, 0.7),
                                   fadeScreen = 0.4,
                                   relief = DGG.FLAT,
                                   frameTexture = "Assets/UI/stoneFrame.png")
        
        label = DirectLabel(text = "Game Over!",
                            parent = self.screen,
                            scale = 0.1,
                            pos = (0, 0, 0.2),
                            relief = None)

        self.finalScoreLabel = DirectLabel(text = "",
                                           parent = self.screen,
                                           scale = 0.07,
                                           pos = (0, 0, 0),
                                           relief = None)
        
        btn = DirectButton(text = "Restart",
                           command = self.app.startGame,
                           pos = (-0.3, 0, -0.2),
                           parent = self.screen,
                           scale = 0.07,
                           clickSound = self.app.clickSound,
                           frameTexture = self.app.buttonImages,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)

        btn = DirectButton(text = "Menu",
                           command = self.app.mainMenu,
                           pos = (0, 0, -0.4),
                           parent = self.screen,
                           scale = 0.07,
                           clickSound = self.app.clickSound,
                           frameTexture = self.app.buttonImages,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)
        
        btn = DirectButton(text = "Quit",
                           command = self.app.quit,
                           pos = (0.3, 0, -0.2),
                           parent = self.screen,
                           scale = 0.07,
                           clickSound = self.app.clickSound,
                           frameTexture = self.app.buttonImages,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)
  
class MainMenuScreen(Screen):
  def hide(self):
    self.titleMenu.hide()
    self.titleMenuBackdrop.hide()
    
  def show(self):
    self.titleMenu.show()
    self.titleMenuBackdrop.show()
    
  def setup(self):
        self.titleMenuBackdrop = DirectFrame(frameColor = (.1, .1, .1, 1),
                                               frameSize = (-1, 1, -1, 1),
                                               parent = render2d)

        self.titleMenu = DirectFrame(frameColor = (1, 1, 1, 0))

        title = DirectLabel(text = "PyShot",
                            scale = 0.4,
                            pos = (0, 0, 0.6),
                            parent = self.titleMenu,
                            relief = None,
                            text_fg = (1, 1, 1, 1))

        btn = DirectButton(text = "Start Game",
                           command = self.app.startGame,
                           pos = (0, 0, -0.4),
                           parent = self.titleMenu,
                           scale = 0.1,
                           clickSound = self.app.clickSound,
                           frameTexture = self.app.buttonImages,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)

        if 0:
          btn = DirectButton(text = "Quit",
                             command = self.app.quit,
                             pos = (0, 0, -0.3),
                             parent = self.titleMenu,
                             scale = 0.1,
                             clickSound = self.app.clickSound,
                             frameTexture = self.app.buttonImages,
                             frameSize = (-4, 4, -1, 1),
                             text_scale = 0.75,
                             relief = DGG.FLAT,
                             text_pos = (0, -0.2))
          btn.setTransparency(True)

        title = DirectLabel(text = "[z] left  [x] right  [space] step  [q] quit  [esc] exit",
                            scale = 0.08,
                            pos = (0, 0, -.9),
                            parent = self.titleMenu,
                            relief = None,
                            text_fg = (1, 1, 1, 1))
          
class CountDownScreen(Screen):
  def update(self):
    self.updateTimer()

  def on_change(self):
    self.endTime = time.time() + 4

  def updateTimer(self):
    dt = int(self.endTime - time.time())
    self.timer.setText("%01d" % dt)

    if dt <= 0:
      self.app.changeScreen("game")
    
  def setup(self):
    self.screen = DirectFrame(frameColor = (1, 1, 1, 0))

    self.timer = OnscreenText(text='00',
                              parent=self.screen,
                              pos=(0., -.2),
                              fg=(1,0,0,1),
                              font=self.app.digitfont,
                              scale=1)
      
class GameScreen(Screen):
  def update(self):
    self.updateTimer()

  def updateScores(self):
    self.scoreNodes[0].setText("%02d" % self.app.scores[0])
    self.scoreNodes[1].setText("%02d" % self.app.scores[1])
    
  def on_change(self):
    self.app.endTime = time.time()+31
    self.updateTimer()
    
  def updateTimer(self):
    dt = int(self.app.endTime - time.time())
    self.timerNode.setText("%02d" % dt)

    if dt <= 0:
      self.app.changeScreen("gameover")
      
  def setup(self):
      self.accept("z", self.app.leftBasket)
      self.accept("x", self.app.rightBasket)
      self.accept("space", self.app.stepTime)
      self.accept("q", self.app.endGame)
      
      self.screen = DirectFrame(frameColor = (1, 1, 1, 0))

      self.scoreNodes = []

      text = OnscreenText(text='00',
                          parent=self.screen,
                          pos=(-0.6, -0),
                          fg=(1,0,0,1),
                          font=self.app.digitfont,
                          scale=0.9)
      self.scoreNodes.append(text)

      text = OnscreenText(text='00',
                          parent=self.screen,
                          pos=(0.6, -0),
                          fg=(1,0,0,1),
                          font=self.app.digitfont,
                          scale=0.9)
      self.scoreNodes.append(text)
      
      self.timerNode = OnscreenText(text=':00',
                                    parent=self.screen,
                                    pos=(0, -0.7),
                                    fg=(1,0,0,1),
                                    font=self.app.digitfont,
                                    scale=0.7)
      
      label = OnscreenText(text='HOME',
                           parent=self.screen,
                           pos=(-0.6, 0.75),
                           fg=(1,1,1,1),
                           scale=0.2)

      label = OnscreenText(text='GUEST',
                           parent=self.screen,
                           pos=(0.6, 0.75),
                           fg=(1,1,1,1),
                           scale=0.2)


  
class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.screens = {}
        self.currentScreen = None
        
        self.disableMouse()

        properties = WindowProperties()
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)

        self.exitFunc = self.cleanup

        if 0:
          mainLight = DirectionalLight("main light")
          self.mainLightNodePath = render.attachNewNode(mainLight)
          self.mainLightNodePath.setHpr(45, -45, 0)
          render.setLight(self.mainLightNodePath)

          ambientLight = AmbientLight("ambient light")
          ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
          self.ambientLightNodePath = render.attachNewNode(ambientLight)
          render.setLight(self.ambientLightNodePath)

          render.setShaderAuto()

        #self.environment = loader.loadModel("Models/Misc/environment")
        #self.environment.reparentTo(render)

        self.camera.setPos(0, 0, 32)
        self.camera.setP(-90)

        if 0:
          self.pusher.setHorizontal(True)

          self.pusher.add_in_pattern("%fn-into-%in")

        self.updateTask = taskMgr.add(self.update, "update")

        #self.font = loader.loadFont("Fonts/Wbxkomik.ttf")
        #self.digitfont = loader.loadFont("Fonts/DS-DIGIT.TTF")
        self.digitfont = loader.loadFont("Assets/Fonts/digital_counter_7.ttf")
        self.font = None

        self.buttonImages = (
            loader.loadTexture("Assets/UI/UIButton.png"),
            loader.loadTexture("Assets/UI/UIButtonPressed.png"),
            loader.loadTexture("Assets/UI/UIButtonHighlighted.png"),
            loader.loadTexture("Assets/UI/UIButtonDisabled.png")
        )
        
        self.music = loader.loadMusic("Assets/Music/spacejam.wav")
        self.music.setLoop(True)
        self.music.setVolume(0.075)

        self.clickSound = loader.loadSfx("Assets/Sounds/UIClick.ogg")
        self.basketSound = loader.loadSfx("Assets/Sounds/basket.wav")
        self.basketSound.setVolume(0.075)
        
        self.setBackgroundColor(0,0,0)
        
        self.gameOverScreen = GameOverDialog(self)
        self.gameOverScreen.setup()
        self.addScreen("gameover", self.gameOverScreen)
        
        self.gameScreen = GameScreen(self)
        self.gameScreen.setup()
        self.addScreen("game", self.gameScreen)
        
        self.countdownScreen = CountDownScreen(self)
        self.countdownScreen.setup()
        self.addScreen("countdown", self.countdownScreen)

        self.mainMenuScreen = MainMenuScreen(self)
        self.mainMenuScreen.setup()
        self.addScreen("menu", self.mainMenuScreen)
        
        self.accept("escape", self.quit)
        
        self.scores = [0, 0]

        self.mainMenu()

    def setupAccept(self, name, screen):
      self.accept(name, self._accept, [name])
      
    def _accept(self, name):
      self.screens[self.currentScreen].event(name)
        
    def leftBasket(self):
      self.scores[0] += 2
      self.gameScreen.updateScores()
      self.basketSound.play()

    def rightBasket(self):
      self.scores[1] += 2
      self.gameScreen.updateScores()
      self.basketSound.play()

    def stepTime(self):
      self.endTime -= 1
      self.gameScreen.updateTimer()

    def addScreen(self, name, screen):
      self.screens[name] = screen
      
    def changeScreen(self, name):
      for _name, screen in self.screens.items():
        screen.hide()
      screen = self.screens[name]
      screen.on_change()
      screen.show()
      self.currentScreen = name

        
    def startGame(self):
      self.music.stop()
      self.changeScreen("countdown")

      self.scores = [0, 0]
      self.startTime = time.time()
      self.endTime = time.time()+31

      self.gameScreen.updateScores()
      self.gameScreen.updateTimer()
        
    def mainMenu(self):
      self.changeScreen("menu")
      self.music.play()
        
    def endGame(self):
      self.changeScreen("gameover")

      self.gameOverScreen.finalScoreLabel["text"] = "Final score: " + str(0)
      self.gameOverScreen.finalScoreLabel.setText()

    def update(self, task):
        dt = globalClock.getDt()

        self.screens[self.currentScreen].update()

        return task.cont

    def cleanup(self):
      pass

    def quit(self):
        base.userExit()

game = Game()
game.run()
