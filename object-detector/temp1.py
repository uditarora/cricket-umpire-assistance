# Scientific libraries
import numpy as np

def quadraticRegression(data):
  x1 = []
  y1 = []
  w1 = []
  weights1 = 1
  
  x2 = []
  y2 = []
  w2 = []
  weights2 = 5


  changing_point = 0
  i = 0
  for(x,_,y,_,bounce_point) in data:
    if bounce_point:
      changing_point = 1
      w1[i-1] = 5

    if changing_point == 0:        
      w1.append(weights1)
      x1.append(x)
      y1.append(y)

    else:
      w2.append(weights2)
      weights2 = 1
      x2.append(x)
      y2.append(y)
    i = i + 1  

  # calculate polynomial
  z1 = np.polyfit(x1, y1, 1, None, False, w1, False)
  f1 = np.poly1d(z1)
  
  # calculate new x's and y's
  x_new1 = x1
  y_new1 = f1(x_new1)

  # calculate polynomial
  z2 = np.polyfit(x2, y2, 1, None, False, w2, False)
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