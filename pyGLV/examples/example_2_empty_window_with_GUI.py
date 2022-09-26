"""
Running the basic RenderWindow (SDL2Window) with an ImGUIDecorator on top
"""


from pyGLV.GUI.Viewer import SDL2Window, ImGUIDecorator

    
gWindow = SDL2Window()
gGUI = ImGUIDecorator(gWindow)

gGUI.init() #calls ImGUIDecorator::init()-->SDL2Window::init()

running = True
# MAIN RENDERING LOOP
while running:
  gGUI.display()
  running = gGUI.event_input_process(running)
  gGUI.display_post()
gGUI.shutdown()
