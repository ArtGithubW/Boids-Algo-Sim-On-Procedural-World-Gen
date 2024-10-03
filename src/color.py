from config import WINDOW_WIDTH,WINDOW_HEIGHT,GRADIENTS

'''
Function to get the interpolation between two colors using the heightmap factor
''' 
def interpolate_color(color1, color2, Color_height):
    return (
        int(color1[0] + (color2[0] - color1[0]) * Color_height),
        int(color1[1] + (color2[1] - color1[1]) * Color_height),
        int(color1[2] + (color2[2] - color1[2]) * Color_height)
    )


'''
This function takes the integer map and apply gradient colors to the pygame surface.
'''    
def drawColors(background_surface,noise_map,map_int,max_terrain_heights,min_height):
    for y, row in enumerate(map_int):
        for x, value in enumerate(row):

            if x >= WINDOW_WIDTH or y >= WINDOW_HEIGHT:  # Check boundary conditions
                continue
            
            # This switch case will create a float from 0 to 1 depending on the height of the terrain in respect to its min and max range
            match value:
                case 0:
                    color_height = normalize_Zero_to_One(noise_map[y][x],min_height,max_terrain_heights[0])
                case 1:
                    color_height = normalize_Zero_to_One(noise_map[y][x],max_terrain_heights[0],max_terrain_heights[1])
                case 2:
                    color_height = normalize_Zero_to_One(noise_map[y][x],max_terrain_heights[1],max_terrain_heights[2])
                case 3:
                    color_height = normalize_Zero_to_One(noise_map[y][x],max_terrain_heights[2],max_terrain_heights[3])
                case 4:
                    color_height = normalize_Zero_to_One(noise_map[y][x],max_terrain_heights[3],max_terrain_heights[4])
                case 5:
                    color_height = normalize_Zero_to_One(noise_map[y][x],max_terrain_heights[4],max_terrain_heights[5])
                    
            # Use the gradient color for each pixel
            color = interpolate_color(GRADIENTS[value][0],GRADIENTS[value][1],color_height)  
            background_surface.set_at((x, y), color)
    return background_surface

"""
This function takes a minimum and maximum and input and normalizes the input(0.0 to 1.0) based on the minimum and maximum
"""
def normalize_Zero_to_One(inputVal, old_min, old_max, new_min = 0.0, new_max=1.0 ):
    return (inputVal - old_min) / (old_max - old_min) * (new_max - new_min) + new_min



#! EXPERIMENTAL
"""
This function will animate the world procedurally generating in
"""
#TODO TURN EXPERIMENT CODE IN MAIN TO THIS FUNCTION