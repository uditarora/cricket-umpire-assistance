from visual import *
import quadFit
import temp1

rlist = []
xlist = []
ylist = []
zlist = []
bouncing_pt = []
START_RADIUS = 0.0
END_RADIUS = 0.0

PITCH_WIDTH = 305.0
PITCH_LENGTH = 2012.0
PITCH_THICKNESS = 10
CREASE_LENGTH = 122
XWASTE = 405.4

FY = 1120.0

SCALE = [1, 0.5, PITCH_LENGTH - (2*CREASE_LENGTH)]

# with open('coordinates_slow2.txt') as coord_file:
with open('coordinates.txt') as coord_file:
    for i,row in enumerate(coord_file):
        x,y,r,frame_no,is_bouncing_pt,r_new,y_new= row.split()
        r_new = float(r_new)
        x = ((float(x)-XWASTE)*305/500)-152
        y = (720.0-float(y_new))*SCALE[1]
        bouncing_pt.append(int(is_bouncing_pt))
        # print x
        xlist.append(x)
        ylist.append(y)
        if i == 0:
            START_RADIUS = r_new
        END_RADIUS = r_new
        rlist.append(r_new)

# Manually define start and end position radii
START_RADIUS = 16
END_RADIUS = 3.5

for i,radius in enumerate(rlist):   
    z = (START_RADIUS-radius)/(START_RADIUS-END_RADIUS)
    zlist.append(z*SCALE[2])
    # zlist.append(((-162)*radius) + 1590)

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
FX = 300
# Display balls with trail
yp = ylist[0]*FY/(FY+zlist[0])
# yp = ylist[0] - ((z-700)/5)
zp = xlist[0]*zlist[0]/(FX+zlist[0])
# zp = xlist[0]*zlist[0]/300
# zp = xlist[0]
coords_3d = []
# balls.append(sphere(pos=(zlist[0]-((PITCH_LENGTH-2*CREASE_LENGTH)/2),yp, zp), radius=6, color=color.red, make_trail=True, trail_type="points"))

# Without perspective correction
# balls.append(sphere(pos=(zlist[0]-((PITCH_LENGTH-2*CREASE_LENGTH)/2),ylist[0], xlist[0] - 150), radius=6, color=color.green, make_trail=True, trail_type="points"))

# print "Start y: {}".format(balls[0].pos[1])

# y_correction = 0
for i in range(1,len(xlist)):
    # rate(2)

    # Draw ball at previous position
    # balls.append(sphere(pos=(zlist[i-1]-((PITCH_LENGTH-2*CREASE_LENGTH)/2),yp, zp - 150), radius=6, color=color.red))
    coords_3d.append((zlist[i-1]-((PITCH_LENGTH-2*CREASE_LENGTH)/2), yp, zp,1,bouncing_pt[i-1]))
    # if(bouncing_pt[i-1]):
    #     y_correction = i
    # coords_3d.append((zlist[i-1], yp, zp,1,bouncing_pt[i-1]))
    
    # textFile.write("{} {} {}\n".format(zlist[i]-300.0,ylist[i],xlist[i]-50))
    # Without perspective correction
    # balls.append(sphere(pos=(zlist[i-1]-((PITCH_LENGTH-2*CREASE_LENGTH)/2),ylist[i], xlist[i] - 150), radius=6, color=color.green))
    # yp = (ylist[i]*FY)/(FY+zlist[i])
    # zp = (xlist[i]*FY)/(FY+zlist[0])
    # Display balls with trail
    # yp = ylist[i] - ((zlist[i-1]-700)/5)
    yp = ylist[i]*FY/(FY+zlist[i])
    zp = xlist[i]*zlist[i]/(FX+zlist[i])
    # if zlist[i] < 300:
    #   zp = xlist[i]*zlist[i]/300
    # else:
    #   zp = xlist[i]  
    # zp = xlist[i]
    # New postion using vectors
    # vx = zlist[i]-(PITCH_LENGTH-2*CREASE_LENGTH)/2-balls[0].pos[0]
    # vy = yp-balls[0].pos[1]
    # vz = xlist[i]-150-balls[0].pos[2]
    # balls[0].pos += vector(vx,vy,vz)

    # Move ball0 to new position
    # balls[0].pos = balls[i].pos
coords_3d.append((zlist[i-1]-((PITCH_LENGTH-2*CREASE_LENGTH)/2), yp, zp,1,bouncing_pt[i-1]))
        
# print "End y: {}\n".format(balls[-1].pos[1])
quadraticReg = quadFit.quadraticRegression(coords_3d)
linearReg = temp1.quadraticRegression(coords_3d)
# y_correction = quadraticReg[y_correction - 1]
for i in range(1,len(coords_3d)+1):
    # rate(2)

    # Draw ball at previous position
    if coords_3d[i-1][0] > -400:
      balls.append(sphere(pos=(coords_3d[i-1][0],quadraticReg[i-1], linearReg[i-1]), radius=6, color=color.red))
coord_file.close()