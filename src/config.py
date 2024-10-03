#! Window Dimensions
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

#! Terrain and color configs:
debug = False


SNOW = 5
MOUNT = 4
GRASS = 3
BEACH = 2
OCEAN = 1
OCEAN_DEEP = 0

        
SEED = 11 #For consistency for now 9 is best, 12 is also good
TERRAINWEIGHT =     [70, 20, 15, 40, 30, 20]      
TERRAINTYPE = [OCEAN_DEEP,OCEAN,BEACH,GRASS,MOUNT,SNOW]
    
GRADIENTS = {
    0: ((30, 176, 250), (38, 240, 250)),    # Ocean Deep (Darker to Dark)
    1: ((38, 240, 250), (40, 253, 255)),   # Ocean (Dark to Light)
    2: ((230, 210, 171), (255, 243, 190)), # Beach (Dark to Light)
    3: ((20, 177, 150), (102, 233, 127)),    # Grass (Dark to Light)
    4: ((73, 72, 72), (120, 119, 124)),   # Mountain (Dark to Light)
    5: ((224, 224, 224), (255, 255, 255)) # Snow (Grayish to White)
}

#! Boid Configs

MIN_SPEED = 0.05
MAX_SPEED = 0.10
MAX_FORCE = 1
PERCEPTION = 30         #* Distance where boids can "See" each other(Higher is bigger radius)
CROWDING = 6           #* Distance between boids(lower is more crowded as there is less(no) seperation)
CAN_WRAP = False        #* If boids can wrap to other side
EDGE_DISTANCE_PCT = 2   #* Distance before boids gets pushed back by the edges

universal_follow_flag = False

