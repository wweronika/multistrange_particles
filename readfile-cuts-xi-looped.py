# import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

from GaussFit import *

value_ranges = [[1.31,1.34], [1.1, 1.2], [35, 45], [25,35], [0.97, 0.99], [0.97, 0.99], [15, 25], [3, 5], [4, 6], [1.5, 2.5], [1.5, 2.5], [2,3], [10,14], [-1, 2], [-1, 3], [-1, 2]]

def ximass_correct(columns, v, percent):
#  v = 1.31, 1.34
  return columns[1] > v*(1+percent) and columns[1] < v*(1-percent)

def vmass_correct(columns, v, percent):
  # 1.1, 1.2
    return columns[2] > v*(1+percent)  and columns[2] < v*(1-percent)

def v0radius_correct(columns, v, percent):
  return columns[3] < v

def casradius_correct(columns, v, percent):
  return columns[4] < v

def cascos_correct(columns, v, percent):
  return columns[5] > v

def v0cos_correct(columns, v, percent):
  return columns[6] > v

def dcaneg_correct(columns, v, percent):
  return columns[7] < v

def dcapos_correct(columns, v, percent):
  return columns[8] < v

def dcabach_correct(columns, v, percent):
  return columns[9] < v

def dcav0_correct(columns, v, percent):
  return columns[10] < v

def dcacas_correct(columns, v, percent):
  return columns[11] < v

def dcav0pv_correct(columns, v, percent):
  return columns[12] < v

def doverm_correct(columns, v, percent):
  return columns[13] < v

def nsigpion_correct(columns, v, percent):
  return columns[14]> v*(1+percent) and columns[14] < v*(1-percent)

def nsigproton_correct(columns, v, percent):
  return columns[15]> v*(1+percent) and columns[15] < v*(1-percent)

def nsigbach_correct(columns, v, percent):
  return columns[16]> v*(1+percent) and columns[16] < v*(1-percent)

parameter_checks = [ximass_correct, vmass_correct, v0radius_correct, casradius_correct, cascos_correct, v0cos_correct, dcaneg_correct, dcapos_correct, dcabach_correct, dcav0_correct, dcacas_correct, dcav0pv_correct, doverm_correct, nsigpion_correct, nsigproton_correct, nsigbach_correct]


def all_correct(columns, v, percent):
  for check in parameter_checks:
    # print(check(columns))
    # print(check.__name__)
    if not check(columns, v, percent):
      return False
  return True

def write_row(f, columns):
  for column in columns:
    f.write(str(column) + " ")
  f.write("\n")














ximass, v0mass = [], []

for j in range(1, 100):
  # print(i, j)
  percent = j * 0.3/100

  f_in= open('real-xi-data.file', 'r')
  f_out = open('cut_xi_real.file', 'w')

  for line in f_in:
    line = line.strip()
    columns = [float(s) for s in line.split()]
    # print(columns)
    
    for i, check in enumerate(parameter_checks):
      a = value_ranges[i][0]
      b = value_ranges[i][1]
      v = (b - a) / 100 * j + a
      if all_correct(columns, v, percent):
        write_row(f_out, columns)

    f_in.close()
    f_out.close()

    f_in_2 = open("cut_xi_real.file", "r")

    ximass = []

    for line in f_in_2:
        line = line.strip()
        columns = [float(s) for s in line.split()]
        ximass.append(columns[1])

    
    # (nHits, bins, patches)=plt.hist(dist,bins=np.arange(-10,10,0.2),density=True,histtype="step")
    nHits, bins, patches = plt.hist(ximass, bins = 500, range = [1.30,1.34])

    # bins is the data file so using bins[:-1] it's just selecting the whole dataset
    x = bins[:-1] 

    # definition of y as the number of Hits (the Y axis of the histogram)
    y =nHits
    try:
      popt,pcov = curve_fit(GplusPoly, x, y, bounds=([0,0,0,0,-30,0,0], [10,10,10,10,0,200,0.5]))

      # print(popt[2])
      # print("aaaaaa")
      # print(pcov)
      # input()

      gpolyIntegral = GplusPolyIntegral(1.25, 1.38, popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], popt[6])
      gaussIntegral = GaussIntegral(1.25, 1.38, popt[0], popt[1], popt[2])
      print(gaussIntegral/gpolyIntegral)
      
      curve_fit0_TR = GplusPoly(x,*popt)
      plt.plot(x,curve_fit0_TR,label='Fitting Curve',color='r',linestyle='--')
      print(popt)
      plt.xlabel("X [arbitrary Units]")
      plt.ylabel("Count")
      plt.legend()
      plt.show()

    except:
      pass

    # mu, sigma = stats.norm.fit(ximass)
    # best_fit_line = stats.norm.pdf(bins, mu, sigma)

  #  print("xi mass", ximass, "V0 mass", v0mass)


# ximass = []

# for line in f_in_2:
#     line = line.strip()
#     columns = [float(s) for s in line.split()]
#     ximass.append(columns[1])

# _, bins, _ = plt.hist(ximass, bins = 1000, range = [1.30,1.34])

# mu, sigma = stats.norm.fit(ximass)
# best_fit_line = stats.norm.pdf(bins, mu, sigma)
# plt.plot(bins, best_fit_line)

# plt.title('Effective mass plot for Xi')
# plt.xlabel('Effective $\Lambda \pi^{-}$ mass (GeV/c$^{2}$)')
# plt.ylabel('No. of Events / 4 MeV/c$^{2}$')
# # plt.savefig('ximass.pdf')
# plt.show()
# #plt.hist2d(ximass, v0mass, bins = 100)
# #plt.show()
