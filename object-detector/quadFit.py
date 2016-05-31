# Scientific libraries
import numpy as np

def quadraticRegression(data, after_bounce_linear = False):
  x1 = []
  y1 = []
  w1 = []
  weights1 = 1
  
  x2 = []
  y2 = []
  w2 = []
  weights2 = 5

  # Lists containing bounce point in the part before bounce - only used for finding polynomial
  x1_with_bounce = []
  y1_with_bounce = []
  w1_with_bounce = []

  # Lists containing the predicted coordinates
  x_pred = []
  y_pred = []
  w_pred = []


  changing_point = 0
  i = 0
  prev_x = 0
  for(x,y,_,_,bounce_point) in data:
    prev_x = x
    if bounce_point:
      changing_point = 1
      if i > 0:
        w1[i-1] = 5
      x1_with_bounce.append(x)
      y1_with_bounce.append(y)
      w1_with_bounce.append(10)

    if changing_point == 0:        
      w1.append(weights1)
      x1.append(x)
      y1.append(y)

      x1_with_bounce.append(x)
      y1_with_bounce.append(y)
      w1_with_bounce.append(weights1)

    else:
      w2.append(weights2)
      weights2 = 1
      x2.append(x)
      y2.append(y)
    i = i + 1  

  # Make w2 vary in decreasing order except first point
  for i in range(1,len(w2)):
    if i <= len(w2)/4:
      w2[i] = 3
    elif i <= len(w2)/2:
      w2[i] = 2
    else:
      w2[i] = 1

  x_new1 = []
  y_new1 = []
  x_new2 = []
  y_new2 = []

  # calculate polynomial before bounce
  if len(x1) > 0:
    z1 = np.polyfit(x1_with_bounce, y1_with_bounce, 2, None, False, w1_with_bounce, False)
    # z1 = np.polyfit(x1, y1, 2, None, False, w1, False)
    f1 = np.poly1d(z1)
    
    # calculate new x's and y's
    x_new1 = x1
    y_new1 = f1(x_new1)
    # Without regression
    # y_new1 = y1


  # calculate polynomial after bounce
  if len(x2) > 0:
    if after_bounce_linear:
      z2 = np.polyfit(x2, y2, 1, None, False, w2, False)
    else:
      z2 = np.polyfit(x2, y2, 2, None, False, w2, False)
    f2 = np.poly1d(z2)
    
    for i in range(1,300):
      x_pred.append(prev_x + i*1)
      w_pred.append(1)

    # calculate new x's and y's
    x_new2 = x2
    y_new2 = f2(x_new2)
    # Without regression
    # y_new2 = y2

    y_pred = f2(x_pred)

  y_new = []

  for i in y_new1:
    y_new.append(i)
    
  for i in y_new2:
    y_new.append(i)

  y_new.extend(y_pred)

  return y_new

# def quadraticRegression_afterBounce(data):
#   x1 = []
#   y1 = []
#   w1 = []
#   weights1 = 1
  
#   x2 = []
#   y2 = []
#   w2 = []
#   weights2 = 5


#   changing_point = 0
#   i = 0
#   prev_x = 0
#   for(x,y,_,_,bounce_point) in data:
#     prev_x = x
#     if bounce_point:
#       changing_point = 1
#       if i > 0:
#         w1[i-1] = 5

#     if changing_point == 0:        
#       w1.append(weights1)
#       x1.append(x)
#       y1.append(y)

#     else:
#       w2.append(weights2)
#       weights2 = 1
#       x2.append(x)
#       y2.append(y)
#     i = i + 1  

#   # calculate polynomial
#   z1 = np.polyfit(x1, y1, 2, None, False, w1, False)
#   f1 = np.poly1d(z1)
  
#   # calculate new x's and y's
#   x_new1 = x1
#   # y_new1 = f1(x_new1)


#   # calculate polynomial
#   z2 = np.polyfit(x2, y2, 2, None, False, w2, False)
#   f2 = np.poly1d(z2)
  
#   for i in range(1,300):
#     x2.append(prev_x + i*1)
#     w2.append(1)

#   # calculate new x's and y's
#   x_new2 = x2
#   y_new2 = f2(x_new2)

#   y_new = []

#   for i in y1:
#     y_new.append(i)
    
#   for i in y_new2:
#     y_new.append(i)

#   return y_new