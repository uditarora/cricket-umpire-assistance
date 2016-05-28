from visual import *
import quadFit
import temp1

rlist = []
xlist = []
ylist = []
zlist = []
bouncing_pt = []
frames_list = []

FPS = 120.0

START_RADIUS = 0.0
END_RADIUS = 0.0
# Manually define start and end position radii
START_RADIUS = 16
# END_RADIUS = 4.5
# WICKET_RADIUS = 4

END_RADIUS = 3.5
WICKET_RADIUS = 3.2

PITCH_WIDTH = 305.0
PITCH_LENGTH = 2012.0
PITCH_THICKNESS = 10
CREASE_LENGTH = 122
XWASTE = 405.4

WICKET_HEIGHT = 71.1
WICKET_WIDTH = 22.86
STUMP_WIDTH = 4.5

WIDE_WIDTH = 264
LINE_WIDTH = 5

BALL_RADIUS = 3.6

FY = 1520.0

SCALE = [1, 0.5, PITCH_LENGTH - (2*CREASE_LENGTH)]

# Stores the index of the bouncing point
bouncing_pt_idx = -1

# Find world coordinates
# with open('coordinates_wideright.txt') as coord_file:
with open('coordinates_bouncer.txt') as coord_file:
# with open('coordinates_171638.txt') as coord_file:  # LBW
# with open('coordinates_171124.txt') as coord_file:    # Spin
# with open('coordinates_slow2.txt') as coord_file:   # Spin
# with open('coordinates_171619.txt') as coord_file:    # Fast ball
    for i,row in enumerate(coord_file):
        x,y,r,frame_no,is_bouncing_pt,r_new,y_new= row.split()
        r_new = float(r_new)
        x = ((float(x)-XWASTE)*305/500)-152
        y = (720.0-float(y_new))*SCALE[1]
        bouncing_pt.append(int(is_bouncing_pt))
        if int(is_bouncing_pt) == 1:
            bouncing_pt_idx = i
        # print x
        xlist.append(x)
        ylist.append(y)
        frames_list.append(float(frame_no))
        # if i == 0:
        #     START_RADIUS = r_new
        # END_RADIUS = r_new
        rlist.append(r_new)

for i,radius in enumerate(rlist):   
    z = (START_RADIUS-radius)/(START_RADIUS-END_RADIUS)
    zlist.append(z*SCALE[2])

# textFile = open("3d_debug.txt", "w")
coord_file.close()

# Draw environment
scene1 = display(title="Automated Cricket Umpiring - HawkEye", width=1280, height=720, range=10, background=(0.2,0.2,0.2), center=(0,30,30))
# Draw pitch floor
floor = box(pos=(0,0,0), size=(PITCH_LENGTH*1.2,PITCH_THICKNESS*1.2,PITCH_WIDTH), material=materials.unshaded, color=(0.97,0.94,0.6))
floor_outer = box(pos=(0,0,0), size=(PITCH_LENGTH*1.25,PITCH_THICKNESS,PITCH_WIDTH*2), material=materials.unshaded, color=(0.2,0.7,0.27))
floor_impact = box(pos=(0,0,0), size=(PITCH_LENGTH,PITCH_THICKNESS*1.3,WICKET_WIDTH), material=materials.unshaded, color=(0.63,0.57,0.93), opacity=0.8)

# Draw wickets and crease lines at batting side
batting_wicket1 = box(pos=(PITCH_LENGTH/2,WICKET_HEIGHT/2,-(WICKET_WIDTH/2-STUMP_WIDTH/2)), size=(5,WICKET_HEIGHT,STUMP_WIDTH), color=color.white)
batting_wicket2 = box(pos=(PITCH_LENGTH/2,WICKET_HEIGHT/2,0), size=(5,WICKET_HEIGHT,STUMP_WIDTH), color=color.white)
batting_wicket3 = box(pos=(PITCH_LENGTH/2,WICKET_HEIGHT/2,(WICKET_WIDTH/2-STUMP_WIDTH/2)), size=(5,WICKET_HEIGHT,STUMP_WIDTH), color=color.white)
line1 = box(pos=(PITCH_LENGTH/2,PITCH_THICKNESS/2,0), size=(LINE_WIDTH,5,WIDE_WIDTH), color=color.white)
line2 = box(pos=(PITCH_LENGTH/2,PITCH_THICKNESS/2,132), size=(244,5,LINE_WIDTH), color=color.white)
line3 = box(pos=(PITCH_LENGTH/2,PITCH_THICKNESS/2,-132), size=(244,5,LINE_WIDTH), color=color.white)
line4 = box(pos=(PITCH_LENGTH/2-122,PITCH_THICKNESS/2,0), size=(LINE_WIDTH,5,366), color=color.white)

