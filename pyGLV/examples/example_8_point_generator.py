

from statistics import mode
from telnetlib import GA
from turtle import position, width
import os
# import unittest

import numpy as np
# from sympy import true

import pyECSS.utilities as util
from pyECSS.Entity import Entity
from pyECSS.Component import BasicTransform, Camera, RenderMesh
from pyECSS.System import System, TransformSystem, CameraSystem, RenderSystem
from pyparsing import line
from stack_data import Line
from pyGLV.GL.Scene import Scene
from pyECSS.ECSSManager import ECSSManager
from pyGLV.GUI.Viewer import SDL2Window, ImGUIDecorator, RenderGLStateSystem, ImGUIecssDecorator

from pyGLV.GL.Shader import InitGLShaderSystem, Shader, ShaderGLDecorator, RenderGLShaderSystem
from pyGLV.GL.VertexArray import VertexArray
from OpenGL.GL import GL_LINES

import OpenGL.GL as gl
import keyboard as key
import time
import random
from pyECSS.Event import Event, EventManager
import pandas as pd

import sys

from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt

import itertools
import os
import imgui
import OpenGL.GLUT as glut
import pygame
from pygame.locals import *

"""
Common setup for all unit tests

Scenegraph for unit tests:

root
    |------------------------------------------------------|
    |                                                      |-LineNode
    |                                                      |-------------|-----------|-------------|          
    |                                                      trans5        mesh5      shaderdec5      vArray5
    |------------------------------------------------------|
    |                                                      |-SplineNode
    |                                                      |-------------|-----------|-------------|          
    |                                                      trans6        mesh6      shaderdec6      vArray6

    |------------------------------------------------------|
    |                                                      |-SuperFunction
    |                                                      |-------------|-----------|-------------|          
    |                                                      trans8        mesh8      shaderdec8      vArray8
    |------------------------------------------------------|
    |                                                      |-TriangleNode
    |                                                      |-------------|-----------|-------------|          
    |                                                       trans7        mesh7      shaderdec7      vArray7
    |
    |------------------------------------------------------|-Histogram
    |                                                      |-------------|-----------|-------------|          
    |---------------------------|                          trans7        mesh7      shaderdec7      vArray7
    entityCam1,                 PointsNode,      
    |-------|                    |--------------|----------|--------------|           
    trans1, entityCam2           trans4,        mesh4,     shaderDec4     vArray4
            |                               
            ortho, trans2                   

"""
dirname = os.path.dirname(__file__)
# PointCoordinates_path = os.path.join(dirname, 'example_materials\\PointCoordinates.csv')

#get random x,y,z planes
if len(sys.argv) == 2:#receive data from a txt via command line
    with open(sys.argv[1], 'r') as f:
        next(f)#skip header
        if(f):
            pointListfromCSV = [tuple(map(float, i.split(','))) for i in f]
else:#receive csv from path
    PointCoordinates_path = os.path.join(dirname, 'example_materials/PointCoordinates.csv')
    reader = pd.read_csv(PointCoordinates_path)
    pointListfromCSV = [tuple(x) for x in reader.values]


df = pd.DataFrame(pointListfromCSV, index=None)
cols = len(df.axes[1]) -2
xPlane = random.randint(0, cols)
yPlane = random.randint(0, cols)


PointCoordinatesZaxis_path = os.path.join(dirname, 'example_materials/PointCoordinatesZaxis.csv')
reader2 = pd.read_csv(PointCoordinatesZaxis_path)
pointListfromCSVZaxis = [tuple(x) for x in reader2.values]
dfz =pd.DataFrame(pointListfromCSVZaxis, index=None)
zcols = len(dfz.axes[1])
zPlane = 0
#zPlane = random.randint(0, cols)

while((yPlane) == xPlane):# having x and y plane from the same csv collumn is ugly!
    yPlane = random.randint(0, cols)

scene = Scene()    
rootEntity = scene.world.createEntity(Entity(name="RooT"))
entityCam1 = scene.world.createEntity(Entity(name="entityCam1"))
scene.world.addEntityChild(rootEntity, entityCam1)
trans1 = scene.world.addComponent(entityCam1, BasicTransform(name="trans1", trs=util.identity()))

entityCam2 = scene.world.createEntity(Entity(name="entityCam2"))
scene.world.addEntityChild(entityCam1, entityCam2)
trans2 = scene.world.addComponent(entityCam2, BasicTransform(name="trans2", trs=util.identity()))
orthoCam = scene.world.addComponent(entityCam2, Camera(util.ortho(-100.0, 100.0, -100.0, 100.0, 2.0, 100.0), "orthoCam","Camera","500"))

PointsNode = scene.world.createEntity(Entity("PointsNode"))
scene.world.addEntityChild(scene.world.root, PointsNode)
trans4 = BasicTransform(name="trans4", trs=util.identity())
scene.world.addComponent(PointsNode, trans4)

LinesNode = scene.world.createEntity(Entity("LinesNode"))
scene.world.addEntityChild(rootEntity, LinesNode)
trans5 = BasicTransform(name="trans5", trs=util.identity())
scene.world.addComponent(LinesNode, trans5)

SplineNode = scene.world.createEntity(Entity("SplineNode"))
scene.world.addEntityChild(rootEntity, SplineNode)
trans6 = BasicTransform(name="trans6", trs=util.identity())
scene.world.addComponent(SplineNode, trans6)

Area3D = scene.world.createEntity(Entity("TriangleNode"))
scene.world.addEntityChild(rootEntity, Area3D)
trans7 = BasicTransform(name="trans7", trs=util.identity())
scene.world.addComponent(Area3D, trans7)

Area2D = scene.world.createEntity(Entity("TriangleNode"))
scene.world.addEntityChild(rootEntity, Area2D)
trans11 = BasicTransform(name="trans11", trs=util.identity())
scene.world.addComponent(Area2D, trans11)

SuperFunction2D = scene.world.createEntity(Entity("SuperFunction"))
scene.world.addEntityChild(rootEntity, SuperFunction2D)
trans8 = BasicTransform(name="trans8", trs=util.identity())
scene.world.addComponent(SuperFunction2D, trans8)

SuperFunction3D = scene.world.createEntity(Entity("SuperFunction"))
scene.world.addEntityChild(rootEntity, SuperFunction3D)
trans12 = BasicTransform(name="trans12", trs=util.identity())
scene.world.addComponent(SuperFunction3D, trans12)

Histogram2D = scene.world.createEntity(Entity("Histogram"))
scene.world.addEntityChild(rootEntity, Histogram2D)
trans9 = BasicTransform(name="trans9", trs=util.identity())
scene.world.addComponent(Histogram2D, trans9)

Histogram3D = scene.world.createEntity(Entity("Histogram"))
scene.world.addEntityChild(rootEntity, Histogram3D)
trans10 = BasicTransform(name="trans10", trs=util.identity())
scene.world.addComponent(Histogram3D, trans10)

Ravdogram2D = scene.world.createEntity(Entity("Ravdogram"))
scene.world.addEntityChild(rootEntity, Ravdogram2D)
trans13 = BasicTransform(name="trans13", trs=util.identity())
scene.world.addComponent(Ravdogram2D, trans13)

Ravdogram3D = scene.world.createEntity(Entity("Ravdogram"))
scene.world.addEntityChild(rootEntity, Ravdogram3D)
trans14 = BasicTransform(name="trans14", trs=util.identity())
scene.world.addComponent(Ravdogram3D, trans14)

LSR2D = scene.world.createEntity(Entity("LSR"))
scene.world.addEntityChild(rootEntity, LSR2D)
trans15 = BasicTransform(name="trans15", trs=util.identity())
scene.world.addComponent(LSR2D, trans15)

LSR3D = scene.world.createEntity(Entity("LSR"))
scene.world.addEntityChild(rootEntity, LSR3D)
trans16 = BasicTransform(name="trans16", trs=util.identity())
scene.world.addComponent(LSR3D, trans16)

Pie2D = scene.world.createEntity(Entity("Pie"))
scene.world.addEntityChild(rootEntity, Pie2D)
trans17 = BasicTransform(name="trans17", trs=util.identity())
scene.world.addComponent(Pie2D, trans17)

Pie3D = scene.world.createEntity(Entity("Pie"))
scene.world.addEntityChild(rootEntity, Pie3D)
trans18 = BasicTransform(name="trans18", trs=util.identity())
scene.world.addComponent(Pie3D, trans18)

funcPlatformX = scene.world.createEntity(Entity("funcPlatform"))
scene.world.addEntityChild(rootEntity, funcPlatformX)
trans19 = BasicTransform(name="trans19", trs=util.identity())
scene.world.addComponent(funcPlatformX, trans19)

funcPlatformZ = scene.world.createEntity(Entity("funcPlatform"))
scene.world.addEntityChild(rootEntity, funcPlatformZ)
trans20 = BasicTransform(name="trans20", trs=util.identity())
scene.world.addComponent(funcPlatformZ, trans20)

spotPoints = scene.world.createEntity(Entity("spotPoints"))
scene.world.addEntityChild(rootEntity, spotPoints)
trans21 = BasicTransform(name="trans21", trs=util.identity())
scene.world.addComponent(spotPoints, trans21)

axes = scene.world.createEntity(Entity(name="axes"))
scene.world.addEntityChild(rootEntity, axes)
axes_trans = scene.world.addComponent(axes, BasicTransform(name="axes_trans", trs=util.identity()))
axes_mesh = scene.world.addComponent(axes, RenderMesh(name="axes_mesh"))

# Systems
transUpdate = scene.world.createSystem(TransformSystem("transUpdate", "TransformSystem", "001"))
camUpdate = scene.world.createSystem(CameraSystem("camUpdate", "CameraUpdate", "200"))
renderUpdate = scene.world.createSystem(RenderGLShaderSystem())
initUpdate = scene.world.createSystem(InitGLShaderSystem())

#global point size integer
keys = []
values = []
PointSize = 5    

CSVxyValues= xPlane,yPlane,zPlane
CSVButtonclicked = 0
def CSV_GUI():
    global xPlane
    global yPlane
    global zPlane
    global CSVxyValues
    global CSVButtonclicked

    imgui.begin("- Program - Select CSV Dimension Values")
    if(CSVButtonclicked):
        imgui.same_line() 

        imgui.text("X: %d, Y: %d, Z: %d" % (CSVxyValues[0],CSVxyValues[1],CSVxyValues[2]))
        xPlane = CSVxyValues[0]
        yPlane = CSVxyValues[1]
        zPlane = CSVxyValues[2]
        CSVButtonclicked = imgui.button("change")
        CSVButtonclicked = (CSVButtonclicked - 1) * (CSVButtonclicked - 1)

        #we split our csv based on common Z plane values and pass it to 2 lists for later use
        keys.clear()
        values.clear()
        for Zplanekey, value in itertools.groupby(pointListfromCSV, lambda x: x[7]):
            keys.append(Zplanekey)
            values.append(list(value))
        for i in range(len(keys)):
            values[i].sort(key = lambda row: (row[xPlane]),reverse=False)
    else:
        imgui.text("Choose Dimension from CSV file for X,Y,Z ")
        changed, CSVxyValues = imgui.input_int3('', *CSVxyValues) 
        l=0
        for l in range(len(CSVxyValues)):
            if(CSVxyValues[l] > cols):
                CSVxyValues[l] = cols
            elif(CSVxyValues[l] < 0):
                CSVxyValues[l] = 0
        if(CSVxyValues[2] > zcols):
            CSVxyValues[2] = zcols
        elif(CSVxyValues[2] < 0):
            CSVxyValues[2] = 0

        #imgui.same_line() 
        imgui.text("X: %d, Y: %d, Z: %d" % (CSVxyValues[0],CSVxyValues[1],CSVxyValues[2]))
        CSVButtonclicked = imgui.button("Save")
    #implementation for csv import
    if imgui.is_item_hovered():
        imgui.set_tooltip("Please save the changes or they won't be passed")
    imgui.end()

