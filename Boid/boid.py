import pygame as pg
from random import uniform, randint


import pygame as pg
import random

class Vehicle(pg.sprite.Sprite):

    colors = [
        pg.Color('red'),
        pg.Color('green'),
        pg.Color('blue'),
        pg.Color('yellow'),
        pg.Color('purple'),
        pg.Color('orange')
    ]
    
    random_color = random.choice(colors)

    image = pg.Surface((10, 10), pg.SRCALPHA)
    pg.draw.polygon(image, random_color, [(5, 5), (0, 2), (0, 5)])

    def __init__(self, position, velocity, min_speed, max_speed,
                 max_force, can_wrap):

        super().__init__()

        # set limits
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.max_force = max_force

        # set position
        dimensions = len(position)
        assert (1 < dimensions < 4), "Invalid spawn position dimensions"

        if dimensions == 2:
            self.position = pg.Vector2(position)
            self.acceleration = pg.Vector2(0, 0)
            self.velocity = pg.Vector2(velocity)
        else:
            self.position = pg.Vector3(position)
            self.acceleration = pg.Vector3(0, 0, 0)
            self.velocity = pg.Vector3(velocity)

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
    
    def avoid_extremes(self):       #TODO: Check if the current vehicle object is on top of any extreme terrain(OCEAN_DEEP, or SNOW)
        return None

    def wrap(self):
        if self.position.x < 0:
            self.position.x += Vehicle.max_x
        elif self.position.x > Vehicle.max_x:
            self.position.x -= Vehicle.max_x

        if self.position.y < 0:
            self.position.y += Vehicle.max_y
        elif self.position.y > Vehicle.max_y:
            self.position.y -= Vehicle.max_y

    @staticmethod
    def set_boundary(edge_distance_pct):
        info = pg.display.Info()
        Vehicle.max_x = info.current_w
        Vehicle.max_y = info.current_h
        margin_w = Vehicle.max_x * edge_distance_pct / 100
        margin_h = Vehicle.max_y * edge_distance_pct / 100
        Vehicle.edges = [margin_w, margin_h, Vehicle.max_x - margin_w,
                         Vehicle.max_y - margin_h]

    def clamp_force(self, force):
        if 0 < force.magnitude() > self.max_force:
            force.scale_to_length(self.max_force)

        return force


class Boid(Vehicle):

    # CONFIG
    min_speed = 0.05
    max_speed = 0.20
    max_force = 1
    perception = 30 #* Distance where boids can "See" each other(Higher is bigger radius)
    crowding = 10 #* Distance between boids(lower is more crowded as there is less(no) seperation)
    can_wrap = False #* If boids can wrap to other side
    edge_distance_pct = 2 #* Distance before boids gets pushed back by the edges
    follow_cursor = True #* If boids follow the on-screen cursor

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
        for boid in boids: #? For each individual boid 
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
        return steering / 100

    def seek_cursor(self): 
        mouse_pos = pg.mouse.get_pos()
        mouse_vec = pg.Vector2(mouse_pos)
        desired_velocity = mouse_vec - self.position
        desired_velocity = desired_velocity.normalize() * self.max_speed
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
    
    def update(self, dt, boids):
        steering = pg.Vector2()

        if not self.can_wrap:
            steering += self.avoid_edge()

        neighbors = self.get_neighbors(boids)
        if neighbors:
            separation = self.separation(neighbors)
            alignment = self.alignment(neighbors)
            cohesion = self.cohesion(neighbors)

            steering += separation + alignment + cohesion

        if not self.follow_cursor:
            steering += self.seek_cursor()

        super().update(dt, steering)