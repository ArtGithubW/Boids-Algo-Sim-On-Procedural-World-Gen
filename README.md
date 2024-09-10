# Boids Algorithm Simulation on Procedural Generated World

## Features

This repo simulates flocks of birds flying around in a procedurally generated world. <br/>
Birds will avoid extremely high terrain like top of mountains. <br/>
There are some settings that the user can tweak and play around with.<br/>
More technical configurations is located in /Boid/config.py

## Dependencies

pip install pygame <br/>
pip install pygame_gui <br/>
pip install numpy <br/>
pip install perlin_noise

## 3 Main concepts of Boid:

1. Seperation(To make each boid not collide with eachother)
2. Alignment(To make boids align with other boids' forward velocity)
3. Cohesion(To make the boids move to the center of the flock)

https://vanhunteradams.com/Pico/Animal_Movement/Boids-algorithm.html

## Perlin noise:

https://medium.com/nerd-for-tech/generating-digital-worlds-using-perlin-noise-5d11237c29e9

### Notes:

- TODO LIST:
  figure out the numpy inhomogeneous shape after 1 dimension problem that is not consistent problem, caused by switching resolution <br/>
  combine colliding pygame.Rect objects into 1 object to optimize performance
  optimize world gen speed
