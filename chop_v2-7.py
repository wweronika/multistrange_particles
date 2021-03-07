##Dominic Herd, Anwesha Sahu, Lewis Kilbride
##Credit to Marc mmg998@student.bham.ac.uk for the guassian fitting function
##Date: 01/03/2021
##Version = 2.5
#Known Bugs:
 
import numpy as np
from matplotlib import colors
norm = colors.LogNorm()
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
import scipy.integrate as integrate
plt.ion()
 
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
 
def save():
    FileSaveLocation = input("")
    np.savetxt(FileSaveLocation, RealXiData)
 
def plot(scaleCheck = "n"):
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
 
def integrator(arugments, start, finish):
    value = integrate.quad(GplusPoly, start, finish,args = tuple(arugments))
    return value
 
def integrateSignal(arugments): 
    tempArg = np.copy(arugments)
    tempArg[3] = 0; tempArg[4] = 0; tempArg[5] = 0; tempArg[6] = 0    
    value = integrate.quad(GplusPoly, standToValue(-2,fit), standToValue(2,fit), args = tuple(tempArg))
    return value
 
def integrateBackgroundSig(arugments):
    tempArg = np.copy(arugments)
    tempArg[0] = 0; tempArg[1] = 0; tempArg[2] = 0
    value = integrate.quad(GplusPoly, standToValue(-2,fit), standToValue(2,fit), args = tuple(tempArg))
    return value
 
def standToValue(divations,fit):
    return fit[2]*divations + fit[1]
 
def significance(peak,background):
    return peak/np.sqrt(peak + background)
 
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
def noGraphFit(RealXiDataClone, bounds = ([30,1.31,0,-5,-30,0,0], [150,1.34,0.01,10,5,200,500]), Bins = 500):
    (nHits, bins, patches) = plt.hist(RealXiDataClone[:,1], bins=Bins, label= 'Real Xi', range = [1.28,1.55])
    plt.clf()
    x = bins[:-1]
    y = nHits
    popt,pcov = curve_fit(GplusPoly, x, y, bounds=bounds)
    return popt
 
def gPlusPolyFit(data, Bounds = ([30,1.31,0,-5,-30,0,0], [150,1.34,0.01,10,5,200,500]), Column = 1, Bins = 500, Range = [1.28,1.55]):
    RealXiDataClone = np.copy(data)
    (nHits, bins, patches) = plt.hist(RealXiDataClone[:,Column], bins=Bins, label= 'Real Xi', range = Range)
 
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
 
    popt,pcov = curve_fit(GplusPoly, x, y, bounds = Bounds)
    curve_fit0_TR = GplusPoly(x,*popt)
    plt.plot(x,curve_fit0_TR,label='Fitting Curve',color='r',linestyle='--')
    print(popt)
    plt.xlabel(xAxis[Column])
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
 
