# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

yellowLower = (20,100,100)
yellowUpper = (30,255,255)

pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    print "Path not specified"
    camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

# keep looping
while True:
    # grab the first frame
    (grabbed1, frame1) = camera.read()

    cv2.imshow("Original", frame1)

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed1:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    # frame = imutils.resize(frame, width=1300, height=800)
    frame1 = imutils.resize(frame1, width=854, height=480)
    # blurred1 = cv2.GaussianBlur(frame1, (11, 11), 0)
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

    # grab the second frame
    (grabbed2, frame2) = camera.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed2:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space
    # frame = imutils.resize(frame, width=1300, height=800)
    frame2 = imutils.resize(frame2, width=854, height=480)
    # blurred2 = cv2.GaussianBlur(frame2, (11, 11), 0)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    difference = cv2.absdiff(gray1, gray2)
    retval, threshold = cv2.threshold(difference, 30, 255, cv2.THRESH_BINARY)
    # threshold_guass = cv2.adaptiveThreshold(difference,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,3,5)
    # cv2.imshow("guassian", threshold_guass)

    # cv2.imshow("difference", difference)
    # cv2.imshow("threshold", threshold)

    blur = cv2.blur(threshold, (10,10))
    retval, threshold = cv2.threshold(blur, 30, 1, cv2.THRESH_BINARY)

    frame3 = threshold[..., None] * frame2

    blurred = cv2.GaussianBlur(frame3, (11, 11), 0)
    hsv = cv2.cvtColor(frame3, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, yellowLower, yellowUpper)
    # mask = cv2.inRange(hsv, yellowLower, yellowUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cv2.imshow("masked", mask)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    # cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    #     cv2.CHAIN_APPROX_SIMPLE)[-2]
    # center = None

    # # print str(cnts)

    # # only proceed if at least one contour was found
    # if len(cnts) > 0:
    #     # find the largest contour in the mask, then use
    #     # it to compute the minimum enclosing circle and
    #     # centroid
    #     # print "Contour found"
    #     c = max(cnts, key=cv2.contourArea)
    #     ((x, y), radius) = cv2.minEnclosingCircle(c)
    #     M = cv2.moments(c)
    #     center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    #     # only proceed if the radius meets a minimum size
    #     if radius > 10:
    #         # draw the circle and centroid on the frame,
    #         # then update the list of tracked points
    #         cv2.circle(frame3, (int(x), int(y)), int(radius),
    #             (0, 255, 255), 2)
    #         cv2.circle(frame3, center, 5, (0, 0, 255), -1)

    # # update the points queue
    # pts.appendleft(center)

    # # loop over the set of tracked points
    # for i in xrange(1, len(pts)):
    #     # if either of the tracked points are None, ignore
    #     # them
    #     if pts[i - 1] is None or pts[i] is None:
    #         continue

    #     # otherwise, compute the thickness of the line and
    #     # draw the connecting lines
    #     thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
    #     cv2.line(frame3, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # cv2.imshow("final", frame3)

    # cv2.imshow("blur", threshold)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