spotPointschild=0
SpotPointsColor = 0., 1., 1., 1
def bountries(xmin=-1, xmax =1, ymin=-1,ymax=1,zmin=-1,zmax=1):


    global spotPointschild
    removeEntityChilds(spotPoints)
    spotPointschild=0
    xminR = round(xmin)
    xmaxR = round(xmax)
    yminR = round(ymin)
    ymaxR = round(ymax)
    zminR = round(zmin)
    zmaxR = round(zmax)
    passingx = xminR
    passingy = yminR
    passingz = zminR
    while(passingy <= ymaxR):
        passingx = xminR
        while(passingx <= xmaxR):
            passingz = zminR
            while(passingz <= zmaxR):
                spotPointschild += 1
                DynamicVariable = "spotPoints" + str(spotPointschild)
                point1 = passingx,passingy,passingz,1
                vars()[DynamicVariable]: GameObjectEntity_Point = PointSpawn(DynamicVariable,point1,0,1,1)
                scene.world.addEntityChild(spotPoints, vars()[DynamicVariable]) 
                passingz += 0.5
            passingx += 0.5
        passingy += 0.5
    scene.world.traverse_visit(initUpdate, scene.world.root)
    


FuncValues= 0.,1.,0.,1.
f_x = 'x**2+x*4'
f_x_y = 'x**2+y**2'
superfuncchild2D =0
toggleSuperFunc2D = True

superfuncchild3D =0
toggleSuperFunc3D = True
funcDetail = 10

platforms = 0
childplatX = 0
childplatZ = 0
plattoggleX = True
plattoggleZ = True
togglepoints = True
def Func_GUI():
    global FuncValues
    global f_x_y
    global f_x

    global superfuncchild2D
    global toggleSuperFunc2D
    global superfuncchild3D
    global toggleSuperFunc3D
    global funcDetail
    global platforms
    global childplatX
    global childplatZ 
    global plattoggleX 
    global plattoggleZ 
    global togglepoints
    imgui.begin("Give Function X,Y Values")

    #implementation for a,b,c,d points for X,Y functions
    changed, f_x = imgui.input_text(':F(x)',f_x,256)

    Func_Button2D = imgui.button("Print f(x)")
    imgui.same_line() 
    Func_Button2D_toggle = imgui.button("Print f(x) toggle")

    changed, f_x_y = imgui.input_text(':F(x,y)',f_x_y,256)

    Func_Button3D = imgui.button("Print f(x,y)")
    imgui.same_line() 
    Func_Button3D_toggle = imgui.button("Print f(x,y) toggle")
    if(Func_Button2D_toggle):
        toggleSuperFunc2D = not toggleSuperFunc2D
    elif(Func_Button3D_toggle):
        toggleSuperFunc3D = not toggleSuperFunc3D

    imgui.text("Give a to b values for X and c to d for Y")
    changed, FuncValues = imgui.input_float4('', *FuncValues) 
    #imgui.same_line() 
    imgui.text("a: %.1f, b: %.1f, c: %.1f, d: %.1f" % (FuncValues[0],FuncValues[1],FuncValues[2],FuncValues[3]))
    changed, funcDetail = imgui.input_int('Detailed', funcDetail) 
    if imgui.is_item_hovered():
        imgui.set_tooltip("Make sure the detail is between 4 to 100")
        
    clicked, platforms = imgui.combo("platforms", platforms, ["none","X", "Z"])
    
    global PointSize
    global SpotPointsColor
    changed, PointSize = imgui.drag_float("spot point Size", PointSize, 0.02, 0.1, 40, "%.1f")
    if (changed):
        gl.glPointSize(PointSize)
        
        
    imgui.text("PointSize: %s" % (PointSize))
    imgui.text("")
    changed, SpotPointsColor = imgui.color_edit3("Spot Color", *SpotPointsColor)
    if(funcDetail > 100):
        funcDetail = 100
    elif(funcDetail<4):
        funcDetail = 4
    if(Func_Button2D):
        removeEntityChilds(SuperFunction2D)
        superfuncchild2D=0
        x = np.linspace(FuncValues[0],FuncValues[1],funcDetail) 
        y = f_X(x)
        l=0
        while (l < len(x)-1):
            superfuncchild2D+=1
            l+=1
            DynamicVariable = "SuperFunction" + str(superfuncchild2D)
            point1 =  x[l], y[l], 0 , 1 
            point2 =  x[l-1], y[l-1], 0 , 1
            vars()[DynamicVariable]: GameObjectEntity = LineSpawn(DynamicVariable,point2,point1, 1, 1, 0)
            scene.world.addEntityChild(SuperFunction2D, vars()[DynamicVariable])
            
        scene.world.traverse_visit(initUpdate, scene.world.root)
    if(Func_Button3D):
        removeEntityChilds(SuperFunction3D)
        superfuncchild3D=0

        removeEntityChilds(funcPlatformX)
        childplatX=0
        removeEntityChilds(funcPlatformZ)
        childplatZ=0

        x = np.linspace(FuncValues[0],FuncValues[1],funcDetail) 
        z = np.linspace(FuncValues[2],FuncValues[3],funcDetail)
        yValues = [] 
        for xiterate in x:
            for ziterate in z:
                yValues.append(f_Z(xiterate,ziterate))

        maximumy = np.max(yValues) # NEEDED to print the color based on y axis
        minimumy = np.min(yValues) # NEEDED to print the color based on y axis
        if(maximumy == 0):
            maximumy=1
        q=0
        r = 0.34
        g = 0.15
        b = 0.
        while (q < len(z)-1):
            q+=1
            l = 0
            while (l < len(x)-1):
                currY = f_Z(x[l],z[q])
                r = 0.34 + ((currY-minimumy)/(maximumy+abs(minimumy))) * 0.6
                g = 0.15 + ((currY-minimumy)/(maximumy+abs(minimumy))) * 0.6
                b = ((currY-minimumy)/(maximumy+abs(minimumy))) * 0.6

                l += 1
                #first triangle
                superfuncchild3D += 1
                DynamicVariable = "Function" + str(superfuncchild3D)
                point1 = x[l-1], f_Z(x[l-1],z[q-1]), z[q-1], 1
                point2 = x[l], f_Z(x[l],z[q-1]), z[q-1], 1
                point3 = x[l], f_Z(x[l],z[q]), z[q], 1
                vars()[DynamicVariable]: GameObjectEntity = TriangleSpawn(DynamicVariable,point1,point2,point3,r ,g, b)
                scene.world.addEntityChild(SuperFunction3D, vars()[DynamicVariable])
                #second triangle
                superfuncchild3D += 1
                DynamicVariable = "Function" + str(superfuncchild3D)
                point1 = x[l-1], f_Z(x[l-1],z[q-1]), z[q-1], 1
                point2 = x[l], f_Z(x[l],z[q]), z[q], 1
                point3 = x[l-1], f_Z(x[l-1],z[q]), z[q], 1
                vars()[DynamicVariable]: GameObjectEntity = TriangleSpawn(DynamicVariable,point1,point2,point3,r ,g, b)
                scene.world.addEntityChild(SuperFunction3D, vars()[DynamicVariable])
        #for X platform
        znext = FuncValues[3]
        zold = FuncValues[2]
        
        l = 0
        while (l < len(x)):
            l += 1
            #first triangle
            childplatX += 1
            DynamicVariable = "funcPlatform" + str(childplatX)
            point1 = x[l-1], minimumy, zold, 1
            point2 = x[l-1], maximumy, zold, 1
            point3 = x[l-1], maximumy, znext, 1
            vars()[DynamicVariable]: GameObjectEntity = TriangleSpawn(DynamicVariable,point1,point2,point3,0.6 ,0.6, 0.6)
            scene.world.addEntityChild(funcPlatformX, vars()[DynamicVariable])
            #second triangle
            childplatX += 1
            DynamicVariable = "funcPlatform" + str(childplatX)
            point1 = x[l-1], minimumy, zold, 1
            point2 = x[l-1], maximumy, znext, 1
            point3 = x[l-1], minimumy, znext, 1
            vars()[DynamicVariable]: GameObjectEntity = TriangleSpawn(DynamicVariable,point1,point2,point3,0.6 ,0.6, 0.6)

            scene.world.addEntityChild(funcPlatformX, vars()[DynamicVariable])
        #for Z platform
        xnext = FuncValues[1]
        xold = FuncValues[0]
        l = 0
        while (l < len(z)):
            l += 1
            #first triangle
            childplatZ += 1
            DynamicVariable = "funcPlatform" + str(childplatZ)
            point1 = xold, maximumy, z[l-1], 1
            point2 = xnext, minimumy, z[l-1], 1
            point3 = xnext, maximumy, z[l-1], 1
            vars()[DynamicVariable]: GameObjectEntity = TriangleSpawn(DynamicVariable,point1,point2,point3,0.6 ,0.6, 0.6)
            scene.world.addEntityChild(funcPlatformZ, vars()[DynamicVariable])
            #second triangle
            childplatZ += 1
            DynamicVariable = "funcPlatform" + str(childplatZ)
            point1 = xold, minimumy, z[l-1], 1
            point2 = xnext, minimumy, z[l-1], 1
            point3 = xold, maximumy, z[l-1], 1
            vars()[DynamicVariable]: GameObjectEntity = TriangleSpawn(DynamicVariable,point1,point2,point3,0.6 ,0.6, 0.6)

            scene.world.addEntityChild(funcPlatformZ, vars()[DynamicVariable])
        scene.world.traverse_visit(initUpdate, scene.world.root)
        bountries(FuncValues[0],FuncValues[1],minimumy,maximumy,FuncValues[2],FuncValues[3])
    togglepointsbutton = imgui.button("toggle points")
    if(togglepointsbutton):
        togglepoints= not togglepoints 
    if(platforms == 1):
        plattoggleX = True
        plattoggleZ = False
    elif(platforms == 2):
        plattoggleX = False
        plattoggleZ = True
    else:
        plattoggleX = False
        plattoggleZ = False
    imgui.end()



SplineList = []
togglePlatformSwitch3D = True
togglePlatformSwitch2D = True
trianglechild3D =0
trianglechild2D =0

