from helper import GenNoiseMap,GenIntMap
import pygame
from config import * 


noise_map = GenNoiseMap()
map_int = GenIntMap(noise_map)



# Now we draw the map_int 
pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

for y, row in enumerate(map_int):
    for x, value in enumerate(row):
        if x == WINDOW_WIDTH or y == WINDOW_HEIGHT: #If we hit the edges then move on
            continue
        # Use the color map to set individual pixel at set map_int locations
        color = COLOR_MAP[value]
        display_surface.set_at((x, y), color)


pygame.display.flip() # Show the screen
while True:
    event = pygame.event.wait()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
            pygame.quit()
            quit()
        break