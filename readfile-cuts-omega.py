# import numpy as np
import matplotlib.pyplot as plt

def ximass_correct(columns):
    return columns[2] > 1.25 and columns[2] < 1.5

def vmass_correct(columns):
  return columns[3] > 1.11 and columns[3] < 1.2

def v0radius_correct(columns):
  return columns[4] < 50

def casradius_correct(columns):
  return columns[5] < 15

def cascos_correct(columns):
  return columns[6] > 0.99

def v0cos_correct(columns):
  return columns[7] > 0.985

def dcaneg_correct(columns):
  return columns[8] < 15

def dcapos_correct(columns):
  return columns[9] < 3.5

def dcabach_correct(columns):
  return columns[10] < 2.5

def dcav0_correct(columns):
  return columns[11] < 0.7

def dcacas_correct(columns):
  return columns[12] < 0.5

def dcav0pv_correct(columns):
  return columns[13] < 1.6

def doverm_correct(columns):
  return columns[14] < 5


def nsigpion_correct(columns):
  return columns[15] > -1.5 and columns[15] < 2.5

def nsigproton_correct(columns):
  return columns[16] > -1.5 and columns[16] < 3

def nsigbach_correct(columns):
  return columns[17] < 16


parameter_checks = [ximass_correct, vmass_correct, v0radius_correct, casradius_correct, cascos_correct, v0cos_correct, dcaneg_correct, dcapos_correct, dcabach_correct, dcav0_correct, dcacas_correct, dcav0pv_correct, doverm_correct, nsigpion_correct, nsigproton_correct, nsigbach_correct]



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

f_in= open('real-Omega-data.file', 'r')
f_out = open('cut_omega_real.file', 'w')

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

f_in_2 = open("cut_omega_real.file", "r")

ximass = []

for line in f_in_2:
    line = line.strip()
    columns = [float(s) for s in line.split()]
    ximass.append(columns[1])

plt.hist(ximass, bins = 100, range = [1.3,2])
plt.title('Effective mass plot for Xi')
plt.xlabel('Effective $\Lambda \pi^{-}$ mass (GeV/c$^{2}$)')
plt.ylabel('No. of Events / 4 MeV/c$^{2}$')
# plt.savefig('ximass.pdf')
plt.show()
#plt.hist2d(ximass, v0mass, bins = 100)
#plt.show()
