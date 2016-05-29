from cv2 import imread, imshow, waitKey, GaussianBlur, findContours, drawContours, RETR_TREE, CHAIN_APPROX_SIMPLE,\
    equalizeHist, circle, CHAIN_APPROX_NONE, minEnclosingCircle
import cv2
import math
import random
import glob 
import numpy as np

THRESHOLD = 75.0
MAX_INTENSITY = 255
MIN_INTENSITY = 0

############################### CODE FOR MINIMAL ENCLOSING CIRCLE #########################################
 
def make_circle(points):
    # Convert to float and randomize order
    shuffled = [(float(p[0]), float(p[1])) for p in points]
    random.shuffle(shuffled)
    
    # Progressively add points to circle or recompute circle
    c = None
    for (i, p) in enumerate(shuffled):
        if c is None or not _is_in_circle(c, p):
            c = _make_circle_one_point(shuffled[0 : i + 1], p)
    return c


# One boundary point known
def _make_circle_one_point(points, p):
    c = (p[0], p[1], 0.0)
    for (i, q) in enumerate(points):
        if not _is_in_circle(c, q):
            if c[2] == 0.0:
                c = _make_diameter(p, q)
            else:
                c = _make_circle_two_points(points[0 : i + 1], p, q)
    return c


# Two boundary points known
def _make_circle_two_points(points, p, q):
    diameter = _make_diameter(p, q)
    if all(_is_in_circle(diameter, r) for r in points):
        return diameter
    
    left = None
    right = None
    for r in points:
        cross = _cross_product(p[0], p[1], q[0], q[1], r[0], r[1])
        c = _make_circumcircle(p, q, r)
        if c is None:
            continue
        elif cross > 0.0 and (left is None or _cross_product(p[0], p[1], q[0], q[1], c[0], c[1]) > _cross_product(p[0], p[1], q[0], q[1], left[0], left[1])):
            left = c
        elif cross < 0.0 and (right is None or _cross_product(p[0], p[1], q[0], q[1], c[0], c[1]) < _cross_product(p[0], p[1], q[0], q[1], right[0], right[1])):
            right = c
    return left if (right is None or (left is not None and left[2] <= right[2])) else right


def _make_circumcircle(p0, p1, p2):
    # Mathematical algorithm from Wikipedia: Circumscribed circle
    ax = p0[0]; ay = p0[1]
    bx = p1[0]; by = p1[1]
    cx = p2[0]; cy = p2[1]
    d = (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by)) * 2.0
    if d == 0.0:
        return None
    x = ((ax * ax + ay * ay) * (by - cy) + (bx * bx + by * by) * (cy - ay) + (cx * cx + cy * cy) * (ay - by)) / d
    y = ((ax * ax + ay * ay) * (cx - bx) + (bx * bx + by * by) * (ax - cx) + (cx * cx + cy * cy) * (bx - ax)) / d
    return (x, y, math.hypot(x - ax, y - ay))


