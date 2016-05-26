# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
import time

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    print "Path not specified"
    camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

frame_no = 0

(grabbed1, frame1) = camera.read()

while True:
    frame_no += 1
    # frame1 = imutils.resize(frame1, width=360, height=480)
    (grabbed2, frame2) = camera.read()

    if args.get("video") and (not grabbed1 or not grabbed2):
        break

    # if frame_no < 51:
    #     continue

    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    difference = cv2.absdiff(gray1, gray2)
    retval, threshold = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)

    blur = cv2.blur(threshold, (20,20))
    retval, threshold = cv2.threshold(blur, 30, 1, cv2.THRESH_BINARY)
    frame3 = threshold[..., None] * frame2
    
    cv2.imwrite("frames/"+str(frame_no)+".jpg", frame2)

    print "Written frame "+str(frame_no)

    (grabbed1, frame1) = (grabbed2, frame2)

    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()