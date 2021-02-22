import numpy as np
from matplotlib import colors
norm = colors.LogNorm()
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp

########################################
#########   Function definitions
########################################

def gauss(t,a,mu,sigma):
    return a*2.71828**(-(t-mu)**2/(2*sigma**2))

def poly2D(t,A,B,C):
    return A*t**2+B*t+C

def GplusPoly(t,a,mu,sigma,A,B,C,D):
    return gauss(t,a,mu,sigma)+D*poly2D(t,A,B,C)



########################################
#########  Rdm nums under certian pdf
########################################

size =10000

dist=np.array([])
#x=np.array([np.random.uniform(-5,5,size*5)])
l=0

for t in range(size*5):
    x=np.array([np.random.uniform(-10,10,1)])
    y = np.array([np.random.uniform(0,10,1)])
    if y <= GplusPoly(x,5,2,3,1,-20,100,0.01):
        dist= np.append(dist,x)        
        l = 1+l
    if l==size:
         break

f_in_2 = open("cut_xi_real.file", "r")

ximass = []

for line in f_in_2:
    line = line.strip()
    columns = [float(s) for s in line.split()]
    ximass.append(columns[1])

# (nHits, bins, patches)=plt.hist(dist,bins=np.arange(-10,10,0.2),density=True,histtype="step")
nHits, bins, patches = plt.hist(ximass, bins = 300, range = [1.29, 1.35])

# bins is the data file so using bins[:-1] it's just selecting the whole dataset
x = bins[:-1] 

# definition of y as the number of Hits (the Y axis of the histogram)
y =nHits



########################################
#########   Function definitions
########################################

#curve_fit is a useful tool for fitting any function with Python.
#The first argument is the function we want to fit: GplusPoly (the function defined above as the sum of a 2nd degree polynomia and a Guassian.)
#Second argument: x the X values we want to work with
#Third argument: y are the Y values of the function associated to X
#Fourth argument: bounds are the bounds of the parameters of the fit Notice the form: [p1_min,p2_min,p3_min,...] and [p1_max,p2_max,p3_max,...]
#NOTICE also that the bounds are very important here. Vague limits too much could lead to a bad fitting.

popt,pcov = curve_fit(GplusPoly, x, y, bounds=([0,0,0,0,-30,0,0], [10,10,10,10,0,200,0.5]))
curve_fit0_TR = GplusPoly(x,*popt)
plt.plot(x,curve_fit0_TR,label='Fitting Curve',color='r',linestyle='--')
print(popt)
plt.xlabel("X [arbitrary Units]")
plt.ylabel("Count")
plt.legend()
plt.show()



