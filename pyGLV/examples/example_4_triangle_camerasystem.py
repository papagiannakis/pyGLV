import numpy as np


import pyECSS.utilities as util
from pyECSS.Entity import Entity
from pyECSS.Component import BasicTransform, Camera, RenderMesh
from pyECSS.System import TransformSystem, CameraSystem
from pyGLV.GL.Scene import Scene


from pyGLV.GL.Shader import InitGLShaderSystem, Shader, RenderGLShaderSystem
from pyGLV.GL.VertexArray import VertexArray

from OpenGL.GL import GL_LINES





"""
Common setup for all unit tests

Scenegraph for unit tests:

root
    |---------------------------|           
    entityCam1,                 node4,      
    |-------|                    |--------------|----------|--------------|           
    trans1, entityCam2           trans4,        mesh4,     shaderDec4     vArray4
            |                               
            ortho, trans2                   

"""


scene = Scene()    

# Scenegraph with Entities, Components
rootEntity = scene.world.createEntity(Entity(name="RooT"))
entityCam1 = scene.world.createEntity(Entity(name="entityCam1"))
scene.world.addEntityChild(rootEntity, entityCam1)
trans1 = scene.world.addComponent(entityCam1, BasicTransform(name="trans1", trs=util.identity()))

entityCam2 = scene.world.createEntity(Entity(name="entityCam2"))
scene.world.addEntityChild(entityCam1, entityCam2)
trans2 = scene.world.addComponent(entityCam2, BasicTransform(name="trans2", trs=util.identity()))
orthoCam = scene.world.addComponent(entityCam2, Camera(util.ortho(-100.0, 100.0, -100.0, 100.0, 1.0, 100.0), "orthoCam","Camera","500"))

node4 = scene.world.createEntity(Entity(name="node4"))
scene.world.addEntityChild(rootEntity, node4)
trans4 = scene.world.addComponent(node4, BasicTransform(name="trans4", trs=util.identity()))
mesh4 = scene.world.addComponent(node4, RenderMesh(name="mesh4"))

vertexData = np.array([
    [0.0, 0.0, 0.0, 1.0],
    [0.5, 1.0, 0.0, 1.0],
    [1.0, 0.0, 0.0, 1.0]
],dtype=np.float32) 
colorVertexData = np.array([
    [1.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 1.0],
    [0.0, 0.0, 1.0, 1.0]
], dtype=np.float32)


#index arrays for above vertex Arrays
index = np.array((0,1,2), np.uint32) #simple triangle



# Systems
transUpdate = scene.world.createSystem(TransformSystem("transUpdate", "TransformSystem", "001"))
camUpdate = scene.world.createSystem(CameraSystem("camUpdate", "CameraUpdate", "200"))
renderUpdate = scene.world.createSystem(RenderGLShaderSystem())
initUpdate = scene.world.createSystem(InitGLShaderSystem())


shaderDec4 = scene.world.addComponent(node4, Shader())
# attach that simple triangle in a RenderMesh
mesh4.vertex_attributes.append(vertexData) 
mesh4.vertex_attributes.append(colorVertexData)
mesh4.vertex_index.append(index)
vArray4 = scene.world.addComponent(node4, VertexArray())



# MAIN RENDERING LOOP
running = True

scene.init(imgui=True, windowWidth = 1024, windowHeight = 768, windowTitle = "pyglGA test_renderTriangle")
scene.world.traverse_visit(initUpdate, scene.world.root)

while running:
    running = scene.render(running)
    scene.world.traverse_visit(renderUpdate, scene.world.root)
    scene.render_post()
    
scene.shutdown()
