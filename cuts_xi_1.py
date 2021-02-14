# import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

def vmass_correct():
    if columns[2] > 1.1 and columns[2] < 1.2:
        return True
    return False



f = open('real-xi-data.file', 'r')
out = open('output.file', 'w')

ximass, v0mass, icand = [], [], []
correct_indices = []
i = 0
for line in f:
    line = line.strip()
    columns = [float(s) for s in line.split()]
    if columns[15] > -7.5 and columns[15] < 5:
        correct_indices.append(i)
        v0mass.append(columns[15])
        ximass.append(columns[1])
        icand.append(columns[0])
    i += 1
for i in range(len(ximass)):
    print(ximass[i])
    out.write(str(float(i)) + " " + str(ximass[i]) + " " + str(v0mass[i])+"\n")

  #  print("xi mass", ximass, "V0 mass", v0mass)