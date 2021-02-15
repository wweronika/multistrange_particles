##Dominic Herd
##Date: 08/02/2021
##Version = 1.3
###Known Bugs: Bars are not of constant width after cuts are applied

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
norm = colors.LogNorm()
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
import math 
import scipy.stats as stats


### Change axis Names
Names = ["icand","Ximass","Vmass","V0radius","Casradius","Cascos","V0cos","DCAneg","DCApos", "DCAbach", "DCAV0", "DCAcas","DCAV0PV", "dOverM",
      "NsigPion", "NgisProton", "NsigBach"]

xAxis = ["","Effective mass of the bachelor pion and Lambda system (GeV)",
         "Effective mass of the V0 daughters (GeV)",
         "Distance between the primary vertex (PV) and the Lambda vertex (cm)",
         "Distance between the primary vertex (PV) and the Xi vertex (cm)",
         "Cosine of the angle between the PV and the Xi’s line of flight",
         "Cosine of the angle between the PV and the Lambda’s line of flight",
         "Distance of closest approach (DCA) between pion daughter and PV (cm)",
         "Distance of closest approach (DCA) between proton daughter and PV (cm)",
         "Distance of closest approach (DCA) between bachelor and PV (cm)",
         "Distance of closest approach between the Lambda daughters (sigmas)",
         "Distance of closest approach between the bachelor and Lambda (cm)",
         "Distance of closest approach between the Lambda and PV (cm)",
         "Distance cascade candidate travels before decaying divided by its momentum (cm/GeV)",
         "PID of daughter pion i.e. no. of sigmas (standard deviations) from being a pion",
         "PID of proton i.e. no. of sigmas (standard deviations) from being a proton",
         "PID of bachelor i.e. no. of sigmas (standard deviations) from being a pion"
         ]

Titles = ["","Effective mass of the bachelor pion and Lambda system",
          "Effective mass of the V0 daughters",
          "Distance between the primary vertex (PV) and the Lambda vertex",
          "Distance between the primary vertex (PV) and the Xi vertex",
          "Cosine of the angle between the PV and the Xi’s line of flight",
          "Cosine of the angle between the PV and the Lambda’s line of flight",
          "Distance of closest approach (DCA) between pion daughter and PV",
          "Distance of closest approach (DCA) between proton daughter and PV",
          "Distance of closest approach (DCA) between bachelor and PV",
          "Distance of closest approach between the Lambda daughters",
          "Distance of closest approach between the bachelor and Lambda",
          "Distance of closest approach between the Lambda and PV",
          "Distance cascade candidate travels before decaying divided by its momentum",
          "PID of daughter pion",
          "PID of proton",
          "PID of bachelor"
          ]

column = int(input('Which column?  '))

col_data = []
def fileHandler(filename):
    r = open(filename, 'r')
    

    data = np.zeros(17)  #Formating Declaration
    for line in r:
        line = line.strip()
        newData = np.array([float(s) for s in line.split()])
        data = np.vstack((data, newData)) # data holds 2d array: List[Particle Array Index,Data value: 0-16]            
       
    r.close()
    data = np.delete(data, 0, 0) #Removing Formating Declaration
    return data
    for i in data[:,column]:
        col_data.append(i)
    
    

filename = r'C:\Users\neham\Downloads\Year 2\Lab project\Code\Canvas data files\real-xi-data.file.txt'
fileHandler(filename)

#Gaussian Stuff below:

plt.hist(col_data, density=True, bins=250)

mu = np.average(col_data)
diff_sqrd = []
for i in col_data:
    diff = i - mu
    diff_sqrd.append(diff**2)
sum_var = sum(diff_sqrd)   
variance = sum_var/len(col_data)
sigma = math.sqrt(variance)
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
plt.plot(x, stats.norm.pdf(x, mu, sigma))
plt.ylabel('counts')
plt.xlabel(Names[column])
plt.title(Titles[column])
plt.show()

'''
Imposing cuts where Gaussian curve seems to end: 
    
'''
col_cut = []

def check(col_data): 
    for i in col_data:
        if 1.296 <= float(i) <= 1.3390: 
            col_cut.append(i)    

check(col_data) 
       
plt.hist(col_cut, density=True, bins=100)

mu = np.average(col_cut)
diff_sqrd = []
for i in col_cut:
    diff = i - mu
    diff_sqrd.append(diff**2)
sum_var = sum(diff_sqrd)   
variance = sum_var/len(col_cut)
sigma = math.sqrt(variance)
x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
plt.plot(x, stats.norm.pdf(x, mu, sigma))
plt.ylabel('counts')
plt.xlabel(Names[column])
plt.title(Titles[column])

plt.show()

'''
Marc's Fitting tool
'''

def gauss(t,a,mu,sigma):
    return a*2.71828**(-(t-mu)**2/(2*sigma**2))

def poly2D(t,A,B,C):
    return A*t**2+B*t+C

def GplusPoly(t,a,mu,sigma,A,B,C,D):
    return gauss(t,a,mu,sigma)+D*poly2D(t,A,B,C)
        


(nHits, bins, patches)=plt.hist(data,bins=np.arange(-2,2,0.2),density=True,histtype="step")
x = data[:-1] 

