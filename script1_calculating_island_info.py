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

# Delete files before running
if not os.path.isfile(os.getcwd() + '/angles/'):
    os.mkdir(os.getcwd() + '/angles/')
if not os.path.isfile(os.getcwd() + '/phis/'):
    os.mkdir(os.getcwd() + '/phis/')
if not os.path.isfile(os.getcwd() + '/thetas/'):
    os.mkdir(os.getcwd() + '/thetas/')

# Choose Number of 'images' to generate
numberOfImages = 5

# Choose minimum and maximum islands per image
minimumIslands = 50
maximumIslands = 100

# Choose minimum and maximum island size (anything between 0 and 10)
minimumSize = 0
maximumSize = 2

# If you have already run this stopped after some images were created, this will choose where to continue
startNum = len(g.glob("./thetas/*"))

for k in range(startNum, numberOfImages):

    # Generating name of 'image'
    nameID = str(k).zfill(len(str(numberOfImages)))

    # Number of random caps to create.
    number = minimumIslands + int((maximumIslands - minimumIslands)*r.random())

    # Store current island data here
    capAngles = []
    capPhis = []
    capThetas = []

    # Defining each cap
    for i in range(number):
        created = False
        intersecting = True

        # Keep calculating until it doesn't intersect
        while intersecting:

            # Cap size parameter (Choose cap size between 0 and 10)
            cSize = minimumSize + (maximumSize - minimumSize)*r.random()

            # Euler angles of the cap.
            euler = (r.random()*2*np.pi, r.random()*np.pi, 0)

            # If the first island, you don't need to check intersection
            if i > 0:
                intersecting = capIntersection(np.pi/75 + (cSize/10)*(np.pi/4 - np.pi/75), euler[1], euler[0], capAngles, capPhis, capThetas)
            else:
                intersecting = False

        # Storing cap size and euler angles
        capAngles.append(cSize)
        capPhis.append(euler[1])
        capThetas.append(euler[0])

    # Saving cap properties as list in text files
    print("number of caps:",len(capAngles))
    with open(os.getcwd() + '/angles/' + nameID + '.txt', 'w') as f:
        for item in capAngles:
            f.write("%s\n" % item)
    f.close()

    with open(os.getcwd() + '/phis/' + nameID + '.txt', 'w') as f:
        for item in capPhis:
            f.write("%s\n" % item)
    f.close()

    with open(os.getcwd() + '/thetas/' + nameID + '.txt', 'w') as f:
        for item in capThetas:
            f.write("%s\n" % item)
    f.close()

print("")
print("Reached end of script 1.")
print("Ensure all files are created correctly and no objects exist in Blender file.")
print("Run script 2 now.")
print("")