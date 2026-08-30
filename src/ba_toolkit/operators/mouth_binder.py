from pathlib import Path

import bpy

from ..common.utils import find_parent_with_metadata, find_root_armature


class MouthBinder(bpy.types.Operator):
    bl_idname = "ba_toolkit_for_blender.mouth_binder"
    bl_label = "Bind Mouth to Selected"
    bl_options = {'REGISTER', 'UNDO'}
    bl_icon = 'LINK_BLEND'
    bl_description = "Bind mouth controller to selected mesh.\n" \
                     "Instructions:\n" \
                     "1. Select the mouth mesh (e.g., Aris_Origin_Body_Mouth).\n" \
                     '2. Click "Bind Mouth to Selected". A mouth controller will be added to the scene.\n' \
                     "3. Switch to Pose Mode.\n" \
                     "4. Click the little selection box on the surface of the 'Mouth Sprite Sheet'.\n" \
                     "5. Press 'G' to move it around and pick the mouth shape you like.\n" \
                     'Thanks to BlackMaLou for sharing the "Mouth Sprite Sheet"'

    def execute(self, context):
        mouth = context.active_object
        if not mouth or mouth.type != 'MESH':
            self.report({'ERROR'}, "No mesh selected. Please select a mouth mesh!")
            return {'CANCELLED'}

        template_path = Path(__file__).parent.parent.joinpath('assets/Mouth_BlackMaLou.blend')

        print(template_path)
        with bpy.data.libraries.load(str(template_path), link=False) as (src, dst):
            dst.collections = ["Mouth Controller"]

        imported = dst.collections[0]
        imported.name = f"{mouth.name} Controller"

        # Set `Controller` as the child of `bone_root`
        # This will traverse up to find the root object which contains metadata
        controller: bpy.types.Object = next(
            (o for o in imported.objects if o.type == 'ARMATURE' and 'controller' in o.name.lower()),
            None
        )
        ch_obj = find_parent_with_metadata(mouth)
        bone_root = find_root_armature(ch_obj)

        # Here set the parent.
        # DO NOT set all objects of the collection imported as the children of the `bone_root`!
        # Note that the default transform of the controller is changed here.
        controller.parent = bone_root
        controller.location = (0, 0, 0)
        controller.rotation_euler = (0, 0, 0)
        controller.scale = (1.0, 1.0, 1.0)

        context.scene.collection.children.link(imported)

        # Find the mouth template in the collection
        template = next(
            (o for o in imported.objects if o.type == 'MESH' and 'template' in o.name.lower()),
            None
        )
        if not template:
            self.report({'ERROR'}, f'Mouth Template is None? Did you modify "{template_path}"?')
            return {'CANCELLED'}

        # Delete all old materials!
        while mouth.data.materials:
            mouth.data.materials.pop(index=0)

        for mat in template.data.materials:
            mouth.data.materials.append(mat)

        self.report({'INFO'}, f"Bound {template.name} to {mouth.name} successfully!")
        return {'FINISHED'}
