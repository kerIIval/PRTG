import bpy
import numpy as np
from PIL import Image



class MyProperties(bpy.types.PropertyGroup): # a class containing all the properties/variables that the user can input in the UI
    
    bpy.types.Scene.res = bpy.props.IntProperty(
        name = "Choose resolution of the terrain: ", 
        min = 3, 
        max = 16384,
        default = 1024
    )
    
    bpy.types.Scene.long = bpy.props.FloatProperty(
        min = -180,
        max = 180,
        default = 0
    )
        
    bpy.types.Scene.lat = bpy.props.FloatProperty(
        min = -90,
        max = 90,
        default = 0
    )

    bpy.types.Scene.mount_strength = bpy.props.FloatProperty(
        min = 0,
        max = 1,
        default = 0.5
    )

    bpy.types.Scene.plain_strength = bpy.props.FloatProperty(
        min = 0,
        max = 1,
        default = 0.5
    )

    bpy.types.Scene.mount_x = bpy.props.FloatProperty(
        min = 0.1,
        max = 20,
        default = 5
    )

    bpy.types.Scene.mount_y = bpy.props.FloatProperty(
        min = 0.1,
        max = 20,
        default = 4
    )

    bpy.types.Scene.plain_x = bpy.props.FloatProperty(
        min = 0.1,
        max = 20,
        default = 1
    )

    bpy.types.Scene.plain_y = bpy.props.FloatProperty(
        min = 0.1,
        max = 20,
        default = 1
    )

    bpy.types.Scene.seed = bpy.props.IntProperty(
        min = 0,
        default = 0
    )

    bpy.types.Scene.rand_seed = bpy.props.BoolProperty(
        default = True
    )

    bpy.types.Scene.advanced = bpy.props.BoolProperty(
        default = False
    )
    
    bpy.types.Scene.exp = bpy.props.BoolProperty(
        name = "Auto Exposure",
        default = True
    )

    bpy.types.Scene.ocean = bpy.props.BoolProperty(
        default = False
    )

    bpy.types.Scene.manual = bpy.props.BoolProperty(
        name = "Manually choose",
        default = False
    )

    bpy.types.Scene.scale = bpy.props.FloatProperty(
        min = 2,
        default = 4
    )
    
    bpy.types.Scene.max_height = bpy.props.IntProperty(
        name = "Maximum height",
        min = 0,
        max = 8848,
        default = 8848
    )

    bpy.types.Scene.min_height = bpy.props.IntProperty(
        name = "Minimum height",
        min = 0,
        max = 8848,
        default = 0
    )

    bpy.types.Scene.path = bpy.props.StringProperty(
        name = "",
        description="Choose a file:",
        default="",
        maxlen=1024,
        subtype='FILE_PATH'
    )
        
    bpy.types.Scene.interp = bpy.props.IntProperty(
        name = "Level (0 for None)", 
        min = 0, 
        max = 4,
        default = 0
    ) 

class PRTG_manual(bpy.types.Panel): # a sub menu to for terrain generation using local heightmaps
    bl_parent_id = "SCENE_PT_layout"
    bl_label = "Manual"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    

    def draw(self, context): # function to draw the sub menu
        layout = self.layout
        scene = context.scene

        layout.label(text=" Manual Terrain Generation:")

        row = layout.row()
        row.prop(scene, "res") # the resolution slider
        row.scale_y = 1.2
        

        split = layout.split() # 2 columns, one for text another a path input field

        col = split.column()
        col.label(text="Heightmap File Path:")        

        col = split.column(align=True)
        col.prop(scene, "path")
        col.scale_x = 1.2
        col.scale_y = 1.2
        
        row = layout.row()

        row = layout.row()
        row.label(text = "Interpolation") 
        # interpolation slider
        row = layout.row()    
        row.prop(scene, "interp")
    
        row = layout.row()
        row.label(text = "High levels will significantly increase processing time!") # a warning about performance of interpolation
        row.scale_x = 0.5

        row = layout.row() # blank row to make it look nicer
        
        row = layout.row(align=True)
        row.scale_y = 2.0
        row.operator(Generate_Manual.bl_idname)  # Generate button     

