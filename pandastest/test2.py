import os, sys

from direct.showbase import ShowBase
#from direct.showbase.ShowBase import ShowBase
import ShowMultiBase
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
  #class MyApp(ShowBase.ShowBase):
  class MyApp(ShowMultiBase.ShowMultiBase):
    def __init__(self):
        wp = WindowProperties()
        #wp.setFullscreen(1)
        #wp.setSize(1920, 1080)
        wp.setSize(800, 600)
        wp.setOrigin(0, 0)
        WindowProperties.setDefault(wp)
                            
        if 0:
          wp = WindowProperties()
          wp.setFullscreen(1)
          wp.setSize(1920, 1080)
        
          self.openMainWindow()
          self.win.requestProperties(wp)
          self.graphicsEngine.openWindows()

        self.accept("escape",sys.exit)

        #ShowBase.__init__(self)
        super().__init__(self, windowType='none')
        #self.setBackgroundColor(0,0,0)
        self.disableMouse()
        
        if 1:
          self.wp2 = WindowProperties()
          self.wp2.setSize(800, 600)
          self.wp2.setOrigin(900, 0)
          self.win2 = self.openWindow(props=self.wp2, aspectRatio=1, name="Window 2")
          
          #self.setBackgroundColor(0,0,0)
          
        if 1:
          text = TextNode('node name')
          text.setText("Every day in every way I'm getting better and better.")
          textNodePath = self.aspect2d.attachNewNode(text)

          #base.camList[-1].reparentTo(textNodePath)
          cmr12 = self.loader.loadFont('cmr12.egg')
          text.setAlign(TextNode.ACenter)

          text.setFont(cmr12)
          textNodePath.setScale(0.1)

  app = MyApp()
  app.run()