def Area_Chart():
    global SplineList
    global keys
    global values

    global togglePlatformSwitch3D
    global togglePlatformSwitch2D
    global trianglechild3D
    global trianglechild2D
    imgui.begin("- Calculate Area 3D -")
    imgui.text("Calculate Area 3D ")
    Area_Diagram_Button3D = imgui.button("3D")
    imgui.same_line() 
    Area_Diagram_Button3D_toggle = imgui.button("3D toggle")

    Area_Diagram_Button2D = imgui.button("2D")
    imgui.same_line() 
    Area_Diagram_Button2D_toggle = imgui.button("2Dtoggle")

    if(Area_Diagram_Button2D_toggle):
        togglePlatformSwitch2D = not togglePlatformSwitch2D
    elif(Area_Diagram_Button3D_toggle):
        togglePlatformSwitch3D = not togglePlatformSwitch3D

    if(Area_Diagram_Button3D):
        removeEntityChilds(Area3D)
        trianglechild3D=0

        SplineList.clear()
        for i in range(len(keys)):
            if(values[i]):
                arr = np.array(values[i])
                xPointToSpline = arr[:,xPlane]
                yPointToSpline = arr[:,yPlane]
                
                f = CubicSpline(xPointToSpline,yPointToSpline, bc_type='natural')
                x_new = np.linspace(0.2, 3, len(values[i])*6)
                SplineList.append(f)#pass the spline functions to a list for later use
        lengthoflist = 0
        #get random rgb color for the platform
        r = random.uniform(0, 1.0)
        g = random.uniform(0, 1.0)
        b = random.uniform(0, 1.0)
        while(lengthoflist < len(SplineList) -1):
            lengthoflist += 1
            spline1 = SplineList[lengthoflist-1]
            spline2 = SplineList[lengthoflist]
            x_new = np.linspace(0.2, 3, len(values[i])*6)

            y_spline1 = spline1(x_new)
            y_spline2 = spline2(x_new)
            z_spline1 = keys[lengthoflist-1]
            z_spline2 = keys[lengthoflist]
            l =0
            while l < len(x_new) -1 :
                l += 1
                #first triangle
                trianglechild3D += 1
                DynamicVariable = "Triangle" + str(trianglechild3D)
                point1 = x_new[l-1], y_spline1[l-1], z_spline1, 1
                point2 = x_new[l], y_spline1[l], z_spline1, 1
                point3 = x_new[l-1], y_spline2[l-1], z_spline2, 1
                vars()[DynamicVariable]: GameObjectEntity = TriangleSpawn(DynamicVariable,point1,point2,point3,r ,g, b)
                scene.world.addEntityChild(Area3D, vars()[DynamicVariable])
                #second triangle
                trianglechild3D += 1
                DynamicVariable = "Triangle" + str(trianglechild3D)
                point1 = x_new[l-1], y_spline2[l-1], z_spline2, 1
                point2 = x_new[l], y_spline2[l], z_spline2, 1
                point3 = x_new[l], y_spline1[l], z_spline1, 1
                vars()[DynamicVariable]: GameObjectEntity = TriangleSpawn(DynamicVariable,point1,point2,point3,r ,g, b)
                scene.world.addEntityChild(Area3D, vars()[DynamicVariable])
            scene.world.traverse_visit(initUpdate, scene.world.root)

    elif(Area_Diagram_Button2D):
        removeEntityChilds(Area2D)
        trianglechild2D=0
        SplineList.clear()
        for i in range(len(keys)):
            if(values[i]):
                arr = np.array(values[i])
                xPointToSpline = arr[:,xPlane]
                yPointToSpline = arr[:,yPlane]
                
                f = CubicSpline(xPointToSpline,yPointToSpline, bc_type='natural')
                x_new = np.linspace(0.2, 3, len(values[i])*6)
                SplineList.append(f)#pass the spline functions to a list for later use
        lengthoflist = 0
        #get random rgb color for the platform
        r = random.uniform(0, 1.0)
        g = random.uniform(0, 1.0)
        b = random.uniform(0, 1.0)
        while(lengthoflist < len(SplineList) -1):
            lengthoflist += 1
            spline1 = SplineList[lengthoflist-1]
            spline2 = SplineList[lengthoflist]
            x_new = np.linspace(0.2, 3, len(values[i])*6)

            y_spline1 = spline1(x_new)
            y_spline2 = spline2(x_new)
            z_spline1 = keys[lengthoflist-1]
            z_spline2 = keys[lengthoflist]
            l =0
            while l < len(x_new) -1 :
                l += 1
                #first triangle
                trianglechild2D += 1
                DynamicVariable = "Triangle" + str(trianglechild2D)
                point1 = x_new[l-1], y_spline1[l-1], 0, 1
                point2 = x_new[l], y_spline1[l], 0, 1
                point3 = x_new[l-1], y_spline2[l-1], 0, 1
                vars()[DynamicVariable]: GameObjectEntity = TriangleSpawn(DynamicVariable,point1,point2,point3,r ,g, b)
                scene.world.addEntityChild(Area2D, vars()[DynamicVariable])
                #second triangle
                trianglechild2D += 1
                DynamicVariable = "Triangle" + str(trianglechild2D)
                point1 = x_new[l-1], y_spline2[l-1], 0, 1
                point2 = x_new[l], y_spline2[l], 0, 1
                point3 = x_new[l], y_spline1[l], 0, 1
                vars()[DynamicVariable]: GameObjectEntity = TriangleSpawn(DynamicVariable,point1,point2,point3,r ,g, b)
                scene.world.addEntityChild(Area2D, vars()[DynamicVariable])
            scene.world.traverse_visit(initUpdate, scene.world.root)
    #implementation for csv import
    if imgui.is_item_hovered():
        imgui.set_tooltip("Please save the changes or they won't be passed")
    imgui.end()


toggle_scatterplot = True
pointchild = 0
PointsColor = 0., 1., 1., 1

lsr2Dchild =0
lsr3Dchild =0
lsr2Dtoggle = True
lsr3Dtoggle = True
lsrfunclist = []
lsrXlist = []

def ScatterPlot_Chart():
    global pointchild
    global toggle_scatterplot

    imgui.begin("- Calculate Scatterplot -")
    imgui.text("Scatterplot ")
    Scatterplot_Button2D = imgui.button("2D Scatterplot")
    imgui.same_line() 
    Scatterplot_Button3D = imgui.button("3D Scatterplot")

    if (Scatterplot_Button2D or Scatterplot_Button3D):
        if (pointchild == 0 ):
            for i in range(len(pointListfromCSV)):
                pointchild += 1
                DynamicVariable = "Point" + str(pointchild)
                point1 = 0, 0,0,1
                vars()[DynamicVariable]: GameObjectEntity_Point = PointSpawn(DynamicVariable,point1,0,1,1)
                scene.world.addEntityChild(PointsNode, vars()[DynamicVariable]) 
                PointsNode.getChild(pointchild).trans.l2cam =  util.translate(pointListfromCSV[i][xPlane], pointListfromCSV[i][yPlane], pointListfromCSV[i][zPlane])
            scene.world.traverse_visit(initUpdate, scene.world.root)

        pointchild = 0
        for i in range(len(pointListfromCSV)):
            pointchild += 1
            if Scatterplot_Button3D:
                PointsNode.getChild(pointchild).trans.l2cam =  util.translate(pointListfromCSV[i][xPlane], pointListfromCSV[i][yPlane], pointListfromCSV[i][zPlane])
            elif Scatterplot_Button2D:
                PointsNode.getChild(pointchild).trans.l2cam =  util.translate(pointListfromCSV[i][xPlane], pointListfromCSV[i][yPlane], 0)
    
        time.sleep(0.15)

    if imgui.is_item_hovered():
        imgui.set_tooltip("Please save the changes or they won't be passed")

    #size, color of scaterplot(points)
    global PointSize
    global PointsColor
    changed, PointSize = imgui.drag_float("Point Size", PointSize, 0.02, 0.1, 40, "%.1f")
    if (changed):
        gl.glPointSize(PointSize)
        
        
    imgui.text("PointSize: %s" % (PointSize))
    imgui.text("")
    changed, PointsColor = imgui.color_edit3("Color", *PointsColor)

    toggle_scatterplot_Button = imgui.button("Toggle Scaterplot On/Off")
    if (toggle_scatterplot_Button):
        toggle_scatterplot = not toggle_scatterplot
    imgui.text("")

    global lsr2Dchild
    global lsr3Dchild
    global lsr2Dtoggle
    global lsr3Dtoggle
    global lsrfunclist
    global lsrXlist
    lsr_Button = imgui.button("Print l.s.r Line")
    imgui.same_line() 
    lsr2Dtogglebutton = imgui.button("toggle l.s.r Line")


    lsr_platform_Button = imgui.button("Print l.s.r Platform")
    imgui.same_line() 
    lsr3Dtogglebutton = imgui.button("toggle l.s.r platform")

    if(lsr2Dtogglebutton):
        lsr2Dtoggle = not lsr2Dtoggle
    elif(lsr3Dtogglebutton):
        lsr3Dtoggle = not lsr3Dtoggle

    if(lsr_Button):
        removeEntityChilds(LSR2D)
        lsr2Dchild = 0
        arrayfromtupple = np.asarray(pointListfromCSV)
        x =np.asarray(arrayfromtupple[:,xPlane])
        M = np.vstack([x, np.ones(len(x))]).T
        y =np.asarray(arrayfromtupple[:,yPlane])
        m, c = np.linalg.lstsq(M, y, rcond=None)[0]
        
        f = m*x+c
        l=0
        
        while(l < len(x) -1):
            lsr2Dchild+=1
            l+=1
            DynamicVariable = "LSR2D" + str(lsr2Dchild)
            point1 =  x[l], f[l], 0 , 1 
            point2 =  x[l-1], f[l-1], 0 , 1
            vars()[DynamicVariable]: GameObjectEntity = LineSpawn(DynamicVariable,point2,point1, 1, 1, 0)
            scene.world.addEntityChild(LSR2D, vars()[DynamicVariable])
        scene.world.traverse_visit(initUpdate, scene.world.root)
    elif(lsr_platform_Button):
        removeEntityChilds(LSR3D)
        lsr3Dchild = 0
        lsrfunclist.clear()
        lsrXlist.clear()
        for i in range(len(keys)):
            if(values[i]):
                arr = np.array(values[i])
                x = arr[:,xPlane]
                y = arr[:,yPlane]
                M = np.vstack([x, np.ones(len(x))]).T
                m, c = np.linalg.lstsq(M, y, rcond=None)[0]
                
                f = m*x+c
                lsrfunclist.append(f)#pass the spline functions to a list for later use
                lsrXlist.append(x)
        lengthoflist = 0
        #get random rgb color for the platform
        r = random.uniform(0, 1.0)
        g = random.uniform(0, 1.0)
        b = random.uniform(0, 1.0)
        while(lengthoflist < len(lsrfunclist) -1):
            lengthoflist += 1
            
            spline1 = lsrfunclist[lengthoflist-1]
            spline2 = lsrfunclist[lengthoflist]

            x_new = lsrXlist[lengthoflist]
            x_old = lsrXlist[lengthoflist-1]

            z_spline1 = keys[lengthoflist-1]
            z_spline2 = keys[lengthoflist]
            l =0
            if(lsr3Dchild==0):#SplineList and lsr3Dchild==0
                while l < len(x_new) -1 :
                    l += 1
                    #first triangle
                    lsr3Dchild += 1
                    DynamicVariable = "LSR3D" + str(lsr3Dchild)
                    point1 = x_old[l-1], spline1[l-1], z_spline1, 1
                    point2 = x_new[l-1], spline2[l-1], z_spline2, 1
                    point3 = x_old[l], spline1[l], z_spline1, 1
                    vars()[DynamicVariable]: GameObjectEntity = TriangleSpawn(DynamicVariable,point1,point2,point3,r ,g, b)
                    scene.world.addEntityChild(LSR3D, vars()[DynamicVariable])
                    #second triangle
                    lsr3Dchild += 1
                    DynamicVariable = "LSR3D" + str(lsr3Dchild)
                    point1 = x_new[l-1], spline2[l-1], z_spline2, 1
                    point2 = x_old[l], spline1[l], z_spline1, 1
                    point3 = x_new[l], spline2[l], z_spline2, 1
                    vars()[DynamicVariable]: GameObjectEntity = TriangleSpawn(DynamicVariable,point1,point2,point3,r ,g, b)
                    scene.world.addEntityChild(LSR3D, vars()[DynamicVariable])
                scene.world.traverse_visit(initUpdate, scene.world.root)

    imgui.end()


