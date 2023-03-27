import time

def interpolate(im, res, level):

    start_time = time.time() # saves the start time to later display how long it took

    for i in range(level): # a for loop to call the interpolation function the number of times that the user inputted
        print('Level '+ str(i+1) +' interpolation started')
        im = script(im)
        print('Level '+ str(i+1) +' interpolation complete')
    
    print("---- ---- ---- ---- ----\n Interpolation finished \n" + " It took % seconds \n---- ---- ---- ---- ----" % (time.time() - start_time)) 

    from .generator import createGrid # sends the interpolated heightmap to the generator
    createGrid(res, im)


def script(im):
    map = [[None for j in range(2 * len(im[0]) - 1)] for r in range(2 * len(im) - 1)]

    progress = 0

    for i in range(len(map)):
        for j in range(len(map[0])):
            sum = 0 # sets the sum to 0 on every iteration, its purpose is to allow the calculation of the average
            div = 0
            if map[i][j] == None: 
                if i % 2 == 0 and j % 2 == 0: 
                # this if statement is to check if this element in the new larger bitmap corresponds to the original heightmap element, if so it sets the same value in the bitmap
                    map[i][j] = im[i // 2][j // 2]
                else:
                # otherwise it will interpolate the value based on the values surrounding it
                    if i > 0: # checks if the current element has a left neighbour
                        # adds the neighbour to the sum to be averaged later 
                        sum += int(map[i - 1][j])
                        div += 1

                    if j > 0: # checks if the current element has a top neighbour
                        # adds the neighbour to the sum to be averaged later
                        sum += int(map[i][j - 1])
                        div += 1

                    if j + 1 < len(map[0]): # checks if a right neighbour exists
                        if i % 2 == 1: # adds th right neighbour element which was already calculated by the next if statement (bottom)
                            sum += map[i][j + 1]

                        else: # if it's an even row we can grab the original value from the original heightmap
                            sum += int(im[i // 2][j // 2 + 1])
                        div += 1

                    if i + 1 < len(map): # checks if a bottom neighbour exists
                        if j % 2 == 1: # if it's an odd column it interpolates the bottom neighbour by averaging between the elements of the original heightmap that would be around it
                            bottom = (int(im[i // 2][j // 2]) + int(im[i // 2 + 1][j // 2]) + int(im[i // 2][j // 2 + 1]) + int(im[i // 2 + 1][j // 2 + 1])) // 4
                            map[i + 1][j] = bottom # saves the bottom neighbour in the lest as it is later used as a right neighbour
                            sum += bottom

                        else: # otherwise the bottom neighbour is one of the original elements
                            sum += im[i // 2 + 1][j // 2]
                        div += 1

                    map[i][j] = sum / div # this saves the averaged out element

        if progress + 0.05 <= i / len(map):
            progress = i / len(map) 
            print("Progress - " + str(round(100*progress)) + '%')

    return map