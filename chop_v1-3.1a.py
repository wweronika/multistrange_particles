##Dominic Herd
##Date: 08/02/2021
##Version = 1.3
###Known Bugs: Bars are not of constant width after cuts are applied

##Anwesha Sahu
##Date: 10/02/2021
##Version = 1-3.1a

'''
ANWESHA:
    
    
BUGS
-   When doing a single run through, applying a cut has no impact and the program ends after 
    asking for the upper and lower limits
    (THIS HAS BEEN FIXED)

'''

import matplotlib.pyplot as plt
import numpy as np


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

def FactorToOne(data, plt, alpha = 0.5, label = ""): #Force Histogram y axis max to be 1
    (counts, bins) = np.histogram(data, bins=100)
    factor = 1/np.max(counts)
    plt.hist(bins[:-1], bins, weights = factor*counts, alpha=alpha, label=label)

def tryFloat(data):
    try:
        return float(data)
    except ValueError:
        print("Error (Please ignore)")
        return "null"

print("Please wait, this may take a while...")
MCXiData = fileHandler(r'C:\Users\neham\Downloads\Year 2\Lab project\Code\Canvas data files\MC-xi-data.file.txt') #Enter you file path for the Monte Carlo Data file!
RealXiData = fileHandler(r'C:\Users\neham\Downloads\Year 2\Lab project\Code\Canvas data files\real-xi-data.file.txt') #Enter you file path for the real Data file!

ifBreak = False
breaker = input('Do you want to do a single run through (y/n)?')
if breaker == 'y':
    ifBreak = True
    
while True:    
    num = int(input("What column?"))
    FactorToOne(MCXiData[:,num],plt, alpha = 0.8, label = "MC Xi")
    FactorToOne(RealXiData[:,num],plt, label = "Real Xi")

    plt.legend(loc='upper right')
    
    plt.title(Titles[num])
    plt.xlabel(xAxis[num]) 
    plt.ylabel('Scalar Factored Events (Arbitary Units)')
    plt.show()
    
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
                
    if ifBreak == True:
        num = num
        FactorToOne(MCXiData[:,num],plt, alpha = 0.8, label = "MC Xi")
        FactorToOne(RealXiData[:,num],plt, label = "Real Xi")
    
        plt.legend(loc='upper right')
        
        plt.title(Titles[num])
        plt.xlabel(xAxis[num]) 
        plt.ylabel('Scalar Factored Events (Arbitary Units)')
        plt.show()
        break 
        
