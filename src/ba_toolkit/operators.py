from pathlib import Path

import bpy
from bpy.props import StringProperty
from .schema import Animator, Texture
from .analyzer import get_original_animator


class AnimatorImporter(bpy.types.Operator):
    bl_idname = "ba_toolkit_for_blender.import_from_animator_folder"
    bl_label = "Import from Animator Folder (Original)"
    bl_options = {'REGISTER', 'UNDO'}
    directory: StringProperty(
        name="Animator Folder",
        subtype='DIR_PATH',
        description="Select the folder containing the animator files (FBX and textures) exported from Assets Studio.\n"
        'For example, D:/AssetsStudioOutput/Animator/Aris_Original'
    )  # type: ignore

    def execute(self, context):
        dir = Path(str(self.directory))
        assert dir.exists()
        anim = get_original_animator(dir=dir)

        # Fixed the importing issue by setting `use_image_search` to True.
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
