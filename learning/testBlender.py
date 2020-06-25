
import bpy
import time


outputFolder = r"D:\Technic\Repositories\mc2unity\results\\"

view_layer = bpy.context.view_layer

# bpy.ops.import_scene.obj('D:\Technic\Repositories\mc2unity\models\Suzanne.obj')
bpy.ops.import_scene.obj(filepath=r"D:\Technic\Repositories\mc2unity\models\Suzanne.obj", filter_glob="*.obj;*.mtl", use_edges=True, use_smooth_groups=True, use_split_objects=True, use_split_groups=False, use_groups_as_vgroups=False, use_image_search=True, split_mode='ON', global_clight_size=0.0, axis_forward='-Z', axis_up='Y')

# lod_0 = bpy.data.objects[0]
lod_0 = bpy.data.objects['Suzanne']
lod_0.name = 'Suzanne_LOD_0'

lod_0.select_set(True)
view_layer.objects.active = lod_0

# print(bpy.context.object)

for i in range(1,4):
	bpy.ops.object.duplicate()
	bpy.context.object.name = 'Suzanne_LOD_{0}'.format(i)
	# print(bpy.context.object)
	# print(lod_0.name)
	bpy.ops.object.modifier_add(type='DECIMATE')
	bpy.context.object.modifiers['Decimate'].ratio = 0.5
	bpy.ops.object.modifier_apply(apply_as='DATA', modifier='Decimate')


bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
	
	obj.select_set(True)

	# some exporters only use the active object
	view_layer.objects.active = obj

	bpy.ops.export_scene.fbx(filepath=outputFolder + obj.name + ".fbx", use_selection=True)

	print("Exporting: " + obj.name)

	obj.select_set(False)



# mcWorld = input('Enter Minecraft world path: ')

# terrainTex = input('Enter Mineways terrain file path: ')

# print(mcWorld)
# print(terrainTex)



# mesh = bpy.data.meshes.new(name="MyMesh")

# print(bpy.data.objects[1].name)

# print(bpy.data.objects[1].modifier_add(type='DECIMATE'))

# print(mesh.name)

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


