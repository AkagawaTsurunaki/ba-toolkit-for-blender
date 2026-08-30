import bpy

from ..common.utils import find_objs, find_bones, find_root_armature


class HaloAnimBinder(bpy.types.Operator):
    bl_idname = "ba_toolkit_for_blender.halo_anim_binder"
    bl_label = "Bind Halo to Head"
    bl_options = {'REGISTER', 'UNDO'}
    bl_icon = 'ANTIALIASED'
    bl_description = "Bind halo to the head bone.\n" \
                     "Instructions:\n" \
                     "1. Select the imported model\'s root object in the Hierarchy panel.\n" \
                     '2. Click "Bind Halo to Head"\n' \

    def execute(self, context):
        ch_obj = context.active_object
        if ch_obj is None:
            self.report({"ERROR"}, "No object selected. Please select the root element of the imported model!")
            return {'CANCELLED'}

        halo_roots = find_objs(ch_obj, pattern="HaloRoot")
        assert len(halo_roots) == 1, \
            f"There should be exactly one object in the hierarchy. Now we have:\n{halo_roots}"
        halo_root = halo_roots[0]

        bone_root = find_root_armature(ch_obj)

        bones = find_bones(bone_root, pattern="Head")
        assert len(bones) == 1, \
            f'There should be exactly one bone containing "Head" in its name. Now we have:\n{armatures}'
        head_bone = bones[0]

        world_matrix = halo_root.matrix_world.copy()
        halo_root.parent = bone_root
        halo_root.parent_type = 'BONE'
        halo_root.parent_bone = head_bone.name
        halo_root.matrix_world = world_matrix

        self.report({'INFO'}, f"Bound {halo_root.name} to {head_bone.name} successfully!")

        return {"FINISHED"}
