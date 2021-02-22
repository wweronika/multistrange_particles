##Dominic Herd and Anwesha Sahu
##Credit to Marc mmg998@student.bham.ac.uk for the guassian fitting function
##Date: 15/02/2021
##Version = 1.7
#Known Bugs:

import numpy as np
from matplotlib import colors
norm = colors.LogNorm()
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp

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

def plot(scaleCheck):
    ###plots RealXiData and MCXiData 
    global MCXiData, RealXiData, plt, num     
    numOfBins = 250
    binwidth = (np.max(RealXiData[:,num]) - np.min(RealXiData[:,num]))/numOfBins
    standardBins = np.linspace(np.min(RealXiData[:,num]), np.max(RealXiData[:,num]) + binwidth, numOfBins)  
    
    if scaleCheck == "y":        
        FactorToOne(MCXiData[:,num], alpha = 0.8, label = "MC Xi")
        FactorToOne(RealXiData[:,num], label = "Real Xi")
        yText = 'Scalar Factored Counts (Arbitary Units)'
        
    else:
        plt.hist(MCXiData[:,num], bins = standardBins, alpha=0.8, label='MC Xi')
        plt.hist(RealXiData[:,num], bins = standardBins, alpha=0.5, label='Real Xi')
        yText = "Counts"
        
    plt.legend(loc='upper right')
    
    plt.title(Titles[num])
    plt.xlabel(xAxis[num]) 
    plt.ylabel(yText)
    plt.show()

def FactorToOne(data, alpha = 0.5, label = ""): #Force Histogram y axis max to be 1
    global plt
    (counts, bins) = np.histogram(data, bins=100)
    factor = 1/np.max(counts)
    plt.hist(bins[:-1], bins, weights = factor*counts, alpha=alpha, label= label + " | Y Factor:"+format(factor,'.6f'))

def integrator(data, start, finish):
    pass


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

def gPlusPolyFit():
    RealXiDataClone = RealXiData
    (nHits, bins, patches) = plt.hist(RealXiDataClone[:,num], bins=500, label= 'Real Xi', range = [1.28,1.55])
    
    # bins is the data file so using bins[:-1] it's just selecting the whole dataset
    x = bins[:-1] 
    
    # definition of y as the number of Hits (the Y axis of the histogram)
    y = nHits
    
    ########################################
    #########   Function definitions
    ########################################
    
    #curve_fit is a useful tool for fitting any function with Python.
    #The first argument is the function we want to fit: GplusPoly (the function defined above as the sum of a 2nd degree polynomia and a Guassian.)
    #Second argument: x the X values we want to work with
    #Third argument: y are the Y values of the function associated to X
    #Fourth argument: bounds are the bounds of the parameters of the fit Notice the form: [p1_min,p2_min,p3_min,...] and [p1_max,p2_max,p3_max,...]
    #NOTICE also that the bounds are very important here. Vague limits too much could lead to a bad fitting.
    
    popt,pcov = curve_fit(GplusPoly, x, y, bounds=([40,1.31,0,-5,-30,0,0], [150,1.34,0.01,10,5,200,500]))
    curve_fit0_TR = GplusPoly(x,*popt)
    plt.plot(x,curve_fit0_TR,label='Fitting Curve',color='r',linestyle='--')
    print(popt)
    plt.xlabel(xAxis[num])
    plt.ylabel("Count")
    plt.legend()
    plt.show()
    
    return popt


def tryFloat(data):
    try:
        return float(data)
    except ValueError:
        print("Error (Please ignore)")
        return "null"

def cuts():
    global RealXiData, num
    while True:    
        num = int(input("What column?"))  
      
        scaleCheck = input("Do you want the y-axis to be Scalared to 1? (y/n) ")
        plot(scaleCheck)
        
        lowerLim = input("Lower Limit ('null' = No Limit): ")
        lowerLim = tryFloat(lowerLim)
        
        UpperLim = input("Upper Limit ('null' = No Limit): ")
        UpperLim = tryFloat(UpperLim)
        
        if type(lowerLim) != str:
            x = 0
            while x < len(RealXiData):
                if RealXiData[x,num] < lowerLim:
                    RealXiData = np.delete(RealXiData, x, 0)
                else:
                    x += 1
        
        if type(UpperLim) != str:
            x = 0
            while x < len(RealXiData):
                if RealXiData[x,num] > UpperLim:
                    RealXiData = np.delete(RealXiData, x, 0)
                else:
                    x += 1
             
        plot(scaleCheck)
        
        breaker = input('Do you want stop applying cuts? (y/n) ')
        if breaker == "y":
            break

print("Please wait, this may take a while...")
MCXiData = fileHandler(r'C:\root_v5.34.38\MC-xi-data.file') #Enter you file path for the Monte Carlo Data file!
RealXiData = fileHandler(r'C:\root_v5.34.38\real-xi-data.file') #Enter you file path for the real Data file!
   
###Main Code        
vChoice = None
while vChoice != "0":

    print(
    """
    Menu
    
    0 - Exit
    1 - Start Cuts
    2 - Graph
    3 - Fit
    4 - Integrate
    
    """
    )
    
    vChoice = input("Choice: ")

    # exit
    if vChoice == "0":
        exit()

    # choice  1
    elif vChoice == "1":
        cuts()

    # choice  2
    elif vChoice == "2":
        num = int(input("What column?"))      
        scaleCheck = input("Do you want the y-axis to be Scalared to 1? (y/n) ")
        plot(scaleCheck)
        
    # choice  3
    elif vChoice == "3":
        num = int(input("What column?"))
        fit = gPlusPolyFit()

    # choice  4
    elif vChoice == "4":
        num = int(input("What column?"))
        plot("")   
        print(integrator(RealXiData, 1.30, 1.35))

    # some unknown choice
    else:
        print("Sorry, but", vChoice, "isn't a valid choice.")
        
