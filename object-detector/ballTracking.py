# Import the necessary packages
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
args = vars(ap.parse_args())
camera = cv2.VideoCapture(args["video"])
bowling_attack = int(args["attack"])

# Number of frames to skip after initial movement detected
SKIP = 65

# Number of frames to detect after ball detection
DURATION = 40

# If bowling attack is spin then increase the number of frames 
if bowling_attack:
    DURATION = 80

def findRadius(frame, x, y, frame_no):

    """Function to find radius of the detected ball"""

    # Parameters to find radius of the ball
    THRESHOLD_brightness = 75
    MAX_INTENSITY = 255
    MIN_INTENSITY = 0
    START_RADIUS = 21.8 #151
    FINISH_RADIUS = 7.2 #223
    PITCH_DIST = 16
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

# Detecting the frame when bowler starts to bowl

#Initialization
frame_no = 1
initial_frame = 0

# Rectangular Coordinates for lower half of the image
y_start = 360
y_end = 720
x_start = 100
x_end = 900 
    
(grabbed1, prev) = camera.read()
while True:
    
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
    white_percentage = 0.03
    lower_height = 360
    lower_width = 800

    if white > (white_percentage * lower_width * lower_height):
        # Skip frames
        for i in range(0,SKIP):
            (grabbed1, frame1) = camera.read()

        initial_frame = frame_no + SKIP
        frame_no = frame_no + SKIP
        break


# Ball detection
# Find coordinates of the ball for the first time

# Window coordinates for focussed image
y_start = 130
y_end = 720
x_start = 100
x_end = 900 
 
# Parameters for detector.py
step_size = (10, 10)
threshold = 0.5

# Array to store coordinates
ball_detection = []

# Tracks the current ball position
current_ballPos = (0,0)
            
while True:
    """Loop until ball gets detected"""

    # Grab frames one by one, modify it and send it to detector.py
    (grabbed1, frame1) = camera.read()
    # cv2.imshow("Balls First Frame",frame1)
    gray_image_1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    crop_img = gray_image_1[y_start: y_end, x_start: x_end]
    current_ballPos_temp = (0,0)

    # Image sent to detector.py to get ball coordinates
    current_ballPos_temp = detector.find(crop_img, step_size, threshold)
    
    # If ball coordinate is not (0,0), it means ball has been detected
    if(not(current_ballPos_temp[0] == 0 and current_ballPos_temp[1] == 0)):
        # Calculate coordinates according to full frame (1080*720) by adding ball coordinates to focussed window coordinates 
        current_ballPos = (current_ballPos_temp[0] + x_start, current_ballPos_temp[1] + y_start)
        ball_detection.append(current_ballPos)
        break


# Ball tracking, given coordinates of the ball detected first time(current_ballPos)

# Parameters for detector.py
step_size = (3, 3)
threshold = 0.7
  
while True:
    """Windowing technique, search around the ball detected in previous frame"""

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
    current_ballPos_temp = detector.find(crop_img, step_size,threshold)
    
    # If not detected
    if(current_ballPos_temp[0] == 0 and current_ballPos_temp[1] == 0):
        continue
    
    # Get coordinates according to full frame
    current_ballPos = (x1 + current_ballPos_temp[0], y1 + current_ballPos_temp[1])
    
    # Crop the ball image
    img_ball = img_copy[current_ballPos[1]: current_ballPos[1] + 50, current_ballPos[0]: current_ballPos[0] + 50]
    
    ball_detection.append(current_ballPos)
    
    # Call find radius
    findRadius(img_ball, current_ballPos[0], current_ballPos[1], frame_no)

# Calculate the bouncing point and mark ball tracks
bouncing_coordinates = (0,0)
idx = 0
bouncing_idx = 0
for (x, y) in ball_detection:
    if idx > 45:
        cv2.rectangle(last_frame, (x+23, y+23), (x+27, y+27), (0, 0, 0), thickness=2)
    if y > bouncing_coordinates[1]:
        bouncing_coordinates = (x,y)
        bouncing_idx = idx
    idx = idx + 1
Textlines[bouncing_idx] = (Textlines[bouncing_idx][0], Textlines[bouncing_idx][1], Textlines[bouncing_idx][2], Textlines[bouncing_idx][3], 1)
cv2.rectangle(last_frame, (bouncing_coordinates[0]+23, bouncing_coordinates[1]+23), (bouncing_coordinates[0]+27, bouncing_coordinates[1]+27), (0, 0, 255), thickness=2)

# Show the final tracked path!!
if DEBUG_VISUALIZE:
    cv2.imshow("Ball Path", last_frame)
    cv2.waitKey(0)


# Regressions
linearReg = linReg.linearRegression(Textlines)
quadraticReg = quadFit.quadraticRegression(Textlines)

# Qutput to text file
idx = 0
for (x,y,radius,frame_no,is_bouncing_point) in Textlines:
    Coordinates_file.write("{:.3f} {:.3f} {:.3f} {:.3f} {} {:.3f} {:.3f}\n".format(x, y, radius, frame_no, is_bouncing_point, linearReg[idx], quadraticReg[idx]))
    idx = idx + 1

# Close coordinates text file
Coordinates_file.close()

# Close any open windows
cv2.destroyAllWindows()