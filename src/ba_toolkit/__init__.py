bl_info = {
    "name": "BA Toolkit for Blender",
    "author": "AkagawaTsurunaki",
    "version": (0, 1, 0),
    "blender": (4, 5, 6),
    "location": "View3D > Sidebar > BA Toolkit",
    "description": "...",
    "category": "Material",
}

import bpy
from . import operators

class BAToolkitPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "BA Toolkit"
    bl_idname = "BA_TOOLKIT"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "BA Toolkit"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.operator(operators.AnimatorImporter.bl_idname)



def register():
    bpy.utils.register_class(operators.AnimatorImporter)
    bpy.utils.register_class(BAToolkitPanel)


def unregister():
    bpy.utils.unregister_class(operators.AnimatorImporter)
    bpy.utils.unregister_class(BAToolkitPanel)


if __name__ == "__main__":
    register()
