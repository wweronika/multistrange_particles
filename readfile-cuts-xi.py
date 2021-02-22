# import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def ximass_correct(columns):
  return columns[1] > 1.31 and columns[1] < 1.34

def vmass_correct(columns):
    return columns[2] > 0.9 and columns[2] < 1.4

def v0radius_correct(columns):
  return columns[3] < 45

def casradius_correct(columns):
  return columns[4] < 35

def cascos_correct(columns):
  return columns[5] > 0.98

def v0cos_correct(columns):
  return columns[6] > 0.98

def dcaneg_correct(columns):
  return columns[7] < 25

def dcapos_correct(columns):
  return columns[8] < 6

def dcabach_correct(columns):
  return columns[9] < 6

def dcav0_correct(columns):
  return columns[10] < 2.5

def dcacas_correct(columns):
  return columns[11] < 2.5

def dcav0pv_correct(columns):
  return columns[12] < 3

def doverm_correct(columns):
  return columns[13] < 20

def nsigpion_correct(columns):
  return columns[14] > -2 and columns[14] < 3

def nsigproton_correct(columns):
  return columns[15] > -3 and columns[15] < 5

def nsigbach_correct(columns):
  return columns[16] > -3 and columns[16] < 4


parameter_checks = [vmass_correct, v0radius_correct, casradius_correct, cascos_correct, v0cos_correct, dcaneg_correct, dcapos_correct, dcabach_correct, dcav0_correct, dcacas_correct, dcav0pv_correct, doverm_correct, nsigpion_correct, nsigproton_correct, nsigbach_correct]



def all_correct(columns):
  for check in parameter_checks:
    # print(check(columns))
    # print(check.__name__)
    if not check(columns):
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
    if all_correct(columns):
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

_, bins, _ = plt.hist(ximass, bins = 200, range = [1.25,1.38])

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
