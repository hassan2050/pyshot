import direct.directbase.DirectStart
from panda3d.core import *
from direct.gui.DirectGui import *

base.setBackgroundColor(0, 0, 0)
base.disableMouse()
camera.setPos ( 0, 0, 45 )
camera.setHpr ( 0, -90, 0 )

wp = WindowProperties()
wp.setSize(200, 200)
wp.setOrigin(0, 0)
win = base.openWindow(props = wp, aspectRatio = 1)

myRender = NodePath('myRender')

base.camList[-1].reparentTo(myRender)
myRender2d = NodePath('myRender2d')
myCamera2d = base.makeCamera2d(win)
myCamera2d.reparentTo(myRender2d)

testButton = DirectButton(text = "Button1", scale = 0.5)
testButton.setPos(0, 0, 0) 
testButton.reparentTo(myRender2d)

run()

