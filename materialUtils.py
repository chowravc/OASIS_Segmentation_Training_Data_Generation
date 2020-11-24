import bpy
from bpy_extras.node_shader_utils import PrincipledBSDFWrapper
from bpy_extras.image_utils import load_image

def setMaterial(ob, mat, debug=False):
    if ob.data.materials:
        # assign to 1st material slot
        ob.data.materials[0] = mat
        if debug:
            print("Set material for",ob.name)
    else:
        # no slots
        ob.data.materials.append(mat)
        print("Did not find material slot on", ob.name)

def createMaterial(name, baseColor, removeShader=False):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    principled = PrincipledBSDFWrapper(mat, is_readonly=False)
    principled.base_color = baseColor
    # principled.specular_texture.image = load_image("/path/to/image.png")

    # Export
    principled = PrincipledBSDFWrapper(mat, is_readonly=True)
    base_color = principled.base_color
    specular_texture = principled.specular_texture
    if specular_texture and specular_texture.image:
        specular_texture_filepath = principled.specular_texture.image.filepath
    if removeShader:
        #Get the node in its node tree (replace the name below)
        node_to_delete =  mat.node_tree.nodes['Principled BSDF']
        #Remove it
        mat.node_tree.nodes.remove(node_to_delete)

def createBubbleMaterial(name, baseColor):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.blend_method = 'BLEND'
    principled = PrincipledBSDFWrapper(mat, is_readonly=False)
    principled.base_color = baseColor
    principled.metallic = 0.5
    principled.specular = 0.2
    principled.roughness = 0.05
    #principled.IOR = 1.1
    principled.alpha = 0.3
    # principled.specular_texture.image = load_image("/path/to/image.png")

    # Export
    principled = PrincipledBSDFWrapper(mat, is_readonly=True)
    base_color = principled.base_color
    specular_texture = principled.specular_texture
    if specular_texture and specular_texture.image:
        specular_texture_filepath = principled.specular_texture.image.filepath

if __name__ == "__main__":
    
    ob1 = bpy.data.objects[1]
    mat1 = bpy.data.materials.get("Material")
    
    setMaterial(ob1, mat1, True)