import re
import bpy
from typing import List


def find_meshes(root_obj, pattern=None):
    return find_objs(root_obj, "MESH", pattern)


def find_objs(root_obj, obj_type=None, pattern=None):
    found = []

    def _search(obj):
        if (obj_type is None) or (obj_type is not None and obj.type == obj_type):
            name = obj.name
            if (pattern is None) or (pattern and re.search(pattern, name)):
                found.append(obj)
        for child in obj.children:
            _search(child)

    _search(root_obj)
    return found


def find_armatures(root, pattern=None):
    found = []

    def _search(obj):
        if hasattr(obj, 'type') and obj.type == 'ARMATURE':
            if (pattern is None) or (pattern is not None and re.search(pattern, obj.name)):
                found.append(obj)
        if hasattr(obj, 'children'):
            for child in obj.children:
                _search(child)
        if hasattr(obj, 'objects'):
            for obj_in_coll in obj.objects:
                _search(obj_in_coll)

    _search(root)
    return found


def find_bones(obj, pattern) -> List[bpy.types.Bone]:
    if not obj or obj.type != 'ARMATURE':
        return []

    matched = []
    for bone in obj.data.bones:
        name = bone.name
        if re.search(pattern, name):
            matched.append(bone)

    return matched


def find_parent_with_metadata(obj):
    if obj is None:
        return None
    else:
        if obj.get('ba_toolkit_metadata.json', None):
            return obj
        return find_parent_with_metadata(obj.parent)


def find_root_armature(ch_obj):
    # 1. Some good models may just contain `bone_root` as the only armature
    # 2. But some may name its armature as the character's name, so fallback method we will search all armatures.
    armatures = find_armatures(ch_obj, pattern="bone_root")
    if len(armatures) > 0:
        assert len(armatures) == 1, \
            (f"There should be exactly one armature with name pattern `bone_root` in the hierarchy. "
             f"Now we have:\n{armatures}")
        return armatures[0]
    else:
        armatures = find_armatures(ch_obj)
        if len(armatures) > 0:
            assert len(armatures) == 1, \
                f"There should be exactly one armature in the hierarchy. Now we have:\n{armatures}"
        return armatures[0]