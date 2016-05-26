import numpy as np
import cv2
import glob

GRID_X = 5
GRID_Y = 5

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((GRID_X*GRID_Y,3), np.float32)
objp[:,:2] = np.mgrid[0:GRID_X,0:GRID_Y].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('board_images/*.jpg')
count = 0

images.sort()

for fname in images:
    print "Reading image: "+str(fname)
    count += 1
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (GRID_X,GRID_Y),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        objpoints.append(objp)

        cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, (GRID_X,GRID_Y), corners2, ret)
        cv2.imshow('img',img)
        # cv2.imwrite(str(count)+'_.jpg',img)
        cv2.waitKey(0)

cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

print "ret: "+str(ret)
print "mtx: "+str(mtx)
print "dist: "+str(dist)
# print "rvecs: "+str(rvecs)
# print "tvecs: "+str(tvecs)

np.save('parameters_intrinsic', (mtx, dist[0]))
# mtx, dist = np.load('parameters_intrinsic.npy')   # To load from the saved parameters file

# img = cv2.imread('board_images/14.jpg')
# h, w = img.shape[:2]
# newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

# # undistort
# dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

# # crop the image
# x,y,w,h = roi
# dst = dst[y:y+h, x:x+w]
# cv2.imwrite('calibresult.png',dst)