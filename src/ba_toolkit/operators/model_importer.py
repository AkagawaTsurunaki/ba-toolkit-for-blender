import json
from pathlib import Path

import bpy  # type: ignore
from bpy.props import StringProperty  # type: ignore

from ..common.schema import Metadata
from ..common.analyzer import get_animator_schema


class ModelImporter(bpy.types.Operator):
    bl_idname = "ba_toolkit_for_blender.model_importer"
    bl_label = "Import from Folder"
    bl_options = {'REGISTER', 'UNDO'}
    bl_icon = 'IMPORT'
    bl_description = "Import model from specific folder containing FBX and texture files (.png) exported from Assets Studio.\n"\
        "For example, D:/AssetsStudioOutput/Animator/Aris_Original"
    directory: StringProperty(
        name="Model Folder",
        subtype='DIR_PATH',
        description="Select the folder containing the FBX and texture files exported from Assets Studio."
    )  # type: ignore
    METADATA_KEY = "ba-toolkit.model.metadata.json"

    def execute(self, context):
        dir = Path(str(self.directory))
        assert dir.exists()
        anim = get_animator_schema(dir=dir)

        existing_objs = set(bpy.context.scene.objects)
        # Fixed the importing issue by setting `use_image_search` to True.
        # But we find there are still some models that may lose their textures.
        # Fixed the bone orientation issue by setting `automatic_bone_orientation` to True.
        # Maybe the GUI of Blender doesn't have these options in the import dialog?
        # This `global_scale` is set to 200 because the original model is too small in Blender.
        # And this scale is also good for Minecraft based animation creation.
        try:
            bpy.ops.import_scene.fbx(filepath=str(anim.fbx_path),
                                     use_image_search=True,
                                     automatic_bone_orientation=True,
                                     global_scale=200)
        except RuntimeError as e:
            # Known issue of the exported model, we will not fix it.
            pass

        new_objs = [
            o for o in bpy.context.scene.objects if o not in existing_objs]
        top_level_objs = [o for o in new_objs if o.parent is None]
        assert len(top_level_objs) == 1
        root = top_level_objs[0]
        
        # Here change the root name
        root.name = anim.ch_name

        # Write metadata
        metadata = Metadata(animator=anim)
        metadata_json = metadata.to_json()
        root["ba_toolkit_metadata.json"] = metadata_json
        
        self.report({"INFO"}, f'Imported "{anim.ch_name}" successfully, metadata injected.')

        return {'FINISHED'}

    def invoke(self, context, event):
        self.directory = ""
        context.window_manager.fileselect_add(self)  # type: ignore
        return {'RUNNING_MODAL'}
