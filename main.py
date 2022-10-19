import math
import pygame
import random as r
from scipy.interpolate import interp1d as map_range

pygame.init()

disp = pygame.display

METER = 100 #1meter = 10000 pixels
K = 9 * (10**9)
MIN_DISTANCE = 0.005
Q = 10 * (10**(-9))
M = 0.01
PARTICLE_COUNT = 20
FULLSCREEN = False
DRAW_LINES = True

if FULLSCREEN:
    win = disp.set_mode((0, 0), pygame.FULLSCREEN)
else:
    win = disp.set_mode((900, 900))
draw = pygame.draw
disp.set_caption('MATEMATIKA MID')

class Vector:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return f"Vector({self.x}, {self.y})"
    
    def divide(self, X: float):
        return Vector(self.x / X, self.y / X)
    
    def mult(self, X: float):
        return Vector(self.x * X, self.y * X)
    
    def to_pixels(self):
        return self.mult(METER)

    def to_meters(self):
        return self.divide(METER)
    
    @property
    def tuple(self) -> tuple:
        return (self.x, self.y)
    
    @property
    def mag(self) -> float:
        return abs(math.sqrt((self.x**2) + (self.y**2)))
    
    @staticmethod
    def distance_x(v1, v2) -> float:
        dist = v2.x-v1.x
        f = math.copysign(max(abs(dist), MIN_DISTANCE), dist)
        return f
    
    @staticmethod
    def distance_y(v1, v2) -> float:
        dist = v2.y-v1.y
        f = math.copysign(max(abs(dist), MIN_DISTANCE), dist)
        return f
    
    @staticmethod
    def distance(v1, v2) -> float:
        distance = math.sqrt((Vector.distance_x(v1, v2)**2)+(Vector.distance_y(v1, v2)**2))
        return max(distance, MIN_DISTANCE)
    
    @staticmethod
    def random(x1, x2, x3='X', x4='X'):
        x3 = x1 if x3 == 'X' else x3
        x4 = x2 if x4 == 'X' else x4
        return Vector(r.randrange(x1, x2), r.randrange(x3, x4))
        
class Particle:
    acc = Vector(0, 0)
    vel = Vector(0, 0)
    colors = [(255, 51, 51), (51, 255, 51)]
    forces = []
    
    #Random position, sign and q charge if not passed as parameters.
    def __init__(self, pos=0, sign=0, q=0, m=M) -> None:
        self.pos = Vector.random(200, win.get_width()-200, 200, win.get_height()-200) if pos == 0 else pos
        self.pos = self.pos.to_meters()
        self.sign = r.choice([1, -1]) if sign == 0 else sign
        self.q = r.randrange(5, 20)*(10**(-9)) if q == 0 else q
        self.q = abs(self.q)*self.sign
        self.m = m

    def update(self) -> None:
        #Some kind of drag so particles dont go crazy
        self.vel.x *= 0.92
        self.vel.y *= 0.92
        
        self.vel.x += self.acc.x
        self.vel.y += self.acc.y
        
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        
        #print('\n'.join(map(str, self.forces)), end='\n__________________________________\n')
        self.forces = []
        self.acc = Vector(0, 0)
        print(self.pos.to_pixels().x)
        draw.circle(win, self.colors[0] if self.sign < 0 else self.colors[1], self.pos.to_pixels().tuple, 4)#abs(self.q)*(10**8.8))
    
    @property
    def x(self) -> float:
        return self.pos.x
    
    @property
    def y(self) -> float:
        return self.pos.y
    
    @staticmethod
    def apply_force(p, force) -> None:
        p.forces.append(force)
        p.acc.x += force.x/p.m
        p.acc.y += force.y/p.m
        
    @staticmethod
    def calc_force(p1, p2) -> None:
        q1q2 = abs(p1.q)*abs(p2.q)
        dist = Vector.distance(p1.pos, p2.pos)
        
        force_scalar = ( q1q2 / (dist**2) ) * K
        forcex, forcey = force_scalar*( Vector.distance_x(p1, p2)/dist ), force_scalar*( Vector.distance_y(p1, p2)/dist )
        #print(dist)
        
        if p1.sign == p2.sign:
            return Vector(-forcex, -forcey)
        
        return Vector(forcex, forcey)
   
particles = [
    Particle(q=Q) for x in range(PARTICLE_COUNT)
]
#Textbook example
#particles = [
#    Particle(Vector(500, 500), sign=-1, q=Q),#20*(10**(-9))),
#    Particle(Vector(600, 500), sign=1, q=Q),
#    Particle(Vector(700, 500), sign=-1, q=Q),
#]

clock = pygame.time.Clock()

while True:
    win.fill((51, 51, 51))
            
    for i in range(len(particles)):
        for j in range(len(particles)):
            if i == j:
                continue
            
            p1 = particles[i]
            p2 = particles[j]

            force = Particle.calc_force(p1, p2)
            Particle.apply_force(p1, force)

            if DRAW_LINES:
                draw.line(win, (150, 150, 150), (p1.pos.to_pixels().x, p1.pos.to_pixels().y), (p2.pos.to_pixels().x, p2.pos.to_pixels().y), max(1, min(3, round(force.mag*400))))
    [p.update() for p in particles]
    disp.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                quit()
            if event.key == pygame.K_SPACE:
                pygame.image.save(win, "screenshot.jpg")
    
    clock.tick(120)