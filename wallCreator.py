# Importing packages.
import bpy
import numpy as np
import random as r

# Importing utility python scripts.
from materialUtils import *

def createWall(objname, p1, p2, p3, p4, material):

    # Define arrays for holding data    
    myvertex = []
    myfaces = []

    # Create all Vertices

    # vertex 0
    mypoint = [p1]
    myvertex.extend(mypoint)

    # vertex 1
    mypoint = [p2]
    myvertex.extend(mypoint)

    # vertex 2
    mypoint = [p3]
    myvertex.extend(mypoint)

    # vertex 3
    mypoint = [p4]
    myvertex.extend(mypoint)

    # -------------------------------------
    # Create all Faces
    # -------------------------------------
    myface = [(0, 1, 2, 3)]
    myfaces.extend(myface)

    # Define mesh and object.
    
    mesh = bpy.data.meshes.new(objname)
    wall = bpy.data.objects.new(objname, mesh)

    # Set location, rotation and scene of object.
    
    wall.location = (0,0,0)#location
    wall.rotation_euler = (0,0,0)#euler
    bpy.context.collection.objects.link(wall)

    # Create mesh.

    mesh.from_pydata(myvertex,[],myfaces)
    mesh.update(calc_edges=True)

    # Set Material
    setMaterial(wall, material)