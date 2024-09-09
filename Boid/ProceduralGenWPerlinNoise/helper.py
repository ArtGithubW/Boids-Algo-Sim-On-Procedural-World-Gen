from perlin_noise import PerlinNoise
from config import *

"""
This function generates perlin noises then add them all up into a 2d matrix noise map
"""
#! This perlin noise library does not have fall off support so I'll just make more noises at higher octaves and add them up at lower values :P
def GenerateNoiseMap(Inputseed) -> list:
    noise_map = []
    noise1 = PerlinNoise(octaves=3,seed = Inputseed) 
    noise2 = PerlinNoise(octaves=6,seed = Inputseed) 
    noise3 = PerlinNoise(octaves=12,seed = Inputseed)
    noise4 = PerlinNoise(octaves=25,seed = Inputseed)
    noise5 = PerlinNoise(octaves=50,seed = Inputseed) # Adding a 5th noise makes the space looks so much more organic....my lord the time it takes to run though
    noise6 = PerlinNoise(octaves=80,seed = Inputseed) # screw it, 6th noise :D
    

    x_loc, y_loc = WINDOW_WIDTH + 1, WINDOW_HEIGHT + 1
    for j in range(y_loc):
        row = []
        for i in range(x_loc):   
            noise_val = noise1([i/x_loc, j/y_loc])          # Main curve
            noise_val += 0.5 * noise2([i/x_loc, j/y_loc])   # the remaining adds to main curve
            noise_val += 0.25 * noise3([i/x_loc, j/y_loc])  
            noise_val += 0.125 * noise4([i/x_loc, j/y_loc])
            noise_val += 0.0625 * noise5([i/x_loc, j/y_loc])
            noise_val += 0.003125 * noise6([i/x_loc, j/y_loc])
            row.append(noise_val)
        noise_map.append(row)
    return noise_map
"""
This function returns the max heights of each of the terrain and also the minimum height of the whole noise map
"""
def GenerateMaxHeights(NoiseMap):
    flat_list = [item for sublist in NoiseMap for item in sublist]
    min_value,max_value = min(flat_list),max(flat_list)
    

    total_TERRAINWEIGHT = sum(TERRAINWEIGHT)
    total_range = max_value + abs(min_value) 
    
    # calculate maximum height for each terrain type, based on weight values
    max_terrain_heights = []
    previous_height = min_value

    for terrain_type in TERRAINTYPE:
        height = total_range * (TERRAINWEIGHT[terrain_type] / total_TERRAINWEIGHT) + previous_height #! Making sure next height is larger than last 
        max_terrain_heights.append(height)
        previous_height = height
    max_terrain_heights[SNOW] = max_value # Makes sure the SNOW is the last value in this list
    
    return max_terrain_heights,min_value
"""
This function will calculate the threshold for each terrain and use the noise map to create an terrain map of integers
"""
def GenerateIntMap(NoiseMap,max_terrain_heights):

    terrain_int_map = []

    for row in NoiseMap:
        map_row = []
        for value in row:
            for terrain_type in TERRAINTYPE:
                if value <= max_terrain_heights[terrain_type]:
                    map_row.append(terrain_type)
                    break
        terrain_int_map.append(map_row) 
    return terrain_int_map


"""
This function takes a minimum and maximum and input and normalizes the input(0.0 to 1.0) based on the minimum and maximum
"""
def normalize_Zero_to_One(inputVal, old_min, old_max, new_min = 0.0, new_max=1.0 ):
    return (inputVal - old_min) / (old_max - old_min) * (new_max - new_min) + new_min