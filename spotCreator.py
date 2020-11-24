# Importing packages.
import bpy
import bmesh
import numpy as np
import random as r

# Importing utility python scripts.
from materialUtils import *


# Creates a cap with the following properties.
def createSpot(radius, spotRadius, material):

    # Create an empty mesh and the object.
    mesh = bpy.data.meshes.new('Spot0')
    basic_sphere = bpy.data.objects.new("Spot0", mesh)

    # Add the object into the scene.
    bpy.context.collection.objects.link(basic_sphere)

    # Select the newly created object
    bpy.context.view_layer.objects.active = basic_sphere
    basic_sphere.select_set(True)

    # Construct the bmesh sphere and assign it to the blender mesh.
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, diameter=1*spotRadius)
    bm.to_mesh(mesh)
    bm.free()

    basic_sphere.location = (radius*1.2, 0, 0)

    basic_sphere.modifiers.new("subd", type='SUBSURF')
    basic_sphere.modifiers['subd'].levels = 3
    basic_sphere.modifiers['subd'].render_levels = 4

    bpy.ops.object.shade_smooth()

    # Set Material
    setMaterial(basic_sphere, material)