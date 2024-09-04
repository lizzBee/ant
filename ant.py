import bpy



#blindly coding an ant with bpy

"""
i need
-head
-torso(s)
-antenna
-6 legs
above rigged
above colored
-zigzag path
-2d lighting
"""


import bpy

def create_ellipsoid(center, width, length, name):
    # Add a UV Sphere (which will be scaled into an ellipsoid)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=1, location=center)
    
    # Get the active object (the one we just created)
    obj = bpy.context.active_object
    obj.name = name
    
    # Scale the object to turn the sphere into an ellipsoid
    obj.scale = (width, width, length)
    return obj

# Ellipsoid 1: Center (0,0,0), Width=1, Length=1
head = create_ellipsoid(center=(0, 0, 0), width=1, length=1, name="head")

# Ellipsoid 2: Center (2,0,0), Width=1.8, Length=0.8
torso = create_ellipsoid(center=(2, 0, 0), width=1.8, length=0.8, name="torso")

# Ellipsoid 3: Center (4,0,0), Width=1.2, Length=1.8
butt = create_ellipsoid(center=(4, 0, 0), width=1.2, length=1.8, name="butt")

def create_latex_material():
    # Create a new material
    mat = bpy.data.materials.new(name="Latex_Material")
    
    # Enable 'Use Nodes' for the material
    mat.use_nodes = True
    
    # Get the material nodes
    nodes = mat.node_tree.nodes
    
    # Clear all nodes to start fresh
    nodes.clear()
    
    # Create necessary nodes
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    principled_node = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Set the Principled BSDF shader to be black and shiny
    principled_node.inputs['Base Color'].default_value = (0, 0, 0, 1)  # Black
    principled_node.inputs['Roughness'].default_value = 0.1  # Low roughness for shiny effect
    principled_node.inputs['Metallic'].default_value = 0.8  # Some metallic to give a latex-like sheen
    
    # Connect the Principled BSDF shader to the Material Output
    mat.node_tree.links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])
    
    return mat
latex_material = create_latex_material()
object_names = ['head','torso','butt']

for obj_name in object_names:
    bpy.data.objects[obj_name].select_set(True)

# Make the first object the active objecting all objects in the scene to ens~ now only head exists
bpy.context.view_layer.objects.active = bpy.data.objects[object_names[0]]

# Join the selected objects
bpy.ops.object.join()

ant = bpy.data.objects.get('head')

ant.data.materials.append(latex_material)

def applyMirror(obj):
    #establish mirror modifier'
    mirror_modifier = obj.modifiers.new(name="Mirror", type='MIRROR')

    # Ensure that the modifier is set to mirror along the X-axis
    mirror_modifier.use_axis[0] = True  # X-axis
    mirror_modifier.use_axis[1] = False # Y-axis
    mirror_modifier.use_axis[2] = False # Z-axis

    # Apply the Mirror Modifier
    bpy.ops.object.modifier_apply(modifier="Mirror")


#delete -x half
def deleteMirrored(axis): #x...xy...z...xz....
    center = [0,0,0]
    if ('x' in axis.lower()):
        center[0] = -1
    elif ('y' in axis.lower()):
        center[1] = -1
    elif ('z' in axis.lower()):
        center[2] = -2
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.bisect(plane_co=(0, 0, 0), plane_no=tuple(center), use_fill=False, clear_outer=True)

    # Switch back to Object Mode
    bpy.ops.object.mode_set(mode='OBJECT') # idk if i need this but 

applyMirror(ant)
deleteMirrored('x')


# Create an armature
bpy.ops.object.armature_add()

# Get reference to the armature
armature = bpy.context.object

# Enter Edit Mode
bpy.ops.object.mode_set(mode='EDIT')
def addBone(head,tail):

    # Add a bone
    bone = armature.data.edit_bones.new('Bone')

    # Positioning the bone
    bone.head = head
    bone.tail = tail

    # Exit Edit Mode
    bpy.ops.object.mode_set(mode='OBJECT')

legs = [[(1,.5,.5),(1,1.5,.5)], [(2,.5,.5),(2,1.5,.5)],[(3,.5,.5),(3,1.5,.5)],
        [(1,1.5,.5),(1,3.75,.5)], [(2,1.5,.5),(2,3.75,.5)],[(3,1.5,.5),(3,3.75,.5)]]
feet = [[(1,3.5,.4),(1,1.5,.5),], [(2,3.5,.4),(2,1.5,.5),],[(3,3.5,.4),(3,1.5,.5),]]
spine = [[(1,0,.5),(2,0,.5)], [(2,0,.5),(3,0,.5)],[(3,0,.5),(4,0,.5)]]