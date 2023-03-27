import bpy
from .install_dependencies import dependencies_installed

class PRTG(bpy.types.Panel): # the parent menu 
    """Creates a Panel in the scene context of the properties editor"""
    bl_label = "PRTG"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        
        if not dependencies_installed:
            row = layout.row()
            row.operator('prtg.install_dependencies') # the button to install modules appears when the modules are not installed



def register():
    bpy.utils.register_class(PRTG)
    print(dependencies_installed)
    if dependencies_installed: # if the dependencies are installed this calls the UI register function which will draw the main UI
        from . import UI
        UI.register()

def unregister():
    bpy.utils.unregister_class(PRTG)
    from . import UI
    UI.unregister()