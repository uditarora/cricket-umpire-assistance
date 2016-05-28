# Import the necessary packages
from __future__ import division
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time
import detector
import linReg
import quadFit
import warnings
import math
from imutils.object_detection import non_max_suppression
from imutils import paths

DEBUG_VISUALIZE = True

# Coordinates file
Coordinates_file = open("coordinates.txt", "w")
Textlines = []
# Warning filter
warnings.filterwarnings("ignore")

# Construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file", required=True)
ap.add_argument("-a", "--attack", help="specify bowling attack - 1 for Spin bowling and 0 for Fast", default=0)
ap.add_argument("-s", "--sliding", help="Show sliding", default=0)
args = vars(ap.parse_args())
camera = cv2.VideoCapture(args["video"])
bowling_attack = int(args["attack"])
show_slide = int(args["sliding"])
# Number of frames to skip after initial movement detected
SKIP = 45

if bowling_attack:
    SKIP = 65

# Number of frames to detect after ball detection
DURATION = 50

# If bowling attack is spin then increase the number of frames 
if bowling_attack:
    DURATION = 80

def findRadius(frame, x, y, frame_no):

    """Function to find radius of the detected ball"""

    # Parameters to find radius of the ball
    THRESHOLD_brightness = 90
    MAX_INTENSITY = 255
    MIN_INTENSITY = 0
    # START_RADIUS = 21.8 #151
    # FINISH_RADIUS = 7.2 #223
    # PITCH_DIST = 16
    blurredFrame = cv2.GaussianBlur(frame,(5,5),0)
    # cv2.imshow("Blurred Frame", blurredFrame)

    for i in range(len(blurredFrame)):
        for j in range(len(blurredFrame[0])):
            if(blurredFrame[i][j]<THRESHOLD_brightness):
                blurredFrame[i][j]=MAX_INTENSITY
            else:
                blurredFrame[i][j]=MIN_INTENSITY
    # cv2.imshow("Tracked Ball",blurredFrame)

    _,contours,_ = cv2.findContours(blurredFrame,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(blurredFrame, contours, -1, (255,0,0), 1)
    # cv2.imshow("Contours", blurredFrame)

    if len(contours) == 0:
        return False

    circleIndex = 0
    for i,j in enumerate(contours):
        if(len(j)>len(contours[circleIndex])):
            circleIndex = i;
                
    # centre_X,centre_Y,radius = findAppropriateCircle(contours[circleIndex])
    (centre_X,centre_Y),radius = cv2.minEnclosingCircle(contours[circleIndex])
    cv2.circle(frame,(int(centre_X),int(centre_Y)), int(radius), (255,0,0), 2)
    if DEBUG_VISUALIZE:
       cv2.imshow("Best Fit Circle",frame)
    Textlines.append((x+centre_X, y+centre_Y, radius, frame_no,0))

    return True

# Detecting the frame when bowler starts to bowl

#Initialization
frame_no = 1
initial_frame = 0

# Rectangular Coordinates for lower half of the image
y_start = 360
y_end = 720
x_start = 0
x_end = 1080 
    
(grabbed1, prev) = camera.read()
while True:
    """
        Captures the frame in which bowler starts to bowl
    """
    # Grab a frame and take difference from prev frame
    (grabbed1, frame1) = camera.read()
    frame_no += 1
    if not grabbed1:
        break

    gray1 = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    final1 = gray1[y_start: y_end, x_start: x_end]
    final2 = gray2[y_start: y_end, x_start: x_end]
    difference = cv2.absdiff(final1, final2)
    retval, threshold = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)
    prev = frame1
    
    # Count number of white difference pixels 
    white = cv2.countNonZero(threshold)

    # If white pixels in the lower half of the image is greater than 3%, that means it's a bowlers arm.
    # Skip above mentioned number of frames
    white_percentage = 0.02
    lower_height = 360
    lower_width = 1080

    if white > (white_percentage * lower_width * lower_height):
        # cv2.imshow("Bowlers Frame",frame1)
    
        # Skip frames
        for i in range(0,SKIP):
            (grabbed1, frame1) = camera.read()

        initial_frame = frame_no + SKIP
        frame_no = frame_no + SKIP
        break

