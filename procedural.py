import opensimplex
from random import randint
import numpy as np
from sys import maxsize

def proceduralSetup(res, interplvl, MountainFactor, PlainFactor, seed, MountainX, MountainY, PlainX, PlainY):

    print("Generating random heightmap \n")

    if seed != None: opensimplex.seed(seed) # in the case where the user has inputted a seed it uses it, otherwise the function uses a random seed
    else: opensimplex.seed(randint(0, maxsize))
    
    # initiates an empty list for the heightmap and a progress variable which will be used to write the progress of the creation
    heightmap = []
    progress = 0

    for x in range(res):
        row = []
        for y in range(res):

            if MountainFactor > 0:
                mounts_z = mountains(x, y, MountainX, MountainY) # if the user wants mountains, a seperate function will be called for the purpose of creating a mountain heightmap
            else: mounts_z = 0

            if PlainFactor > 0:
                plains_z = plains(x, y, PlainX, PlainY) # if the user wants plains/hills, a seperate function will be called for the purpose of creating a hill heightmap
            else: plains_z = 0

            row.append((0 + MountainFactor * mounts_z + PlainFactor * plains_z) * 256) # combines the 2 random generated maps

        heightmap.append(row)

        if progress + 0.05 <= x / res:
            progress = x / res # displays a progress message
            print("Progress - " + str(round(100*progress)) + '%')

    im = np.array(heightmap) # converts the heightmap to a numpy array which will allow for easy manipulation

    print("\n Random heightmap complete\n")

    # the if statement calls the interpolate function if the heightmap needs to be interpolated, if not it ust calls the generator
    if interplvl > 0: 
        from .interpolation import interpolate
        interpolate(im, res, interplvl)

    else:
        from .generator import createGrid
        createGrid(res, im)

    
def plains(x, y, xFactor, yFactor): # a function which returns height for hills/plains
    value = opensimplex.noise2((x/100)*xFactor,(y/100)*yFactor)
    value = (value+1)/2
    value = value**0.25
    # by raising the value to a power of 1/4 (root of 4) we will decontrast the heightmap meaning will have height differences similar to hills
    return value

def mountains(x, y, xFactor, yFactor): # a similar function but for mountains
    value = opensimplex.noise2((x/100)*xFactor,(y/100)*yFactor)
    value = (value+1)/3
    return value

#proceduralSetup(16,0,1,0,None,3.0,5.0,1,1)