def _make_diameter(p0, p1):
    return ((p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0, math.hypot(p0[0] - p1[0], p0[1] - p1[1]) / 2.0)


_EPSILON = 1e-12

def _is_in_circle(c, p):
    return c is not None and math.hypot(p[0] - c[0], p[1] - c[1]) < c[2] + _EPSILON


# Returns twice the signed area of the triangle defined by (x0, y0), (x1, y1), (x2, y2)
def _cross_product(x0, y0, x1, y1, x2, y2):
    return (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0)

############################################################################################################

def findAppropriateCircle(circleContour):
    
    numberOfContourPoints = len(circleContour)
    contourCoordinates = []
    
    centre_X = 0
    centre_Y = 0
    radius = 0
    
    for i in range(numberOfContourPoints):
        contourCoordinates.append(circleContour[i][0])
        
    (centre_X,centre_Y,radius) = make_circle(contourCoordinates)
            
    return (centre_X,centre_Y,radius)

####################################### MAIN CODE STARTS HERE ###################################

radiusVStimePlot = np.zeros((512,512,3), np.uint8)
# path = "../data/dataset/BallData/pos/*.jpg"
# path = "../data/dataset/BallData/pos/103.jpg"

found = False
path = "../data/dataset/posDataset/*.jpg"
for time,imagePath in enumerate(glob.glob(path)):

    found = True
    frame = imread(imagePath,1)
    imshow("Coloured Image",frame)

    frame = imread(imagePath,0)
    imshow("Original Image",frame)

    blurredFrame = GaussianBlur(frame,(5,5),0)
    # blurredFrame = cv2.blur(frame, (35,35))
    #equalizeHist(frame,blurredFrame)

    height, width = blurredFrame.shape[:2]
    frame_center_x = width/2
    frame_center_y = height/2

    # Find average color of the entire frame
    avg_color_frame = float(np.sum(blurredFrame))/float(width*height)

    # Find average color around the blurred frame center
    avg_color_ball = 0.0
    for dx in range(1,6):
        for dy in range(1,6):
            avg_color_ball += blurredFrame[frame_center_y+dy][frame_center_x+dx]
    avg_color_ball /= 25.0

    print "Average ball color: "+str(avg_color_ball)
    print "Average frame color: "+str(avg_color_frame)
    print "Difference: "+str(avg_color_frame - avg_color_ball)


    # if avg_color_ball > 110.0: reject
    if avg_color_ball > 100.0:
        THRESHOLD = 95.0
    elif avg_color_ball > 80.0:
        THRESHOLD = min(90.0,avg_color_ball)
    elif avg_color_ball < 65.0:
        THRESHOLD = 65.0
    else:
        THRESHOLD = 75.0

    if avg_color_frame - avg_color_ball < 20:
        print "Difference in colors = {} is too less. Reject.".format(avg_color_frame - avg_color_ball)


    imshow("Blurred Frame", blurredFrame)

    for i in range(len(blurredFrame)):
        for j in range(len(blurredFrame[0])):
            if(blurredFrame[i][j]<THRESHOLD):
                blurredFrame[i][j]=MAX_INTENSITY
            else:
                blurredFrame[i][j]=MIN_INTENSITY
            
    imshow("Tracked Ball",blurredFrame)

    _,contours,_ = findContours(blurredFrame,RETR_TREE,CHAIN_APPROX_NONE)
    drawContours(blurredFrame, contours, -1, (255,0,0), 1)

    imshow("Contours", blurredFrame)

##############################################################################

    circleIndex = 0

    # for i,j in enumerate(contours):
    #     if(len(j)>len(contours[circleIndex])):
    #         circleIndex = i;

    centre_X = 0
    centre_Y = 0
    radius = 0
    min_diff = 100000
    # Find contour closest to centre
    for contour in contours:
        (x,y),r = cv2.minEnclosingCircle(contour)
        diff = abs(x-25)+abs(y-25)
        if diff < min_diff:
            if r < 1:
                print "Radius too low. Reject contour."
                continue
            # print "Found new min at: {},{} with r={}".format(x,y,r)
            centre_X = x
            centre_Y = y
            radius = r
            min_diff = abs(x-25)+abs(y-25)
        elif abs(x-25)+abs(y-25) == min_diff:
            if r > radius:
                centre_X = x
                centre_Y = y
                radius = r
    if min_diff > 20:
        print "Selected contour is too far away from centre. Reject point."
                
    # centre_X,centre_Y,radius = findAppropriateCircle(contours[circleIndex])
    # (centre_X,centre_Y),radius = minEnclosingCircle(contours[circleIndex])

    circle(frame,(int(centre_X),int(centre_Y)), int(radius), (255,0,0), 1)
    imshow("Best Fit Circle",frame)
    
    
    print "Image: "+str(imagePath)+", radius: "+str(radius)
    #circle(radiusVStimePlot,(time*5+10,400-int(radius)), 1, (0,0,255), -1)
    #imshow("Radius VS Time Plot",radiusVStimePlot)    

##############################################################################

    waitKey(0)
    
print "Finished"
# if found:
#     waitKey(0)