# for i in range(0,1):
#     (grabbed1, frame1) = camera.read()

# initial_frame = 1
# frame_no = 1

# Ball detection
# Find coordinates of the ball for the first time

# Window coordinates for focussed image
y_start = 130
y_end = 720
x_start = 100
x_end = 900 
 
# Parameters for detector.py
step_size = (10, 10)
threshold = 0.7

# Array to store coordinates
ball_detection = []

# Tracks the current ball position
current_ballPos = (0,0)
            
while True:
    """
        Loop until ball gets detected
    """

    # Grab frames one by one, modify it and send it to detector.py
    (grabbed1, frame1) = camera.read()
    gray_image_1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    crop_img = gray_image_1[y_start: y_end, x_start: x_end]
    current_ballPos_temp = (0,0)

    # Image sent to detector.py to get ball coordinates
    current_ballPos_temp = detector.find(crop_img, step_size, threshold,gray_image_1,x_start,y_start,x_end, y_end)
    
    # If ball coordinate is not (0,0), it means ball has been detected
    if(not(current_ballPos_temp[0] == 0 and current_ballPos_temp[1] == 0)):
        # Calculate coordinates according to full frame (1080*720) by adding ball coordinates to focussed window coordinates 
        current_ballPos = (current_ballPos_temp[0] + x_start, current_ballPos_temp[1] + y_start)
        # ball_detection.append(current_ballPos)
        break


# Ball tracking, given coordinates of the ball detected first time(current_ballPos)

# Parameters for detector.py
step_size = (3, 3)
threshold = 0.2
# cv2.imshow("Balls First Frame",frame1)
stop_search = 0

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Dictionary storing the (xmid,ymid) coordinates of batsman rectangle
batsman_mid = {}
# If the batsman hasn't been detected so far this value is True
batsman_first_detection = True
batsman_area = ()
      
