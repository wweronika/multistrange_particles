# import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

#  1.32181076e+00  1.56580305e-03

def ximass_correct(columns):
  return columns[2] < 1.30 or columns[2] > 1.35

def vmass_correct(columns):
    return columns[3] > 1.11018 and columns[3] < 1.12025

def v0radius_correct(columns):
  return columns[4] < 46.95

def casradius_correct(columns):
  return columns[5] < 19.45

def cascos_correct(columns):
  return columns[6] > 0.99

def v0cos_correct(columns):
  return columns[7] > 0.99

def dcaneg_correct(columns):
  return columns[8] < 16.0

def dcapos_correct(columns):
  return columns[9] < 5.96

def dcabach_correct(columns):
  return columns[10] > 0.4

def dcav0_correct(columns):
  return columns[11] < 0.636

def dcacas_correct(columns):
  return columns[12] < 0.508

def dcav0pv_correct(columns):
  return columns[13] < 2.30

def doverm_correct(columns):
  return columns[14] < 9.61

def nsigpion_correct(columns):
  return columns[15] > -2 and columns[15] < 3

def nsigproton_correct(columns):
  return columns[16] > -2 and columns[16] < 2

def nsigbach_correct(columns):
  return columns[17] > -3 and columns[17] < 4


parameter_checks = [vmass_correct, v0radius_correct, casradius_correct, cascos_correct, v0cos_correct, dcaneg_correct, dcapos_correct, dcabach_correct, dcav0_correct, dcacas_correct, dcav0pv_correct, doverm_correct, nsigpion_correct, nsigproton_correct, nsigbach_correct]
parameter_checks_2 = [ximass_correct, dcabach_correct, nsigproton_correct, cascos_correct, v0cos_correct]


def all_correct(columns):
  for check in parameter_checks_2:
    # print(check(columns))
    # print(check.__name__)
    if not check(columns):
      return False
  return True


def any_correct(columns):
  for check in parameter_checks:
    # print(check(columns))
    # print(check.__name__)
    if check(columns):
      return True
  return False

def write_row(f, columns):
  for column in columns:
    f.write(str(column) + " ")
  f.write("\n")

f_in= open('real-omega-data.file', 'r')
f_out = open('cut_omega_real.file', 'w')

ximass, v0mass = [], []
for line in f_in:
    line = line.strip()
    columns = [float(s) for s in line.split()]
    # print(columns)
    if all_correct(columns):
      write_row(f_out, columns)
      # print(columns)

  #  print("xi mass", ximass, "V0 mass", v0mass)

f_in.close()
f_out.close()

f_in_2 = open("cut_omega_real.file", "r")

ximass = []

for line in f_in_2:
    line = line.strip()
    columns = [float(s) for s in line.split()]
    ximass.append(columns[1])

_, bins, _ = plt.hist(ximass, bins = 100, range = [1.6, 2])

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

