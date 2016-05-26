import numpy as np
import cv2

# Load previously saved data
mtx, dist = np.load('parameters_intrinsic.npy')

# Define image and object points
# imagep = np.array([[627, 360], [650, 360], [673, 360], [466, 498]], dtype=np.float64)
# objp = np.array([[-11.43,71.1,0.0], [0.0,71.1,0.0], [11.43,71.1,0.0], [-132,0.0,0.0]], dtype=np.float64)

imagep = np.array([(627, 360), (650, 360), (673, 360), (466, 498), (646,498)], dtype=np.float64)
objp = np.array([(-11.43,71.1,0.0), (0.0,71.1,0.0), (11.43,71.1,0.0), (-132,0.0,0.0), (0,0,0)], dtype=np.float64)

imagep = np.resize(imagep, (4,1,2))
objp = np.resize(objp, (4,1,3))

# Find the rotation and translation vectors
# print str(cv2.solvePnP(objp, imagep, mtx, dist))
_, rvec, tvec = cv2.solvePnP(objp, imagep, mtx, dist)

# Obtain camera pos
rotM = cv2.Rodrigues(rvec)[0]
print "rotM: "+str(rotM)
cameraPosition = -np.matrix(rotM).T * np.matrix(tvec)

# Rt = cv2.Rodrigues(rvec)[0]
# # print str(Rt)
# R = Rt.transpose()
# cameraPosition = -R * tvec

print "Camera position:\n"
print str(cameraPosition)

# print "\n\nRANSAC:\n\n"

# # Find the rotation and translation vectors using ransac
# print str(cv2.solvePnPRansac(objp, imagep, mtx, dist))
# _, rvec, tvec, _ = cv2.solvePnPRansac(objp, imagep, mtx, dist)

# # Obtain camera pos
# rotM = cv2.Rodrigues(rvec)
# print "rotM: "+str(rotM)
# cameraPosition = -np.matrix(rotM).T * np.matrix(tvec)

# print "\n\nCamera position:\n"
# print str(cameraPosition)