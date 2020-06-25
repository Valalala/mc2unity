
import bpy
import time


view_layer = bpy.context.view_layer

# bpy.ops.import_scene.obj('D:\Technic\Repositories\mc2unity\models\Suzanne.obj')
bpy.ops.import_scene.obj(filepath=r"D:\Technic\Repositories\mc2unity\models\Suzanne.obj", filter_glob="*.obj;*.mtl", use_edges=True, use_smooth_groups=True, use_split_objects=True, use_split_groups=False, use_groups_as_vgroups=False, use_image_search=True, split_mode='ON', global_clight_size=0.0, axis_forward='-Z', axis_up='Y')

current = bpy.data.objects['Suzanne']

current.select_set(True)

view_layer.objects.active = current

print(bpy.context.object)

bpy.ops.object.modifier_add(type='DECIMATE')

print(bpy.context.object)

print(bpy.context.object.modifiers['Decimate'].ratio)

bpy.context.object.modifiers['Decimate'].ratio = 0.2

print(bpy.context.object.modifiers['Decimate'].ratio)

bpy.ops.object.modifier_apply(apply_as='DATA', modifier='Decimate')

bpy.ops.export_scene.fbx(filepath=r"D:\Technic\Repositories\mc2unity\results\out.fbx", use_selection=True)



# mcWorld = input('Enter Minecraft world path: ')

# terrainTex = input('Enter Mineways terrain file path: ')

# print(mcWorld)
# print(terrainTex)



# mesh = bpy.data.meshes.new(name="MyMesh")

# print(bpy.data.objects[1].name)

# print(bpy.data.objects[1].modifier_add(type='DECIMATE'))

# print(mesh.name)


# needs to make relevant object active first.
# bpy.ops.object.modifier_add(type='SUBSURF')
# bpy.ops.object.modifier_apply(apply_as='DATA', modifier='Subsurf')
# bpy.ops.object.modifier_add(type='SUBSURF')
# bpy.context.object.modifiers['Subsurf'].levels = 2

time.sleep(2)



# mineways script template:
# Minecraft world: C:\Users\erich\AppData\Roaming\.minecraft\saves\Round World
# Terrain file name: C:\Users\erich\Desktop\Mineways\terrainExt_Sphax.png
# Selection location: 60, 0, 60 to 80, 255, 100
# Set render type: Wavefront OBJ absolute indices
# Export for Rendering: C:\Users\erich\Desktop\tile00.obj

# os.system('D:\Technic\mineways\mineways.exe -m D:\Technic\Repositories\mc2unity\learning\file.mwscript')
# subprocess.run(["D:\Technic\mineways\mineways.exe", "-m", "D:\Technic\Repositories\mc2unity\learning\file.mwscript"])



# remember blender script templates.
# http://www.realtimerendering.com/erich/minecraft/public/mineways/scripting.html
# https://docs.blender.org/api/current/bpy.ops.import_scene.html?highlight=import#module-bpy.ops.import_scene
# https://docs.blender.org/api/current/bpy.ops.export_scene.html?highlight=export#module-bpy.ops.export_scene
# https://medium.com/@behreajj/creative-coding-in-blender-a-primer-53e79ff71e


