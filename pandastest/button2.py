import os, sys
import ShowMultiBase

#from direct.showbase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *

from panda3d.core import *

class Screen:
  def __init__(self, app, name):
    self.app = app
    self.name = name
    self.aspect2d = self.app.aspect2d
    
  def init(self):
    pass
           
  def on_switch(self):
    pass

class Screen1(Screen):
  def init(self):
    #self.aspect2d.clear()
    #self.aspect2d.clear_model_nodes()
    
    self.text = TextNode('node name')
    self.text.setText("Hello, World!")
    self.text.setAlign(TextNode.ACenter)
    self.textNodePath = self.aspect2d.attachNewNode(self.text)
    self.textNodePath.setScale(0.2)
    self.textNodePath.setPos((0, 0.0, 0.5))

    self.app.accept("mouse1", self.click)

  def on_switch(self):
    self.app.ignore("mouse1")

  def click(self):
    print ("click")
    self.app.switchScreen("game")

class Screen2(Screen):
  def init(self):
    #self.aspect2d.clear_model_nodes()
    self.aspect2d.clear()

    bk_text = "This is my Demo"
    self.textObject = OnscreenText(parent=self.aspect2d, text=bk_text, pos=(0.95,-0.95), scale=0.1,
                                   fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter,
                                   mayChange=1)

    # Callback function to set  text
    def setText():
      bk_text = "Button Clicked"
      self.textObject.setText(bk_text)
    # Add button
    self.b = DirectButton(parent=self.aspect2d, text=("OK", "click!", "rolling over", "disabled"),
                          scale=.2, command=setText)

    

class MyApp(ShowMultiBase.ShowMultiBase):
#class MyApp(ShowBase.ShowBase):
  def __init__(self):
    wp = WindowProperties()

    wp.setUndecorated(1)
    wp.setSize(800, 600)
    wp.setOrigin(800, 0)
    WindowProperties.setDefault(wp)

    super().__init__(self)

    self.accept("escape",sys.exit)

    self.setBackgroundColor(0,0,0)
    
    self.screens = {}

    self.addScreen(Screen1(self, 'title'))
    self.addScreen(Screen2(self, 'game'))

    self.current = None
    self.switchScreen("title")

  def addScreen(self, screen):
    self.screens[screen.name] = screen
    
  def switchScreen(self, name):
    if self.current:
      self.current.on_switch()
    screen = self.screens.get(name)
    screen.init()
    self.current = screen
    
      
app2 = MyApp()
app2.run()

