# import numpy as np
import matplotlib.pyplot as plt

f = open('real-xi-data.file', 'r')

ximass, v0mass = [], []
for line in f:
    line = line.strip()
    columns = [float(s) for s in line.split()]
    ximass.append(columns[1])
    v0mass.append(columns[2])
  #  print("xi mass", ximass, "V0 mass", v0mass)

f.close()
plt.hist(ximass, bins = 100, range = [1.2,1.6])
plt.title('Effective mass plot for Xi')
plt.xlabel('Effective $\Lambda \pi^{-}$ mass (GeV/c$^{2}$)')
plt.ylabel('No. of Events / 4 MeV/c$^{2}$')
plt.savefig('ximass.pdf')
plt.show()
#plt.hist2d(ximass, v0mass, bins = 100)
#plt.show()