# Draw wickets at bowling side
bowling_wicket1 = box(pos=(-PITCH_LENGTH/2,WICKET_HEIGHT/2,-(WICKET_WIDTH/2-STUMP_WIDTH/2)), size=(5,WICKET_HEIGHT,STUMP_WIDTH), color=color.white)
bowling_wicket2 = box(pos=(-PITCH_LENGTH/2,WICKET_HEIGHT/2,0), size=(5,WICKET_HEIGHT,STUMP_WIDTH), color=color.white)
bowling_wicket3 = box(pos=(-PITCH_LENGTH/2,WICKET_HEIGHT/2,(WICKET_WIDTH/2-STUMP_WIDTH/2)), size=(5,WICKET_HEIGHT,STUMP_WIDTH), color=color.white)
line1 = box(pos=(-PITCH_LENGTH/2,PITCH_THICKNESS/2,0), size=(LINE_WIDTH,5,WIDE_WIDTH), color=color.white)
line2 = box(pos=(-PITCH_LENGTH/2,PITCH_THICKNESS/2,132), size=(244,5,LINE_WIDTH), color=color.white)
line3 = box(pos=(-PITCH_LENGTH/2,PITCH_THICKNESS/2,-132), size=(244,5,LINE_WIDTH), color=color.white)
line4 = box(pos=(-PITCH_LENGTH/2+122,PITCH_THICKNESS/2,0), size=(LINE_WIDTH,5,366), color=color.white)


# Draw balls
balls = []
FX = 250
# Display balls with trail
yp = ylist[0]*FY/(FY+zlist[0])
# yp = ylist[0] - ((z-700)/5)
zp = xlist[0]*zlist[0]/(FX+zlist[0])
# zp = xlist[0]*zlist[0]/300
# zp = xlist[0]

# List of (x,y,z,*waste-remove later*,bouncing_pt)
coords_3d = []
# balls.append(sphere(pos=(zlist[0]-((PITCH_LENGTH-2*CREASE_LENGTH)/2),yp, zp), radius=6, color=color.red, make_trail=True, trail_type="points"))

# y_correction = 0

num_detected_points = len(xlist)
for i in range(len(xlist)):
    # rate(2)

    yp = ylist[i]*FY/(FY+zlist[i])
    zp = xlist[i]*zlist[i]/(FX+zlist[i])

    # Draw ball at current position
    # balls.append(sphere(pos=(zlist[i-1]-((PITCH_LENGTH-2*CREASE_LENGTH)/2),yp, zp - 150), radius=6, color=color.red))
    coords_3d.append((zlist[i]-((PITCH_LENGTH-2*CREASE_LENGTH)/2), yp, zp,1,bouncing_pt[i]))

    # if(bouncing_pt[i]):
    #     y_correction = i
    # coords_3d.append((zlist[i], yp, zp,1,bouncing_pt[i]))
    
    # textFile.write("{} {} {}\n".format(zlist[i]-300.0,ylist[i],xlist[i]-50))
    
    # if zlist[i] < 300:
    #   zp = xlist[i]*zlist[i]/300
    # else:
    #   zp = xlist[i]  
    # zp = xlist[i]

quadraticReg = quadFit.quadraticRegression(coords_3d)
linearReg = temp1.quadraticRegression(coords_3d)

# Append predicted points to coords_3d list
for idx in range(1,300):
    coords_3d.append(((coords_3d[num_detected_points-1][0] + idx),0,0,0,0))

# y_correction = quadraticReg[y_correction - 1]

# Stores the final regressed 3D coordinates
final_coords_3d = []

# Draw balls at detected points
for idx in range(num_detected_points):
    # rate(2)
    final_coords_3d.append((coords_3d[idx][0],quadraticReg[idx], linearReg[idx]))
    # Draw detected ball at position
    if coords_3d[idx][0] > -400:
        balls.append(sphere(pos=(coords_3d[idx][0],quadraticReg[idx], linearReg[idx]), radius=BALL_RADIUS, color=(0.52,0.15,0.19)))
        # balls.append(sphere(pos=(coords_3d[idx][0],quadraticReg[idx], coords_3d[idx][2]), radius=6, color=color.blue))
        # Draw cylindrical trajectory
        if idx > 0:
            displacement = (final_coords_3d[idx][0]-final_coords_3d[idx-1][0], final_coords_3d[idx][1]-final_coords_3d[idx-1][1], final_coords_3d[idx][2]-final_coords_3d[idx-1][2])
            cylinder(pos=(final_coords_3d[idx-1][0], final_coords_3d[idx-1][1], final_coords_3d[idx-1][2]), axis=displacement, radius=BALL_RADIUS, color=(0.52,0.15,0.19), opacity=0.3)