histogramchild2D = 0
histogramchild3D = 0
detailedHistogram = 10
toggle2DHistogram = True
toggle3DHistogram = True
def Histogram_Chart():
    global histogramchild2D
    global histogramchild3D
    global detailedHistogram
    global toggle2DHistogram
    global toggle3DHistogram
    imgui.begin("- Calculate Histogram -")
    imgui.text("Histogram ")
    Histogram_Button2D = imgui.button("2D Histogram")
    imgui.same_line() 
    toggle2DHistogrambutton = imgui.button("2D Histogram toggle")
    imgui.text("")
    Histogram_Button3D = imgui.button("3D Histogram")
    imgui.same_line() 
    toggle3DHistogrambutton = imgui.button("3D Histogram toggle")

    if(toggle2DHistogrambutton):
        toggle2DHistogram = not toggle2DHistogram
    elif(toggle3DHistogrambutton):
        toggle3DHistogram = not toggle3DHistogram

    changed, detailedHistogram = imgui.input_int('', detailedHistogram) 
    bins = np.linspace(0, 3, detailedHistogram)
 
    if (Histogram_Button2D):
        removeEntityChilds(Histogram2D)
        histogramchild2D=0

        arrayfromtupple = np.asarray(pointListfromCSV)
        HistogramY,HistogramX = np.histogram(arrayfromtupple[:,xPlane], bins )#= [0, 0.4, 0.8, 1.2, 1.6,2.0, 2.4, 2.8]
        i=0
        while i < len(HistogramX) -1:
            r = random.uniform(0, 1.0)
            g = random.uniform(0, 1.0)
            b = random.uniform(0, 1.0)
            i+=1
            histogramchild2D+=1
            DynamicVariable = "Cube" + str(histogramchild2D)

            point1 = HistogramX[i-1], 0, 0
            point2 = HistogramX[i-1], HistogramY[i-1], 0
            point3 = HistogramX[i], HistogramY[i-1], 0
            point4 = HistogramX[i], 0, 0              
            point5 = HistogramX[i-1], 0, 0
            point6 = HistogramX[i-1], HistogramY[i-1], 0
            point7 = HistogramX[i], HistogramY[i-1], 0
            point8 = HistogramX[i], 0, 0
            
            vars()[DynamicVariable]: GameObjectEntity = CubeSpawn(DynamicVariable,point1,point2,point3,point4,point5,point6,point7,point8,r,g,b)
            scene.world.addEntityChild(Histogram2D, vars()[DynamicVariable])
        scene.world.traverse_visit(initUpdate, scene.world.root)
            
    elif(Histogram_Button3D):
        removeEntityChilds(Histogram3D)
        histogramchild3D=0

        for x in range(len(keys)):
            if(values[x]):
                arr = np.array(values[x])
            HistogramY,HistogramX = np.histogram(arr[:,xPlane], bins )#= [0, 0.4, 0.8, 1.2, 1.6,2.0, 2.4, 2.8]
            i=0
            while i < len(HistogramX) -1:
                r = random.uniform(0, 1.0)
                g = random.uniform(0, 1.0)
                b = random.uniform(0, 1.0)
                i+=1
                histogramchild3D+=1
                DynamicVariable = "Cube" + str(histogramchild3D)

                point1 = HistogramX[i-1], 0, keys[x]+1
                point2 = HistogramX[i-1], HistogramY[i-1], keys[x]+1
                point3 = HistogramX[i], HistogramY[i-1], keys[x]+1
                point4 = HistogramX[i], 0, keys[x]+1              
                point5 = HistogramX[i-1], 0, keys[x]
                point6 = HistogramX[i-1], HistogramY[i-1], keys[x]
                point7 = HistogramX[i], HistogramY[i-1], keys[x]
                point8 = HistogramX[i], 0, keys[x]
                
                vars()[DynamicVariable]: GameObjectEntity = CubeSpawn(DynamicVariable,point1,point2,point3,point4,point5,point6,point7,point8,r,g,b)
                scene.world.addEntityChild(Histogram3D, vars()[DynamicVariable])
        scene.world.traverse_visit(initUpdate, scene.world.root)

    imgui.end()



ravdogramchild2D = 0
ravdogramchild3D = 0
detailedravdogram = 10
toggle2Dravdogram = True
toggle3Dravdogram = True

ravXListFrom = []
ravYListFrom = []
ravXListTo = []
ravYListTo = []
def Ravdogram_Chart():
    global ravXListFrom
    global ravYListFrom
    global ravXListTo
    global ravYListTo

    global ravdogramchild2D
    global ravdogramchild3D

    global toggle2Dravdogram
    global toggle3Dravdogram

    imgui.begin("- Calculate Ravdogram -")
    imgui.text("Ravdogram ")
    ravdogram_Button2D = imgui.button("2D Ravdogram")
    imgui.same_line() 
    toggle2Dravdogrambutton = imgui.button("2D Ravdogram toggle")

    ravdogram_Button3D = imgui.button("3D Ravdogram")
    imgui.same_line() 
    toggle3Dravdogrambutton = imgui.button("3D Ravdogram toggle")
    

    if(toggle2Dravdogrambutton):
        toggle2Dravdogram = not toggle2Dravdogram
    elif(toggle3Dravdogrambutton):
        toggle3Dravdogram = not toggle3Dravdogram

    if (ravdogram_Button2D):
        removeEntityChilds(Ravdogram2D)
        ravdogramchild2D=0
        arrayfromtupple = np.asarray(pointListfromCSV)
        
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])

        bars = ax.bar(arrayfromtupple[:,xPlane],arrayfromtupple[:,yPlane], width=0.05)    
        for i in ax.patches:
            ravXListTo.append(i.get_width())
            ravYListTo.append(i.get_height())
            
        for i in range(len(bars)):
            ravXListFrom.append(bars[i].xy[0])
            ravYListFrom.append(bars[i].xy[1])
            ravXListTo[i] = ravXListFrom[i] + ravXListTo[i]
            ravYListTo[i] = ravYListFrom[i] + ravYListTo[i]

        i=0
        while i < len(ravXListFrom):
            r = random.uniform(0, 1.0)
            g = random.uniform(0, 1.0)
            b = random.uniform(0, 1.0)
            ravdogramchild2D+=1
            DynamicVariable = "Cube" + str(ravdogramchild2D)

            point1 = ravXListFrom[i], ravYListFrom[i], 0
            point2 = ravXListFrom[i], ravYListTo[i], 0
            point3 = ravXListTo[i], ravYListTo[i], 0
            point4 = ravXListTo[i], ravYListFrom[i], 0              
            point5 = ravXListFrom[i], ravYListFrom[i], 0
            point6 = ravXListFrom[i], ravYListTo[i], 0
            point7 = ravXListTo[i], ravYListTo[i], 0
            point8 = ravXListTo[i], ravYListFrom[i], 0
            
            vars()[DynamicVariable]: GameObjectEntity = CubeSpawn(DynamicVariable,point1,point2,point3,point4,point5,point6,point7,point8,r,g,b)
            scene.world.addEntityChild(Ravdogram2D, vars()[DynamicVariable])
            i+=1
        scene.world.traverse_visit(initUpdate, scene.world.root)
    elif(ravdogram_Button3D):
        removeEntityChilds(Ravdogram3D)
        ravdogramchild3D=0
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])    
        for x in range(len(keys)):
            if(values[x]):
                arr = np.array(values[x])
            bars = ax.bar(arr[:,xPlane],arr[:,yPlane], width=0.2)  

            ravXListFrom.clear()
            ravYListFrom.clear()
            ravXListTo.clear()
            ravYListTo.clear()
            for i in ax.patches:
                ravXListTo.append(i.get_width())
                ravYListTo.append(i.get_height())
                
            for i in range(len(bars)):
                ravXListFrom.append(bars[i].xy[0])
                ravYListFrom.append(bars[i].xy[1])
                ravXListTo[i] = ravXListFrom[i] + ravXListTo[i]
                ravYListTo[i] = ravYListFrom[i] + ravYListTo[i]
                
            i=0
            while i < len(ravXListFrom):
                r = random.uniform(0, 1.0)
                g = random.uniform(0, 1.0)
                b = random.uniform(0, 1.0)
                ravdogramchild3D+=1
                DynamicVariable = "Cube" + str(ravdogramchild3D)

                point1 = ravXListFrom[i], ravYListFrom[i], keys[x]+1
                point2 = ravXListFrom[i], ravYListTo[i], keys[x]+1
                point3 = ravXListTo[i], ravYListTo[i], keys[x]+1
                point4 = ravXListTo[i], ravYListFrom[i], keys[x]+1              
                point5 = ravXListFrom[i], ravYListFrom[i], keys[x]
                point6 = ravXListFrom[i], ravYListTo[i], keys[x]
                point7 = ravXListTo[i], ravYListTo[i], keys[x]
                point8 = ravXListTo[i], ravYListFrom[i], keys[x]
                
                vars()[DynamicVariable]: GameObjectEntity = CubeSpawn(DynamicVariable,point1,point2,point3,point4,point5,point6,point7,point8,r,g,b)
                scene.world.addEntityChild(Ravdogram3D, vars()[DynamicVariable])
                i+=1
        scene.world.traverse_visit(initUpdate, scene.world.root)
    
        
    imgui.end()

piechild2D = 0
piechild3D = 0
toggle2Dpie = True
toggle3Dpie = True
def Pita_Chart():
    global piechild2D
    global piechild3D
    global toggle2Dpie
    global toggle3Dpie
    
    imgui.begin("- Calculate pie -")
    imgui.text("pie chart")

    arrayfromtupple = np.asarray(pointListfromCSV)  
    pie_Button2D = imgui.button("2D pie") 
    imgui.same_line() 
    toggle2Dpiebutton = imgui.button("2D pie toggle") 

    pie_Button3D = imgui.button("3D pie") 
    imgui.same_line() 
    toggle3Dpiebutton = imgui.button("3D pie toggle") 
    
    if(toggle2Dpiebutton):
        toggle2Dpie = not toggle2Dpie
    elif(toggle3Dpiebutton):
        toggle3Dpie = not toggle3Dpie

    if(pie_Button2D):
        removeEntityChilds(Pie2D)
        piechild2D=0

        xPercentagevalues = np.rint(arrayfromtupple[:,xPlane]/sum(arrayfromtupple[:,xPlane])*100).astype(int)
        x = np.linspace(0.2, 1.8, sum(xPercentagevalues)+5)
        
        i=0
        counter = 0
        while counter < len(xPercentagevalues):
            r = random.uniform(0, 1.0)
            g = random.uniform(0, 1.0)
            b = random.uniform(0, 1.0)
            i+=xPercentagevalues[counter]
            
            
            piechild2D+=1
            DynamicVariable = "Cube" + str(piechild2D)

            point1 = x[i-xPercentagevalues[counter]], 0, 0
            point2 = x[i-xPercentagevalues[counter]], 0.5, 0
            point3 = x[i], 0.5, 0
            point4 = x[i], 0, 0              
            point5 = x[i-xPercentagevalues[counter]], 0, 0
            point6 = x[i-xPercentagevalues[counter]], 0.5, 0
            point7 = x[i], 0.5, 0
            point8 = x[i], 0, 0
            
            vars()[DynamicVariable]: GameObjectEntity = CubeSpawn(DynamicVariable,point1,point2,point3,point4,point5,point6,point7,point8,r,g,b)
            scene.world.addEntityChild(Pie2D, vars()[DynamicVariable])
            counter+=1
        scene.world.traverse_visit(initUpdate, scene.world.root)
    elif(pie_Button3D):
        removeEntityChilds(Pie3D)
        piechild3D=0
        xPercentagevalues = np.rint(arrayfromtupple[:,xPlane]/sum(arrayfromtupple[:,xPlane])*100).astype(int)
        x = np.linspace(0.2, 1.8, sum(xPercentagevalues)+5)
        
        i=0
        counter = 0
        while counter < len(xPercentagevalues):
            r = random.uniform(0, 1.0)
            g = random.uniform(0, 1.0)
            b = random.uniform(0, 1.0)
            i+=xPercentagevalues[counter]
            
            
            piechild3D+=1
            DynamicVariable = "Cube" + str(piechild3D)

            point1 = x[i-xPercentagevalues[counter]], 0, 1
            point2 = x[i-xPercentagevalues[counter]], 0.5, 1
            point3 = x[i], 0.5, 1
            point4 = x[i], 0, 1              
            point5 = x[i-xPercentagevalues[counter]], 0, 0
            point6 = x[i-xPercentagevalues[counter]], 0.5, 0
            point7 = x[i], 0.5, 0
            point8 = x[i], 0, 0
            
            vars()[DynamicVariable]: GameObjectEntity = CubeSpawn(DynamicVariable,point1,point2,point3,point4,point5,point6,point7,point8,r,g,b)
            scene.world.addEntityChild(Pie3D, vars()[DynamicVariable])
            counter+=1
        scene.world.traverse_visit(initUpdate, scene.world.root)

    #imgui.same_line() 
    #ravdogram_Button3D = imgui.button("3D pie")
    imgui.end()
    
