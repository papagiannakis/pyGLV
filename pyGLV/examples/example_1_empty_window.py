"""
Running the basic RenderWindow with the concrete basic Compoment of the decorator
patter, that is the SDL2Window, without any decorator on top
"""


import numpy as np
import OpenGL.GL as gl

from pyGLV.GUI.Viewer import SDL2Window, ImGUIDecorator


gWindow = SDL2Window()
gGUI = ImGUIDecorator(gWindow)

gWindow.init()



running = True
# MAIN RENDERING LOOP

while running:
    gWindow.display()
    running = gWindow.event_input_process(running)
    gWindow.display_post()
gWindow.shutdown()
