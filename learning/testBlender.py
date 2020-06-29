# testBlender.py
# Walter Rasmussen
# Testing code for a project that converts Minecraft worlds to Unity.

import bpy
import bmesh
import time



###### Alpha ######
# Only useful when viewing the file in blender.
def fixAlpha():
# Note: mineways has a blender script, details texture and material import.

	for name in [s.lower() for s in transparentBlocks]:
		if name not in bpy.data.materials.keys():
			continue
		# print(name)

		bpy.data.materials[name].blend_method = 'BLEND'
		bpy.data.materials[name].shadow_method = 'HASHED'
		socket_in = bpy.data.materials[name].node_tree.nodes['Principled BSDF'].inputs['Alpha']
		socket_out = bpy.data.materials[name].node_tree.nodes['Image Texture'].outputs['Alpha']
		bpy.data.materials[name].node_tree.links.new(socket_in, socket_out)

		# mat = bpy.data.materials[name]
		# mat.blend_method = 'BLEND'
		# mat.shadow_method = 'HASHED'
		# socket_in = mat.node_tree.nodes['Principled BSDF'].inputs['Alpha']
		# socket_out = mat.node_tree.nodes['Image Texture'].outputs['Alpha']
		# mat.node_tree.links.new(socket_in, socket_out)
	

###### UV edit ######
def fixUVs():

	# Get the active mesh
	me = bpy.context.object.data

	# Cube projection
	bpy.ops.object.mode_set(mode = 'EDIT')
	bpy.ops.mesh.select_all(action='SELECT')
	bpy.ops.mesh.dissolve_limited()
	bpy.ops.uv.cube_project(cube_size=2, correct_aspect=False)
	bpy.ops.object.mode_set(mode = 'OBJECT')

	# Get a BMesh representation
	bm = bmesh.new()   # create an empty BMesh
	bm.from_mesh(me)   # fill it in from a Mesh

	uv_layer = bm.loops.layers.uv.verify()

	bm.faces.ensure_lookup_table()
	uv_offset = bm.faces[0].loops[0][uv_layer].uv.xy

	for f in bm.faces:
		# Offset must be per face because cube projection can give non whole number values
		uv_offset.x = f.loops[0][uv_layer].uv.x - round(f.loops[0][uv_layer].uv.x)
		uv_offset.y = f.loops[0][uv_layer].uv.y - round(f.loops[0][uv_layer].uv.y)
		for loop in f.loops:
			loop_uv = loop[uv_layer]
			# align to zero
			loop_uv.uv = loop_uv.uv + uv_offset
			if(f.normal.x == 1 or f.normal.x == -1):
				# 90 deg turn then mirror
				loop_uv.uv = (loop_uv.uv.y, loop_uv.uv.x)
			if(f.normal.y == 1 or f.normal.y == -1):
				# virtical flip
				loop_uv.uv = (-loop_uv.uv.x, loop_uv.uv.y)


	# Finish up, write the bmesh back to the mesh
	bm.to_mesh(me)
	bm.free()  # free and prevent further access




###### Setup ######
# disolveMaterials = {'oak_leaves', 'birch_leaves', 'water_still'}
# transparentMaterials = {'water_still'}
# cutoutMaterials = {'grass', 'oak_leaves', 'birch_leaves', 'dandelion', 'poppy', 'sugar_cane'}

