from visual import *

rlist = []
xlist = []
ylist = []
zlist = []

START_RADIUS = 0.0
END_RADIUS = 0.0

PITCH_WIDTH = 305.0
PITCH_LENGTH = 2012.0
PITCH_THICKNESS = 10
CREASE_LENGTH = 122
XWASTE = 300.0

FY = 1120.0

SCALE = [(PITCH_WIDTH/(1080.0-(2*XWASTE))), 0.5, PITCH_LENGTH - (2*CREASE_LENGTH)]

# with open('coordinates_slow2.txt') as coord_file:
with open('coordinates_fast2.txt') as coord_file:
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

# Manually define start and end position radii
START_RADIUS = 16
END_RADIUS = 3.8

for i,radius in enumerate(rlist):   
    z = (START_RADIUS-radius)/(START_RADIUS-END_RADIUS)
    zlist.append(z*SCALE[2])

# textFile = open("3d_debug.txt", "w")

scene1 = display(title="Automated Cricket Umpiring - HawkEye", width=1280, height=720, range=10, background=(0.2,0.2,0.2), center=(0,30,30))
# Draw pitch floor
floor = box(pos=(0,0,0), size=(PITCH_LENGTH*1.2,PITCH_THICKNESS*1.2,PITCH_WIDTH), material=materials.unshaded, color=color.yellow)
floor_outer = box(pos=(0,0,0), size=(PITCH_LENGTH*1.25,PITCH_THICKNESS,PITCH_WIDTH*2), material=materials.unshaded, color=color.green)

# Draw wickets and crease lines at batting side
batting_wicket1 = box(pos=(PITCH_LENGTH/2,35.55,-8), size=(5,71.1,4), color=color.white)
batting_wicket2 = box(pos=(PITCH_LENGTH/2,35.55,0), size=(5,71.1,4), color=color.white)
batting_wicket3 = box(pos=(PITCH_LENGTH/2,35.55,8), size=(5,71.1,4), color=color.white)
line1 = box(pos=(PITCH_LENGTH/2,PITCH_THICKNESS/2,0), size=(10,5,264), color=color.white)
line2 = box(pos=(PITCH_LENGTH/2,PITCH_THICKNESS/2,132), size=(244,5,10), color=color.white)
line3 = box(pos=(PITCH_LENGTH/2,PITCH_THICKNESS/2,-132), size=(244,5,10), color=color.white)
line4 = box(pos=(PITCH_LENGTH/2-122,PITCH_THICKNESS/2,0), size=(10,5,366), color=color.white)

# Draw wickets at bowling side
bowling_wicket1 = box(pos=(-PITCH_LENGTH/2,35.55,-8), size=(5,71.1,4), color=color.white)
bowling_wicket2 = box(pos=(-PITCH_LENGTH/2,35.55,0), size=(5,71.1,4), color=color.white)
bowling_wicket3 = box(pos=(-PITCH_LENGTH/2,35.55,8), size=(5,71.1,4), color=color.white)
line1 = box(pos=(-PITCH_LENGTH/2,PITCH_THICKNESS/2,0), size=(10,5,264), color=color.white)
line2 = box(pos=(-PITCH_LENGTH/2,PITCH_THICKNESS/2,132), size=(244,5,10), color=color.white)
line3 = box(pos=(-PITCH_LENGTH/2,PITCH_THICKNESS/2,-132), size=(244,5,10), color=color.white)
line4 = box(pos=(-PITCH_LENGTH/2+122,PITCH_THICKNESS/2,0), size=(10,5,366), color=color.white)

balls = []

# Display balls with trail
yp = ylist[0]*FY/(FY+zlist[0])
zp = xlist[0]*FY/(FY+zlist[0])

balls.append(sphere(pos=(zlist[0]-((PITCH_LENGTH-2*CREASE_LENGTH)/2),yp, zp - 150), radius=6, color=color.red, make_trail=True, trail_type="points"))

# Without perspective correction
# balls.append(sphere(pos=(zlist[0]-((PITCH_LENGTH-2*CREASE_LENGTH)/2),ylist[0], xlist[0] - 150), radius=6, color=color.green, make_trail=True, trail_type="points"))

print "Start y: {}".format(balls[0].pos[1])

for i in range(1,len(xlist)):
    # rate(2)

    # Draw ball at previous position
    balls.append(sphere(pos=(zlist[i-1]-((PITCH_LENGTH-2*CREASE_LENGTH)/2),yp, zp - 150), radius=6, color=color.red))
    # textFile.write("{} {} {}\n".format(zlist[i]-300.0,ylist[i],xlist[i]-50))

    # Without perspective correction
    # balls.append(sphere(pos=(zlist[i-1]-((PITCH_LENGTH-2*CREASE_LENGTH)/2),ylist[i], xlist[i] - 150), radius=6, color=color.green))

    yp = ylist[i]*FY/(FY+zlist[i])
    zp = xlist[i]*FY/(FY+zlist[0])

    # New postion using vectors
    # vx = zlist[i]-(PITCH_LENGTH-2*CREASE_LENGTH)/2-balls[0].pos[0]
    # vy = yp-balls[0].pos[1]
    # vz = xlist[i]-150-balls[0].pos[2]
    # balls[0].pos += vector(vx,vy,vz)

    # Move ball0 to new position
    balls[0].pos = balls[i].pos

print "End y: {}\n".format(balls[-1].pos[1])

# sphere(pos=(0,0,0), radius=10, color=color.white)
# sphere(pos=(0,720,0), radius=10, color=color.red)
# sphere(pos=(0,360,0), radius=10, color=color.green)
# sphere(pos=(0,50,0), radius=10, color=color.blue)

# textFile.close()
coord_file.close()