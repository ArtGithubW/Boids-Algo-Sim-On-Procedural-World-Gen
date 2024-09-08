# Procedual Generation:

- uses a gradient noise instead of white noise.

white noise: <br>

![alt text](image.png)

gradient noise: <br>
![alt text](image-2.png)

- We can use the gradient/perlin noise to create a height map and then map it to different materials.
- We can turn the generated 1D gradient/perlin noise into a 2D matrix

Perlin noise function can take in specified octaves. The higher the octaves, the higher the frequency of noise becomes
=> We can combine several perlin noise function outputs with different octaves to create a final cohesive perlin noise map.

How This Works:

1. Generate a 4 perlin noise lists and then put them in a 2D matrix list
2. Get the highest and lowest value in the 2D matrix for height map
3. Use the highest and lowest value in the height map matrix to compare to the weights of terrain to a new 2D integer matrix
4. This integer matrix is used to finalize the terrain generation

# Terrain Detection/Boid Collision Detection

1. We first use BFS on the integer map created from the procedural generation to find clumps of connecting terrain
2. Then we calculate the x and y mean of each clump to find the center of each clump
3. Then we create a rectangle object and expand from the center of each clump until the 4 edges of the rectangle does not cover the terrain anymore. => This is kinda dumb but I cant find a better way yet

- Step 2 and 3 can DEFINITELY be done in a better way. Brain needs to work better honestly
