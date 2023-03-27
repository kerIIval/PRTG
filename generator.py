import bpy
import time



def createGrid(res, im): # this is the main function behind the addon which generates the base mesh
    start_time = time.time()
    warningMessage = False


    
    col = len(im)
    row = len(im[0])
    
    if res > row: # there is no point to have a resolution higher than the inputted image
        res = row
        warningMessage = True

    relRow = res
    relCol = round(res*(col/row))

    # sets the origin vertice
    x = -2.5
    y = -2.5*(col/row)

    factor = round((relRow*relCol)/20) # allows the program to calculate the progress
    
    # initiating lists for the vertices and faces to be later used to generate the mesh    

    vertices = []     
    faces = [(a, a + 1, a + 1 + relCol, a + relCol) for a in range(relRow * relCol - relCol) if (a + 1) % relCol != 0] # list comprehension to initiate faces from vertices
    
    
    for i in range(relRow):
        for j in range(relCol):
            
            xRel = i/relRow
            yRel = j/relCol
            vert = ((x+5*i/res),(y+5*j/res), getHeight(round(row*xRel), round(col*yRel), im)) # adds a tuple to the list of vertices with the z value calculated by the geteHeight function
            vertices.append(vert)
            
            if (relCol*i+j) % factor == 0: #prints a progress message every 5%
                print(str(5*(relCol*i+j) / factor) + '% of the mesh has been generated \n')         
        
    
      
    

    if warningMessage:
        print("The inputted resolution is higher than the resolution of the provided image \nTerrain has been generated with the resolution of the immage \nIf you want a smoother mesh use interpolation :P\n")

    grid = bpy.data.meshes.new(name = 'terrain') # these few lines add the generated mesh to the blender scene
    grid.from_pydata(vertices, [], faces)
    terrain = bpy.data.objects.new('Terrain', grid)
    new_collection = bpy.data.collections.new('new_collection')
    bpy.context.scene.collection.children.link(new_collection)
    new_collection.objects.link(terrain)

    print("Terrain was generated succesfully :D\n--- %s seconds ---" % (time.time() - start_time))

    return bpy.context.view_layer.objects.active  # returns the grid in case it needs to be interpolated
    # deprecated as now the heightmap is being interpolated before the mesh generation



def getHeight(x, y, im): # this function finds the relative x and y on the heightmap and returns the pixels value (height)
    try:
        return im[y][x]/500
    except:
        return 0

# the following is the old version, which didn't allow for variable resolutions only powers of 2 and also had a very poor implementation of interpolation

# def interpolation(vertices):
#     len = (len(vertices))**(1/2)


# def listTransform(list): #transforms a 1d list into a 2d list
#     return np.array(list).reshape(2,2)
#     #returnList = []
#     #len = (len(list))**(1/2)
#     #for i in range(len):
#     #    tempList = []
#     #    for j in range(len):
#     #        tempList.append(list[j+i*len])
#     #    returnList.append(tempList)
#     #return returnList

# need to implement a slider for the resolution or in case of random terrain generation link it with another addon

# im = Image.open("C:\\Users\\grabs\\OneDrive\\Documents\\project\\heightmapper.png").convert('L')

# row, col = im.size

# im = np.array(im) #you can pass multiple arguments in single line

    
# def createPlane(res = 512, size = 8, x = 0, y = 0, z = 0):
    
#     bpy.ops.mesh.primitive_plane_add(size=size, enter_editmode=False, align='WORLD', location=(x, y, z), scale=(1, 1, 1)) 
#     #creates the plane
    
#     if row != col: #if the heightmap is not square it will scale the plane apropriately 
#         bpy.ops.object.editmode_toggle()
#         bpy.ops.transform.resize(value=(row/col, 1, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
#         bpy.ops.object.editmode_toggle()

    
    
#     bpy.ops.object.modifier_add(type='SUBSURF')
#     bpy.context.object.modifiers["Subdivision"].subdivision_type = 'SIMPLE'
#     bpy.context.object.modifiers["Subdivision"].levels = log(res, 2)
#     bpy.ops.object.modifier_apply(modifier="Subdivision") 
    
#     #subdivides the plane depending on the resolution given
    
#     return bpy.context.view_layer.objects.active

#     #returns the newly created plane  

# def planeToArray(plane):
   
#    vertices = np.zeros(resolution*4, dtype=np.float32)
#    plane.data.vertices.foreach_get(vertices)
#    vertices = np.reshape(vertices, (res, 4))
    
#    return vertices

# def interpolatedHeight(xRel, yRel):
#     x = row*xRel
#     y = col*yRel
    
#     xOffset = x - round(x)
#     yOffset = y - round(y)
    
#     topValueY = bottomValueY = round(y) - 2
    
#     topValueX = bottomValueX = round(x) - 2
    
#     value = im[bottomValueX][bottomValueY]
    
#     if xOffset >= 0.2:
        
#         topValueX += 1
        
#     if yOffset <= -0.2:
        
#         bottomValueX += -1
        
#     if yOffset >= 0.2:
            
#         topValueY += 1
    
#     if yOffset <= -0.2:
            
#         bottomValueY += -1
            
    
#     offset = (yOffset + xOffset)/2
    
#     #print(str(yOffset) + " - " + str(xOffset) + " - " + str(offset))   
    
#     value = (im[bottomValueX][bottomValueY]  + offset*(im[topValueX-2][topValueY]-im[bottomValueX][bottomValueY])) / 320
    

#     return value



# def displaceMesh(plane, res, interpolation = False): #fucntion to displace the vertices of the mesh depending on their coordinates
    
#     firstX = plane.data.vertices[0].co.x 
#     firstY = plane.data.vertices[0].co.y
#     #as these values are used multiple times later in the loop this makes sure that the plane doesn't get unnecessarily called each time
    
#     i = 0
#     factor = round((res**2)/20)
    
#     #these are variables that help me track progress of the operation

#     for vert in plane.data.vertices:

#         x = vert.co.x
#         y = vert.co.y
#         #gets the coordinates of the vertice from the mesh
        
        
#         xRel = (x - firstX) / (-2*firstX)
#         yRel = (-y - firstY) / (-2*firstY)
#         #calculates the relative positions of the vertices
    
#         if interpolation:
#             vert.co.z = interpolatedHeight(xRel, yRel)
            
#         else:
#             vert.co.z = getHeight(xRel, yRel)
            
#         #sets the z coordinate of the mesh to the value given by the image using the x and y coordinates
        
#         if i % factor == 0: #prints a progress message every 5%
#             print(str(5*i / factor) + '% of the mesh has been generated \n')     
            
        
#         i += 1 #iteration to be able to show progress



# def register():
#     bpy.utils.register_class(generate)

# def unregister():
#     bpy.utils.unregister_class(generate)