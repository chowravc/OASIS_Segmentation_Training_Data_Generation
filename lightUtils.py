import bpy

def customLight(lightNumber, lLocation, lRotation, lightType, energy, size):
	bpy.ops.object.light_add(location=lLocation, rotation=lRotation)
	bpy.data.lights[lightNumber].type = lightType
	if lightType == 'AREA':
		bpy.data.lights[lightNumber].shape = 'DISK'
		bpy.data.lights[lightNumber].size = size
	bpy.data.lights[lightNumber].energy = energy
	bpy.data.lights[lightNumber].name = 'Light'+str(lightNumber)