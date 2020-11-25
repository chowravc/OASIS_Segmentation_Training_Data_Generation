# Importing Packages
import bpy
import sys
import os
import numpy as np
import random as r
import glob as g

# Adding directory to PATH
dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

# Importing useful python scripts
from capCreator import *
from wallCreator import *
from bubbleCreator import *
from spotCreator import *
from lightUtils import *
from materialUtils import *
from intersectionCheck import *


# CHANGE CODE HERE-----

# Choose render resolution here
res = (256, 256)

# END OF CHANGE CODE-----


numberOfImages = len(g.glob("./angles/*"))

startNum = len(g.glob("./images/*"))

for k in range(startNum, numberOfImages):
    nameID = str(k).zfill(len(str(numberOfImages)))
    # Creating a number of randomly decided caps.

    # Number of random caps to create.
    number = len(open("./angles/"+nameID+".txt", "r").read().splitlines())

    # Radius of the sphere the cap will be on.
    radius = 1

    # Location of the cap.
    location = (0, 0, 0)

    if k == startNum:
        # Materials of cap
        materialName = "frontCapMaterial"
        materialColor = (0.8, 0.8, 0.8)
        createMaterial(materialName, materialColor)
        frontCapMaterial = bpy.data.materials[materialName]

        materialName = "backCapMaterial"
        materialColor = (0.8, 0.8, 0.8)
        createMaterial(materialName, materialColor)
        backCapMaterial = bpy.data.materials[materialName]

        # Material of wall
        materialName = "wallMaterial"
        materialColor = (0, 0, 0)
        createMaterial(materialName, materialColor, removeShader=True)
        wallMaterial = bpy.data.materials[materialName]

        # Material of bubble
        materialName = "bubbleMaterial"
        materialColor = (0, 0, 0)
        createBubbleMaterial(materialName, materialColor)
        bubbleMaterial = bpy.data.materials[materialName]

    # Accessing island data from text files
    capAngles = open("./angles/"+nameID+".txt", "r").read().splitlines()
    capPhis = open("./phis/"+nameID+".txt", "r").read().splitlines()
    capThetas = open("./thetas/"+nameID+".txt", "r").read().splitlines()

    # Rendering each image
    for i in range(number):

        # Cap size parameter (Choose cap size between 0 and 10)
        cSize = float(capAngles[i])

        # Euler angles of the cap.
        euler = (float(capThetas[i]), float(capPhis[i]), 0)
        
        # Name the cap.
        name = "Cap" + str(i).zfill(len(str(number)))

        # Giving different material baxsed on whether it is a front or a back island
        if np.pi/2 <= euler[0] < 3*np.pi/2:
            createCap(radius, cSize, euler, location, name, backCapMaterial)
        else:
            createCap(radius, cSize, euler, location, name, frontCapMaterial)

    # Setting render path
    bpy.context.scene.render.filepath = os.getcwd() + '/images/' + nameID + '.png'

    # Creating walls
    if k == startNum:
        # Creating three walls
        createWall("Wall0", (2, -2, -10), (-5, -2, -10), (-5, -2, 10), (2, -2, 10), wallMaterial)
        createWall("Wall1", (2, 2, -10), (-5, 2, -10), (-5, 2, 10), (2, 2, 10), wallMaterial)
        createWall("Wall2", (-5, -2, -10), (-5, 2, -10), (-5, 2, 10), (-5, -2, 10), wallMaterial)

        # Creating bubble
        createBubble(radius, bubbleMaterial)

        # Creating dark spot
        spotRadius = 0.024
        createSpot(radius, spotRadius, wallMaterial)

        # Creating lighting
        customLight(0, (10, 0, 0), (np.pi/2, 0, np.pi/2), 'AREA', 2000, 5)

        # Creating and linking camera
        bpy.ops.object.camera_add(location=(3, 0, 0), rotation=(np.pi/2, 0, np.pi/2))

    # Changing camera size and setting to current scene
    bpy.data.cameras['Camera'].lens = 45
    bpy.context.scene.camera = bpy.data.objects['Camera']

    # Rendering Scene

    # Get the scene
    scene = bpy.data.scenes["Scene"]

    # Set render resolution
    scene.render.resolution_x = res[0]
    scene.render.resolution_y = res[1]
    scene.render.resolution_percentage = 100
    bpy.ops.render.render(write_still = True)

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Deleting all caps
    for capNumber in range(number):
        bpy.data.objects["Cap" + str(capNumber).zfill(len(str(number)))].select_set(True)
        bpy.ops.object.delete()

# Deleting everything

# Bubble
bpy.data.objects["Bubble0"].select_set(True)
bpy.ops.object.delete()

# Spot
bpy.data.objects["Spot0"].select_set(True)
bpy.ops.object.delete()

# Walls
bpy.data.objects["Wall0"].select_set(True)
bpy.ops.object.delete()

bpy.data.objects["Wall1"].select_set(True)
bpy.ops.object.delete()

bpy.data.objects["Wall2"].select_set(True)
bpy.ops.object.delete()

# Plane light
bpy.data.objects["Point"].select_set(True)
bpy.ops.object.delete()

# Camera
bpy.data.objects["Camera"].select_set(True)
bpy.ops.object.delete()

# Creating wall for user to edit material

createWall("ChangeEmissionToRed100OnMe", (10, 10, 0), (10, -10, 0), (-10, -10, 0), (-10, 10, 0), frontCapMaterial)
createWall("ChangeEmissionToGreen100OnMe", (10, 10, 0), (10, -10, 0), (-10, -10, 0), (-10, 10, 0), backCapMaterial)

print("")
print("Reached end of script 2.")
print("Ensure all images are rendered correctly and no objects exist in Blender file.")
print("Two walls should exist, please edit its material as per instuction to have 100 red or green emission.")
print("Please also change world ambient to 0.")
print("Run script 3 now.")
print("")