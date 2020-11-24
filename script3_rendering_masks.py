# Importing Packages
import bpy
import sys
import os
import numpy as np
import random as r
import glob as g

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


# Deleting wall used to add emission in last script
bpy.data.objects["ChangeEmissionToRed100OnMe"].select_set(True)
bpy.ops.object.delete()

bpy.data.objects["ChangeEmissionToGreen100OnMe"].select_set(True)
bpy.ops.object.delete()

# Finding out number of images to produce
numberOfImages = len(g.glob("./angles/*"))

# If true, separate masks for each island will be produced
# If false, front and back masks will be produced
insanceSegmentation = True

# Creating separate masks for each island in each image
if insanceSegmentation:

    # For each image
    for k in range(numberOfImages):

        # Deciding name of image
        nameID = str(k).zfill(len(str(numberOfImages)))

        # Creating a number of randomly decided caps.

        # Number of random caps to create.
        number = len(open("./angles/"+nameID+".txt", "r").read().splitlines())

        # Radius of the sphere the cap will be on.
        radius = 1

        # Location of the cap.
        location = (0, 0, 0)

        # If on first image, access these materials as variables
        if k == 0:

            # Cap materials
            frontCapMaterial = bpy.data.materials["frontCapMaterial"]
            backCapMaterial = bpy.data.materials["backCapMaterial"]

            # Material of wall
            materialName = "wallMaterial"
            materialColor = (0, 0, 0)
            createMaterial(materialName, materialColor, removeShader=True)
            wallMaterial = bpy.data.materials[materialName]

        # Read information on each cap in image
        capAngles = open("./angles/"+nameID+".txt", "r").read().splitlines()
        capPhis = open("./phis/"+nameID+".txt", "r").read().splitlines()
        capThetas = open("./thetas/"+nameID+".txt", "r").read().splitlines()

        # Creating walls
        if k == 0:
            createWall("Wall0", (2, -2, -10), (-5, -2, -10), (-5, -2, 10), (2, -2, 10), wallMaterial)
            createWall("Wall1", (2, 2, -10), (-5, 2, -10), (-5, 2, 10), (2, 2, 10), wallMaterial)
            createWall("Wall2", (-5, -2, -10), (-5, 2, -10), (-5, 2, 10), (-5, -2, 10), wallMaterial)

            # Creating and linking camera
            bpy.ops.object.camera_add(location=(3, 0, 0), rotation=(np.pi/2, 0, np.pi/2))

        # Saving masks for each cap
        for i in range(number):

            # Cap size parameter (Choose cap size between 0 and 10)
            cSize = float(capAngles[i])

            # Euler angles of the cap.
            euler = (float(capThetas[i]), float(capPhis[i]), 0)
            
            # Name the cap.
            name = "Cap" + str(i).zfill(len(str(number)))

            # Creating cap
            createCap(radius, cSize, euler, location, name, frontCapMaterial)

            # Changing camera size and activating
            bpy.data.cameras['Camera'].lens = 45
            bpy.context.scene.camera = bpy.data.objects['Camera']
            
            # Deselect all
            bpy.ops.object.select_all(action='DESELECT')

            # Setting render path
            bpy.context.scene.render.filepath = os.getcwd() + '/masks/' + nameID + "/" + name + '.png'

            # Rendering Scene
            # Get the scene
            scene = bpy.data.scenes["Scene"]

            # Set render resolution
            scene.render.resolution_x = 512
            scene.render.resolution_y = 512
            scene.render.resolution_percentage = 100
            bpy.ops.render.render(write_still = True)

            # Deselect all
            bpy.ops.object.select_all(action='DESELECT')

            # Deleting all caps
            bpy.data.objects[name].select_set(True)
            bpy.ops.object.delete()

# Creating front and back masks
if not insanceSegmentation:

    # Saving masks for each image
    for k in range(numberOfImages):

        # Deciding name of image
        nameID = str(k).zfill(len(str(numberOfImages)))

        # Number of caps to create.
        number = len(open("./angles/"+nameID+".txt", "r").read().splitlines())

        # Radius of the sphere the cap will be on.
        radius = 1

        # Location of the cap.
        location = (0, 0, 0)

        # Accessing these materials as variables
        if k == 0:
            # Cap materials
            frontCapMaterial = bpy.data.materials["frontCapMaterial"]
            backCapMaterial = bpy.data.materials["backCapMaterial"]

            # Material of wall
            materialName = "wallMaterial"
            materialColor = (0, 0, 0)
            createMaterial(materialName, materialColor, removeShader=True)
            wallMaterial = bpy.data.materials[materialName]

        # Accessing relevant cap information for each island
        capAngles = open("./angles/"+nameID+".txt", "r").read().splitlines()
        capPhis = open("./phis/"+nameID+".txt", "r").read().splitlines()
        capThetas = open("./thetas/"+nameID+".txt", "r").read().splitlines()

        # Placing individual caps
        for i in range(number):

            # Cap size parameter (Choose cap size between 0 and 10)
            cSize = float(capAngles[i])

            # Euler angles of the cap.
            euler = (float(capThetas[i]), float(capPhis[i]), 0)
            
            # Name the cap.
            name = "Cap" + str(i).zfill(len(str(number)))

            # Creating caps with different emission based on back/foreground
            if np.pi/2 <= euler[0] < 3*np.pi/2:
                createCap(radius, cSize, euler, location, name, frontCapMaterial)
            else:
                createCap(radius, cSize, euler, location, name, backCapMaterial)

        # Creating walls
        if k == 0:
            createWall("Wall0", (2, -2, -10), (-5, -2, -10), (-5, -2, 10), (2, -2, 10), wallMaterial)
            createWall("Wall1", (2, 2, -10), (-5, 2, -10), (-5, 2, 10), (2, 2, 10), wallMaterial)
            createWall("Wall2", (-5, -2, -10), (-5, 2, -10), (-5, 2, 10), (-5, -2, 10), wallMaterial)

            # Creating and linking camera
            bpy.ops.object.camera_add(location=(3, 0, 0), rotation=(np.pi/2, 0, np.pi/2))

        # Resizing and activating camera
        bpy.data.cameras['Camera'].lens = 45
        bpy.context.scene.camera = bpy.data.objects['Camera']
        
        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')

        # Setting render path
        bpy.context.scene.render.filepath = os.getcwd() + '/masks/' + nameID + '.png'

        # Rendering Scene
        # Get the scene
        scene = bpy.data.scenes["Scene"]

        # Set render resolution
        scene.render.resolution_x = 512
        scene.render.resolution_y = 512
        scene.render.resolution_percentage = 100
        bpy.ops.render.render(write_still = True)

        # Deselect all
        bpy.ops.object.select_all(action='DESELECT')

        # Deleting all caps
        for capID in range(number):
            bpy.data.objects["Cap"+str(capID).zfill(len(str(number)))].select_set(True)
            bpy.ops.object.delete()

print("")
print("Reached end of script 3. Check if correct masks were created. Thanks!")
print("")