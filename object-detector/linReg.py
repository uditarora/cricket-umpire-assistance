# Scientific libraries
from numpy import arange,array,ones
from scipy import stats

def linearRegression(data):
  xi = []
  y = []
  start = 0
  for(_,_,z,_,_) in data:
    y.append(z)
    xi.append(start)
    start = start + 1

  A = array([ xi, ones(start)])

  # Generated linear fit
  slope, intercept, r_value, p_value, std_err = stats.linregress(xi,y)
  line = []
  for i in range(0,start):
    line.append((slope*xi[i]) + intercept)
    # print line[i]
  return line    