for idx in range(num_detected_points, len(coords_3d)):
    final_coords_3d.append((coords_3d[idx][0],quadraticReg[idx], linearReg[idx]))

# Draw balls at predicted points
STEP_SIZE = 20
for idx in range(num_detected_points, len(coords_3d),20):
    # rate(2)
    # Draw predicted ball at position, skipping 20 positions
    if coords_3d[idx][0] > -400:
        balls.append(sphere(pos=(coords_3d[idx][0],quadraticReg[idx], linearReg[idx]), radius=BALL_RADIUS, color=color.blue, opacity=0.8))
        # balls.append(sphere(pos=(coords_3d[idx][0],quadraticReg[idx], coords_3d[idx][2]), radius=6, color=color.blue))
        # Draw cylindrical trajectory
        if idx-STEP_SIZE > 0 and idx > num_detected_points:
            displacement = (final_coords_3d[idx][0]-final_coords_3d[idx-STEP_SIZE][0], final_coords_3d[idx][1]-final_coords_3d[idx-STEP_SIZE][1], final_coords_3d[idx][2]-final_coords_3d[idx-STEP_SIZE][2])
            cylinder(pos=(final_coords_3d[idx-STEP_SIZE][0], final_coords_3d[idx-STEP_SIZE][1], final_coords_3d[idx-STEP_SIZE][2]), axis=displacement, radius=BALL_RADIUS, color=color.blue, opacity=0.3)

# Stores the speed at given index
speed_list = []
# Stores the average delivery speed before bounce
average_speed = 0.0

# Calculate speed at detected points
for idx in range(num_detected_points):
    if idx == 0:
        speed_list.append(0)
    else:
        displacement = vector(final_coords_3d[idx][0]-final_coords_3d[idx-1][0], final_coords_3d[idx][1]-final_coords_3d[idx-1][1], final_coords_3d[idx][2]-final_coords_3d[idx-1][2])
        time = float(frames_list[idx]-frames_list[idx-1])/FPS
        speed = (mag(displacement)/time)*3.6/100
        speed_list.append(speed)
        if idx <= bouncing_pt_idx:
            average_speed += speed

    # Debug printing
    # print "Speed[{}]: {}".format(idx, speed_list[idx])
    # if idx > 1 and abs(speed_list[idx]-speed_list[idx-1])/speed_list[idx-1] > 0.1:
    #     print "\nAnomally detected at idx: {} and frame_no: {}".format(idx, frames_list[idx])
    #     print "x1: {}, y1: {}, z1: {}\nx2: {}, y2: {}, z2: {}\n".format(final_coords_3d[idx-1][0], final_coords_3d[idx-1][1], final_coords_3d[idx-1][2], final_coords_3d[idx][0], final_coords_3d[idx][1], final_coords_3d[idx][2])
    #     box(pos=(final_coords_3d[idx][0],final_coords_3d[idx][1]/2,final_coords_3d[idx][2]), size=(5,final_coords_3d[idx][1],5))

average_speed = average_speed/(bouncing_pt_idx+1)

print "Speed of delivery: {:.3f} km/h".format(average_speed)


""" Umpiring decisions below """

def get_nearest_ball_params(near_crease=False):
    """
        Returns the index of the ball closest to wicket, absolute difference in position
        of nearest ball, and index of the last ball just before the wicket
    """
    near_wicket_idx = 0
    before_wicket_idx = num_detected_points-1
    min_diff = 1000000

    # The distance from which to check nearest ball
    dist = PITCH_LENGTH/2
    if near_crease:
        dist = PITCH_LENGTH/2-122

    for i in range(len(final_coords_3d)):
        diff = abs(dist-final_coords_3d[i][0])
        if diff < min_diff:
            min_diff = diff
            near_wicket_idx = i
        if dist-final_coords_3d[i][0] < 0 and before_wicket_idx == num_detected_points-1:
            before_wicket_idx = i-1
    return near_wicket_idx, min_diff, before_wicket_idx