def significance_calculations():
    signalIntegral = np.zeros(2)
    backgroundIntegral = np.zeros(2)
    signif = np.zeros(1)
 
    RealXiDataClone = np.copy(RealXiData)
    column = int(input("Enter Column Number: "))
    num = column
    plot()
 
    ##Find where the max value is
    (counts, bins) = np.histogram(RealXiData[:,column], bins=100)
    largestBin = bins[np.argmax(counts)] #value of largest bin
    Binwidth = bins[1] - bins[0]
    #Min and Max data points
    Min = np.min(RealXiData[:,column])
    Max = np.max(RealXiData[:,column])
    numPoints = 200 # Please Enter an Even Value
    cutPoints = np.linspace(np.min(RealXiData[:,column]),np.max(RealXiData[:,column]),num=numPoints)   
    j = 1
    vType = ""        
 
    if column == 2:
        setBounds = ([1,1.115,0,-5,-30,0,0], [150,1.1175,0.001,10,5,200,500])
    elif column == 14:
        setBounds = ([1,-1,0,-5,-30,0,0], [2500,1,5,10,5,200,500])
    elif column == 15:
        setBounds = ([1,-1,0,-5,-30,0,0], [1000,1,5,10,5,200,500])
    elif column == 16:
        setBounds = ([1,-1,0,-5,-30,0,0], [3000,1,5,10,5,200,500])    
 
    #Find if peak close to being at min/max
    else:
        #Find If closer to Min or max
        # If DCA_bachelor (column 10), then cut the min values
        if abs(Max - largestBin) < abs(largestBin - Min) or column == 10: # Then have a Peak value at Max
            vType = "Max"
            print("Max")
 
        else:   # Then have a Peak value at Min
            vType = "Min"
            print("Min")
            cutPoints = np.flip(cutPoints) #Allows optomisation via not needing data to be reset
 
    if vType != "Max" and vType != "Min":            
        vType = "Gauss"    #Then have a gaussian
        (fit) = gPlusPolyFit(RealXiData, Bounds = setBounds, Column = column, Bins = 200, Range = None)
        lowerSigma = fit[1] - 2*fit[2]    
        upperSigma = fit[1] + 2*fit[2]
 
 
        lowerPoints = np.linspace(np.min(RealXiData[:,column]),lowerSigma,num=int(numPoints/2))
        HigherPoints = np.flip(np.linspace(upperSigma,np.max(RealXiData[:,column]),num=int(numPoints/2)))
 
        cutPoints = np.concatenate((lowerPoints,HigherPoints))
 
 
    for i in cutPoints:
        x = 0
        if vType == "Max":
            while x < len(RealXiDataClone):
                if RealXiDataClone[x,column] < i:
                    RealXiDataClone = np.delete(RealXiDataClone, x, 0)
                else:
                    x += 1
 
        elif vType == "Min":
            while x < len(RealXiDataClone):
                if RealXiDataClone[x,column] > i:
                    RealXiDataClone = np.delete(RealXiDataClone, x, 0)
                else:
                    x += 1
        else:
            if i <= lowerPoints[-1]:    
                while x < len(RealXiDataClone):
                    if RealXiDataClone[x,column] < i:
                        RealXiDataClone = np.delete(RealXiDataClone, x, 0)
                    else:
                        x += 1
                if i == lowerPoints[-1]:
                    RealXiDataClone = np.copy(RealXiData)
            else:    
                while x < len(RealXiDataClone):
                    if RealXiDataClone[x,column] > i:
                        RealXiDataClone = np.delete(RealXiDataClone, x, 0)
                    else:
                        x += 1
 
        try:    #Check if Guassian can still be fitted on data set
            (fit) = noGraphFit(RealXiDataClone, Bins = 300)
        except RuntimeError:
            print(j)
            cutPoints = cutPoints[:j]
            break
 
        peak = integrateSignal(fit)
        background = integrateBackgroundSig(fit)
 
        signalIntegral = np.vstack((signalIntegral, peak))                
        backgroundIntegral = np.vstack((backgroundIntegral,background))
 
        signif = np.vstack((signif,significance(peak[0],background[0])))
        print(j)
        j+=1
 
    signalIntegral = np.delete(signalIntegral, 0, 0)
    backgroundIntregral = np.delete(backgroundIntegral, 0, 0)    
    signif = np.delete(signif, 0)
 
    if vType != "Gauss":
        plt.plot(cutPoints, signalIntegral[:,0],label='Signal',color='r',linestyle='--')
        plt.plot(cutPoints, backgroundIntregral[:,0],label='Background',color='b',linestyle='--')
        plt.plot(cutPoints, signif,label='Significance',color='g')
    else:
        marker = int((numPoints/2)-1)
        marker2 = int((numPoints/2))
        plt.plot(cutPoints[:marker], signalIntegral[:marker,0],label='Signal',color='r',linestyle='--')
        plt.plot(cutPoints[:marker], backgroundIntregral[:marker,0],label='Background',color='b',linestyle='--')
        plt.plot(cutPoints[:marker], signif[:marker],label='Significance',color='g')
 
        plt.xlabel("Cut value of:  "+xAxis[column]) ##Create two grpahs - easier to read
        plt.ylabel("Integral value")
        plt.legend()
        plt.show()            
 
        plt.plot(cutPoints[marker2:], signalIntegral[marker2:,0],color='r',linestyle='--')
        plt.plot(cutPoints[marker2:], backgroundIntregral[marker2:,0],color='b',linestyle='--')
        plt.plot(cutPoints[marker2:], signif[marker2:],color='g')
 
    plt.xlabel("Cut value of:  "+xAxis[column])
    plt.ylabel("Integral value")
    plt.legend()
    plt.show()
    plt.pause(30)
 
print("Please wait, this may take a while...")
MCXiData = fileHandler(r'MC-xi-data.file') #Enter you file path for the Monte Carlo Data file!
RealXiData = fileHandler(r'real-xi-data.file') #Enter you file path for the real Data file!
 
 
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
    5 - Save
    6 - Significance Graph
 
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
        (fit) = gPlusPolyFit(RealXiData)
 
    # choice  4
    elif vChoice == "4":
        breaker = False
        try:
            fit = fit
        except NameError:
            breaker = True
 
        if not breaker:
            lowerLimDev = float(input("Lower Limit in sigma: "))
            UpperLimDev = float(input("Upper Limit in sigma: "))
            lowerLimVal = standToValue(lowerLimDev, fit)
            UpperLimVal = standToValue(UpperLimDev, fit)
 
            print(integrator(fit, lowerLimVal, UpperLimVal))
 
    # choice  5
    elif vChoice == "5":
        save()
 
   # choice  6
    elif vChoice == "6":
        significance_calculations()
 
    # some unknown choice
    else:
        print("Sorry, but", vChoice, "isn't a valid choice.")