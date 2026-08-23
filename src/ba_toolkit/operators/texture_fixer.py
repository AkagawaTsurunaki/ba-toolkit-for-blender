from pathlib import Path
import re
from typing import List

import bpy

from ..common.schema import Metadata, Texture


def _find_meshes(root_obj, pattern=None):
    found = []

    def _search(obj):
        if obj.type == 'MESH':
            name = obj.name
            if (pattern is None) or (pattern and re.search(pattern, name)):
                found.append(obj)
        for child in obj.children:
            _search(child)

    _search(root_obj)
    return found


def _setup_material(name: str, path_main: Path, path_mask: Path | None) -> bpy.types.Material | None:
    """Create a material matching the node setup: base color + optional normal map."""

    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Create core nodes
    out = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    tex_c = nodes.new("ShaderNodeTexImage")
    nmap = nodes.new("ShaderNodeNormalMap")

    # Layout
    out.location = (400, 0)
    bsdf.location = (100, 0)
    tex_c.location = (-400, 200)
    nmap.location = (-100, -250)

    # BSDF params
    bsdf.inputs["Metallic"].default_value = 1.0
    bsdf.inputs["Roughness"].default_value = 0.553
    bsdf.inputs["IOR"].default_value = 1.5

    # Base color image
    tex_c.image = bpy.data.images.load(str(path_main), check_existing=True)
    tex_c.image.colorspace_settings.name = "sRGB"
    links.new(tex_c.outputs["Color"], bsdf.inputs["Base Color"])

    # Normal map
    nmap.space = "TANGENT"
    nmap.inputs["Strength"].default_value = 1.0
    links.new(nmap.outputs["Normal"], bsdf.inputs["Normal"])

    # Optional normal map
    if path_mask:
        print(f">>>>>>>>>>>>>>>>>> {path_mask}")
        tex_n = nodes.new("ShaderNodeTexImage")
        tex_n.location = (-400, -250)
        tex_n.image = bpy.data.images.load(str(path_mask), check_existing=True)
        tex_n.image.colorspace_settings.name = "Non-Color"
        links.new(tex_n.outputs["Alpha"], bsdf.inputs["Alpha"])

    # Final link
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])

    return mat


def _get_mask_texture(textures: List[Texture], texture_main: Texture) -> Texture | None:
    ret = []
    for texture in textures:
        if texture.part == texture_main.part and texture.type is not None:
            if texture.type.lower() == "mask":
                print(f"!!!!!!!!!!!!!!!!! {texture}")
                ret.append(texture)

    if len(ret) == 1:
        return ret[0]
    else:
        return None


class TextureFixer(bpy.types.Operator):
    bl_idname = "ba_toolkit_for_blender.texture_fixer"
    bl_label = "Auto Fix Textures (EXP)"
    bl_options = {'REGISTER', 'UNDO'}
    bl_icon = 'TEXTURE'
    bl_description = 'Automatically assigns textures to the corresponding meshes of the imported model by matching texture file names.\n' \
                     'Note: This feature is experimental; it may fail or assign textures to incorrect meshes.\n' \
                     'Instructions:\n' \
                     '1. Select the imported model\'s root object in the Hierarchy panel.\n' \
                     '2. Click "Auto Fix Textures (EXP)"'

    def execute(self, context):
        ch_obj = bpy.context.active_object
        if ch_obj is None:
            return {"CANCELED"}
        metadata_json = ch_obj.get("ba_toolkit_metadata.json")
        if metadata_json is None:
            self.report(
                {"ERROR"}, "No metadata found. Are you sure this model is imported by BA Tookit?")
            return {"CANCELED"}
        metadata = Metadata.from_json(metadata_json)

        # Try assign textures to meshes
        err_info = []
        err_count, total_count = 0, 0
        for texture in metadata.animator.textures:
            tex_type, part, path = texture.type, texture.part, texture.path
            assert path.exists(), f"Texture dose not exist: {path}"
            if tex_type is None:
                meshes = _find_meshes(ch_obj, part)
                total_count += 1
                if len(meshes) == 1:
                    mesh = meshes[0]
                    ch_name = metadata.animator.ch_name
                    mat_name = f"BATK.{ch_name}.{part}.{tex_type}" if tex_type else f"BATK.{ch_name}.{part}"
                    tex_mask = _get_mask_texture(
                        metadata.animator.textures, texture)
                    mat = _setup_material(
                        mat_name, texture.path, tex_mask.path if tex_mask else None)
                    mesh.data.materials.append(mat)

                elif len(meshes) >= 1:
                    err_count += 1
                    err_info.append(f"{part}: {texture.path} -?> {meshes}")
                else:
                    err_count += 1
                    err_info.append(f'{part}: {texture.path} -x>')

        if len(err_info) > 0:
            self.report({"WARNING"}, f'Tried fixing textures but something went wrong, please fix them manually!\n'
                                     "  -?> Means there are more than 2 meshes, and we can't determine which one is correct.\n"
                                     "  -x> Means there is no mesh that matches the name pattern.\n"
                        + "\n".join(err_info)
                        + f"{total_count - err_count} textures are setup while {err_count} textures are not."
                        )

        return {"FINISHED"}
