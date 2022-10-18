import math
from numpy import ndarray
import pygame
import random as r
from scipy.interpolate import interp1d as map_range

pygame.init()

disp = pygame.display
win = disp.set_mode((1000, 1000))
draw = pygame.draw
METER = 10000
K = 9 * (10**9)
MIN_DISTANCE = 0.01
Q = 10 * (10**(-9))
M = 0.01

disp.set_caption('MATEMATIKA MID')
class Vector:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def divide(self, X: float):
        return Vector(self.x / X, self.y / X)
    
    def mult(self, X: float):
        return Vector(self.x * X, self.y * X)
    
    @property
    def mag(self) -> float:
        return abs(math.sqrt((self.x**2) + (self.y**2)))
    
    @staticmethod
    def distance_x(v1, v2) -> float:
        return (v2.x-v1.x)/METER
    
    @staticmethod
    def distance_y(v1, v2) -> float:
        return (v2.y-v1.y)/METER
    
    @staticmethod
    def distance(v1, v2) -> float:
        f = math.sqrt((Vector.distance_x(v1, v2)**2)+(Vector.distance_y(v1, v2)**2))
        return max(abs(f), MIN_DISTANCE)
    
    @staticmethod
    def random(x1, x2):
        return Vector(r.randrange(x1, x2), r.randrange(x1, x2))
        
class Particle:
    acc = Vector(0, 0)
    vel = Vector(0, 0)
    colors = [(255, 51, 51), (51, 255, 51)]
    
    def __init__(self, pos=0, sign=1, q=Q, m=M) -> None:
        self.pos = Vector.random(50, 750) if pos == 0 else pos
        self.sign = sign
        self.q = abs(q)*self.sign
        self.m = m

    def update(self) -> None:
        self.vel.x += self.acc.x
        self.vel.y += self.acc.y
        self.vel.x *= 0.9
        self.vel.y *= 0.9
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        
        self.acc = Vector(0, 0)
        draw.circle(win, self.colors[0] if self.sign < 0 else self.colors[1], (self.x, self.y), 4)
    
    @property
    def x(self) -> float:
        return self.pos.x
    
    @property
    def y(self) -> float:
        return self.pos.y
    
    @staticmethod
    def apply_force(p, force) -> None:
        p.acc.x += force.x/p.m
        p.acc.y += force.y/p.m
        
    @staticmethod
    def calc_force(p1, p2) -> None:
        q1q2 = abs(p1.q)*abs(p2.q)
        dist = Vector.distance(p1.pos, p2.pos)
        
        force_mag = ( q1q2 / (dist**2) ) * K
        forcex, forcey = force_mag*( Vector.distance_x(p1, p2)/dist ), force_mag*( Vector.distance_y(p1, p2)/dist )
        
        if p1.sign == p2.sign:
            return Vector(-forcex, -forcey)
        
        return Vector(forcex, forcey)
    
particles = [
    Particle(sign=r.choice([1, -1])) for x in range(10)
]

#Textbook example
#particles = [
#    Particle(Vector(400, 500), sign=-1, q=20*(10**(-9))),
#    Particle(Vector(600, 500), sign=1),
#    Particle(Vector(700, 500), sign=-1),
#]

clock = pygame.time.Clock()

while True:
    win.fill((51, 51, 51))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
            
    for i in range(len(particles)):
        for j in range(len(particles)):
            p1 = particles[i]
            p2 = particles[j]
            
            force1 = Particle.calc_force(p1, p2)
            Particle.apply_force(p1, force1)

            draw.line(win, (150, 150, 150), (p1.x, p1.y), (p2.x, p2.y), max(1, min(3, round(force1.mag*4000))))
            
    [p.update() for p in particles]
    disp.update()
    clock.tick(120)