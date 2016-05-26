# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api

import plotly.plotly as py
import plotly.graph_objs as go
py.sign_in('sohitverma94', 'jp33d78olv')
# Scientific libraries
import numpy as np

x1 = []
y1 = []
x2 = []
y2 = []
w = []

weights = 10
start = 0
with open('coordinates.txt') as file:
  for line in file:
      x, y, _, _,isBouncingPoint,_,_ = line.split()
      x = float(x)
      y = 720 - float(y)
      isBouncingPoint = int(isBouncingPoint)  
      if isBouncingPoint == 1:
        start = 1

      if start == 0:  
        x1.append(x)
        y1.append(y) 
      else:
        w.append(weights)
        weights = 1  
        x2.append(x)
        y2.append(y)


# calculate polynomial
z1 = np.polyfit(x1, y1, 2)
f1 = np.poly1d(z1)

# calculate new x's and y's
x_new1 = x1
y_new1 = f1(x_new1)

print x_new1
print y_new1


# calculate polynomial
z2 = np.polyfit(x2, y2, 2, None, False, w, False)
f2 = np.poly1d(z2)
print f2
# calculate new x's and y's
x_new2 = x2
y_new2 = f2(x_new2)

print x_new2
print y_new2

# Creating the dataset, and generating the plot
trace1 = go.Scatter(
                  x=x2,
                  y=y2,
                  mode='markers',
                  marker=go.Marker(color='rgb(255, 127, 14)'),
                  name='Data'
                  )

trace2 = go.Scatter(
                  x=x_new2,
                  y=y_new2,
                  mode='lines',
                  marker=go.Marker(color='rgb(31, 119, 180)'),
                  name='Fit'
                  )

annotation = go.Annotation(
                  x=500,
                  y=400,
                  text='$\textbf{Fit}: 0.43X^3 - 0.56X^2 + 16.78X + 10.61$',
                  showarrow=False
                  )
layout = go.Layout(
                title='Polynomial Fit in Python',
                plot_bgcolor='rgb(229, 229, 229)',
                  xaxis=go.XAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
                  yaxis=go.YAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
                  annotations=[annotation]
                )

data = [trace1, trace2]
fig = go.Figure(data=data, layout=layout)

py.plot(fig, filename='Polynomial-Fit-in-python')