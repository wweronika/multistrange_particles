##Dominic Herd, Anwesha Sahu, Lewis Kilbride, Weronika Wiesiolek
##Credit to Marc mmg998@student.bham.ac.uk for the guassian fitting function
##Date: 08/03/2021
##Version = 2.8
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
Names = ["icand","Ommass","Ximass","Vmass","V0radius","Casradius","Cascos","V0cos","DCAneg","DCApos", "DCAbach", "DCAV0", "DCAcas","DCAV0PV", "dOverM",
      "NsigPion", "NgisProton", "NsigBach"]
 
xAxis = ["","Effective mass of the bachelor kaon and Lambda system (GeV)",
         "Effective mass of the bachelor pion and Lambda system (GeV)",
         "Effective mass of the V0 daughters (GeV)",
         "Distance between the primary vertex (PV) and the Lambda vertex (cm)",
         "Distance between the primary vertex (PV) and the Omega vertex (cm)",
         "Cosine of the angle between the PV and the Omega’s line of flight",
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
 
Titles = ["", "Effective mass of the bachelor kaon and Lambda system",
          "Effective mass of the bachelor pion and Lambda system",
          "Effective mass of the V0 daughters",
          "Distance between the primary vertex (PV) and the Lambda vertex",
          "Distance between the primary vertex (PV) and the Omega vertex",
          "Cosine of the angle between the PV and the Omega’s line of flight",
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
 
    data = np.zeros(18)  #Formating Declaration
    for line in r:
        line = line.strip()
        newData = np.array([float(s) for s in line.split()])
        data = np.vstack((data, newData)) # data holds 2d array: List[Particle Array Index,Data value: 0-16]            
 
    r.close()
    data = np.delete(data, 0, 0) #Removing Formating Declaration
 
    return data
 
def save():
    FileSaveLocation = input("Enter Save Location: ")
    np.savetxt(FileSaveLocation, RealXiData)
 
def soloPlot():
    global RealXiData, plt
    #numOfBins = 50
    Range = [min(RealXiData[:,1]),1.75]
    #binwidth = (Range[1] - Range[0])/numOfBins
    #standardBins = np.linspace(Range[0], Range[1] + binwidth, numOfBins)
    #plt.hist(RealXiData[:,1], bins = standardBins, label='Real Omega', range = Range)
    plt.hist(RealXiData[:,1], bins = 50, label='Real Omega', range = Range)
    yText = "Counts"
 
    plt.legend(loc='upper right')
 
    plt.title(Titles[1])
    plt.xlabel(xAxis[1]) 
    plt.ylabel(yText)
    plt.show()
 
def plot(scaleCheck = "n",Range = None):
    ###plots RealXiData and MCXiData 
    global MCXiData, RealXiData, plt, num
    numOfBins = 50
    if num == 1:
        Range = [1.6,1.8]
        binwidth = (1.8 - 1.6)/numOfBins
        standardBins = np.linspace(1.6, 1.8 + binwidth, numOfBins)
        
    else:           
        binwidth = (np.max(RealXiData[:,num]) - np.min(RealXiData[:,num]))/numOfBins
        standardBins = np.linspace(np.min(RealXiData[:,num]), np.max(RealXiData[:,num]) + binwidth, numOfBins)  
 
    if scaleCheck == "y":        
        FactorToOne(MCXiData[:,num], alpha = 0.8, label = "MC Omega", Range = Range, bins = numOfBins)
        FactorToOne(RealXiData[:,num], label = "Real Omega", Range = Range, bins = numOfBins)
        yText = 'Scalar Factored Counts (Arbitary Units)'
 
    else:
        plt.hist(MCXiData[:,num], bins = standardBins, alpha=0.8, label='MC Omega', range = Range)
        plt.hist(RealXiData[:,num], bins = standardBins, alpha=0.5, label='Real Omega', range = Range)
        yText = "Counts"
 
    plt.legend(loc='upper right')
 
    plt.title(Titles[num])
    plt.xlabel(xAxis[num]) 
    plt.ylabel(yText)
    plt.show()
 
def FactorToOne(data, alpha = 0.5, label = "",Range = None, bins = 100): #Force Histogram y axis max to be 1
    global plt
    if Range != None:
        data = data[data > Range[0]]
        data = data[data < Range[1]]
        
    (counts, bins) = np.histogram(data, bins=bins)
    factor = 1/np.max(counts)
    plt.hist(bins[:-1], bins, weights = factor*counts, alpha=alpha, label= label + " | Y Factor:"+format(factor,'.6f'))
 
def integrator(arugments, start, finish):
    value = integrate.quad(GplusPoly, start, finish,args = tuple(arugments))
    return value
 
def integrateSignal(arugments): 
    tempArg = np.copy(arugments)
    tempArg[3] = 0; tempArg[4] = 0; tempArg[5] = 0; tempArg[6] = 0    
    value = integrate.quad(GplusPoly, standToValue(-2,arugments), standToValue(2,arugments), args = tuple(tempArg))
    return value
 
def integrateBackgroundSig(arugments):
    tempArg = np.copy(arugments)
    tempArg[0] = 0; tempArg[1] = 0; tempArg[2] = 0
    value = integrate.quad(GplusPoly, standToValue(-2,arugments), standToValue(2,arugments), args = tuple(tempArg))
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
def noGraphFit(RealXiDataClone, bounds = ([2,1.66,0,-5,-30,0,0], [25,1.68,0.2,10,5,200,500]), Bins = 50, Range = [1.6,1.825]):
    (nHits, bins, patches) = plt.hist(RealXiDataClone[:,1], bins=Bins, label= 'Real Omega', range = Range)
    plt.clf()
    x = bins[:-1]
    y = nHits
    popt,pcov = curve_fit(GplusPoly, x, y, bounds=bounds)
    return popt
 
def gPlusPolyFit(data, Bounds = ([2,1.66,0,-5,-30,0,0], [25,1.68,0.1,10,5,200,500]), Column = 1, Bins = 50, Range = [1.6,1.825]):
    RealXiDataClone = np.copy(data)
    (nHits, bins, patches) = plt.hist(RealXiDataClone[:,Column], bins=Bins, label= 'Real Omega', range = Range)
 
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
    values = np.linspace(min(x), max(x), num = 1000)
    curve_fit0_TR = GplusPoly(values,*popt)
    plt.plot(values,curve_fit0_TR,label='Fitting Curve',color='r',linestyle='--')
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
 
def presetCuts():
    global RealXiData, num
    
    cutPoints = [[None,None],
                [1.11,1.122],
                [0,55],
                [None,None],
                [0.992,None],
                [0.98,None],
                [None,None],
                [None,2],
                [0,5],
                [0,1],
                [None,0.6],
                [None,2],
                [None,8],
                [-5,5],
                [-3,3],
                [-8,8]]
        
    for i in range(16):
        lowerLim = cutPoints[i][0]
        if lowerLim != None:
            x = 0
            while x < len(RealXiData):
                if RealXiData[x,i+2] < lowerLim:
                    RealXiData = np.delete(RealXiData, x, 0)
                else:
                    x += 1
                    
        upperLim = cutPoints[i][1]
        if upperLim != None:
            x = 0
            while x < len(RealXiData):
                if RealXiData[x,i+2] > upperLim:
                    RealXiData = np.delete(RealXiData, x, 0)
                else:
                    x += 1
        
        if i == 0:
            x = 0
            while x < len(RealXiData):
                if RealXiData[x,i+2] > 1.315 and RealXiData[x,i+2] < 1.34:
                    RealXiData = np.delete(RealXiData, x, 0)
                else:
                    x += 1
    
    soloPlot()
 
def cuts():
    global RealXiData, num
    while True:
        num = int(input("What column?"))  
 
        #scaleCheck = input("Do you want the y-axis to be Scalared to 1? (y/n) ")
        #plot(scaleCheck)
        
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

                    
        #plot(scaleCheck)
 
        breaker = input('Do you want stop applying cuts? (y/n) ')
        if breaker == "y":
            break
 
def significance_calculations():
    global num
    signalIntegral = np.zeros(2)
    backgroundIntegral = np.zeros(2)
    signif = np.zeros(1)
 
    RealXiDataClone = np.copy(RealXiData)
    column = int(input("Enter Column Number: "))
    num = column
    plot()
 
    ##Find where the max value is
    (counts, bins) = np.histogram(RealXiData[:,column], bins=50)
    largestBin = bins[np.argmax(counts)] #value of largest bin
    Binwidth = bins[1] - bins[0]
    #Min and Max data points
    Min = np.min(RealXiData[:,column])
    Max = np.max(RealXiData[:,column])
    numPoints = 100 # Please Enter an Even Value
    cutPoints = np.linspace(np.min(RealXiData[:,column]),np.max(RealXiData[:,column]),num=numPoints)   
    j = 1
    vType = ""        
 
    
    if column == 3:
        setBounds = ([1,1.115,0,-5,-30,0,0], [30,1.1175,0.001,10,5,200,500])
    elif column == 15:
        setBounds = ([1,-1,1,-5,-30,0,0], [50,1,5,10,5,200,500])
    elif column == 16:
        setBounds = ([1,-1,1,-5,-30,0,0], [50,1,5,10,5,200,500])
    elif column == 17:
        setBounds = ([1,-1,1,-5,-30,0,0], [50,1,5,10,5,200,500])    
 
    #Find if peak close to being at min/max
    else:
        #Find If closer to Min or max
        # If DCA_bachelor (column 10), then cut the min values
        if abs(Max - largestBin) < abs(largestBin - Min): # Then have a Peak value at Max   ###or column == 10: 
            vType = "Max"
            print("Max")
 
        else:   # Then have a Peak value at Min
            vType = "Min"
            print("Min")
            cutPoints = np.flip(cutPoints) #Allows optomisation via not needing data to be reset
 
    if vType != "Max" and vType != "Min":            
        vType = "Gauss"    #Then have a gaussian
        if column == 2:
            lowerSigma = 1.5
            upperSigma = 1.5
        
        elif column == 10:
            lowerSigma = 0.05
            upperSigma = 0.055
        else:
            (fit) = gPlusPolyFit(RealXiData, Bounds = setBounds, Column = column, Bins = 50, Range = None)
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
            (fit) = noGraphFit(RealXiDataClone, Bins = 50)
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
    #plt.pause(30)
 
def histogram2d():
    col = int(input("Which column?"))
        
    y_start = min(RealXiData[:,col])
    y_end = max(RealXiData[:,col])
    
    yRangeArray = [[None,None], #col 2
                [None,None],    #col 3
                [0,75],         #col 4 etc.
                [0,20],
                [0.99,1],
                [0.95,1],
                [0,15],
                [0,10],
                [0,5],
                [0,2],
                [0,2],
                [0,4],
                [0,10],
                [-10,10],
                [-20,5],
                [-5,25]]

    if col <= 4:
        yRange = [y_start,y_end]
    else:
        yRange = yRangeArray[col-2]
    
    n_bins = 50
    h = plt.hist2d(RealXiData[:,1], RealXiData[:,col], bins = n_bins, range=[[1.6, 1.8], yRange])
    plt.xlabel(xAxis[1])
    plt.ylabel(xAxis[col])
    plt.show()
 
print("Please wait, this may take a while...")
MCXiData = fileHandler(r'C:\root_v5.34.38\MC-Omega-data.file') #Enter you file path for the Monte Carlo Data file!
RealXiData = fileHandler(r'C:\root_v5.34.38\Real-Omega-data.file') #Enter you file path for the real Data file!
presetCuts() ##Comment out if you want to handle Original Data

###Main Code        
vChoice = None
while vChoice != "0":
 
    print(
    """
    Menu
 
    0 - Exit
    1 - Start Cuts
    2 - Graph
    3 - 2d Histogram
    4 - Fit
    5 - Integrate
    6 - Save
    7 - Significance Graph
    8 - Set Cuts
 
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
        histogram2d()

    # choice  4
    elif vChoice == "4":
        (fit) = gPlusPolyFit(RealXiData)

    # choice  5
    elif vChoice == "5":
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
 
    # choice  6
    elif vChoice == "6":
        save()
 
   # choice  7
    elif vChoice == "7":
        significance_calculations()
 
    # choice  8
    elif vChoice == "8":
        presetCuts()
        
    # some unknown choice
    else:
        print("Sorry, but", vChoice, "isn't a valid choice.")