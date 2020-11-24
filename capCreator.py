# Importing packages.
import bpy
import numpy as np
import random as r

# Importing utility python scripts.
from materialUtils import *


# Creates a cap with the following properties.
def createCap(radius, cSize, euler, location, name, material):
    
    # Number of corners the cap will have on the xy plane.
    corners = 6 + int((cSize/10)*(16 - 6))

    # Number of layers being stacked in the z direction.
    layers = 2 + int((cSize/10)*(10 - 2))

    # Angular size of the cap.
    angle = np.pi/75 + (cSize/10)*(np.pi/4 - np.pi/75)
    
    # Stores the vertices and faces respectively.
    
    verts = []
    faces = []

    # Creates lists of angles in latitude and longitude.
    
    u = np.linspace(0, 2*np.pi, corners + 1)
    h = np.linspace(np.pi/2 - angle, np.pi/2, layers + 1)

    # Uses the lists of angles to make vertices.

    for phi in h:
        for theta in u:
            x = radius*np.cos(theta)*np.cos(phi)
            y = radius*np.sin(theta)*np.cos(phi)
            z = radius*np.sin(phi)

            vert = (x,y,z)
            verts.append(vert)

    # Creates faces from the vertices.
    
    for j in range(layers):
        for i in range(1, corners + 1):
            
            a = i + j*(corners+1)
            b = (i%corners) + 1 + j*(corners+1)
            c = (i%corners) + 1 + (j+1)*(corners+1)
            d = i + (j+1)*(corners+1)

            face = (a, b, c, d)
            faces.append(face)

    # Define mesh and object.
    
    mesh = bpy.data.meshes.new(name)
    cap = bpy.data.objects.new(name, mesh)

    # Set location, rotation and scene of object.
    
    cap.location = location
    cap.rotation_euler = euler
    bpy.context.collection.objects.link(cap)

    # Create mesh.

    mesh.from_pydata(verts,[],faces)
    mesh.update(calc_edges=True)
    
    # subdivide modifier
    
    cap.modifiers.new("subd", type='SUBSURF')
    cap.modifiers['subd'].levels = 3
    cap.modifiers['subd'].render_levels = 4

    # Set Material
    setMaterial(cap, material)
    
if __name__ == "__main__":
    
    # Radius of the sphere the cap will be on.
    radius = 1
    # Location of the cap.
    location = (0, 0, 0)
    # Cap size parameter (Choose cap size between 0 and 10)
    cSize = 4
    # Euler angles of the cap.
    euler = (r.random()*2*np.pi, r.random()*np.pi, 0)
    # Name the cap.
    name = "Cap"
    # Material to apply
    material = None
    
    createCap(radius, cSize, euler, location, name, material)