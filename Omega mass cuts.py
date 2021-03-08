# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
norm = colors.LogNorm()
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp

def omegamass_high(columns):
    return columns[1] > 1.7

def ximass_far(columns):
  return not(columns[2] > 1.31 and columns[2] < 1.33) 

# def probably_not_xi(columns):
#   return not (omegamass_low(columns) and not nsigproton_correct(columns))

def ximass_correct(columns):
    return not (columns[2] > 1.31 and columns[2] < 1.34) and columns[2] <1.5
def vmass_correct(columns):
  return columns[3] > 1.1125 and columns[3] < 1.125

def v0radius_correct(columns):
  return columns[4] > 0 and columns[4] < 60

def casradius_correct(columns):
  return columns[5] > 0 and columns[5] < 15

def cascos_correct(columns):
  return columns[6] > 0.999

def v0cos_correct(columns):
  return columns[7] > 0.998

def dcaneg_correct(columns):
  return columns[8] > 0 and columns[8] < 2

def dcapos_correct(columns):
  return columns[9] > 0 and columns[9] < 0.2

def dcabach_correct(columns):
  return columns[10] > 0 and columns[10] < 5

def dcav0_correct(columns):
  return columns[11] > 0 and columns[11] < 0.75

def dcacas_correct(columns):
  return columns[12] > 0 and columns[12] < 0.5

def dcav0pv_correct(columns):
  return columns[13] > 0 and columns[13] < 2

def doverm_correct(columns):
  return columns[14] > 0 and columns[14] < 8

def nsigpion_correct(columns):
  return columns[15] > -3 and columns[15] < 3

def nsigproton_correct(columns):
  return columns[16] > -2 and columns[16] < 2

def nsigbach_correct(columns):
  return columns[17] > -5 and columns[17] < 5


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
  #plt.hist(property, bins = 120, range = [min(property), max(property)])
  plt.hist(property, bins = 50, range = [1.62, 1.75])
  plt.title('Effective mass plot for Omega')
  plt.xlabel('Effective $\Lambda \pi^{-}$ mass (GeV/c$^{2}$)')
  plt.ylabel('No. of Events / 4 MeV/c$^{2}$')
  # plt.savefig('ximass.pdf')
  plt.show()
  #plt.hist2d(ximass, v0mass, bins = 100)
  #plt.show()
  
def gauss(t,a,mu,sigma):
    return a*2.71828**(-(t-mu)**2/(2*sigma**2))

def poly2D(t,A,B,C):
    return A*t**2+B*t+C

def GplusPoly(t,a,mu,sigma,A,B,C,D):
    return gauss(t,a,mu,sigma)+D*poly2D(t,A,B,C)

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
    #print(columns[2])
    for i in range(18):
      data[i].append(columns[i])

show_plot(data[1])