CleanData = 0 
def CleanData():
    imgui.begin("- CleanData -")
    imgui.text("Clean Data")
    global pointchild
    global trianglechild3D
    global trianglechild2D
    global superfuncchild2D
    global superfuncchild3D
    global histogramchild2D
    global histogramchild3D
    global ravdogramchild2D
    global ravdogramchild3D
    global lsr2Dchild
    global lsr3Dchild
    global piechild2D
    global piechild3D
    global childplatX
    global childplatZ
    global spotPointschild

    CleanData = imgui.button("clean") 
    if(CleanData):
        i=1
        #print points
        removeEntityChilds(PointsNode)
        removeEntityChilds(Area3D)
        removeEntityChilds(Area2D)
        removeEntityChilds(SuperFunction2D)
        removeEntityChilds(SuperFunction3D)
        removeEntityChilds(Histogram2D)
        removeEntityChilds(Histogram3D)
        removeEntityChilds(Ravdogram2D)
        removeEntityChilds(Ravdogram3D)
        removeEntityChilds(LSR2D)
        removeEntityChilds(LSR3D)
        removeEntityChilds(Pie2D)
        removeEntityChilds(Pie3D)
        removeEntityChilds(funcPlatformX)
        removeEntityChilds(funcPlatformZ)
        removeEntityChilds(spotPoints)

        
        pointchild=0
        trianglechild3D=0
        trianglechild2D=0
        superfuncchild3D=0
        superfuncchild2D=0
        histogramchild2D=0
        histogramchild3D=0
        ravdogramchild2D=0
        ravdogramchild3D=0
        lsr2Dchild=0
        lsr3Dchild=0
        piechild2D=0
        piechild3D=0
        childplatX=0
        childplatZ=0
        spotPointschild=0
        #scene.world.traverse_visit(initUpdate, scene.world.root)

    imgui.end()

def removeEntityChilds(entity: Entity):
    while entity.getChild(1) != None:
        entity.remove(entity.getChild(1))

LightPosionValues= 0.4,8.,0.5

def light_GUI():
    global LightPosionValues
    imgui.begin("-Light Controls -")
    imgui.text("Light Position Values X,Y,Z ")
    #changed, LightPosionValues = imgui.input_float3('', *LightPosionValues) 
    changed, LightPosionValues = imgui.drag_float3("Light Position Settings", *LightPosionValues, 0.02, 0.1, 40, "%.1f")

    imgui.end()

def displayGUI():
    """
        displays ImGui
    """
    #global value
    Func_GUI()
    CSV_GUI()
    Area_Chart()
    ScatterPlot_Chart()
    Histogram_Chart()
    Ravdogram_Chart()
    Pita_Chart()    
    light_GUI()

    CleanData()

def f_Z (x,y):
    import numpy as np
    global f_x_y
    d= {}
    d['x'] = x
    d['y'] = y
    z = eval(f_x_y,d)
    return z

def f_X (x):
    global f_x
    d= {}
    d['x'] = x
    y = eval(f_x,d)
    return y


COLOR_FRAG = """
    #version 410

    in vec4 color;
    out vec4 outputColor;

    void main()
    {
        outputColor = color;
        //outputColor = vec4(0.1, 0.1, 0.1, 1);
    }
"""

COLOR_VERT_MVP = """

    #version 410

    layout (location=0) in vec4 vPosition;
    layout (location=1) in vec4 vColor;

    out     vec4 color;
    uniform mat4 modelViewProj;
    uniform vec4 extColor;

    void main()
    {

        gl_Position = modelViewProj * vPosition;
        color = extColor;
    }
"""
    
VERT_PHONG_MVP = """
    #version 410

    layout (location=0) in vec4 vPosition;
    layout (location=1) in vec4 vColor;
    layout (location=2) in vec4 vNormal;

    out     vec4 pos;
    out     vec4 color;
    out     vec3 normal;
    
    uniform mat4 modelViewProj;
    uniform mat4 model;

    void main()
    {
        gl_Position = modelViewProj * vPosition;
        pos = model * vPosition;
        color = vColor;
        normal = mat3(transpose(inverse(model))) * vNormal.xyz;
    }
"""

FRAG_PHONG = """
    #version 410

    in vec4 pos;
    in vec4 color;
    in vec3 normal;

    out vec4 outputColor;

    // Phong products
    uniform vec3 ambientColor;
    uniform float ambientStr;

    // Lighting 
    uniform vec3 viewPos;
    uniform vec3 lightPos;
    uniform vec3 lightColor;
    uniform float lightIntensity;

    // Material
    uniform float shininess;
    uniform vec3 matColor;

    void main()
    {
        vec3 norm = normalize(normal);
        vec3 lightDir = normalize(lightPos - pos.xyz);
        vec3 viewDir = normalize(viewPos - pos.xyz);
        vec3 reflectDir = reflect(-lightDir, norm);
        

        // Ambient
        vec3 ambientProduct = ambientStr * ambientColor;
        // Diffuse
        float diffuseStr = max(dot(norm, lightDir), 0.0);
        vec3 diffuseProduct = diffuseStr * lightColor;
        // Specular
        float specularStr = pow(max(dot(viewDir, reflectDir), 0.0), 32);
        vec3 specularProduct = shininess * specularStr * color.xyz;
        
        vec3 result = (ambientProduct + (diffuseProduct + specularProduct) * lightIntensity) * matColor;
        outputColor = vec4(result, 1);
    }
"""

class IndexedConverter():
    
    # Assumes triangulated buffers. Produces indexed results that support
    # normals as well.
    def Convert(self, vertices, colors, indices, produceNormals=True):

        iVertices = [];
        iColors = [];
        iNormals = [];
        iIndices = [];
        for i in range(0, len(indices), 3):
            iVertices.append(vertices[indices[i]]);
            iVertices.append(vertices[indices[i + 1]]);
            iVertices.append(vertices[indices[i + 2]]);
            iColors.append(colors[indices[i]]);
            iColors.append(colors[indices[i + 1]]);
            iColors.append(colors[indices[i + 2]]);
            

            iIndices.append(i);
            iIndices.append(i + 1);
            iIndices.append(i + 2);

        if produceNormals:
            for i in range(0, len(indices), 3):
                iNormals.append(util.calculateNormals(vertices[indices[i]], vertices[indices[i + 1]], vertices[indices[i + 2]]));
                iNormals.append(util.calculateNormals(vertices[indices[i]], vertices[indices[i + 1]], vertices[indices[i + 2]]));
                iNormals.append(util.calculateNormals(vertices[indices[i]], vertices[indices[i + 1]], vertices[indices[i + 2]]));

        iVertices = np.array( iVertices, dtype=np.float32 )
        iColors   = np.array( iColors,   dtype=np.float32 )
        iIndices  = np.array( iIndices,  dtype=np.uint32  )

        iNormals  = np.array( iNormals,  dtype=np.float32 )

        return iVertices, iColors, iIndices, iNormals;
class GameObjectEntity_Point(Entity):
    def __init__(self, name=None, type=None, id=None, primitiveID = gl.GL_LINES) -> None:
        super().__init__(name, type, id)

        # Gameobject basic properties
        self._color          = [1, 0.5, 0.2, 1.0] # this will be used as a uniform var
        # Create basic components of a primitive object
        self.trans          = BasicTransform(name="trans", trs=util.identity())
        self.mesh           = RenderMesh(name="mesh")
        # self.shaderDec      = ShaderGLDecorator(Shader(vertex_source=Shader.VERT_PHONG_MVP, fragment_source=Shader.FRAG_PHONG))
        self.shaderDec      = ShaderGLDecorator(Shader(vertex_source= COLOR_VERT_MVP, fragment_source=COLOR_FRAG))
        self.vArray         = VertexArray(primitive= primitiveID)
        # Add components to entity
        scene = Scene()
        scene.world.createEntity(self)
        scene.world.addComponent(self, self.trans)
        scene.world.addComponent(self, self.mesh)
        scene.world.addComponent(self, self.shaderDec)
        scene.world.addComponent(self, self.vArray)
        

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, colorArray):
        self._color = colorArray

    def drawSelfGui(self, imgui):
        changed, value = imgui.color_edit3("Color", self.color[0], self.color[1], self.color[2])
        self.color = [value[0], value[1], value[2], 1.0]

    def SetVertexAttributes(self, vertex, color, index, normals = None):
        self.mesh.vertex_attributes.append(vertex)
        self.mesh.vertex_attributes.append(color)
        self.mesh.vertex_index.append(index)
        if normals is not None:
            self.mesh.vertex_attributes.append(normals)

class GameObjectEntity(Entity):

    def __init__(self, name=None, type=None, id=None, primitiveID = gl.GL_LINES) -> None:
        super().__init__(name, type, id)

        # Gameobject basic properties
        self._color          = [1, 0.5, 0.2, 1.0] # this will be used as a uniform var
        # Create basic components of a primitive object
        self.trans          = BasicTransform(name="trans", trs=util.identity())
        self.mesh           = RenderMesh(name="mesh")
        self.shaderDec      = ShaderGLDecorator(Shader(vertex_source=VERT_PHONG_MVP, fragment_source=FRAG_PHONG))
        #self.shaderDec      = ShaderGLDecorator(Shader(vertex_source= Shader.COLOR_VERT_MVP, fragment_source=Shader.COLOR_FRAG))
        self.vArray         = VertexArray(primitive= primitiveID)
        # Add components to entity
        scene = Scene()
        scene.world.createEntity(self)
        scene.world.addComponent(self, self.trans)
        scene.world.addComponent(self, self.mesh)
        scene.world.addComponent(self, self.shaderDec)
        scene.world.addComponent(self, self.vArray)
        
        

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self, colorArray):
        self._color = colorArray

    def drawSelfGui(self, imgui):
        changed, value = imgui.color_edit3("Color", self.color[0], self.color[1], self.color[2])
        self.color = [value[0], value[1], value[2], 1.0]

    def SetVertexAttributes(self, vertex, color, index, normals = None):
        self.mesh.vertex_attributes.append(vertex)
        self.mesh.vertex_attributes.append(color)
        self.mesh.vertex_index.append(index)
        if normals is not None:
            self.mesh.vertex_attributes.append(normals)