def get_nearest_ball_coords(idx, min_diff, before_wicket_idx, near_crease=False):
    """
        Returns the y and z coordinates of the ball closest to the wicket
    """

    # The distance from which to check nearest ball
    dist = PITCH_LENGTH/2
    if near_crease:
        dist = PITCH_LENGTH/2-122

    # There is a ball position at the wicket
    if abs(min_diff) <= 1:
        y = final_coords_3d[idx][1]
        z = final_coords_3d[idx][2]
        return y, z
    else:
        # Find coordinates of ball at wicket using linear approximation
        y2 = final_coords_3d[before_wicket_idx+1][1]
        y1 = final_coords_3d[before_wicket_idx][1]
        z2 = final_coords_3d[before_wicket_idx+1][2]
        z1 = final_coords_3d[before_wicket_idx][2]
        x2 = final_coords_3d[before_wicket_idx+1][0]
        x1 = final_coords_3d[before_wicket_idx][0]

        slopey = (y2-y1)/(x2-x1)
        slopez = (z2-z1)/(x2-x1)
        ynew = y1 + slopey*(dist-x1)
        znew = z1 + slopez*(dist-x1)

        # print "x2: {}, y2: {}, z2: {}\nx1: {}, y1: {}, z1: {}\nslopey: {}, slopez: {}".format(x2,y2,z2,x1,y1,z1,slopey,slopez)

        return ynew, znew

# Check LBW Decision
def check_lbw():
    """
        Checks if the ball delivery would result in lbw
    """
    near_wicket_idx, min_diff, before_wicket_idx = get_nearest_ball_params()

    # print "Min_diff: {}, near_wicket_idx: {}".format(min_diff, near_wicket_idx)

    # If bouncing point found, check if the bounce is in the impact zone or on off side (only right hand batting)
    # Bounce found and in impace zone
    if bouncing_pt_idx != -1 and final_coords_3d[bouncing_pt_idx][2] <= WICKET_WIDTH/2:
        if final_coords_3d[bouncing_pt_idx][2] >= -WICKET_WIDTH/2:
            print "PITCHING: INSIDE IMACT ZONE"
        else:
            print "PITCHING: OUTSIDE OFF"
        # Check if last point in impact zone
        if final_coords_3d[num_detected_points-1][2] >= -(WICKET_WIDTH/2+BALL_RADIUS) and final_coords_3d[num_detected_points-1][2] <= (WICKET_WIDTH/2+BALL_RADIUS):
            print "IMPACT: IN-LINE"
            return check_nearest_coord(near_wicket_idx, min_diff, before_wicket_idx)
        else:
            print "IMPACT: OUTSIDE"
            return False
    # No bounce point found
    elif bouncing_pt_idx == -1:
        print "PITCHING: NO BOUNCE"
        if final_coords_3d[num_detected_points-1][2] >= -(WICKET_WIDTH/2+BALL_RADIUS) and final_coords_3d[num_detected_points-1][2] <= (WICKET_WIDTH/2+BALL_RADIUS):
            print "IMPACT: IN-LINE"
            return check_nearest_coord(near_wicket_idx, min_diff, before_wicket_idx)
        else:
            print "IMPACT: OUTSIDE"
            return False
    # Bounce out of impact zone
    else:
        print "PITCHING: OUTSIDE LEG"
        return False

def check_nearest_coord(idx, min_diff, before_wicket_idx):
    """
        Checks if the ball hits the wicket
    """
    # Get y,z coordinates of ball closeset to wicket
    y, z = get_nearest_ball_coords(idx, min_diff, before_wicket_idx)

    if y <= (WICKET_HEIGHT+BALL_RADIUS) and z >= -(WICKET_WIDTH/2+BALL_RADIUS) and z <= WICKET_WIDTH/2+BALL_RADIUS:
        return True
    else:
        return False

if check_lbw():
    print "WICKETS: HITTING"
    print "\nLBW DECISION: OUT"
else:
    print "WICKETS: NOT HITTING"
    print "\nLBW DECISION: NOT-OUT"

# Check Wide Decision
def check_wide():
    """
        Checks if the ball delivery would result in wide decision
    """
    # Get y,z coordinates of the ball closest to crease
    near_wicket_idx, min_diff, before_wicket_idx = get_nearest_ball_params(near_crease=True)
    y, z = get_nearest_ball_coords(near_wicket_idx, min_diff, before_wicket_idx, near_crease=True)


    # Wide debug displays
    # box(pos=(final_coords_3d[before_wicket_idx][0],y/2,z), size=(10,y,5))
    # print "Y: {}, Z: {}".format(y,z)

    if z <= -(WIDE_WIDTH/2-LINE_WIDTH-BALL_RADIUS) or z >= (WICKET_WIDTH+BALL_RADIUS):
        return True
    else:
        return False

if check_wide():
    print "\nWIDE DECISION: WIDE"
else:
    print "\nWIDE DECISION: NOT WIDE"

def check_bouncer():
    """
        Checks if the ball delivery would result in bouncer
    """
    # Get y,z coordinates of the ball closest to crease
    near_wicket_idx, min_diff, before_wicket_idx = get_nearest_ball_params(near_crease=True)
    y, z = get_nearest_ball_coords(near_wicket_idx, min_diff, before_wicket_idx, near_crease=True)

