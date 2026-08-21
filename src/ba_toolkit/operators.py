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
    )


    def execute(self, context):
        dir = Path(str(self.directory))
        assert dir.exists()
        anim = get_original_animator(dir=dir)
        
        bpy.ops.import_scene.fbx(filepath=str(anim.fbx_path), use_image_search=True)
        print(anim)
        return {'FINISHED'}

    def invoke(self, context, event):
        self.directory = ""
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
