from pathlib import Path

import bpy  # type: ignore
from bpy.props import StringProperty  # type: ignore
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

    def execute(self, context):
        dir = Path(str(self.directory))
        assert dir.exists()
        anim = get_animator_schema(dir=dir)

        # Fixed the importing issue by setting `use_image_search` to True.
        # But we find there are still some models that may lose their textures.
        # Fixed the bone orientation issue by setting `automatic_bone_orientation` to True.
        # Maybe the GUI of Blender doesn't have these options in the import dialog?
        # This `global_scale` is set to 200 because the original model is too small in Blender.
        # And this scale is also good for Minecraft based animation creation.
        bpy.ops.import_scene.fbx(filepath=str(anim.fbx_path),
                                 use_image_search=True,
                                 automatic_bone_orientation=True,
                                 global_scale=200)
        print(anim)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.directory = ""
        context.window_manager.fileselect_add(self)  # type: ignore
        return {'RUNNING_MODAL'}
