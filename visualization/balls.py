from visual import *
from random import random

scene1 = display(title="BTP", x=0, y=0, width=800, height=600, range=10, background=color.white, center=(10,0,-10))

floor = box(pos=(50,0,0), size=(150,0.25,10))

balls = []

for i in range(10):
	balls.append(sphere(pos=(5*i, 5, 0), radius=2, color=(random(), random(), random())))
