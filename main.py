import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

BLENDER_SCRIPT = """import os
from pathlib import Path
from math import radians

ARMATURE_NAME = "person"
IMG_LOCATION = "C:/character/"

bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.select_all(action='SELECT')
if bpy.ops.object:
    bpy.ops.object.delete()
bpy.context.scene.cursor.location = (0, 0, 0)

addon_module = "io_import_images_as_planes"

addon_prefs = bpy.context.preferences.addons.get(addon_module)

if addon_prefs is None:
    print(f"{addon_module} is disabled. Enabling...")
    bpy.ops.preferences.addon_enable(module=addon_module)
else:
    print(f"{addon_module} is already enabled")

# import all the sprites in this order
parts = ["armL", "legL", "legR", "torso", "head1", "pupils", "armR"]

toggle = 0.000001
offset = 6 * toggle

sprites = []
for part in parts:
    image_path = IMG_LOCATION + part + ".png"
    filename = os.path.basename(image_path)
    directory = os.path.dirname(image_path)

    bpy.ops.import_image.to_plane(
        files=[{"name": filename}],
        directory=directory,
    )

    obj = bpy.context.active_object
    sprites.append(obj)
    obj.rotation_euler.x += radians(90)
    obj.location.y += offset
    offset -= toggle

# Select everything and set interpolation to closest
bpy.ops.object.select_all(action='SELECT')

for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        for material_slot in obj.material_slots:
            mat = material_slot.material
            if mat and mat.use_nodes:
                for node in mat.node_tree.nodes:
                    if node.type == 'TEX_IMAGE':
                        node.interpolation = 'Closest'

# Create armature
armature_data = bpy.data.armatures.new(ARMATURE_NAME)
armature_obj = bpy.data.objects.new(ARMATURE_NAME, armature_data)
bpy.context.collection.objects.link(armature_obj)
bpy.context.view_layer.objects.active = armature_obj
armature_obj.select_set(True)

# Enter Edit Mode
bpy.ops.object.mode_set(mode='EDIT')

# Add bones
edit_bones = armature_data.edit_bones

# Create bone 1
bone1 = edit_bones.new("locationBone")
bone1.head = (0.012544, offset, -0.519419)
bone1.tail = (0.012544, offset, -0.292673)
bone1.length = 0.226746

# Create bone 2
bone2 = edit_bones.new("torsoBone")
bone2.head = (0.012544, offset, -0.237189)
bone2.tail = (0.012544, offset, -0.057339)
bone2.length = 0.17985

# Create bone 3
bone3 = edit_bones.new("headBone")
bone3.head = (0.012544, offset, -0.053118)
bone3.tail = (0.012544, offset, 0.261916)
bone3.length = 0.315034

# Create bone 4
bone4 = edit_bones.new("armRBone")
bone4.head = (-0.147359, offset, -0.076756)
bone4.tail = (-0.147359, offset, -0.275432)
bone4.length = 0.198676

# Create bone 5
bone5 = edit_bones.new("armLBone")
bone5.head = (0.124558, offset, -0.076756)
bone5.tail = (0.124558, offset, -0.275432)
bone5.length = 0.198676

# Create bone 6
bone6 = edit_bones.new("legRBone")
bone6.head = (-0.094889, offset, -0.252417)
bone6.tail = (-0.094889, offset, -0.358597)
bone6.length = 0.10618

# Create bone 7
bone7 = edit_bones.new("legLBone")
bone7.head = (0.10521, offset, -0.252417)
bone7.tail = (0.10521, offset, -0.358597)
bone7.length = 0.10618

# Create bone 8
bone8 = edit_bones.new("pupilsBone")
bone8.head = (0.215264, offset, 0.159808)
bone8.tail = (0.351959, offset, 0.159808)
bone8.length = 0.136695

bone2.parent = bone1
bone3.parent = bone4.parent = bone5.parent = bone6.parent = bone7.parent = bone2
bone8.parent = bone3

# Exit Edit Mode
bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.select_all(action='DESELECT')
for obj in sprites:
    obj.select_set(True)

obj = bpy.data.objects[ARMATURE_NAME]
obj.select_set(True)

# Parent with armature (creates empty groups)
bpy.ops.object.parent_set(type='ARMATURE')

for sprite_name in parts:
    sprite_obj = bpy.data.objects[sprite_name]
    if sprite_name == "head1":
        bone_name = "headBone"
    else:
        bone_name = sprite_name + "Bone"

        # Get the sprite's mesh data
    mesh = sprite_obj.data

    # Create vertex group for this bone
    vgroup = sprite_obj.vertex_groups.new(name=bone_name)

    # Assign ALL vertices to this group with weight 1.0
    for vertex in mesh.vertices:
        vgroup.add([vertex.index], 1.0, 'REPLACE')

bpy.ops.object.select_all(action='DESELECT')

obj = bpy.data.objects[ARMATURE_NAME]

for bone_name in ["torsoBone", "headBone"]:
    pose_bone = obj.pose.bones[bone_name]
    pose_bone.lock_rotation[0] = pose_bone.lock_rotation[1] = True  # Lock X and Y axis

for bone_name in ["headBone", "armLBone", "armRBone", "legLBone", "legRBone"]:
    pose_bone = obj.pose.bones[bone_name]
    pose_bone.lock_rotation[0] = pose_bone.lock_rotation[1] = True  # Lock X and Y axis"""