def CubeSpawn(cubename = "Cube",p1=[-0.5, -0.5, 0.5, 1.0],p2 = [-0.5, 0.5, 0.5, 1.0],p3 = [0.5, 0.5, 0.5, 1.0]
, p4 = [0.5, -0.5, 0.5, 1.0], p5=[-0.5, -0.5, -0.5, 1.0], p6=[-0.5, 0.5, -0.5, 1.0], p7=[0.5, 0.5, -0.5, 1.0], p8=[0.5, -0.5, -0.5, 1.0], r=0.55,g=0.55,b=0.55): 
    cube = GameObjectEntity(cubename, primitiveID=gl.GL_TRIANGLES)
    vertices = [
        p1,p2,p3,p4,p5,p6,p7,p8        
    ]
    colors = [
        [r, g, b, 1.0],
        [r, g, b, 1.0],
        [r, g, b, 1.0],
        [r, g, b, 1.0],
        [r, g, b, 1.0],
        [r, g, b, 1.0],
        [r, g, b, 1.0],
        [r, g, b, 1.0]                
    ]
    
    #index arrays for above vertex Arrays
    indices = np.array(
        (
            1,0,3, 1,3,2, 
            2,3,7, 2,7,6,
            3,0,4, 3,4,7,
            6,5,1, 6,1,2,
            4,5,6, 4,6,7,
            5,4,0, 5,0,1
        ),
        dtype=np.uint32
    ) #rhombus out of two triangles

    vertices, colors, indices, normals = IndexedConverter().Convert(vertices, colors, indices, produceNormals=True);
    cube.SetVertexAttributes(vertices, colors, indices, normals)
    
    return cube


def TriangleSpawn(trianglename = "Triangle",p1=[0,0,0,1],p2 = [0.4,0.4,0,1],p3 = [0.8,0.0,0,1], r=0.55,g=0.55,b=0.55):
    triangle = GameObjectEntity(trianglename,primitiveID=gl.GL_TRIANGLES)
    vertices = [
        p1,p2,p3
    ]
    colors = [
        [r, g, b, 1.0],
        [r, g, b, 1.0],
        [r, g, b, 1.0]
    ]
    
    indices = np.array(
        (
            1,0,2
        ),
        dtype=np.uint32
    ) 
    vertices, colors, indices, normals = IndexedConverter().Convert(vertices, colors, indices, produceNormals=True)
    triangle.SetVertexAttributes(vertices, colors, indices, normals)

    
    return triangle

def LineSpawn(linename = "Line",p1=[0,0,0,1],p2 = [0.4,0.4,0,1], r=0.7,g=0.7,b=0.7):
    line = GameObjectEntity(linename,primitiveID=gl.GL_LINES)
    vertices = [
        p1,p2
    ]
    colors = [
        [r, g, b, 1.0],
        [r, g, b, 1.0] 
    ]
    
    indices = np.array(
        (
            0,1,3
        ),
        dtype=np.uint32
    ) 

    #vertices, colors, indices, none = IndexedConverter().Convert(vertices, colors, indices, produceNormals=True)
    line.SetVertexAttributes(vertices, colors, indices, None)
    
    return line

def PointSpawn(pointname = "Point",p1=[0,0,0,1],r=0.,g=1.,b=1.): 
    point = GameObjectEntity_Point(pointname,primitiveID=gl.GL_POINTS)
    vertices = [
        p1
    ]
    colors = [
        
        [r, g, b, 1.0]                    
    ]
    indices = np.array(
        (
            0
        ),
        dtype=np.uint32
    ) 

    #vertices, colors, indices, normals = IndexedConverter().Convert(vertices, colors, indices, produceNormals=True)
    point.SetVertexAttributes(vertices, colors, indices, None)
    
    return point



