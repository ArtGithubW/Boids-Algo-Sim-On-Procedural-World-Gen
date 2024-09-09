#! Window Dimensions
WINDOW_WIDTH = 800 
WINDOW_HEIGHT = 700

#! Terrain and color configs:
SNOW = 5
MOUNT = 4
GRASS = 3
BEACH = 2
OCEAN = 1
OCEAN_DEEP = 0

        
SEED = 9 #For consistency for now 9 is best
TERRAINWEIGHT =     [60, 30, 15, 40, 30, 20]      
TERRAINTYPE = [OCEAN_DEEP,OCEAN,BEACH,GRASS,MOUNT,SNOW]
    
GRADIENTS = {
    0: ((20, 58, 100), (50, 90, 105)),    # Ocean Deep (Darker to Dark)
    1: ((50, 90, 105), (99, 185, 215)),   # Ocean (Dark to Light)
    2: ((200, 170, 80), (255, 213, 104)), # Beach (Dark to Light)
    3: ((60, 130, 44), (82, 164, 54)),    # Grass (Dark to Light)
    4: ((80, 80, 80), (120, 119, 124)),   # Mountain (Dark to Light)
    5: ((200, 200, 200), (255, 255, 255)) # Snow (Grayish to White)
}

#! Boid Configs

MIN_SPEED = 0.05
MAX_SPEED = 0.20
MAX_FORCE = 1
PERCEPTION = 30         #* Distance where boids can "See" each other(Higher is bigger radius)
CROWDING = 10           #* Distance between boids(lower is more crowded as there is less(no) seperation)
CAN_WRAP = False        #* If boids can wrap to other side
EDGE_DISTANCE_PCT = 2   #* Distance before boids gets pushed back by the edges