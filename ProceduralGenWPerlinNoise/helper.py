from perlin_noise import PerlinNoise
from config import *


# This function generates 4 perlin noises then add them all up into a 2d matrix
def GenNoiseMap() -> list:
    noise_map = []
    noise1 = PerlinNoise(octaves=3, seed=SEED)
    noise2 = PerlinNoise(octaves=6, seed=SEED)
    noise3 = PerlinNoise(octaves=12, seed=SEED)
    noise4 = PerlinNoise(octaves=24, seed=SEED)
    x_loc, y_loc = WINDOW_WIDTH + 1, WINDOW_HEIGHT + 1
    for j in range(y_loc):
        row = []
        for i in range(x_loc):   
            noise_val = noise1([i/x_loc, j/y_loc])          # Main curve
            noise_val += 0.5 * noise2([i/x_loc, j/y_loc])   # the remaining adds to main curve
            noise_val += 0.25 * noise3([i/x_loc, j/y_loc])  
            noise_val += 0.125 * noise4([i/x_loc, j/y_loc])
            row.append(noise_val)
        noise_map.append(row)
    return noise_map



# This function will calculate the threshold for each terrain and use the noise map to create an terrain map of integers
def GenIntMap(NoiseMap) -> list:
    max_value,min_value = 0.0,0.0

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
    # max_terrain_heights[SNOW] = max_value # Makes sure the SNOW is the last value in this list

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