import sys
import pygame as pg
from random import uniform, randint
from config import * 

class Vehicle(pg.sprite.DirtySprite):

    image = pg.Surface((10, 10), pg.SRCALPHA)
    # The color is black but it is half transparent
    pg.draw.polygon(image, (0, 0, 0, 128), [(3, 3), (0, 1), (0, 3)])

    def __init__(self, position, velocity, min_speed, max_speed,
                 max_force, can_wrap):

        super().__init__()

        # set limits
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.max_force = max_force


        self.position = pg.Vector2(position)
        self.acceleration = pg.Vector2(0, 0)
        self.velocity = pg.Vector2(velocity)


        self.heading = 0.0

        self.rect = self.image.get_rect(center=self.position)

    def update(self, dt, steering):
        self.acceleration = steering * dt

        # enforce turn limit
        _, old_heading = self.velocity.as_polar()
        new_velocity = self.velocity + self.acceleration * dt
        speed, new_heading = new_velocity.as_polar()

        heading_diff = 180 - (180 - new_heading + old_heading) % 360
        if abs(heading_diff) > 6:
            if heading_diff > 6:
                new_heading = old_heading + 10
            else:
                new_heading = old_heading - 10

        self.velocity.from_polar((speed, new_heading))

        # enforce speed limit
        speed, self.heading = self.velocity.as_polar()
        if speed < self.min_speed:
            self.velocity.scale_to_length(self.min_speed)

        if speed > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        # move
        self.position += self.velocity * dt

        if self.can_wrap:
            self.wrap()

        # draw
        self.image = pg.transform.rotate(Vehicle.image, -self.heading)
        self.rect = self.image.get_rect(center=self.position)

    def avoid_edge(self):
        left = self.edges[0] - self.position.x
        up = self.edges[1] - self.position.y
        right = self.position.x - self.edges[2]
        down = self.position.y - self.edges[3]

        scale = max(left, up, right, down)

        if scale > 0:
            center = (Vehicle.max_x / 2, Vehicle.max_y / 2)
            steering = pg.Vector2(center)
            steering -= self.position
        else:
            steering = pg.Vector2()

        return steering

    def wrap(self):
        if self.position.x < 0:
            self.position.x += Vehicle.max_x
        elif self.position.x > Vehicle.max_x:
            self.position.x -= Vehicle.max_x

        if self.position.y < 0:
            self.position.y += Vehicle.max_y
        elif self.position.y > Vehicle.max_y:
            self.position.y -= Vehicle.max_y

    def clamp_force(self, force):
        if force.magnitude() > self.max_force:
            force.scale_to_length(self.max_force)

        return force
    
    @staticmethod
    def set_boundary(edge_distance_pct):
        Vehicle.max_x = WINDOW_WIDTH
        Vehicle.max_y = WINDOW_HEIGHT
        margin_w = Vehicle.max_x * edge_distance_pct / 100
        margin_h = Vehicle.max_y * edge_distance_pct / 100
        Vehicle.edges = [margin_w, margin_h, Vehicle.max_x - margin_w,
                         Vehicle.max_y - margin_h]



class Boid(Vehicle):
    
    min_speed = MIN_SPEED 
    max_speed = MAX_SPEED 
    max_force = MAX_FORCE 
    perception = PERCEPTION 
    crowding = CROWDING 
    can_wrap = CAN_WRAP 
    edge_distance_pct = EDGE_DISTANCE_PCT 

    def __init__(self):
        Boid.set_boundary(Boid.edge_distance_pct)

        # Randomizing starting position and velocity
        start_position = pg.math.Vector2(
            uniform(0, Boid.max_x),
            uniform(0, Boid.max_y))
        start_velocity = pg.math.Vector2(
            uniform(-1, 1) * Boid.max_speed,
            uniform(-1, 1) * Boid.max_speed)

        super().__init__(start_position, start_velocity,
                         Boid.min_speed, Boid.max_speed,
                         Boid.max_force, Boid.can_wrap)

        self.rect = self.image.get_rect(center=self.position)
        self.color = (randint(0, 255), randint(0, 255), randint(0, 255))

    def separation(self, boids):
        steering = pg.Vector2()
        for boid in boids: 
            dist = self.position.distance_to(boid.position)
            if (dist < self.crowding and self.crowding > 0):
                steering -= (boid.position - self.position)
        steering = self.clamp_force(steering)
        return steering

    def alignment(self, boids):
        steering = pg.Vector2()
        for boid in boids:
            steering += boid.velocity
        steering /= len(boids)
        steering -= self.velocity
        steering = self.clamp_force(steering)
        return steering / 8

    def cohesion(self, boids):
        steering = pg.Vector2()
        for boid in boids:
            steering += boid.position
        steering /= len(boids)
        steering -= self.position
        steering = self.clamp_force(steering)
        return steering / 120

    def seek_cursor(self):  
        mouse_pos = pg.mouse.get_pos()
        mouse_vec = pg.Vector2(mouse_pos)
        desired_velocity = mouse_vec - self.position
        steering = desired_velocity - self.velocity
        return self.clamp_force(steering)

    def get_neighbors(self, boids):
        neighbors = []
        for boid in boids:
            if boid != self:
                dist = self.position.distance_to(boid.position)
                if dist < self.perception:
                    neighbors.append(boid)
        return neighbors
    
    
    def avoid_rectangle(self, rect):
        # 2d vector from the center of the rectangle outwards
        rect_center = pg.Vector2(rect.center)

        # Create a steering force away from the rectangle's center
        steering = (self.position - rect_center)
        steering -= self.velocity  # Calculate the steering force relative to current velocity
        return self.clamp_force(steering)

    # Updates steering and calls Vehicle's update() to update the current position and velocity, why did I write it this way
    def update(self, dt, boids, list_of_rects,follow_cursor):
        steering = pg.Vector2()

        if not self.can_wrap:
            steering += self.avoid_edge()

        neighbors = self.get_neighbors(boids)
        if neighbors:
            separation = self.separation(neighbors)
            alignment = self.alignment(neighbors)
            cohesion = self.cohesion(neighbors)

            steering += separation + alignment + cohesion

        if  follow_cursor:
            steering += self.seek_cursor()
        for rect in list_of_rects:
            if rect.collidepoint((self.position.x,self.position.y)):
                # print("Collision!")
                steering += self.avoid_rectangle(rect)
        super().update(dt, steering)


'''
Function to create boid objects
'''
def add_boids(boids, num_boids):
    for _ in range(num_boids):
        boids.add(Boid())