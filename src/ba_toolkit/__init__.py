from .operators import model_importer, mouth_separator
import bpy


bl_info = {
    "name": "BA Toolkit for Blender",
    "author": "AkagawaTsurunaki",
    "version": (0, 1, 0),
    "blender": (4, 5, 6),
    "location": "View3D > Sidebar > BA Toolkit",
    "description": "...",
    "category": "Material",
}


class BAToolkitPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "BA Toolkit"
    bl_idname = "BA_TOOLKIT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "BA Toolkit"

    def draw(self, context):
        layout = self.layout

        if layout:
            row = layout.row()
            if row is not None:
                row.operator(model_importer.ModelImporter.bl_idname,
                             icon=model_importer.ModelImporter.bl_icon)  # type: ignore

            row = layout.row()
            if row is not None:
                row.operator(mouth_separator.MouthSeparator.bl_idname,
                             icon=mouth_separator.MouthSeparator.bl_icon)  # type: ignore


def register():
    bpy.utils.register_class(model_importer.ModelImporter)
    bpy.utils.register_class(mouth_separator.MouthSeparator)
    bpy.utils.register_class(BAToolkitPanel)


def unregister():
    bpy.utils.unregister_class(model_importer.ModelImporter)
    bpy.utils.unregister_class(mouth_separator.MouthSeparator)
    bpy.utils.unregister_class(BAToolkitPanel)


if __name__ == "__main__":
    register()
