import os, sys
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

class MyApp(ShowBase):
  def __init__(self):
      super().__init__(self)
      self.accept("escape",sys.exit)
      self.setBackgroundColor(0,0,0)

      text = TextNode('node name')
      text.setText("Hello, World!")
      text.setAlign(TextNode.ACenter)
      textNodePath = aspect2d.attachNewNode(text)
      textNodePath.setScale(0.2)

app = MyApp()
app.run()

