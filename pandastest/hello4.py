import os, sys
import ShowMultiBase

from panda3d.core import *
from direct.task import Task
from direct.actor.Actor import Actor
from math import pi, sin, cos

class MyAppP(ShowMultiBase.ShowMultiBase):
    def __init__(self):
        wp = WindowProperties()
        #wp.setFullscreen(1)
        #wp.setSize(1920, 1080)
        wp.setUndecorated(1)
        wp.setSize(800, 600)
        wp.setOrigin(800, 0)
        WindowProperties.setDefault(wp)

        super().__init__(self)

        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # Load and transform the panda actor.
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        # Loop its animation.
        self.pandaActor.loop("walk")
        
        self.text = TextNode('node name')
        self.text.setText("Hello, World!")
        self.text.setAlign(TextNode.ACenter)
        self.textNodePath = self.aspect2d.attachNewNode(self.text)
        self.textNodePath.setScale(0.2)


    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont



class MyAppP2(ShowMultiBase.ShowMultiBase):
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

        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # Load and transform the panda actor.
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        # Loop its animation.
        self.pandaActor.loop("walk")
        
        self.text = TextNode('node name')
        self.text.setText("Goodbye, World!")
        self.text.setAlign(TextNode.ACenter)
        self.textNodePath = self.aspect2d.attachNewNode(self.text)
        self.textNodePath.setScale(0.2)


    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), 20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont
      
class MyApp(ShowMultiBase.ShowMultiBase):
  def __init__(self):
      wp = WindowProperties()
      #wp.setFullscreen(1)
      #wp.setSize(1920, 1080)
      wp.setSize(800, 600)
      wp.setOrigin(900, 0)
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
      
app = MyAppP()
app2 = MyAppP2()
app2.run()