while True:
    """
        Windowing technique, search around the ball detected in previous frame
    """

    (grabbed1, frame1) = camera.read()
    frame_no += 1
    if not grabbed1:
        break

    if frame_no > initial_frame + DURATION:
        break

    # cv2.imshow("Current Grabbed Frame",frame1)
    last_frame = frame1
    gray_image_1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    img_copy = gray_image_1.copy()
    img_copy_1 = gray_image_1.copy()

    # detect people in the image
    if not batsman_first_detection:
        batsman_crop = frame1[batsman_area[1]:batsman_area[3], batsman_area[0]:batsman_area[2]]
    else:
        batsman_crop = frame1

    cv2.imshow("batsman_crop", batsman_crop)
    (rects, weights) = hog.detectMultiScale(batsman_crop, winStride=(4, 4), padding=(8, 8), scale=1.05)
    # apply non-maxima suppression to the bounding boxes using a
    # fairly large overlap threshold to try to maintain overlapping
    # boxes that are still people
    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])

    if len(rects) > 0:
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
        xmid = 0
        ymid = 0
        max_rect = ()
        for (x1, y1, x2, y2) in pick:
            if (x1+x2)/2 > xmid:
                xmid = (x1+x2)/2
                ymid = (y1+y2)/2
                max_rect = (x1, y1, x2, y2)

        # Batsman search in full frame
        if batsman_first_detection:
            cv2.rectangle(img_copy_1, (max_rect[0], max_rect[1]), (max_rect[2], max_rect[3]), (0, 255, 0), 2)
            batsman_mid[frame_no] = (xmid,ymid)
        # Batsman search in cropped frame
        else:
            cv2.rectangle(img_copy_1, (max_rect[0]+batsman_area[0], max_rect[1]+batsman_area[1]), (max_rect[2]+batsman_area[0], max_rect[3]+batsman_area[1]), (0, 255, 0), 2)
            batsman_mid[frame_no] = (xmid+batsman_area[0],ymid+batsman_area[1])

        # Set batsman crop area after first detection
        if batsman_first_detection:
            batsman_first_detection = False
            batsman_area = (max_rect[0]-100, 100, max_rect[2]+100, max_rect[3]+100)
    
    # New window coordinates for searching
    x1 = current_ballPos[0] - 50        
    x2 = current_ballPos[0] + 100
    y1 = current_ballPos[1] - 50
    y2 = current_ballPos[1] + 100

    # Checks for out of bound
    if x1 < 0:
        x1 = 0
    if x2 > frame1.shape[1]:
        x2 = frame1.shape[1]
    if y1 < 0:
        y1 = 0
    if y2 > frame1.shape[0]:
        y2 = frame1.shape[0]

    # Crops the searching area 
    crop_img = gray_image_1[y1: y2, x1: x2]
    
    # Image sent to detector.py to get ball coordinates
    current_ballPos_temp = detector.find(crop_img, step_size,threshold,img_copy_1,x1,y1,x2,y2,show_slide)
    
    # If not detected
    if(current_ballPos_temp[0] == 0 and current_ballPos_temp[1] == 0):
        stop_search = stop_search + 1
        if stop_search == 5:
            break
        continue
    
    stop_search = 0
    
    # Get coordinates according to full frame
    current_ballPos = (x1 + current_ballPos_temp[0], y1 + current_ballPos_temp[1])
    # Crop the ball image
    img_ball = img_copy[current_ballPos[1]: current_ballPos[1] + 50, current_ballPos[0]: current_ballPos[0] + 50]
    
    # Call find radius
    found = findRadius(img_ball, current_ballPos[0], current_ballPos[1], frame_no)

    if found:
        ball_detection.append(current_ballPos)


# Calculate the bouncing point and mark ball tracks
bouncing_coordinates = (0,0)
idx = 0
bouncing_idx = 0
last_frame1 = last_frame.copy()
for (x, y) in ball_detection:
    # cv2.rectangle(last_frame, (x+23, y+23), (x+27, y+27), (0, 0, 0), thickness=2)
    if y > bouncing_coordinates[1]:
        bouncing_coordinates = (x,y)
        bouncing_idx = idx
    idx = idx + 1
Textlines[bouncing_idx] = (Textlines[bouncing_idx][0], Textlines[bouncing_idx][1], Textlines[bouncing_idx][2], Textlines[bouncing_idx][3], 1)
cv2.rectangle(last_frame, (bouncing_coordinates[0]+23, bouncing_coordinates[1]+23), (bouncing_coordinates[0]+27, bouncing_coordinates[1]+27), (255, 0, 0), thickness=2)

idx = 0
for (x, y) in ball_detection:
    if idx < bouncing_idx:
        cv2.rectangle(last_frame, (x+23, y+23), (x+27, y+27), (0, 0, 0), thickness=2)
    idx = idx + 1    



corrected = []
rejected = []
for i in range(0,bouncing_idx + 2):
    # print i
    corrected.append((ball_detection[i][0] + 25, ball_detection[i][1] + 25,Textlines[i][2], Textlines[i][3], Textlines[i][4]))

