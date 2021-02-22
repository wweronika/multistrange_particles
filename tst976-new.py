##Dominic Herd's code, with a few changes added by TS
##Date: 08/02/2021
##Version = 1.0 - Uncommented
###Known Bugs: Bars are not of constant width after cuts are applied

import matplotlib.pyplot as plt
import numpy as np

Names = ["icand","Ximass","Vmass","V0radius","Casradius","Cascos","V0cos","DCAneg","DCApos", "DCAbach", "DCAV0", "DCAcas","DCAV0PV", "dOverM",
      "NsigPion", "NgisProton", "NsigBach"]

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

def normalise(data):
    maxim = np.max(data)
    normFactor = 1/maxim
    return data * normFactor

print("Please wait, this may take a while...")
MCXiData = fileHandler(r'C:\Users\tastu\MC-xi-data.file') #Enter you file path for the Monte Carlo Data file!
RealXiData = fileHandler(r'C:\Users\tastu\real-xi-data.file') #Enter you file path for the real Data file!

ifBreak = False
breaker = input('Do you want to do a single run through (y/n)?')
if breaker == 'y':
    ifBreak = True
elif breaker == 'n':
    ifBreak = False

while True:    
    num = int(input("What column?"))

    (counts, bins) = np.histogram(MCXiData[:,num], bins=100)
    factor = 1/np.max(counts)
    plt.hist(bins[:-1], bins, weights=factor*counts, alpha=0.8, label='MC Xi')

    (counts, bins) = np.histogram(RealXiData[:,num], bins=100)
    factor = 1/np.max(counts)
    plt.hist(bins[:-1], bins, weights=factor*counts, alpha=0.5, label='Real Xi')

    plt.legend(loc='upper right')

    plt.title('Effective mass plot for Xi')
    plt.xlabel(Names[num])
    plt.ylabel('Normalised Events (Arbitary Units)')
    plt.show()

    lowerLim = input("Lower Limit ('Null' = No Limit): ")
    try:
        lowerLim = float(lowerLim)
    except ValueError:
        lowerLim = "null"
        #print("Error (Please ignore)")

    UpperLim = input("Upper Limit ('Null' = No Limit): ")
    try:
        UpperLim = float(UpperLim)
    except ValueError:
        UpperLim = "null"
        #print("Error (Please ignore)")

    if type(lowerLim) != str:
        x = 0
        while x < len(RealXiData):
            if RealXiData[x,num] > UpperLim:
                x += 1
            elif RealXiData[x,num] > lowerLim:
                RealXiData = np.delete(RealXiData, x, 0)
            
            else:
                x += 1

    if type(UpperLim) != str:
        x = 0
        while x < len(RealXiData):
            if RealXiData[x,num] < lowerLim:
                x += 1
            elif RealXiData[x,num] < UpperLim:
                RealXiData = np.delete(RealXiData, x, 0)
            else:
                x += 1
    if ifBreak == True:
        np.savetxt('Removed.file', RealXiData)
        break
        
