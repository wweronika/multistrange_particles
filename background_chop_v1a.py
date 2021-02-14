# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 19:48:55 2021

@author: Anwesha Sahu
"""
''' 
README:

THIS PROGRAM PLOTS THE BACKGROUND SIGNAL

-A hefty chunk of this code has been motivated by Dominic's original code to plot cuts
-Feel free to fix any bugs that pop up. Please add your name and make a comment of the changes you make
-Before making any changes, be sure to make a copy of the original code
-I'm still working on my coding skills, excuse any amateur-ish code and feel free to share any 
suggestions/ideas you may have 

'''

#version name: 
#date of last update:

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

print("Please wait, this may take a while...")


breaker = input('Do you want to do a single run through (y/n)?')


def Action():
    MCXiData = fileHandler(r'C:\Users\neham\Downloads\Year 2\Lab project\Code\Canvas data files\MC-xi-data.file.txt') #Enter you file path for the Monte Carlo Data file!
    RealXiData = fileHandler(r'C:\Users\neham\Downloads\Year 2\Lab project\Code\Canvas data files\real-xi-data.file.txt') #Enter you file path for the real Data file!
    
    num = int(input('Which column? '))
    
    chopped_RealXiData = RealXiData[:,num][1156:17884]
    reduced_RealXi = []
    n = 0
    while n < 4182:
        avg = np.average(chopped_RealXiData[n:n+4])
        reduced_RealXi.append(avg)        
        n += 1        
    #print (len(reduced_RealXi))
    
    BackgroundXiData = reduced_RealXi - MCXiData[:,num]
    
    def PlotBackground(data, plt, alpha = 0.5, label = ""):
        (counts, bins) = np.histogram(data, bins=100)
        factor = 1/np.max(counts)
        plt.hist(bins[:-1], bins, weights = factor*counts, alpha=alpha, label=label)
        
    PlotBackground(BackgroundXiData, plt, label = 'Background Noise')
    plt.xlabel(xAxis[num]) 
    plt.ylabel('Scalar Factored Events (Arbitary Units)')
    plt.title('Background for ' + Titles[num])
    plt.show()
    
if breaker == 'n':
    m =  1000
    while m<1000:
        Action()
        m+=1
    
    
if breaker == 'y':
    Action()
    
    
        




