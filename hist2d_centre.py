# import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

f = open('real-xi-data.file', 'r')

ximass, var2 = [], []
n_var = 4  #change number for a different variable
i = 0
for line in f:
    line = line.strip()
    columns = [float(s) for s in line.split()]
    var2.append(columns[n_var])
    ximass.append(columns[1])


f.close()

x_start = min(ximass)
x_end = max(ximass)
y_start = min(var2)
y_end = max(var2)
n_bins = 100

h =plt.hist2d(ximass, var2,  range=[[x_start, x_end], [y_start, y_end]], bins = n_bins)
h = h[0]
print(h)
centre = [0,0]
total_mass = 0
for i in range(len(h)):
  for j in  range(len(h[0])):
    centre[0] += h[i][j] * (x_start + i * (x_end-x_start)/n_bins)
    centre[1] += h[i][j] * (y_start + j * (y_end-y_start)/n_bins)
    print(centre)
    # centre[0] += h[i][j] * i
    # centre[1] += h[i][j] * j
    total_mass += h[i][j]
centre[0] /= total_mass
centre[1] /= total_mass
print(centre)

plt.show()
