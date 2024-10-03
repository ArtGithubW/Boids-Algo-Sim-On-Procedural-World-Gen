# Boids Algorithm Simulation on Procedural Generated World

## Features

This repo simulates flocks of birds flying around in a procedurally generated world. <br/>
Birds will avoid extremely high terrain like top of mountains. <br/>
There are some settings that the user can tweak and play around with.<br/>
More technical configurations is located in /Boid/config.py

![Generation1](https://github.com/user-attachments/assets/6c34ef9a-0a09-4ab6-97a3-0e89def8f1f0) <br/>
![Generation2](https://github.com/user-attachments/assets/27ee3ff6-9290-4b46-884b-4a795d692471)

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
  Add sliders to the side to be able to modify seperation, alignment, and cohesion on the fly <br/>
  figure out the numpy inhomogeneous shape after 1 dimension problem that is not consistent problem, caused by resolution(?) <br/>
  combine colliding pygame.Rect objects into 1 object to optimize performance <br/>
  optimize world gen speed