class PRTG_tangram(bpy.types.Panel): # a sub menu to for terrain generation which webscrapes real world data
    bl_parent_id = "SCENE_PT_layout"
    bl_label = "Tangram"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
     
        layout.label(text=" Tangram Terrain Generation:")

        row = layout.row()
        row.prop(scene, "res") # a slider for the resolution
        row.scale_y = 1.2
        

       

        # Create two columns, one for text another for the longtitude input
        split = layout.split()

        col = split.column()
        col.label(text="Longitude:")
        col = split.column(align=True)
        col.prop(scene, "long", text = '')
        
        # Create two columns, one for text another for the latitude input
        split = layout.split()

        col = split.column()
        col.label(text="Latitude:")
        col = split.column(align=True)
        col.prop(scene, "lat", text = '')
       
        # Create two columns, one for text another for the scale input
        split = layout.split()

        col = split.column()
        col.label(text="Scale:")  
        col = split.column(align=True)
        col.prop(scene, "scale", text = '')


        split = layout.split()

        # a checkbox on wether or not the user wants to adjust the map before downloading the heightmap
        col = split.column()
        col.label(text="Manually Adjust:")
        
        col = split.column(align=True)
        col.prop(scene, "manual", text = '')
        
        # a checkbox on wether or not the user wants the maximum and minimum heights to be adjusted automatically or not
        split = layout.split()

        col = split.column()
        col.label(text="Auto Exposure:")
        
        col = split.column(align=True)
        col.prop(scene, "exp", text = '')

        # a checkbox on wether or not to include ocean data in the heightmap
        split = layout.split()

        col = split.column()
        col.label(text="Ocean data:")
        
        col = split.column(align=True)
        col.prop(scene, "ocean", text = '')

        if context.scene.exp == False: # if the user doesn't want automatic exposure a menu opens up to input maximum and minimum wanted heights            
            
            row = layout.row()
            row.label(text="Maximum:")
            row = layout.row()
            row.prop(scene, "max_height", text = '')
            
            row = layout.row()
            row.label(text="Minimum:")
            row = layout.row()
            row.prop(scene, "min_height", text = '')
    
        
        row = layout.row()

        row = layout.row()
        row.label(text = "Interpolation") # a slider for interpolation
        
        row = layout.row()    
        row.prop(scene, "interp")
    
        row = layout.row()
        row.label(text = "High levels will significantly increase processing time!") # a warning about the performance of interpolation
        row.scale_x = 0.5
        

        row = layout.row() # a blank line to make it look nicer
      
        row = layout.row(align=True)
        row.scale_y = 2.0
        row.operator(Generate_Tangram.bl_idname) # generate button

class PRTG_random(bpy.types.Panel): # a sub menu to for terrain generation which uses noise to randomly generate terrain    
    bl_parent_id = "SCENE_PT_layout"
    bl_label = "Random"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
     
        layout.label(text=" Random terrain generation:")

        row = layout.row()
        row.prop(scene, "res") # resolution slider
        row.scale_y = 1.2  
        
        split = layout.split()

        col = split.column()
        col.label(text="Strength of mountains:")
        # an input for the strength of mountains
        col = split.column(align=True)
        col.prop(scene, "mount_strength", text = '')
        

        split = layout.split()

        col = split.column()
        col.label(text="Strength of hills:")
        # an input for the strength of hills
        col = split.column(align=True)
        col.prop(scene, "plain_strength", text = '')
       
        split = layout.split()

        col = split.column()
        col.label(text="Random Seed:")
        
        col = split.column()
        col.prop(scene, "rand_seed", text = '') # a checkbox to select to have a specific seed

        col = split.column()
        col.prop(scene, "seed", text = '') # input for a specific seed
        if context.scene.rand_seed == True:
            col.active = False

        split = layout.split()
        col = split.column()
        col.label(text = "Advanced Parameters: ")
        col.scale_x = 1.5
        col = split.column()
        col.prop(scene, "advanced", text = '') # checkbox to enable advanced parameters

        if context.scene.advanced == True:

            row = layout.row()
            row.label(text = "Plains/Hills advanced options")

            split = layout.split()            
            col = split.column()
            col.prop(scene, "plain_x", text = "Plains x multiplier")
            col = split.column(align=True)
            col.prop(scene, "plain_y", text = "Plains y multiplier") 

            row = layout.row()   
            row.label(text = "Mountains advanced options")

            split = layout.split()            
            col = split.column()
            col.prop(scene, "mount_x", text = "Mountains x multiplier")
            col = split.column(align=True)
            col.prop(scene, "mount_y", text = "Mountains y multiplier") 
            
        
        row = layout.row()

        row = layout.row()
        row.label(text = "Interpolation") 
        # a slider for interpolation
        row = layout.row()    
        row.prop(scene, "interp")
    
        row = layout.row()
        row.label(text = "High levels will significantly increase processing time!") # a warning about interpolation performance
        row.scale_x = 0.5
        
        row = layout.row()
        
        row = layout.row(align=True)
        row.scale_y = 2.0
        row.operator(Generate_Random.bl_idname)

