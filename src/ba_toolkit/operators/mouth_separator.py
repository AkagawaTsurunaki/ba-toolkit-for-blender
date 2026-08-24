from mathutils.bvhtree import BVHTree
from mathutils import Vector


import bpy
import bmesh
from ..common.utils import find_meshes, find_armatures, find_bones


def _get_bone_world_pos(armature_obj, bone, use_head=True):
    local_pos = bone.head_local if use_head else bone.tail_local
    return armature_obj.matrix_world @ local_pos


def _raycast_against_mesh(mesh_obj, origin_world, direction_world, max_dist=10.0):
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = mesh_obj.evaluated_get(depsgraph)

    bvh = BVHTree.FromObject(eval_obj, depsgraph)  # type: ignore

    to_local = mesh_obj.matrix_world.inverted()
    origin_local = to_local @ origin_world
    direction_local = (to_local.to_3x3() @ direction_world).normalized()

    loc, normal, idx, dist = bvh.ray_cast(
        origin_local, direction_local, max_dist)

    if loc is None:
        return None, None, None, None

    hit_world = mesh_obj.matrix_world @ loc
    normal_world = (mesh_obj.matrix_world.to_3x3() @ normal).normalized()

    return hit_world, normal_world, idx, dist


class MouthSeparator(bpy.types.Operator):
    bl_idname = "ba_toolkit_for_blender.mouth_separator"
    bl_label = "Auto Separate Mouth"
    bl_options = {'REGISTER', 'UNDO'}
    bl_icon = 'MESH_MONKEY'
    bl_description = "Automatically separate the mouth area of the selected character model as a new mesh object. \n" \
                     "Raycast based algorithm is used and may not be successful for all models. \n" \
                     "Instructions:\n" \
                     "1. Select the imported model\'s root object in the Hierarchy panel.\n" \
                     '2. Click "Auto Separate Mouth".\n' \
                     "If it fails, try separating the mouth area manually:\n" \
                     "1. Select the mouth faces in Edit Mode.\n" \
                     "2. Press L to link faces.\n" \
                     "3. Press Alt+M to split the linked faces.\n" \
                     "4. Press P to separate the selected faces as a new mesh object"

    def execute(self, context):
        # @AUTHOR AkagawaTsurunaki
        # Almost all the character models have a head bone,
        # and the head bone is just behind the mouth area.
        #
        # Raycast mouth separation algorithm
        # 1. We search for the armature (should be only one) of the imported character model .
        # 2. And get the position of the head bone (should be only one) of the armature.
        # 3. Then we cast a ray from the head bone position in the forward direction (Y axis)
        #    to find the mouth area on the mesh.
        #    We try to find the mouth area by raycasting in 2 modes:
        #    3.a Outside the head
        #    3.b Inside the head
        # 4. Link, split and separate the selected faces as a MOUTH mesh.

        ch_obj = bpy.context.active_object
        armatures = find_armatures(ch_obj)
        assert len(armatures) == 1, \
            f"There should be exactly one armature in the hierarchy. Now we have:\n{armatures}"
        armature = armatures[0]
        head_bones = find_bones(armature, "Head")

        assert len(head_bones) == 1, \
            f'There should be exactly one bone containing "Head" in the name. Now we have:\n{head_bones}'
        head_bone = head_bones[0]

        # Get head bone origin position in world space
        origin = _get_bone_world_pos(armature, head_bone, use_head=True)
        direction = Vector((0, 1, 0))

        # Find the mesh whose name contains "Body", e.g., "Midori_Original_Body".
        # Assumes only one such mesh exists.
        meshes = find_meshes(ch_obj, pattern="Body")
        assert len(meshes) == 1, \
            f'There should be exactly one mesh containing "Head" in the name. Now we have:\n{meshes}'
        mesh = meshes[0]

        # Raycast in 2 modes
        ray_origin = origin - direction * 10.0
        hit, normal, face_idx, dist = _raycast_against_mesh(
            mesh, ray_origin, direction)
        if not hit:
            hit, normal, face_idx, dist = _raycast_against_mesh(
                mesh, origin, -direction)

        if not hit:
            self.report({'ERROR'}, "Raycast did not hit any face. Try separating mouth faces manually.")
            return {'CANCELLED'}

        # Separate the selected faces as a new mesh object
        context.view_layer.objects.active = mesh  # type: ignore
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='FACE')
        bpy.ops.mesh.select_all(action='DESELECT')

        # Why?
        # Use the hit position to find the closest face in the original mesh
        # To avoid index mismatch with the evaluated mesh which may have modifiers.
        bm = bmesh.from_edit_mesh(mesh.data)
        bm.faces.ensure_lookup_table()

        hit_local = mesh.matrix_world.inverted() @ hit
        target_face = min(bm.faces, key=lambda f: (
                f.calc_center_median() - hit_local).length)
        target_face.select = True
        bmesh.update_edit_mesh(mesh.data)

        # Link, split and separate the selected faces
        bpy.ops.mesh.select_linked()
        selected_count = sum(1 for f in bm.faces if f.select)
        self.report({'INFO'}, f"{selected_count} faces selected.")

        bpy.ops.mesh.split()
        bpy.ops.mesh.separate(type='SELECTED')
        bpy.ops.object.mode_set(mode='OBJECT')

        # Rename the new mesh as *_Mouth
        for obj in context.selected_objects:  # type: ignore
            if obj != mesh and obj.type == 'MESH':
                obj.name = f"{mesh.name}_Mouth"
                break

        self.report({'INFO'}, f"Separated mouth mesh from {mesh} successfully. "
                              f"Check it if it is correct. If not, try separating mouth faces manually.")
        return {'FINISHED'}
