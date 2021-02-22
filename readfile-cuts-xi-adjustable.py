# import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

value_ranges = [ [1.1, 1.2], [35, 45], [25,35], [0.97, 0.99], [0.97, 0.99], [15, 25], [3, 5], [4, 6], [1.5, 2.5], [1.5, 2.5], [2,3], [10,14], [-1, 2], [-1, 3], [-1, 2]]
deltas = [0.3, 10, 10, 0.03, 0.03, 5, 2.5, 2.5, 1, 1, 1.5, 4, 2, 2, 2]
def ximass_correct(columns, v, delta):
#  v = 1.31, 1.34
  # delta = 0.15
  # print(columns[1], v)
  return columns[1] < v + delta and columns[1] > v - delta

def vmass_correct(columns, v, delta):
  # 1.1, 1.2
    # print(columns[2], v)
    # print("aa")
    return columns[2] < v+ delta  and columns[2] > v - delta

def v0radius_correct(columns, v, delta):
  return columns[3] < v

def casradius_correct(columns, v, delta):
  return columns[4] < v

def cascos_correct(columns, v, delta):
  return columns[5] > v

def v0cos_correct(columns, v, delta):
  return columns[6] > v

def dcaneg_correct(columns, v, delta):
  return columns[7] < v

def dcapos_correct(columns, v, delta):
  return columns[8] < v

def dcabach_correct(columns, v, delta):
  return columns[9] < v

def dcav0_correct(columns, v, delta):
  return columns[10] < v

def dcacas_correct(columns, v, delta):
  return columns[11] < v

def dcav0pv_correct(columns, v, delta):
  return columns[12] < v

def doverm_correct(columns, v, delta):
  return columns[13] < v

def nsigpion_correct(columns, v, delta):
  return columns[14] < v+ delta and columns[14] > v - delta

def nsigproton_correct(columns, v, delta):
  return columns[15] < v+ delta and columns[15] > v - delta

def nsigbach_correct(columns, v, delta):
  return columns[16] < v+ delta and columns[16] > v - delta

parameter_checks = [vmass_correct, v0radius_correct, casradius_correct, cascos_correct, v0cos_correct, dcaneg_correct, dcapos_correct, dcabach_correct, dcav0_correct, dcacas_correct, dcav0pv_correct, doverm_correct, nsigpion_correct, nsigproton_correct, nsigbach_correct]


def all_correct(columns, x, y):
  for i in range(len(parameter_checks)):
      # print(i, parameter_checks[i])
      a = value_ranges[i][0]
      b = value_ranges[i][1]
      v = (b - a) / 100 * x + a
      delta = deltas[i] / 100 * y
      if not parameter_checks[i](columns, v, delta):
        print(str(parameter_checks[i]) + " WRONG")
        print(v, columns[i+1])
        return False
  return True

def write_row(f, columns):
  for column in columns:
    f.write(str(column) + " ")
  f.write("\n")

f_in= open('real-xi-data.file', 'r')
f_out = open('cut_xi_real.file', 'w')

ximass, v0mass = [], []
for line in f_in:
    line = line.strip()
    columns = [float(s) for s in line.split()]
    # print(columns)
    if all_correct(columns, 50, 200):
      write_row(f_out, columns)

  #  print("xi mass", ximass, "V0 mass", v0mass)

f_in.close()
f_out.close()

f_in_2 = open("cut_xi_real.file", "r")

ximass = []

for line in f_in_2:
    line = line.strip()
    columns = [float(s) for s in line.split()]
    ximass.append(columns[1])

_, bins, _ = plt.hist(ximass, bins = 1000, range = [1.30,1.34])

mu, sigma = stats.norm.fit(ximass)
best_fit_line = stats.norm.pdf(bins, mu, sigma)
plt.plot(bins, best_fit_line)

plt.title('Effective mass plot for Xi')
plt.xlabel('Effective $\Lambda \pi^{-}$ mass (GeV/c$^{2}$)')
plt.ylabel('No. of Events / 4 MeV/c$^{2}$')
# plt.savefig('ximass.pdf')
plt.show()
#plt.hist2d(ximass, v0mass, bins = 100)
#plt.show()
