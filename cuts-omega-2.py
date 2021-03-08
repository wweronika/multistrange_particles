# import numpy as np
import matplotlib.pyplot as plt

def omegamass_high(columns):
    return columns[1] > 1.7

def ximass_far(columns):
  return not(columns[2] > 1.31 and columns[2] < 1.33) 

# def probably_not_xi(columns):
#   return not (omegamass_low(columns) and not nsigproton_correct(columns))

def ximass_correct(columns):
    return not (columns[2] > 1.31 and columns[2] < 1.34) and columns[2] <1.50
def vmass_correct(columns):
  return columns[3] > 1.05 and columns[3] < 1.13

def v0radius_correct(columns):
  return columns[4] > 2 and columns[4] < 50

def casradius_correct(columns):
  return columns[5] < 15 and columns[5] > 1.5

def cascos_correct(columns):
  return columns[6] > 0.995

def v0cos_correct(columns):
  return columns[7] > 0.99

def dcaneg_correct(columns):
  return columns[8] > 0.4

def dcapos_correct(columns):
  return columns[9] > 0.45

def dcabach_correct(columns):
  return columns[10] > 0.45 and columns[10] > 0.05

def dcav0_correct(columns):
  return columns[11] < 0.7

def dcacas_correct(columns):
  return columns[12] < 0.5

def dcav0pv_correct(columns):
  return columns[13] < 1.6

def doverm_correct(columns):
  return columns[14] < 5 and columns[14] > 1.5


def nsigpion_correct(columns):
  return columns[15] > -2 and columns[15] < 3

def nsigproton_correct(columns):
  return columns[16] > -1.5 and columns[16] < 4

def nsigbach_correct(columns):
  return columns[17] < 20


parameter_checks = [vmass_correct, v0radius_correct, casradius_correct, cascos_correct, v0cos_correct, dcaneg_correct, dcapos_correct, dcabach_correct, dcav0_correct, dcacas_correct, dcav0pv_correct, doverm_correct, nsigpion_correct, nsigproton_correct, nsigbach_correct]
parameter_checks_2 = [ximass_correct, dcabach_correct, nsigproton_correct, cascos_correct, v0cos_correct]


def all_checks_correct(columns):
  for check in parameter_checks_2:
    # print(check(columns))
    # print(check.__name__)
    if not check(columns):
      return False
  return True

def any_checks_correct(columns):
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


def show_all_plots(data):
  for i in range(18):
    plt.hist(data[i], bins = 100, range = [min(data[i]), max(data[i])])
    plt.title('Effective mass plot for Omega')
    plt.xlabel('Effective $\Lambda \pi^{-}$ mass (GeV/c$^{2}$)')
    plt.ylabel('No. of Events / 4 MeV/c$^{2}$')
    # plt.savefig('ximass.pdf')
    plt.show()
    #plt.hist2d(ximass, v0mass, bins = 100)
    #plt.show()

def show_plot(property):
  plt.hist(property, bins = 120, range = [min(property), max(property)])
  plt.title('Effective mass plot for Omega')
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
    print(columns[2])
    for i in range(18):
      data[i].append(columns[i])

show_plot(data[1])

