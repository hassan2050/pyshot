import os, sys
import ShowMultiBase

from panda3d.core import *

class MyApp(ShowMultiBase.ShowMultiBase):
  def __init__(self):
      wp = WindowProperties()
      #wp.setFullscreen(1)
      #wp.setSize(1920, 1080)
      wp.setUndecorated(1)
      wp.setSize(800, 600)
      wp.setOrigin(800, 0)
      WindowProperties.setDefault(wp)
      
      super().__init__(self)
      
      self.accept("escape",sys.exit)
      
      self.setBackgroundColor(0,0,0)

      self.text = TextNode('node name')
      self.text.setText("Hello, World!")
      self.text.setAlign(TextNode.ACenter)
      self.textNodePath = self.aspect2d.attachNewNode(self.text)
      self.textNodePath.setScale(0.2)

class MyApp2(ShowMultiBase.ShowMultiBase):
  def __init__(self):
      wp = WindowProperties()
      #wp.setFullscreen(1)
      #wp.setSize(1920, 1080)
      wp.setUndecorated(1)
      wp.setSize(800, 600)
      wp.setOrigin(0, 0)
      WindowProperties.setDefault(wp)
      
      super().__init__(self)
      self.accept("escape",sys.exit)
      self.setBackgroundColor(0,0,0)

      self.text = TextNode('node name2')
      self.text.setText("Goodbye, World!")
      self.text.setAlign(TextNode.ACenter)
      self.textNodePath = self.aspect2d.attachNewNode(self.text)
      self.textNodePath.setScale(0.2)
      
app = MyApp()
app2 = MyApp2()
app2.run()

