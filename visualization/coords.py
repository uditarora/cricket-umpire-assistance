from visual import *

rlist = []
xlist = []
ylist = []
zlist = []

START_RADIUS = 0.0
FINISH_RADIUS = 0.0

PITCH_WIDTH = 400.0
PITCH_LENGTH = 1000.0
XWASTE = 350.0

SCALE = [(PITCH_WIDTH/(1080.0-XWASTE)), 0.3, 1000.0]

with open('rad.txt') as rad_file:
	for i,row in enumerate(rad_file):
		_,_,_,r = row.split()
		r = float(r)
		if i == 0:
			START_RADIUS = r
		END_RADIUS = r
		rlist.append(r)

for radius in rlist:
	z = (START_RADIUS-radius)/(START_RADIUS-FINISH_RADIUS)
	zlist.append(z*SCALE[2])

with open('XY.txt') as xy_file:
	for row in xy_file:
		_,x,_,y = row.split()
		x = (float(x)-XWASTE)*SCALE[0]
		y = (720.0-float(y))*SCALE[1]
		xlist.append(x)
		ylist.append(y)

textFile = open("coordinates.txt", "w")

# scene1 = display(title="BTP", x=0, y=0, width=800, height=600, range=10, background=color.white, center=(-500,100,0))
floor = box(pos=(0,0,0), size=(PITCH_LENGTH,10,PITCH_WIDTH))

balls = []

for i in range(len(xlist)):
	balls.append(sphere(pos=(zlist[i]-300.0,ylist[i],xlist[i]-50), radius=5, color=color.red))
	textFile.write("{} {} {}\n".format(zlist[i]-300.0,ylist[i],xlist[i]-50))

# sphere(pos=(0,0,0), radius=10, color=color.white)
# sphere(pos=(0,0,50), radius=10, color=color.red)
# sphere(pos=(50,0,0), radius=10, color=color.green)
# sphere(pos=(0,50,0), radius=10, color=color.blue)

# Draw wickets
wicket1 = box(pos=(400,50,-10), size=(5,100,5), color=color.yellow)
wicket2 = box(pos=(400,50,0), size=(5,100,5), color=color.yellow)
wicket1 = box(pos=(400,50,10), size=(5,100,5), color=color.yellow)

textFile.close()