BLENDER_SCRIPT2 = """
import os
from pathlib import Path
from math import radians


ARMATURE_NAME = "person"
IMG_LOCATION = "C:/character/"

bpy.ops.object.mode_set(mode='OBJECT')


bpy.ops.object.select_all(action='SELECT')
if bpy.ops.object:
    bpy.ops.object.delete()
bpy.context.scene.cursor.location = (0, 0, 0)

addon_module = "io_import_images_as_planes"

addon_prefs = bpy.context.preferences.addons.get(addon_module)

if addon_prefs is None:
    print(f"{addon_module} is disabled. Enabling...")
    bpy.ops.preferences.addon_enable(module=addon_module)
else:
    print(f"{addon_module} is already enabled")


# import all the sprites in this order
parts = ["armL", "legL", "legR", "torso", "head1", "pupils", "eyelids", "armR"]

toggle = 0.00001
offset = 6 * toggle

sprites = []
for part in parts:
    image_path = IMG_LOCATION + part + ".png"
    filename = os.path.basename(image_path)
    directory = os.path.dirname(image_path)

    bpy.ops.import_image.to_plane(
        files=[{"name": filename}],
        directory=directory,
    )
    
    obj = bpy.context.active_object
    sprites.append(obj)
    obj.rotation_euler.x += radians(90)
    obj.location.y += offset
    offset -= toggle


# Select everything and set interpolation to closest
bpy.ops.object.select_all(action='SELECT')

for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        for material_slot in obj.material_slots:
            mat = material_slot.material
            if mat and mat.use_nodes:
                for node in mat.node_tree.nodes:
                    if node.type == 'TEX_IMAGE':
                        node.interpolation = 'Closest'


# Create armature
armature_data = bpy.data.armatures.new(ARMATURE_NAME)
armature_obj = bpy.data.objects.new(ARMATURE_NAME, armature_data)
bpy.context.collection.objects.link(armature_obj)
bpy.context.view_layer.objects.active = armature_obj
armature_obj.select_set(True)

# Enter Edit Mode
bpy.ops.object.mode_set(mode='EDIT')

# Add bones
edit_bones = armature_data.edit_bones

# Create bone 1
bone1 = edit_bones.new("locationBone")
bone1.head = (0.012544, offset, -0.519419)
bone1.tail = (0.012544, offset, -0.292673)
bone1.length = 0.226746


# Create bone 2
bone2 = edit_bones.new("torsoBone")
bone2.head = (0.012544, offset, -0.237189)
bone2.tail = (0.012544, offset, -0.057339)
bone2.length = 0.17985

# Create bone 3
bone3 = edit_bones.new("headBone")
bone3.head = (0.012544, offset, -0.053118)
bone3.tail = (0.012544, offset, 0.261916)
bone3.length = 0.315034

# Create bone 4
bone4 = edit_bones.new("armRBone")
bone4.head = (-0.147359, offset, -0.076756)
bone4.tail = (-0.147359, offset, -0.275432)
bone4.length = 0.198676

# Create bone 5
bone5 = edit_bones.new("armLBone")
bone5.head = (0.124558, offset, -0.076756)
bone5.tail = (0.124558, offset, -0.275432)
bone5.length = 0.198676

# Create bone 6
bone6 = edit_bones.new("legRBone")
bone6.head = (-0.094889, offset, -0.252417)
bone6.tail = (-0.094889, offset, -0.358597)
bone6.length = 0.10618

# Create bone 7
bone7 = edit_bones.new("legLBone")
bone7.head = (0.10521, offset, -0.252417)
bone7.tail = (0.10521, offset, -0.358597)
bone7.length = 0.10618

# Create bone 8
bone8 = edit_bones.new("pupilsBone")
bone8.head = (0.215264, offset, 0.159808)
bone8.tail = (0.351959, offset, 0.159808)
bone8.length = 0.136695


# Create bone 9
bone9 = edit_bones.new("eyelidsBone")
bone9.head = (0.059566, offset, 0.194875)
bone9.tail = (0.059566, offset, 0.33157)
bone9.length = 0.136695



bone2.parent = bone1
bone3.parent = bone4.parent = bone5.parent = bone6.parent = bone7.parent = bone2
bone8.parent = bone9.parent = bone3

# Exit Edit Mode
bpy.ops.object.mode_set(mode='OBJECT')

bpy.ops.object.select_all(action='DESELECT')
for obj in sprites:
    obj.select_set(True)

obj = bpy.data.objects[ARMATURE_NAME]
obj.select_set(True)

# Parent with armature (creates empty groups)
bpy.ops.object.parent_set(type='ARMATURE')

for sprite_name in parts:
    sprite_obj = bpy.data.objects[sprite_name]
    if sprite_name == "head1":
        bone_name = "headBone"
    else:
        bone_name = sprite_name + "Bone" 
    
    # Get the sprite's mesh data
    mesh = sprite_obj.data
    
    # Create vertex group for this bone
    vgroup = sprite_obj.vertex_groups.new(name=bone_name)
    
    # Assign ALL vertices to this group with weight 1.0
    for vertex in mesh.vertices:
        vgroup.add([vertex.index], 1.0, 'REPLACE')


bpy.ops.object.select_all(action='DESELECT')


obj = bpy.data.objects[ARMATURE_NAME]

for bone_name in ["torsoBone", "headBone"]:
    pose_bone = obj.pose.bones[bone_name]
    pose_bone.lock_rotation[0] = pose_bone.lock_rotation[1] = True   # Lock X and Y axis

for bone_name in ["headBone", "armLBone", "armRBone", "legLBone", "legRBone"]:
    pose_bone = obj.pose.bones[bone_name]
    pose_bone.lock_rotation[0] = pose_bone.lock_rotation[1] = True   # Lock X and Y axis"""

