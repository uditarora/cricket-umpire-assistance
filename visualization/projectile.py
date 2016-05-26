from visual import *
from math import sin,cos

initialHeight = 4.6
initialVelocity = 10
initialVelocity2 = 10
Angle = 65
Angle2 = 75

bounce_effect = -2

# Set up the display window
scene1 = display(title="Projectile motion zach miller", x=0, y=0, width=800, height=600, range=10, background=color.white, center=(10,initialHeight,0))

# Create objects
table = box(pos=(-1,initialHeight-1,0), size=(5,1,4))
ball1 = sphere(pos=(0,initialHeight,0), radius=1, color=color.green, make_trail=True)
ball2 = sphere(pos=(0,initialHeight,0), radius=1, color=color.red, make_trail=True)

floor = box(pos=(0,0,0), size=(100,0.25,10))

t = 0
dt = 0.01
g = -9.8

Fgrav = vector(0,g*dt,0)

# Velocity vector for ball
ball1v = vector(initialVelocity*cos(Angle*pi/180), initialVelocity*sin(Angle*pi/180), 0)
ball2v = vector(initialVelocity2*cos(Angle2*pi/180), initialVelocity2*sin(Angle2*pi/180), 0)

# Put balls in motion
while True:
	rate(300)
	ball1v = ball1v + Fgrav
	ball2v = ball2v + Fgrav
	ball1.pos += ball1v*dt
	ball2.pos += ball2v*dt
	if ball1.y < 0:
		ball1v.y = -ball1v.y + bounce_effect

	if ball2.y < 0:
		ball2v.y = -ball2v.y + bounce_effect

	t += dt

	if ball1.z > table.z:
		break