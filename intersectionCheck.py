import bpy
import numpy as np
from mathutils.bvhtree import BVHTree

def physIntersection(name1, name2):
	# Get the objects
	obj1 = bpy.data.objects[name1]
	obj2 = bpy.data.objects[name2]

	# Get their world matrix
	mat1 = obj1.matrix_world
	mat2 = obj2.matrix_world

	# Get the geometry in world coordinates
	vert1 = [mat1 @ v.co for v in obj1.data.vertices] 
	poly1 = [p.vertices for p in obj1.data.polygons]

	vert2 = [mat2 @ v.co for v in obj2.data.vertices] 
	poly2 = [p.vertices for p in obj2.data.polygons]

	# Create the BVH trees
	bvh1 = BVHTree.FromPolygons(vert1, poly1)
	bvh2 = BVHTree.FromPolygons(vert2, poly2)

	# Test if overlap
	if bvh1.overlap(bvh2):
	    return True
	else:
		return False

def angleIntersection(a1, a2, phi1, phi2, theta1, theta2):
	psi = np.arccos(np.sin(theta1)*np.sin(theta2)+np.cos(theta1)*np.cos(theta2)*np.cos(phi1-phi2))
	if psi < a1 + a2:
		return True
	else:
		return False

def capIntersection(a1, p1, t1, aList, pList, tList):
	for j in range(len(aList)):
		if angleIntersection(a1, np.pi/75 + (aList[j]/10)*(np.pi/4 - np.pi/75), p1, pList[j], t1, tList[j]):
			return True
	return False

def capIntersectionPhys(i):
	name1 = "Cap" + str(i)
	for j in range(i):
		name2 = "Cap" + str(j)
		if angleIntersection(name1, name2):
			return True
	return False