import pygame as pg
from pygame.locals import *
import pygame_gui
from time import sleep

pg.init()

flags = DOUBLEBUF # Supposedly increases framerate
window_width, window_height = 720,480
screen = pg.display.set_mode((window_width, window_height), flags)
screen.set_alpha(None)
color = (0, 0, 0)
rec_color = (255,0,0)

clock = pg.time.Clock()


growth_rate = 2  # rate at which the rectangle expands
width, height = 1, 1  # initial size of the rectangle
center = (300, 300)
# Changing surface color
screen.fill(color)

pg.display.flip()
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Clear screen
    screen.fill((0, 0, 0))

    # Increase the size of the rectangle
    # width += growth_rate
    # height += growth_rate
    width,height = 200,200
    # if width >= 200:
    #     running = False
        
    # Calculate the top-left position to keep the rectangle centered
    rect_x = center[0] - width // 2
    rect_y = center[1] - height // 2

    rect_object = pg.Rect(rect_x, rect_y, width, height)
    # Draw the expanding rectangle
    pg.draw.rect(screen,rec_color,rect_object)

    # Update the display
    pg.display.flip()

    # Control the frame rate
    clock.tick(20)

# Quit pg
pg.quit()
