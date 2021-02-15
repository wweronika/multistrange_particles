# import numpy as np
import matplotlib.pyplot as plt

def omegamass_low(columns):
    return columns[1] < 1.65

def ximass_far(columns):
  return not (columns[2] > 1.31 and columns[2] < 1.34)

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


parameter_checks = [ximass_far, vmass_correct, v0radius_correct, casradius_correct, cascos_correct, v0cos_correct, dcaneg_correct, dcapos_correct, dcabach_correct, dcav0_correct, dcacas_correct, dcav0pv_correct, doverm_correct, nsigpion_correct, nsigproton_correct, nsigbach_correct]
parameter_checks_2 = [omegamass_low]


def all_checks_correct(columns):
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


def show_all_plots(data):
  for i in range(18):
    plt.hist(data[i], bins = 100, range = [min(data[i]), max(data[i])])
    plt.title('Effective mass plot for Xi')
    plt.xlabel('Effective $\Lambda \pi^{-}$ mass (GeV/c$^{2}$)')
    plt.ylabel('No. of Events / 4 MeV/c$^{2}$')
    # plt.savefig('ximass.pdf')
    plt.show()
    #plt.hist2d(ximass, v0mass, bins = 100)
    #plt.show()

def show_plot(property):
  plt.hist(property, bins = 100, range = [min(property), max(property)])
  plt.title('Effective mass plot for Xi')
  plt.xlabel('Effective $\Lambda \pi^{-}$ mass (GeV/c$^{2}$)')
  plt.ylabel('No. of Events / 4 MeV/c$^{2}$')
  # plt.savefig('ximass.pdf')
  plt.show()
  #plt.hist2d(ximass, v0mass, bins = 100)
  #plt.show()



# Read original file and save to output file if the checks are correct

f_in= open('real-Omega-data.file', 'r')
f_out = open('cut_low_mass_omega_real.file', 'w')

ximass, v0mass = [], []
for line in f_in:
    line = line.strip()
    columns = [float(s) for s in line.split()]
    if all_checks_correct(columns):
      write_row(f_out, columns)

f_in.close()
f_out.close()

# Read cut file and plot data

f_in_2 = open("cut_low_mass_omega_real.file", "r")

omegamass = []
data = [[] for i in range(18)]

for line in f_in_2:
    line = line.strip()
    columns = [float(s) for s in line.split()]
    omegamass.append(columns[1])
    print(columns[1])
    for i in range(18):
      data[i].append(columns[i])

show_plot(omegamass)

