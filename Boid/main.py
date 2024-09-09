import argparse
import sys
import pygame as pg
from pygame.locals import *
import pygame_gui
from boid import Boid
from config import * 
from FindCenter import findCenters
sys.path.insert(1, './ProceduralGenWPerlinNoise')
from ProceduralGenWPerlinNoise.helper import *


num_boids = 100
default_geometry = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"

def update(dt, boids, manager):
    """
    Update boids and checks for button presses. Called once per frame.
    """
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit(0)
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == add_boids_button:
                add_boids(boids, 10)
                print("Added 10 Boids")
            elif event.ui_element == remove_boids_button:
                boids.remove(boids.sprites()[:10])
                print("RM'd 10 Boids")
            elif event.ui_element == reset_boids_button:
                num_boids = len(boids)
                boids.empty()
                add_boids(boids, num_boids)
                print("Reset Boids")
            elif event.ui_element == toggle_cursor_follow_button:
                for boid in boids:
                    boid.follow_cursor = not boid.follow_cursor
                print(f"Follow Cursor: {not boid.follow_cursor}")
            elif event.ui_element == Wrap_button:
                for boid in boids:
                    boid.can_wrap = not boid.can_wrap
                print(f"Wrap?: {boid.can_wrap}")
        manager.process_events(event)

    for b in boids:
        b.update(dt, boids)

    manager.update(dt)

def draw(screen, background, boids, manager,list_of_rects):
    """
    Draws everything to the window. Called once per frame.
    """
    # Draw the background
    screen.blit(background, (0, 0))
    for i in range(len(list_of_rects)):
        pg.draw.rect(screen,"red",list_of_rects[i])

    # boids.draw(screen)
    # manager.draw_ui(screen)

    pg.display.update()

# Function to get the interpolation between two colors using the heightmap factor
def interpolate_color(color1, color2, Color_height):
    return (
        int(color1[0] + (color2[0] - color1[0]) * Color_height),
        int(color1[1] + (color2[1] - color1[1]) * Color_height),
        int(color1[2] + (color2[2] - color1[2]) * Color_height)
    )

    
def main(args):
    # Generates the map and turn it into a background
    noise_map = GenerateNoiseMap(Inputseed=SEED)
    max_terrain_heights,min_height = GenerateMaxHeights(noise_map)
    map_int = GenerateIntMap(noise_map,max_terrain_heights)
    list_of_rects = []
    for Index,Coords in enumerate(findCenters(map_int)): #Coords(x,y)
        print(f"Center {Index}, Coords(Y:{Coords[0]}, X:{Coords[1]})")
        list_of_rects.append(pg.Rect(Coords[1],Coords[0],20,20))
    
    background_surface = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))


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
            
    # Initialize pygame.
    pg.init()

    # Set up the clock to maintain a relatively constant framerate.
    fps = 60.0
    fpsClock = pg.time.Clock()

    # Set up the window.
    pg.display.set_caption("Boids Sim")
    window_width, window_height = [int(x) for x in args.geometry.split("x")]
    flags = DOUBLEBUF # Supposedly increases framerate

    screen = pg.display.set_mode((window_width, window_height), flags)
    screen.set_alpha(None)
    manager = pygame_gui.UIManager((window_width, window_height))

    boids = pg.sprite.RenderUpdates()

    add_boids(boids, args.num_boids)

    # UI manager to add buttons
    global add_boids_button, remove_boids_button, reset_boids_button,toggle_cursor_follow_button,Wrap_button
    add_boids_button = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((10, 10), (100, 30)),
        text='Add Boids',
        manager=manager
    )
    remove_boids_button = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((10, 40), (100, 30)),
        text='Remove Boids',
        manager=manager
    )
    reset_boids_button = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((10, 70), (100, 30)),
        text='Reset Boids',
        manager=manager
    )
    toggle_cursor_follow_button = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((120, 10), (100, 30)),
        text='Tog F-Cursor',
        manager=manager
    )
    Wrap_button = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((120, 40), (100, 30)),
        text='Tog Wrap',
        manager=manager
    )
    

    # Main game loop.
    dt = 1/fps  # dt is the time since last frame.

    while True:
        update(dt, boids, manager)
        draw(screen, background_surface, boids, manager,list_of_rects)
        dt = fpsClock.tick(fps)


def add_boids(boids, num_boids):
    for _ in range(num_boids):
        boids.add(Boid())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Emergent flocking.')
    parser.add_argument('--geometry', metavar='WxH', type=str,
                        default=default_geometry, help='geometry of window')
    parser.add_argument('--number', dest='num_boids', type=int, default=num_boids,
                        help='number of boids to generate')
    args = parser.parse_args()

    main(args)