class Generate_Manual(bpy.types.Operator): # a button which starts to generate the mesh for local heightmaps
    bl_idname = "prtg.generate"    
    bl_label = "Generate"
    bl_description = "Generate terrain using inputted heightmap"

    def execute(self, context):        
        
        heightMapFile = context.scene.path
        res = context.scene.res
        level = context.scene.interp
        im = Image.open(str(heightMapFile)).convert('L')

        if not heightMapFile: # returns an error if there is no heightmap chosen
            self.report({"ERROR"}, "Missing Heightmap!")
            return {"CANCELLED"}       

        from .generator import createGrid
        from .interpolation import interpolate

        im = np.array(im)

        if level == 0:
            createGrid(res, im)
        # depending on the users input either starts interpolating or generating the mesh
        else:
            interpolate(im, res, level)

        return {"FINISHED"}
    
class Generate_Random(bpy.types.Operator): # a button which starts the process of random terrain generation
    bl_idname = "prtg.generate_random"
    bl_label = "Generate"
    bl_description = "Generate random terrain"

    def execute(self, context):        
        
        res = context.scene.res
        level = context.scene.interp        

        plainFactor = context.scene.plain_strength
        mountFactor = context.scene.mount_strength

        plain_x = context.scene.plain_x
        plain_y = context.scene.plain_y
        mount_x = context.scene.mount_x
        mount_y = context.scene.mount_y

        # if the there is no seed chosen the proceduralSetup function will generate a random seed
        if context.scene.rand_seed: 
            seed = None
        else: seed = context.scene.seed    

        from .procedural import proceduralSetup

        proceduralSetup(res, level, mountFactor, plainFactor, seed, mount_x, mount_y, plain_x, plain_y)

        return {"FINISHED"}
    
class Generate_Tangram(bpy.types.Operator): # a button which kicks off the web scraping to allow real world heightmaps
    bl_idname = "prtg.generate_tangram"    
    bl_label = "Generate"
    bl_description = "Generate real world terrain using inputted coordinates"

    def execute(self, context):
        from .tangram import tangram    
        lat = context.scene.lat
        long = context.scene.long
        scale = context.scene.scale
        exp = context.scene.exp
        ocean = context.scene.ocean
        
        res = context.scene.res
        level = context.scene.interp
        manual = context.scene.manual    

        if not exp:
            max = context.scene.max_height
            min = context.scene.min_height
            tangram(lat,long,scale,res,manual,level,exp, min, max, ocean)
        else:
            tangram(lat,long,scale,res,manual,level,exp, ocean = ocean)                 
        
                 
        return {"FINISHED"}

def register(): # registers all the UI elements
    
    bpy.utils.register_class(MyProperties)
    bpy.utils.register_class(PRTG_manual)
    bpy.utils.register_class(PRTG_tangram)
    bpy.utils.register_class(PRTG_random)
    bpy.utils.register_class(Generate_Manual)
    bpy.utils.register_class(Generate_Tangram)
    bpy.utils.register_class(Generate_Random)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MyProperties)  
        
    


def unregister(): # unregisters all the UI elements
    
    bpy.utils.unregister_class(MyProperties)
    bpy.utils.unregister_class(PRTG_manual)
    bpy.utils.unregister_class(PRTG_tangram)
    bpy.utils.unregister_class(PRTG_random)
    bpy.utils.unregister_class(Generate_Manual)
    bpy.utils.unregister_class(Generate_Tangram)
    bpy.utils.unregister_class(Generate_Random)
    del bpy.types.Scene.my_tool
