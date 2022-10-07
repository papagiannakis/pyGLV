"""
First time to test a RenderSystem in a Scene with Shader and VertexArray components
"""


import numpy as np


import pyECSS.utilities as util
from pyECSS.Entity import Entity
from pyECSS.Component import BasicTransform, Camera, RenderMesh
from pyECSS.System import TransformSystem, CameraSystem
from pyGLV.GL.Scene import Scene

from pyGLV.GL.Shader import InitGLShaderSystem, Shader, ShaderGLDecorator, RenderGLShaderSystem
from pyGLV.GL.VertexArray import VertexArray

from OpenGL.GL import GL_LINES

import OpenGL.GL as gl



"""
Scenegraph for unit tests

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

# entityCam2 = scene.world.createEntity(Entity(name="entityCam2"))
# scene.world.addEntityChild(entityCam1, entityCam2)
# trans2 = scene.world.addComponent(entityCam2, BasicTransform(name="trans2", trs=util.identity()))
# orthoCam = scene.world.addComponent(entityCam2, Camera(util.ortho(-100.0, 100.0, -100.0, 100.0, 1.0, 100.0), "orthoCam","Camera","500"))

node4 = scene.world.createEntity(Entity(name="node4"))
scene.world.addEntityChild(rootEntity, node4)
trans4 = scene.world.addComponent(node4, BasicTransform(name="trans4", trs=util.identity()))
mesh4 = scene.world.addComponent(node4, RenderMesh(name="mesh4"))


axes = scene.world.createEntity(Entity(name="axes"))
scene.world.addEntityChild(rootEntity, axes)
axes_trans = scene.world.addComponent(axes, BasicTransform(name="axes_trans", trs=util.identity()))
axes_mesh = scene.world.addComponent(axes, RenderMesh(name="axes_mesh"))


#Simple Cube
vertexCube = np.array([
    [-0.5, -0.5, 0.5, 1.0],
    [-0.5, 0.5, 0.5, 1.0],
    [0.5, 0.5, 0.5, 1.0],
    [0.5, -0.5, 0.5, 1.0], 
    [-0.5, -0.5, -0.5, 1.0], 
    [-0.5, 0.5, -0.5, 1.0], 
    [0.5, 0.5, -0.5, 1.0], 
    [0.5, -0.5, -0.5, 1.0]
],dtype=np.float32) 
colorCube = np.array([
    [0.0, 0.0, 0.0, 1.0],
    [1.0, 0.0, 0.0, 1.0],
    [1.0, 1.0, 0.0, 1.0],
    [0.0, 1.0, 0.0, 1.0],
    [0.0, 0.0, 1.0, 1.0],
    [1.0, 0.0, 1.0, 1.0],
    [1.0, 1.0, 1.0, 1.0],
    [0.0, 1.0, 1.0, 1.0]
], dtype=np.float32)

#index arrays for above vertex Arrays

indexCube = np.array((1,0,3, 1,3,2, 
                  2,3,7, 2,7,6,
                  3,0,4, 3,4,7,
                  6,5,1, 6,1,2,
                  4,5,6, 4,6,7,
                  5,4,0, 5,0,1), np.uint32) #rhombus out of two triangles



# Systems
transUpdate = scene.world.createSystem(TransformSystem("transUpdate", "TransformSystem", "001"))
camUpdate = scene.world.createSystem(CameraSystem("camUpdate", "CameraUpdate", "200"))
renderUpdate = scene.world.createSystem(RenderGLShaderSystem())
initUpdate = scene.world.createSystem(InitGLShaderSystem())
    


model = util.translate(0.0,0.0,0.5)
eye = util.vec(1.0, 1.0, 1.0)
target = util.vec(0,0,0)
up = util.vec(0.0, 1.0, 0.0)
view = util.lookat(eye, target, up)

# projMat = util.perspective(120.0, 1.33, 0.1, 100.0)
projMat = util.ortho(-10.0, 10.0, -10.0, 10.0, -0.5, 10.0)

mvpMat =  projMat @ view @ model

## ADD CUBE ##
# attach a simple cube in a RenderMesh so that VertexArray can pick it up
mesh4.vertex_attributes.append(vertexCube)
mesh4.vertex_attributes.append(colorCube)
mesh4.vertex_index.append(indexCube)
vArray4 = scene.world.addComponent(node4, VertexArray())
# decorated components and systems with sample, default pass-through shader with uniform MVP
shaderDec4 = scene.world.addComponent(node4, ShaderGLDecorator(Shader(vertex_source = Shader.COLOR_VERT_MVP, fragment_source=Shader.COLOR_FRAG)))
shaderDec4.setUniformVariable(key='modelViewProj', value=mvpMat, mat4=True)


scene.world.print()


running = True
# MAIN RENDERING LOOP
scene.init(imgui=False, windowWidth = 1024, windowHeight = 768, windowTitle = "A Cube Scene via ECSS")

# pre-pass scenegraph to initialise all GL context dependent geometry, shader classes
# needs an active GL context
scene.world.traverse_visit(initUpdate, scene.world.root)

while running:
    running = scene.render(running)
    scene.world.traverse_visit(renderUpdate, scene.world.root)
    scene.render_post()
    
scene.shutdown()