root = tk.Tk()
root.title("Armature Builder")
root.geometry("400x550")

# Blender path input
tk.Label(root, text="Blender Path:").pack(pady=5)
blender_path_var = tk.StringVar(value="C:/Program Files/Blender Foundation/Blender 3.6/blender.exe")
tk.Entry(root, textvariable=blender_path_var, width=40).pack(pady=5)
tk.Button(root, text="Browse",
          command=lambda: blender_path_var.set(
              filedialog.askopenfilename(
                  filetypes=[("Executable files", "*.exe"), ("All files", "*.*")],
                  title="Select Blender executable"
              )
          )).pack()

# Folder input
tk.Label(root, text="Folder:").pack(pady=5)
folder_var = tk.StringVar()
tk.Entry(root, textvariable=folder_var, width=40).pack(pady=5)
tk.Button(root, text="Browse", command=lambda: folder_var.set(filedialog.askdirectory())).pack()

# Parameter selection
tk.Label(root, text="Parameter:", font=("Arial", 10, "bold")).pack(pady=(20, 10))

param_var = tk.StringVar(value="Mode 1")

# Define requirements for each mode
mode_requirements = {
    "Mode 1": ["head1.png", "pupils.png", "torso.png", "armL.png", "armR.png", "legL.png", "legR.png"],
    "Mode 2": ["head1.png", "eyelids.png", "pupils.png", "torso.png", "armL.png", "armR.png", "legL.png", "legR.png"],
}


def select_param(param):
    param_var.set(param)
    update_colors()
    update_requirements()


def update_colors():
    if param_var.get() == "Mode 1":
        btn1.config(bg="blue", fg="white")
        btn2.config(bg="gray", fg="black")
    else:
        btn1.config(bg="gray", fg="black")
        btn2.config(bg="blue", fg="white")


def update_requirements():
    mode = param_var.get()
    requirements = mode_requirements.get(mode, [])
    requirements_text = ", ".join(requirements)
    requirements_label.config(text=requirements_text)


btn1 = tk.Button(root, text="Mode 1", width=20, height=2,
                 command=lambda: select_param("Mode 1"))
btn1.pack(pady=5)

btn2 = tk.Button(root, text="Mode 2 (Demo)", width=20, height=2,
                 command=lambda: select_param("Mode 2"))
btn2.pack(pady=5)

update_colors()

# Requirements section
tk.Label(root, text="Requires folder to have:", font=("Arial", 10, "bold")).pack(pady=(20, 10))
requirements_label = tk.Label(root, text="", wraplength=350, justify=tk.LEFT, fg="darkblue")
requirements_label.pack(pady=(5, 10))

update_requirements()


def execute_blender(blender_path, folder_path):
    """Opens Blender, executes bpy code, saves project"""

    folder = Path(folder_path)
    blend_file = folder / "project.blend"

    script = f"""
import bpy

{BLENDER_SCRIPT if param_var.get() == "Mode 1" else BLENDER_SCRIPT2}

bpy.ops.wm.save_mainfile(filepath=r"{blend_file}")
print("Project saved: {blend_file}")
"""

    temp_script = folder / "temp_exec.py"
    with open(temp_script, 'w') as f:
        f.write(script)

    subprocess.run([
        blender_path,
        "--python", str(temp_script),
        "--background"
    ])

    temp_script.unlink()


# Run button
def run():
    blender_path = blender_path_var.get()
    folder = folder_var.get()
    param = param_var.get()

    if not blender_path:
        messagebox.showerror("Error", "Select Blender executable!")
        return

    if not folder:
        messagebox.showerror("Error", "Select a folder!")
        return

    try:
        execute_blender(blender_path, folder, )
        messagebox.showinfo("Success", "Project created!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to execute: {str(e)}")


tk.Button(root, text="RUN", width=20, height=2, bg="green", fg="white",
          command=run).pack(pady=20)

root.mainloop()