def main (imguiFlag = False):
    #Colored Axes
    vertexAxes = np.array([
        [0.0, 0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0, 1.0],
        [0.0, 0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0, 1.0],
        [0.0, 0.0, 0.0, 1.0],
        [0.0, 0.0, 1.0, 1.0]
    ],dtype=np.float32) 
    colorAxes = np.array([
        [1.0, 0.0, 0.0, 1.0],
        [1.0, 0.0, 0.0, 1.0],
        [0.0, 1.0, 0.0, 1.0],
        [0.0, 1.0, 0.0, 1.0],
        [0.0, 0.0, 1.0, 1.0],
        [0.0, 0.0, 1.0, 1.0]
    ], dtype=np.float32)

    #index arrays for above vertex Arrays
    #index = np.array((0,1,2), np.uint32) #simple triangle
    indexAxes = np.array((0,1,2,3,4,5), np.uint32) #3 simple colored Axes as R,G,B lines

    # Systems
    transUpdate = scene.world.createSystem(TransformSystem("transUpdate", "TransformSystem", "001"))
    camUpdate = scene.world.createSystem(CameraSystem("camUpdate", "CameraUpdate", "200"))
    renderUpdate = scene.world.createSystem(RenderGLShaderSystem())
    initUpdate = scene.world.createSystem(InitGLShaderSystem())

    """
    test_renderPointGenaratorEVENT
    """
    # Generate terrain
    from pyGLV.GL.terrain import generateTerrain
    vertexTerrain, indexTerrain, colorTerrain= generateTerrain(size=4,N=20)
    # Add terrain
    terrain = scene.world.createEntity(Entity(name="terrain"))
    scene.world.addEntityChild(rootEntity, terrain)
    terrain_trans = scene.world.addComponent(terrain, BasicTransform(name="terrain_trans", trs=util.identity()))
    terrain_mesh = scene.world.addComponent(terrain, RenderMesh(name="terrain_mesh"))
    terrain_mesh.vertex_attributes.append(vertexTerrain) 
    terrain_mesh.vertex_attributes.append(colorTerrain)
    terrain_mesh.vertex_index.append(indexTerrain)
    terrain_vArray = scene.world.addComponent(terrain, VertexArray(primitive=GL_LINES))
    terrain_shader = scene.world.addComponent(terrain, ShaderGLDecorator(Shader(vertex_source = Shader.COLOR_VERT_MVP, fragment_source=Shader.COLOR_FRAG)))
    # terrain_shader.setUniformVariable(key='modelViewProj', value=mvpMat, mat4=True)
   
    ## ADD AXES ##

    axes = scene.world.createEntity(Entity(name="axes"))
    scene.world.addEntityChild(rootEntity, axes)
    axes_trans = scene.world.addComponent(axes, BasicTransform(name="axes_trans", trs=util.identity()))
    axes_mesh = scene.world.addComponent(axes, RenderMesh(name="axes_mesh"))
    axes_mesh.vertex_attributes.append(vertexAxes) 
    axes_mesh.vertex_attributes.append(colorAxes)
    axes_mesh.vertex_index.append(indexAxes)
    axes_vArray = scene.world.addComponent(axes, VertexArray(primitive=GL_LINES))

    # OR
    axes_shader = scene.world.addComponent(axes, ShaderGLDecorator(Shader(vertex_source = Shader.COLOR_VERT_MVP, fragment_source=Shader.COLOR_FRAG)))
    
    running = True
    # MAIN RENDERING LOOP
    scene.init(imgui=True, windowWidth = 1024, windowHeight = 768, windowTitle = "pyglGA test_renderAxesTerrainEVENT")#, customImGUIdecorator = ImGUIecssDecorator
    imGUIecss = scene.gContext

    # pre-pass scenegraph to initialise all GL context dependent geometry, shader classes
    # needs an active GL context
    
    # vArrayAxes.primitive = gl.GL_LINES
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glDisable(gl.GL_CULL_FACE)

    # gl.glDepthMask(gl.GL_FALSE)  
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glDepthFunc(gl.GL_LESS)
    ################### EVENT MANAGER ###################
    scene.world.traverse_visit(initUpdate, scene.world.root)

    eManager = scene.world.eventManager
    gWindow = scene.renderWindow
    gGUI = scene.gContext

    renderGLEventActuator = RenderGLStateSystem()


    #updateTRS = Event(name="OnUpdateTRS", id=100, value=None) #lines 255-258 contains the Scenegraph in a GUI as is it has issues.. To be fixed
    #updateBackground = Event(name="OnUpdateBackground", id=200, value=None)
    #eManager._events[updateTRS.name] = updateTRS
    #eManager._events[updateBackground.name] = updateBackground


    #eManager._subscribers[updateTRS.name] = gGUI
    #eManager._subscribers[updateBackground.name] = gGUI

    eManager._subscribers['OnUpdateWireframe'] = gWindow
    eManager._actuators['OnUpdateWireframe'] = renderGLEventActuator
    eManager._subscribers['OnUpdateCamera'] = gWindow 
    eManager._actuators['OnUpdateCamera'] = renderGLEventActuator
    
    # Add RenderWindow to the EventManager publishers
    # eManager._publishers[updateBackground.name] = gGUI
    #eManager._publishers[updateBackground.name] = gGUI ## added


    eye = util.vec(1.2, 4.34, 6.1)
    target = util.vec(0.0, 0.0, 0.0)
    up = util.vec(0.0, 1.0, 0.0)
    view = util.lookat(eye, target, up)
    
    projMat = util.perspective(50.0, 1.0, 1.0, 20.0) ## Setting the camera as perspective 

    gWindow._myCamera = view # otherwise, an imgui slider must be moved to properly update

    model_terrain_axes = util.translate(0.0,0.0,0.0)
    
    
    #LISTS
    LinesList = [] 

    #LISTS
    toggleSwitch = True
    toggleLineSwitch = True
    toggleLineZSwitch = True

    #MOST USEFUL GLOBALS
    linechild = 0
    #ALWAYS CHANGING GLOBALS
    linechildZ = 0#used for z=0 lines
    linechildPlane = 0#used for lines that interconnect z=0 with z=1
    ChildMeadian = 0#used for median point
    global pointListfromCSV
    global xPlane
    global yPlane
    global zPlane
    global PointSize
    global values
    global keys

    global  pointchild
    global toggle_scatterplot

    global SplineList

    global trianglechild3D
    global togglePlatformSwitch3D

    global superfuncchild2D
    global toggleSuperFunc2D
    
    global superfuncchild3D
    global toggleSuperFunc3D

    global histogramchild2D
    global histogramchild3D
    global toggle2DHistogram
    global toggle3DHistogram

    global ravdogramchild2D
    global toggle2Dravdogram
    global ravdogramchild3D
    global toggle3Dravdogram


    global lsr2Dchild
    global lsr3Dchild
    global lsr2Dtoggle
    global lsr3Dtoggle

    global piechild2D
    global piechild3D
    global toggle2Dpie
    global toggle3Dpie
    
    global childplatX
    global plattoggleX 
    global childplatZ
    global plattoggleZ 

    global spotPointschild
    global LightPosionValues
    #Light
    
    #Lposition = util.vec(LightPosionValues) #uniform lightpos

    Lambientcolor = util.vec(1.0, 1.0, 5.0) #uniform ambient color
    Lambientstr = 0.1 #uniform ambientStr
    LviewPos = util.vec(2.5, 2.8, 5.0) #uniform viewpos
    Lcolor = util.vec(1.0,1.0,1.0)
    Lintensity = 0.5
    #Material
    Mshininess = 0.0 
    Mcolor = util.vec(0.7, 0.35, 0.0)

    #we split our csv based on common Z plane values and pass it to 2 lists for later use
    for Zplanekey, value in itertools.groupby(pointListfromCSV, lambda x: x[7]):
        keys.append(Zplanekey)
        values.append(list(value))
    for i in range(len(keys)):
        values[i].sort(key = lambda row: (row[xPlane]),reverse=False)
    gl.glPointSize(PointSize)
    #Displays all nodes created
    def Display():
        #drawText(1, 1, "cube")
        i=1
        #print points
        while i<=pointchild:
            if(toggle_scatterplot):
                PointsNode.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=mvp_point @ PointsNode.getChild(i).trans.l2cam, mat4=True)
                PointsNode.getChild(i).shaderDec.setUniformVariable(key='extColor', value=[PointsColor[0], PointsColor[1], PointsColor[2], 1.0], float4=True) #its porpuse is to change color on my_color vertex by setting the uniform                  
            else:
                PointsNode.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=None, mat4=True)
            i +=1
        i = 1
        #print Lines
        while i <= linechild:
            if( linechildPlane + i > linechild):#for lines intertwine z plane
                if(toggleLineZSwitch):
                    LinesNode.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=mvp_point @LinesNode.getChild(i).trans.l2cam, mat4=True)
                else:
                    LinesNode.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=None, mat4=True)
            else:#for lines inside each z plane
                if(toggleLineSwitch):
                    LinesNode.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=mvp_point @LinesNode.getChild(i).trans.l2cam, mat4=True)
                    #LinesNode.getChild(i-1).shaderDec.setUniformVariable(key='my_color', value=[1, 0, 0] , mat4=True)                   

                else:
                    LinesNode.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=None, mat4=True)

            i+=1
        i=1
        #print Area3D
        while i <= trianglechild3D:
            if togglePlatformSwitch3D:
                Area3D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=mvp_point @Area3D.getChild(i).trans.l2cam, mat4=True)
                Area3D.getChild(i).shaderDec.setUniformVariable(key='model',value=Area3D.getChild(i).trans.l2cam,mat4=True)
                Area3D.getChild(i).shaderDec.setUniformVariable(key='ambientColor',value=Lambientcolor,float3=True)
                Area3D.getChild(i).shaderDec.setUniformVariable(key='ambientStr',value=Lambientstr,float1=True)
                Area3D.getChild(i).shaderDec.setUniformVariable(key='viewPos',value=LviewPos,float3=True)
                Area3D.getChild(i).shaderDec.setUniformVariable(key='lightPos',value=Lposition,float3=True)
                Area3D.getChild(i).shaderDec.setUniformVariable(key='lightColor',value=Lcolor,float3=True)
                Area3D.getChild(i).shaderDec.setUniformVariable(key='lightIntensity',value=Lintensity,float1=True)
                Area3D.getChild(i).shaderDec.setUniformVariable(key='shininess',value=Mshininess,float1=True)
                Area3D.getChild(i).shaderDec.setUniformVariable(key='matColor',value=Mcolor,float3=True)
            else:
                Area3D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=None, mat4=True)
            i+=1
        i=1
        #print Area2D
        while i <= trianglechild2D:
            if togglePlatformSwitch2D:
                Area2D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=mvp_point @Area2D.getChild(i).trans.l2cam, mat4=True)
                Area2D.getChild(i).shaderDec.setUniformVariable(key='model',value=Area2D.getChild(i).trans.l2cam,mat4=True)
                Area2D.getChild(i).shaderDec.setUniformVariable(key='ambientColor',value=Lambientcolor,float3=True)
                Area2D.getChild(i).shaderDec.setUniformVariable(key='ambientStr',value=Lambientstr,float1=True)
                Area2D.getChild(i).shaderDec.setUniformVariable(key='viewPos',value=LviewPos,float3=True)
                Area2D.getChild(i).shaderDec.setUniformVariable(key='lightPos',value=Lposition,float3=True)
                Area2D.getChild(i).shaderDec.setUniformVariable(key='lightColor',value=Lcolor,float3=True)
                Area2D.getChild(i).shaderDec.setUniformVariable(key='lightIntensity',value=Lintensity,float1=True)
                Area2D.getChild(i).shaderDec.setUniformVariable(key='shininess',value=Mshininess,float1=True)
                Area2D.getChild(i).shaderDec.setUniformVariable(key='matColor',value=Mcolor,float3=True)
            else:
                Area2D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=None, mat4=True)
            i+=1
        i=1
        #print SuperFunction
        while i <= superfuncchild2D:
            if toggleSuperFunc2D:
                SuperFunction2D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=mvp_point @SuperFunction2D.getChild(i).trans.l2cam, mat4=True)
                SuperFunction2D.getChild(i).shaderDec.setUniformVariable(key='model',value=SuperFunction2D.getChild(i).trans.l2cam,mat4=True)
                SuperFunction2D.getChild(i).shaderDec.setUniformVariable(key='ambientColor',value=Lambientcolor,float3=True)
                SuperFunction2D.getChild(i).shaderDec.setUniformVariable(key='ambientStr',value=Lambientstr,float1=True)
                SuperFunction2D.getChild(i).shaderDec.setUniformVariable(key='viewPos',value=LviewPos,float3=True)
                SuperFunction2D.getChild(i).shaderDec.setUniformVariable(key='lightPos',value=Lposition,float3=True)
                SuperFunction2D.getChild(i).shaderDec.setUniformVariable(key='lightColor',value=Lcolor,float3=True)
                SuperFunction2D.getChild(i).shaderDec.setUniformVariable(key='lightIntensity',value=Lintensity,float1=True)
                SuperFunction2D.getChild(i).shaderDec.setUniformVariable(key='shininess',value=Mshininess,float1=True)
                SuperFunction2D.getChild(i).shaderDec.setUniformVariable(key='matColor',value=Mcolor,float3=True)
            else:
                SuperFunction2D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=None, mat4=True)
            i+=1
        i=1
        while i <= superfuncchild3D:
            if toggleSuperFunc3D:
                SuperFunction3D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=mvp_point @SuperFunction3D.getChild(i).trans.l2cam, mat4=True)
                SuperFunction3D.getChild(i).shaderDec.setUniformVariable(key='model',value=SuperFunction3D.getChild(i).trans.l2cam,mat4=True)
                SuperFunction3D.getChild(i).shaderDec.setUniformVariable(key='ambientColor',value=Lambientcolor,float3=True)
                SuperFunction3D.getChild(i).shaderDec.setUniformVariable(key='ambientStr',value=Lambientstr,float1=True)
                SuperFunction3D.getChild(i).shaderDec.setUniformVariable(key='viewPos',value=LviewPos,float3=True)
                SuperFunction3D.getChild(i).shaderDec.setUniformVariable(key='lightPos',value=Lposition,float3=True)
                SuperFunction3D.getChild(i).shaderDec.setUniformVariable(key='lightColor',value=Lcolor,float3=True)
                SuperFunction3D.getChild(i).shaderDec.setUniformVariable(key='lightIntensity',value=Lintensity,float1=True)
                SuperFunction3D.getChild(i).shaderDec.setUniformVariable(key='shininess',value=Mshininess,float1=True)
                SuperFunction3D.getChild(i).shaderDec.setUniformVariable(key='matColor',value=Mcolor,float3=True)
            else:
                SuperFunction3D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=None, mat4=True)
            i+=1
        i=1
        #print Histogram2D
        while i<= histogramchild2D:
            if(toggle2DHistogram):
                Histogram2D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=mvp_point @Histogram2D.getChild(i).trans.l2cam, mat4=True)
                Histogram2D.getChild(i).shaderDec.setUniformVariable(key='model',value=Histogram2D.getChild(i).trans.l2cam,mat4=True)
                Histogram2D.getChild(i).shaderDec.setUniformVariable(key='ambientColor',value=Lambientcolor,float3=True)
                Histogram2D.getChild(i).shaderDec.setUniformVariable(key='ambientStr',value=Lambientstr,float1=True)
                Histogram2D.getChild(i).shaderDec.setUniformVariable(key='viewPos',value=LviewPos,float3=True)
                Histogram2D.getChild(i).shaderDec.setUniformVariable(key='lightPos',value=Lposition,float3=True)
                Histogram2D.getChild(i).shaderDec.setUniformVariable(key='lightColor',value=Lcolor,float3=True)
                Histogram2D.getChild(i).shaderDec.setUniformVariable(key='lightIntensity',value=Lintensity,float1=True)
                Histogram2D.getChild(i).shaderDec.setUniformVariable(key='shininess',value=Mshininess,float1=True)
                Histogram2D.getChild(i).shaderDec.setUniformVariable(key='matColor',value=Mcolor,float3=True)
            else:
                Histogram2D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=None, mat4=True)
            i+=1
        i=1
        #print Histogram3D
        while i<= histogramchild3D:
            if(toggle3DHistogram):
                Histogram3D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=mvp_point @Histogram3D.getChild(i).trans.l2cam, mat4=True)
                Histogram3D.getChild(i).shaderDec.setUniformVariable(key='model',value=Histogram3D.getChild(i).trans.l2cam,mat4=True)
                Histogram3D.getChild(i).shaderDec.setUniformVariable(key='ambientColor',value=Lambientcolor,float3=True)
                Histogram3D.getChild(i).shaderDec.setUniformVariable(key='ambientStr',value=Lambientstr,float1=True)
                Histogram3D.getChild(i).shaderDec.setUniformVariable(key='viewPos',value=LviewPos,float3=True)
                Histogram3D.getChild(i).shaderDec.setUniformVariable(key='lightPos',value=Lposition,float3=True)
                Histogram3D.getChild(i).shaderDec.setUniformVariable(key='lightColor',value=Lcolor,float3=True)
                Histogram3D.getChild(i).shaderDec.setUniformVariable(key='lightIntensity',value=Lintensity,float1=True)
                Histogram3D.getChild(i).shaderDec.setUniformVariable(key='shininess',value=Mshininess,float1=True)
                Histogram3D.getChild(i).shaderDec.setUniformVariable(key='matColor',value=Mcolor,float3=True)
            else:
                Histogram3D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=None, mat4=True)
            i+=1
        i=1
        #print Ravdogram2D
        while i<= ravdogramchild2D:
            if(toggle2Dravdogram):
                Ravdogram2D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=mvp_point @Ravdogram2D.getChild(i).trans.l2cam, mat4=True)
                Ravdogram2D.getChild(i).shaderDec.setUniformVariable(key='model',value=Ravdogram2D.getChild(i).trans.l2cam,mat4=True)
                Ravdogram2D.getChild(i).shaderDec.setUniformVariable(key='ambientColor',value=Lambientcolor,float3=True)
                Ravdogram2D.getChild(i).shaderDec.setUniformVariable(key='ambientStr',value=Lambientstr,float1=True)
                Ravdogram2D.getChild(i).shaderDec.setUniformVariable(key='viewPos',value=LviewPos,float3=True)
                Ravdogram2D.getChild(i).shaderDec.setUniformVariable(key='lightPos',value=Lposition,float3=True)
                Ravdogram2D.getChild(i).shaderDec.setUniformVariable(key='lightColor',value=Lcolor,float3=True)
                Ravdogram2D.getChild(i).shaderDec.setUniformVariable(key='lightIntensity',value=Lintensity,float1=True)
                Ravdogram2D.getChild(i).shaderDec.setUniformVariable(key='shininess',value=Mshininess,float1=True)
                Ravdogram2D.getChild(i).shaderDec.setUniformVariable(key='matColor',value=Mcolor,float3=True)
            else:
                Ravdogram2D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=None, mat4=True)
            i+=1
        i=1
        while i<= ravdogramchild3D:
            if(toggle3Dravdogram):
                Ravdogram3D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=mvp_point @Ravdogram3D.getChild(i).trans.l2cam, mat4=True)
                Ravdogram3D.getChild(i).shaderDec.setUniformVariable(key='model',value=Ravdogram3D.getChild(i).trans.l2cam,mat4=True)
                Ravdogram3D.getChild(i).shaderDec.setUniformVariable(key='ambientColor',value=Lambientcolor,float3=True)
                Ravdogram3D.getChild(i).shaderDec.setUniformVariable(key='ambientStr',value=Lambientstr,float1=True)
                Ravdogram3D.getChild(i).shaderDec.setUniformVariable(key='viewPos',value=LviewPos,float3=True)
                Ravdogram3D.getChild(i).shaderDec.setUniformVariable(key='lightPos',value=Lposition,float3=True)
                Ravdogram3D.getChild(i).shaderDec.setUniformVariable(key='lightColor',value=Lcolor,float3=True)
                Ravdogram3D.getChild(i).shaderDec.setUniformVariable(key='lightIntensity',value=Lintensity,float1=True)
                Ravdogram3D.getChild(i).shaderDec.setUniformVariable(key='shininess',value=Mshininess,float1=True)
                Ravdogram3D.getChild(i).shaderDec.setUniformVariable(key='matColor',value=Mcolor,float3=True)
            else:
                Ravdogram3D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=None, mat4=True)
            i+=1
        i=1

        while i<= lsr2Dchild:
            if(lsr2Dtoggle):
                LSR2D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=mvp_point @LSR2D.getChild(i).trans.l2cam, mat4=True)
                LSR2D.getChild(i).shaderDec.setUniformVariable(key='model',value=LSR2D.getChild(i).trans.l2cam,mat4=True)
                LSR2D.getChild(i).shaderDec.setUniformVariable(key='ambientColor',value=Lambientcolor,float3=True)
                LSR2D.getChild(i).shaderDec.setUniformVariable(key='ambientStr',value=Lambientstr,float1=True)
                LSR2D.getChild(i).shaderDec.setUniformVariable(key='viewPos',value=LviewPos,float3=True)
                LSR2D.getChild(i).shaderDec.setUniformVariable(key='lightPos',value=Lposition,float3=True)
                LSR2D.getChild(i).shaderDec.setUniformVariable(key='lightColor',value=Lcolor,float3=True)
                LSR2D.getChild(i).shaderDec.setUniformVariable(key='lightIntensity',value=Lintensity,float1=True)
                LSR2D.getChild(i).shaderDec.setUniformVariable(key='shininess',value=Mshininess,float1=True)
                LSR2D.getChild(i).shaderDec.setUniformVariable(key='matColor',value=Mcolor,float3=True)
            else:
                LSR2D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=None, mat4=True)
            i+=1
        i=1
        while i<= lsr3Dchild:
            if(lsr3Dtoggle):
                LSR3D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=mvp_point @LSR3D.getChild(i).trans.l2cam, mat4=True)
                LSR3D.getChild(i).shaderDec.setUniformVariable(key='model',value=LSR3D.getChild(i).trans.l2cam,mat4=True)
                LSR3D.getChild(i).shaderDec.setUniformVariable(key='ambientColor',value=Lambientcolor,float3=True)
                LSR3D.getChild(i).shaderDec.setUniformVariable(key='ambientStr',value=Lambientstr,float1=True)
                LSR3D.getChild(i).shaderDec.setUniformVariable(key='viewPos',value=LviewPos,float3=True)
                LSR3D.getChild(i).shaderDec.setUniformVariable(key='lightPos',value=Lposition,float3=True)
                LSR3D.getChild(i).shaderDec.setUniformVariable(key='lightColor',value=Lcolor,float3=True)
                LSR3D.getChild(i).shaderDec.setUniformVariable(key='lightIntensity',value=Lintensity,float1=True)
                LSR3D.getChild(i).shaderDec.setUniformVariable(key='shininess',value=Mshininess,float1=True)
                LSR3D.getChild(i).shaderDec.setUniformVariable(key='matColor',value=Mcolor,float3=True)
            else:
                LSR3D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=None, mat4=True)
            i+=1
        i=1
        while i<= piechild2D:
            if(toggle2Dpie):
                Pie2D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=mvp_point @Pie2D.getChild(i).trans.l2cam, mat4=True)
                Pie2D.getChild(i).shaderDec.setUniformVariable(key='model',value=Pie2D.getChild(i).trans.l2cam,mat4=True)
                Pie2D.getChild(i).shaderDec.setUniformVariable(key='ambientColor',value=Lambientcolor,float3=True)
                Pie2D.getChild(i).shaderDec.setUniformVariable(key='ambientStr',value=Lambientstr,float1=True)
                Pie2D.getChild(i).shaderDec.setUniformVariable(key='viewPos',value=LviewPos,float3=True)
                Pie2D.getChild(i).shaderDec.setUniformVariable(key='lightPos',value=Lposition,float3=True)
                Pie2D.getChild(i).shaderDec.setUniformVariable(key='lightColor',value=Lcolor,float3=True)
                Pie2D.getChild(i).shaderDec.setUniformVariable(key='lightIntensity',value=Lintensity,float1=True)
                Pie2D.getChild(i).shaderDec.setUniformVariable(key='shininess',value=Mshininess,float1=True)
                Pie2D.getChild(i).shaderDec.setUniformVariable(key='matColor',value=Mcolor,float3=True)
            else:
                Pie2D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=None, mat4=True)
            i+=1
        i=1
        while i<= piechild3D:
            if(toggle3Dpie):
                Pie3D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=mvp_point @Pie3D.getChild(i).trans.l2cam, mat4=True)
                Pie3D.getChild(i).shaderDec.setUniformVariable(key='model',value=Pie3D.getChild(i).trans.l2cam,mat4=True)
                Pie3D.getChild(i).shaderDec.setUniformVariable(key='ambientColor',value=Lambientcolor,float3=True)
                Pie3D.getChild(i).shaderDec.setUniformVariable(key='ambientStr',value=Lambientstr,float1=True)
                Pie3D.getChild(i).shaderDec.setUniformVariable(key='viewPos',value=LviewPos,float3=True)
                Pie3D.getChild(i).shaderDec.setUniformVariable(key='lightPos',value=Lposition,float3=True)
                Pie3D.getChild(i).shaderDec.setUniformVariable(key='lightColor',value=Lcolor,float3=True)
                Pie3D.getChild(i).shaderDec.setUniformVariable(key='lightIntensity',value=Lintensity,float1=True)
                Pie3D.getChild(i).shaderDec.setUniformVariable(key='shininess',value=Mshininess,float1=True)
                Pie3D.getChild(i).shaderDec.setUniformVariable(key='matColor',value=Mcolor,float3=True)
            else:
                Pie3D.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=None, mat4=True)
            i+=1
        i=1
        while i<= childplatX:
            if(plattoggleX):
                funcPlatformX.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=mvp_point @funcPlatformX.getChild(i).trans.l2cam, mat4=True)
            else:
                funcPlatformX.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=None, mat4=True)
            i+=1
        i=1
        while i<= childplatZ:
            if(plattoggleZ):
                funcPlatformZ.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=mvp_point @funcPlatformZ.getChild(i).trans.l2cam, mat4=True)
            else:
                funcPlatformZ.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=None, mat4=True)
            i+=1
        i=1
        while i<= spotPointschild:
            if (togglepoints):
                spotPoints.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=mvp_point @spotPoints.getChild(i).trans.l2cam, mat4=True)
                spotPoints.getChild(i).shaderDec.setUniformVariable(key='extColor', value=[SpotPointsColor[0], SpotPointsColor[1], SpotPointsColor[2], 1.0], float4=True) #its porpuse is to change color on my_color vertex by setting the uniform                  
            else:
                spotPoints.getChild(i).shaderDec.setUniformVariable(key='modelViewProj', value=None, mat4=True)
            i+=1

        
        i=1
        scene.render_post()
    while running:
        Lposition = util.vec(LightPosionValues) #uniform lightpos

        running = scene.render(running)
        scene.world.traverse_visit(renderUpdate, scene.world.root)
        view =  gWindow._myCamera # updates view via the imgui
        mvp_point = projMat @ view 
        mvp_terrain_axes = projMat @ view @ model_terrain_axes
        displayGUI()
        #Toggle mechanism
        if (key.is_pressed("t")):#create points 
            toggleSwitch = not toggleSwitch
            time.sleep(0.15)
        if (toggleSwitch):
            axes_shader.setUniformVariable(key='modelViewProj', value=mvp_terrain_axes, mat4= True)
            terrain_shader.setUniformVariable(key='modelViewProj', value=mvp_terrain_axes, mat4= True)
        else:
            axes_shader.setUniformVariable(key='modelViewProj', value=None, mat4= True)
            terrain_shader.setUniformVariable(key='modelViewProj', value=None, mat4= True)
        #Connect line between two points mechanism
        if (key.is_pressed("s")):
            
            if(linechildZ == 0 and pointchild != 0):
                for i in range(len(keys)):
                    ValuesarrayLength = len(values[i])
                    linechildZCurrPlane=0
                    while(linechildZCurrPlane < ValuesarrayLength-1):
                        r = random.uniform(0, 1.0)
                        g = random.uniform(0, 1.0)
                        b = random.uniform(0, 1.0)
                        linechild +=1
                        linechildZ +=1
                        linechildZCurrPlane += 1
                        DynamicVariable = "Line" + str(linechild)
                        point1 =  values[i][linechildZCurrPlane][xPlane], values[i][linechildZCurrPlane][yPlane] , values[i][linechildZCurrPlane][zPlane], 1 
                        point2 =  values[i][linechildZCurrPlane-1][xPlane], values[i][linechildZCurrPlane-1][yPlane] , values[i][linechildZCurrPlane-1][zPlane], 1 

                        vars()[DynamicVariable]: GameObjectEntity = LineSpawn(DynamicVariable,point2,point1,r,g,b)
                        scene.world.addEntityChild(LinesNode, vars()[DynamicVariable])      
                scene.world.traverse_visit(initUpdate, scene.world.root)    
            else:
                toggleLineSwitch = not toggleLineSwitch
            
            time.sleep(0.15)
        #Line
        elif (key.is_pressed("l")):
            if(linechildPlane==0 and linechildZ != 0):
                for i in range(len(keys)):
                    LinesList += values[i]
                LinesList.sort(key = lambda row: (row[xPlane]),reverse=False)

                while(linechildPlane<pointchild -1):
                    linechild +=1 
                    linechildPlane +=1
                    DynamicVariable = "Line" + str(linechild)
                    point1 =  LinesList[linechildPlane][xPlane], LinesList[linechildPlane][yPlane] , LinesList[linechildPlane][zPlane], 1 
                    point2 =  LinesList[linechildPlane-1][xPlane], LinesList[linechildPlane-1][yPlane] , LinesList[linechildPlane-1][zPlane], 1 
                    vars()[DynamicVariable]: GameObjectEntity = LineSpawn(DynamicVariable,point2,point1,1,0,0)
                    scene.world.addEntityChild(LinesNode, vars()[DynamicVariable])
                scene.world.traverse_visit(initUpdate, scene.world.root)
            else:
                toggleLineZSwitch = not toggleLineZSwitch         
                
            time.sleep(0.15)
        #QUIT button
        elif (key.is_pressed("q")):
            print(" x:", xPlane, " y: ", yPlane, " z: ", zPlane)
            break
        #enlarge points
        elif (key.is_pressed("x")):
            PointSize +=1
            gl.glPointSize(PointSize)
            time.sleep(0.15)
        #make points smaller
        elif (key.is_pressed("z")):
            PointSize -=1
            gl.glPointSize(PointSize)
            time.sleep(0.15)
        Display()
        
    scene.shutdown()
    

if __name__ == "__main__":    
    main(imguiFlag = True)


