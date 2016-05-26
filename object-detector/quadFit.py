# Scientific libraries
import numpy as np

def quadraticRegression(data):
  x1 = []
  y1 = []
  
  x2 = []
  y2 = []

  changing_point = 0
  for(x,y,_,_,bounce_point) in data:
    if bounce_point:
      changing_point = 1

    if changing_point == 0:        
      x1.append(x)
      y1.append(y)

    else:
      x2.append(x)
      y2.append(y)

  # calculate polynomial
  z1 = np.polyfit(x1, y1, 2)
  f1 = np.poly1d(z1)
  
  # calculate new x's and y's
  x_new1 = x1
  y_new1 = f1(x_new1)

  # calculate polynomial
  z2 = np.polyfit(x2, y2, 2)
  f2 = np.poly1d(z2)
  
  # calculate new x's and y's
  x_new2 = x2
  y_new2 = f2(x_new2)

  y_new = []

  for i in y_new1:
    y_new.append(i)
    
  for i in y_new2:
    y_new.append(i)

  return y_new