# Use Mineway's [block test world] to check/complete the list
#List of transparent blocks
transparentBlocks = ["Acacia_Leaves","Dark_Oak_Leaves","Acacia_Door","Activator_Rail","Bed","Beetroot_Seeds","Birch_Door","Brewing_Stand","Cactus","Carrot","Carrots","Cauldron","Chorus_Flower","Chorus_Flower_Dead","Chorus_Plant","Cobweb",
    "Cocoa","Crops","Dandelion","Dark_Oak_Door","Dead_Bush","Detector_Rail","Enchantment_Table","Glass","Glass_Pane","Grass","Iron_Bars","Iron_Door","Iron_Trapdoor","Jack_o'Lantern","Jungle_Door","Large_Flowers",
    "Leaves","Melon_Stem","Monster_Spawner","Nether_Portal","Nether_Wart","Oak_Leaves","Oak_Sapling","Poppy","Potato","Potatoes","Powered_Rail","Pumpkin_Stem","Rail","Red_Mushroom",
    "Redstone_Comparator_(inactive)","Redstone_Torch_(inactive)","Repeater_(inactive)","Sapling","Spruce_Door","Stained_Glass_Pane","Sugar_Cane","Sunflower","Tall_Grass","Trapdoor","Vines","Wheat","Wooden_Door"]
#List of light emitting blocks
lightBlocks = ["Daylight_Sensor","End_Gateway","End_Portal","Ender_Chest","Flowing_Lava","Glowstone","Inverted_Daylight_Sensor","Lava","Magma_Block","Redstone_Lamp_(active)","Stationary_Lava","Sea_Lantern"]
#List of light emitting and transparent block
lightTransparentBlocks = ["Beacon","Brown_Mushroom","Dragon_Egg","Endframe","End_Rod","Fire","Powered_Rail_(active)","Redstone_Comparator_(active)","Redstone_Torch_(active)","Repeater_(active)","Torch"]


outputFolder = r"D:\Technic\Repositories\mc2unity\results\\"

view_layer = bpy.context.view_layer


###### Import ######
# bpy.ops.import_scene.obj('D:\Technic\Repositories\mc2unity\models\Suzanne.obj')
bpy.ops.import_scene.obj(filepath=r"D:\Technic\Repositories\mc2unity\models\skylands.obj", filter_glob="*.obj;*.mtl", use_edges=True, use_smooth_groups=True, use_split_objects=True, use_split_groups=False, use_groups_as_vgroups=False, use_image_search=True, split_mode='ON', global_clight_size=0.0, axis_forward='-Z', axis_up='Y')

lod_0 = bpy.data.objects[0]
# lod_0 = bpy.data.objects['Suzanne']
# lod_0.name = 'Suzanne_LOD_0'

lod_0.select_set(True)
view_layer.objects.active = lod_0



###### MAIN ######

# fixAlpha()

bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.remove_doubles()
bpy.ops.mesh.separate(type='MATERIAL')
bpy.ops.object.mode_set(mode = 'OBJECT')

bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
	obj.select_set(True)
	view_layer.objects.active = obj
	# Should only occur for full blocks
	fixUVs()
	obj.select_set(False)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.join()
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.remove_doubles()
bpy.ops.object.mode_set(mode = 'OBJECT')
bpy.ops.export_scene.fbx(filepath=outputFolder + "test" + ".fbx", use_selection=True)
# bpy.ops.wm.save_mainfile()


# for i in range(1,4):
# 	bpy.ops.object.duplicate()
# 	bpy.context.object.name = 'Suzanne_LOD_{0}'.format(i)
# 	# print(bpy.context.object)
# 	# print(lod_0.name)
# 	bpy.ops.object.modifier_add(type='DECIMATE')
# 	bpy.context.object.modifiers['Decimate'].ratio = 0.5
# 	bpy.ops.object.modifier_apply(apply_as='DATA', modifier='Decimate')


# bpy.ops.object.select_all(action='DESELECT')
# for obj in bpy.data.objects:
	
# 	obj.select_set(True)

# 	# some exporters only use the active object
# 	view_layer.objects.active = obj

# 	bpy.ops.export_scene.fbx(filepath=outputFolder + obj.name + ".fbx", use_selection=True)

# 	print("Exporting: " + obj.name)

# 	obj.select_set(False)



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
# https://docs.blender.org/api/2.82/bmesh.html
# https://medium.com/@behreajj/creative-coding-in-blender-a-primer-53e79ff71e


