# import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

f = open('real-Omega-data.file', 'r')

ommass, var2 = [], []
n_var = 9 #change number for a different variable
i = 0
for line in f:
    line = line.strip()
    columns = [float(s) for s in line.split()]
    var2.append(columns[n_var])
    ommass.append(columns[1])


f.close()

x_start = min(ommass)
x_end = max(ommass)
y_start = min(var2)
y_end = max(var2)
n_bins = 100
print(x_start)
h =plt.hist2d(ommass, var2,  range=[[x_start, 1.8], [0, 0.05]], bins = n_bins)
plt.show()