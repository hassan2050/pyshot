import os, sys
from pandac.PandaModules import ConfigVariableBool
from pandac.PandaModules import ConfigVariableInt

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

if 0:
  wp = WindowProperties()
  #wp.setFullscreen(1)
  #wp.setSize(1024, 768)

if 0:

  base.openMainWindow()
  base.win.requestProperties(wp)
  base.graphicsEngine.openWindows()
  
if 1:
  class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.accept("escape",sys.exit)
        self.setBackgroundColor(0,0,0)

        if 0:
          wp = WindowProperties()
          wp.setFullscreen(1)
          wp.setSize(1920, 1080)
        
          self.openMainWindow()
          self.win.requestProperties(wp)
          self.graphicsEngine.openWindows()

        self.wp1 = WindowProperties()
        self.wp1.setSize(800, 600)
        self.wp1.setOrigin(100, 100)
        self.win1 = base.openWindow(props=self.wp1, aspectRatio=1)
        
        self.wp2 = WindowProperties()
        self.wp2.setSize(800, 600)
        self.wp2.setOrigin(900, 100)
        self.win2 = base.openWindow(props=self.wp2, aspectRatio=1)

        self.disableMouse()

        if 0:
          text = TextNode('node name')
          text.setText("Every day in every way I'm getting better and better.")
          textNodePath = aspect2d.attachNewNode(text)
          cmr12 = loader.loadFont('cmr12.egg')
          text.setAlign(TextNode.ACenter)

          text.setFont(cmr12)
          textNodePath.setScale(0.1)

  app = MyApp()
  app.run()

