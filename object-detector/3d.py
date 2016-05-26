from visual import *

rlist = []
xlist = []
ylist = []
zlist = []

START_RADIUS = 0.0
END_RADIUS = 0.0

PITCH_WIDTH = 305.0
PITCH_LENGTH = 2012.0
CREASE_LENGTH = 122
XWASTE = 300.0

SCALE = [(PITCH_WIDTH/(1080.0-(2*XWASTE))), 0.5, PITCH_LENGTH - (2*CREASE_LENGTH)]

with open('coordinates.txt') as coord_file:
	for i,row in enumerate(coord_file):
		x,y,r,frame_no,is_bouncing_pt,r_new,y_new= row.split()
		r_new = float(r_new)
		x = (float(x)-XWASTE)*0.5
		y = (720.0-float(y_new))*SCALE[1]
		# print x
		xlist.append(x)
		ylist.append(y)
		if i == 0:
			START_RADIUS = r_new
		END_RADIUS = r_new
		rlist.append(r_new)

for i,radius in enumerate(rlist):	
	z = (START_RADIUS-radius)/(START_RADIUS-END_RADIUS)
	zlist.append(z*SCALE[2])

# textFile = open("3d_debug.txt", "w")

# scene1 = display(title="BTP", x=0, y=0, width=800, height=600, range=10, background=color.white, center=(0,0,0))
floor = box(pos=(0,0,0), size=(PITCH_LENGTH,10,PITCH_WIDTH))

balls = []

for i in range(len(xlist)):
	balls.append(sphere(pos=(zlist[i]-884.0,ylist[i],xlist[i] - 150), radius=5, color=color.red))
	
	# textFile.write("{} {} {}\n".format(zlist[i]-300.0,ylist[i],xlist[i]-50))

# sphere(pos=(0,0,0), radius=10, color=color.white)
# sphere(pos=(0,720,0), radius=10, color=color.red)
# sphere(pos=(0,360,0), radius=10, color=color.green)
# sphere(pos=(0,50,0), radius=10, color=color.blue)

# textFile.close()
coord_file.close()