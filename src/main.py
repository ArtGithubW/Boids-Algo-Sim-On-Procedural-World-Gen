import sys
import pygame as pg
from pygame.locals import QUIT,HWSURFACE 
import pygame_gui
from boid import add_boids
from config import WINDOW_WIDTH,WINDOW_HEIGHT
import time
import numpy as np

from color import drawColors
from ProceduralGenWPerlinNoise.FindCenter import findCoords
from ProceduralGenWPerlinNoise.helper import *


def main():
    start_time = time.time()
    
    num_boids = 100
    # Init the world generation
    noise_map = GenerateNoiseMap() #Inputseed=SEED
    max_terrain_heights,min_height = GenerateMaxHeights(noise_map)
    map_int = GenerateIntMap(noise_map,max_terrain_heights)
    
    gen_time = time.time()
    print(f"Time to generate world Map: {gen_time - start_time}")
    
    #Generate boxes that bois will aboid
    RectDicts = findCoords(map_int)

    list_of_rects = []
    for Index in range(len(RectDicts)): #Coords(x,y)
        #! I def messed up somewhere here, the data struct is actually (y,x)?????? BUT EVERYTHING WORKS so EHHHH.
        list_of_rects.append(pg.Rect(RectDicts[Index]["center"][1],RectDicts[Index]["center"][0],1,1))
        inflate_x = RectDicts[Index]["rightmost"][1]-RectDicts[Index]["leftmost"][1] + 20
        inflate_y = RectDicts[Index]["bottommost"][0]-RectDicts[Index]["topmost"][0] + 20
        list_of_rects[Index].inflate_ip(inflate_x,inflate_y)
    
    background_surface = pg.Surface((WINDOW_WIDTH+120, WINDOW_HEIGHT))
    background_surface = drawColors(background_surface,noise_map,map_int,max_terrain_heights,min_height)

    print(f"Time taken to color the world: {time.time() - gen_time}")
    
    
    '''
    Setting up pygame
    '''
    pg.init()
    fps = 24.0
    fpsClock = pg.time.Clock()
    pg.display.set_caption("Boids Sim")

    screen = pg.display.set_mode((WINDOW_WIDTH+120, WINDOW_HEIGHT), flags = HWSURFACE)
    screen.set_alpha(None)
    manager = pygame_gui.UIManager((WINDOW_WIDTH+120, WINDOW_HEIGHT))    
    boids = pg.sprite.RenderUpdates()

    # UI manager to add buttons
    global add_boids_button, remove_boids_button, reset_boids_button,toggle_cursor_follow_button,Wrap_button,debug_button
    add_boids_button = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((WINDOW_WIDTH + 10, 10), (100, 30)),
        text='Add Boids',
        manager=manager
    )
    remove_boids_button = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((WINDOW_WIDTH +10, 40), (100, 30)),
        text='Remove Boids',
        manager=manager
    )
    reset_boids_button = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((WINDOW_WIDTH +10, 70), (100, 30)),
        text='Reset Boids',
        manager=manager
    )
    toggle_cursor_follow_button = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((WINDOW_WIDTH +10, 100), (100, 30)),
        text='Tog F-Cursor',
        manager=manager
    )
    Wrap_button = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((WINDOW_WIDTH +10, 130), (100, 30)),
        text='Tog Wrap',
        manager=manager
    )
    debug_button = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((WINDOW_WIDTH +10, 160), (100, 30)),
        text='Debug',
        manager=manager
    )
    
    #!------------------------------------EXPERIMENTAL-------------------------------------------------------
    final_surface = drawColors(background_surface, noise_map, map_int, max_terrain_heights, min_height)

    # Initialize transition surface (all pixels start as black)
    transition_surface = pg.Surface((WINDOW_WIDTH + 120, WINDOW_HEIGHT))
    transition_surface.fill((0, 0, 0))  # All black surface

    # Get the color values from the final surface
    final_colors = pg.surfarray.pixels3d(final_surface).copy()
    current_colors = np.zeros_like(final_colors, dtype=np.uint8)
    transition_speed = 5  # Change the speed of color transition
    screen.blit(transition_surface, (0, 0))
    time.sleep(3)
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                running = False

        # Calculates the step and difference between colors
        color_difference = final_colors.astype(np.int16) - current_colors.astype(np.int16)
        step = np.clip(color_difference, -transition_speed, transition_speed)

        # Update the current colors within uint8 range
        current_colors = np.clip(current_colors.astype(np.int16) + step, 0, 255).astype(np.uint8)

        # Push the changes to the screen
        pg.surfarray.blit_array(transition_surface, current_colors)
        screen.blit(transition_surface, (0, 0))

        pg.display.update()
        fpsClock.tick(fps)
    #!------------------------------------EXPERIMENTAL-------------------------------------------------------
    add_boids(boids, num_boids)
    fps = 60.0 # Set fps to 60 
    dt = 1/fps  # dt is the time since last frame.

    #Main game loop
    while True:
        update(dt, boids, manager,list_of_rects)
        draw(screen, background_surface, boids, list_of_rects)
        manager.draw_ui(screen)
        pg.display.update()
        dt = fpsClock.tick(fps)
        
# This function updates the boids(and rectangle locations),pygame_gui buttons
def update(dt, boids, manager,list_of_rects):
    global debug,universal_follow_flag
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
                universal_follow_flag = not universal_follow_flag
                for boid in boids:
                    boid.follow_cursor = universal_follow_flag
                print(f"Follow Cursor: {not boid.follow_cursor}")
            elif event.ui_element == Wrap_button:
                for boid in boids:
                    boid.can_wrap = not boid.can_wrap
                print(f"Wrap?: {boid.can_wrap}")
            elif event.ui_element == debug_button:
                debug = not debug
                print(f"Debug Mode: {debug}")
        manager.process_events(event)
        
    for b in boids:
        b.update(dt, boids,list_of_rects,universal_follow_flag)
    manager.update(dt)

# Draws everything onto the main screen every frame
def draw(screen, background, boids,list_of_rects):
    global debug
    boids.clear(screen,background)
    if debug:
        screen.blit(background, (0, 0))
        for i in range(len(list_of_rects)):
            pg.draw.rect(screen,"red",list_of_rects[i])
    else:
        screen.blit(background, (0, 0))
    dirty_sprites = boids.draw(screen)
    pg.display.update(dirty_sprites)


if __name__ == "__main__":
    main()
