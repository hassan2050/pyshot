from direct.showbase.ShowBase import ShowBase

from direct.actor.Actor import Actor
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, CollisionSphere, CollisionTube, CollisionNode
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import Vec4, Vec3
from panda3d.core import WindowProperties

from direct.gui.DirectGui import *

#from GameObject import *

import random

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()

        properties = WindowProperties()
        properties.setSize(1000, 750)
        self.win.requestProperties(properties)

        self.exitFunc = self.cleanup

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

        self.pusher = CollisionHandlerPusher()
        self.cTrav = CollisionTraverser()

        self.pusher.setHorizontal(True)

        self.pusher.add_in_pattern("%fn-into-%in")

        self.updateTask = taskMgr.add(self.update, "update")

        self.player = 0

        self.initialSpawnInterval = 1.0
        self.minimumSpawnInterval = 0.2
        self.spawnInterval = self.initialSpawnInterval
        self.spawnTimer = self.spawnInterval
        
        self.gameOverScreen = DirectDialog(frameSize = (-0.7, 0.7, -0.7, 0.7),
                                           fadeScreen = 0.4,
                                           relief = DGG.FLAT,
                                           frameTexture = "UI/stoneFrame.png")
        self.gameOverScreen.hide()

        self.accept("escape", self.quit)
        self.accept("q", self.endGame)

        #self.font = loader.loadFont("Fonts/Wbxkomik.ttf")
        self.font = None

        buttonImages = (
            loader.loadTexture("UI/UIButton.png"),
            loader.loadTexture("UI/UIButtonPressed.png"),
            loader.loadTexture("UI/UIButtonHighlighted.png"),
            loader.loadTexture("UI/UIButtonDisabled.png")
        )

        label = DirectLabel(text = "Game Over!",
                            parent = self.gameOverScreen,
                            scale = 0.1,
                            pos = (0, 0, 0.2),
                            relief = None)

        self.finalScoreLabel = DirectLabel(text = "",
                                           parent = self.gameOverScreen,
                                           scale = 0.07,
                                           pos = (0, 0, 0),
                                           relief = None)

        btn = DirectButton(text = "Restart",
                           command = self.startGame,
                           pos = (-0.3, 0, -0.2),
                           parent = self.gameOverScreen,
                           scale = 0.07,
                           clickSound = loader.loadSfx("Sounds/UIClick.ogg"),
                           frameTexture = buttonImages,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)

        btn = DirectButton(text = "Menu",
                           command = self.mainMeuu,
                           pos = (0, 0, -0.4),
                           parent = self.gameOverScreen,
                           scale = 0.07,
                           clickSound = loader.loadSfx("Sounds/UIClick.ogg"),
                           frameTexture = buttonImages,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)
        
        btn = DirectButton(text = "Quit",
                           command = self.quit,
                           pos = (0.3, 0, -0.2),
                           parent = self.gameOverScreen,
                           scale = 0.07,
                           clickSound = loader.loadSfx("Sounds/UIClick.ogg"),
                           frameTexture = buttonImages,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)

        self.titleMenuBackdrop = DirectFrame(frameColor = (0, 0, 0, 1),
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
                           command = self.startGame,
                           pos = (0, 0, 0.1),
                           parent = self.titleMenu,
                           scale = 0.1,
                           clickSound = loader.loadSfx("Sounds/UIClick.ogg"),
                           frameTexture = buttonImages,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)

        btn = DirectButton(text = "Quit",
                           command = self.quit,
                           pos = (0, 0, -0.3),
                           parent = self.titleMenu,
                           scale = 0.1,
                           clickSound = loader.loadSfx("Sounds/UIClick.ogg"),
                           frameTexture = buttonImages,
                           frameSize = (-4, 4, -1, 1),
                           text_scale = 0.75,
                           relief = DGG.FLAT,
                           text_pos = (0, -0.2))
        btn.setTransparency(True)

        music = loader.loadMusic("Music/Defending-the-Princess-Haunted.mp3")
        music.setLoop(True)
        music.setVolume(0.075)
        music.play()

    def startGame(self):
        self.titleMenu.hide()
        self.titleMenuBackdrop.hide()
        self.gameOverScreen.hide()

        self.cleanup()

        self.player = 1

    def mainMeuu(self):
        self.titleMenu.show()
        self.titleMenuBackdrop.show()
        self.gameOverScreen.hide()

        self.player = 0

        self.cleanup()
        
    def endGame(self):
      if self.player:
        self.player = 2

    def updateKeyMap(self, controlName, controlState):
        self.keyMap[controlName] = controlState

    def update(self, task):
        dt = globalClock.getDt()

        if self.player == 1:
          pass
        
        if self.player == 2:
          self.player = 0
          if self.gameOverScreen.isHidden():
            self.gameOverScreen.show()
            self.finalScoreLabel["text"] = "Final score: " + str(0)
            self.finalScoreLabel.setText()

        return task.cont

    def cleanup(self):
      pass

    def quit(self):
        self.cleanup()

        base.userExit()

game = Game()
game.run()