if(len(ball_detection) >= bouncing_idx + 2):
    prev_coord = (ball_detection[bouncing_idx + 1][0] + 25,ball_detection[bouncing_idx + 1][1] + 25,Textlines[bouncing_idx + 1][2], Textlines[bouncing_idx + 1][3], Textlines[bouncing_idx + 1][4])
    # print prev_coord
    prev_slope = (prev_coord[1] - (ball_detection[bouncing_idx][1]+ 25) )/(prev_coord[0] - (25+ball_detection[bouncing_idx][0])) 
    for i in range((bouncing_idx+2), len(ball_detection)):
        current_coord = (ball_detection[i][0]+25,ball_detection[i][1]+25,Textlines[i][2], Textlines[i][3], Textlines[i][4])
        # print current_coord
        if (current_coord[0] - prev_coord[0]) == 0:
            slope = 100000
        else:
            slope = (current_coord[1] - prev_coord[1])/(current_coord[0] - prev_coord[0])
        tn = (slope-prev_slope)/(1.0+(slope*prev_slope))
        angle = math.atan(tn)*180.0/math.pi*(-1)
        distance = ((current_coord[1] - prev_coord[1])*(current_coord[1] - prev_coord[1])) + ((current_coord[0] - prev_coord[0])*(current_coord[0] - prev_coord[0]))
        # print angle
        # print distance
        # print "x1 " + str(current_coord[0]) + "y1 " + str(current_coord[1]) + "x2 " + str(prev_coord[0]) + "y2 " + str(prev_coord[1]) + "dist" + str(distance)
        if angle < 0:
            angle = angle* (-1)
        if angle <= 25 or distance <= 500:
            corrected.append(current_coord)  
            prev_coord = current_coord
            prev_slope = slope
        else:
            rejected.append((current_coord[0],current_coord[1]))      

# corrected = []
# if(len(ball_detection) > bouncing_idx + 2):
#   prev_coord = ball_detection[bouncing_idx + 1]
#   prev_dist = ((prev_coord[1] - ball_detection[bouncing_idx][1])*(prev_coord[1] - ball_detection[bouncing_idx][1]))+((prev_coord[0] - ball_detection[bouncing_idx][0])*(prev_coord[0] - ball_detection[bouncing_idx][0]) ) 
#   for i in range(bouncing_idx + 2,len(ball_detection)):
#       current_coord = ball_detection[i]
#       dist = ((current_coord[1] - prev_coord[1])*(current_coord[1] - prev_coord[1]))+((current_coord[0] - prev_coord[0])*(current_coord[0] - prev_coord[0]))
#       # print " " + str(current_coord[1]) + " - " + str(prev_coord[1]) + "/" + str(current_coord[0]) + "- " + str(prev_coord[0]) + " angle" + str(angle) + " prev angle" + str(prev_angle)
#       if dist > 5*prev_dist:
#           continue
#       corrected.append(current_coord) 
#       prev_coord = current_coord
        
i = 0
for (x,y,_,_,_) in corrected:
    if i > bouncing_idx:
        cv2.rectangle(last_frame, (x-2, y-2), (x+2, y+2), (0, 255, 0), thickness=2)
    i = i + 1    

for (x,y) in rejected:
    cv2.rectangle(last_frame, (x-2, y-2), (x+2, y+2), (0, 0, 255), thickness=2)
    
# Show the final tracked path!!
if DEBUG_VISUALIZE:
    cv2.imshow("Ball Path", last_frame)
    cv2.imwrite("path.jpg", last_frame)
    cv2.waitKey(0)


# Regressions
linearReg = linReg.linearRegression(corrected)
quadraticReg = quadFit.quadraticRegression(corrected)

# Qutput to text file in the format: [x y radius frame_no is_bouncing_point regressed_radius regressed_y batsman_mid_x batsman_mid_y]
idx = 0
for (x,y,radius,frame_no,is_bouncing_point) in corrected:
    if frame_no not in batsman_mid:
        batsman_mid[frame_no][0] = -1
        batsman_mid[frame_no][1] = -1
    Coordinates_file.write("{:.3f} {:.3f} {:.3f} {} {} {:.3f} {:.3f} {} {}\n".format(x, y, radius, frame_no, is_bouncing_point, linearReg[idx], quadraticReg[idx], batsman_mid[frame_no][0], batsman_mid[frame_no][1]))
    idx = idx + 1

# Close coordinates text file
Coordinates_file.close()

# Close any open windows
cv2.destroyAllWindows()