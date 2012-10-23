#!/usr/bin/env python                                                                                                                  

from ROOT import *
from numpy import matrix
from numpy.linalg import  eigvals

def UnweightedEta_Avg(particleList):
    AvgEta = 0.
    for particle in particleList:
        AvgEta += particle.Eta()
    AvgEta /= float(len(particleList))

    unWeightedEta = 0.
    for particle in particleList:
        unWeightedEta += pow(particle.Eta()-AvgEta,2)

    return unWeightedEta

def UnweightedEta_VecAvg(particeList, system):
    unWeightedEta = 0.
    for particle in particleList:
        unWeightedEta += pow(particle.Eta()-system.Eta(),2)

    return unWeightedEta

def Centrality(particleList):
    Ht = 0.
    H = 0.
    for particle in particleList:
        H += particle.E()
        Ht += particle.Pt()

    return Ht/H

def GetEvals(particleList):
    xx, xy, xz, yx, yy, yz, zx, zy, zz = 0., 0., 0., 0., 0., 0., 0., 0., 0.
    sumP = 0.
    for particle in particleList:
        xx += particle.Px()*particle.Px()
        xy += particle.Px()*particle.Py()
        xz += particle.Px()*particle.Pz()
        yy += particle.Py()*particle.Py()
        yz += particle.Py()*particle.Pz()
        zz += particle.Pz()*particle.Pz()
        sumP += xx + yy + zz

    A = matrix([[xx,xy,xz],
                [xy,yy,yz],
                [xz,yz,zz]])

    A /= sumP
    eVals = eigvals(A)
    eVals.sort()
    a = eVals/eVals.sum()

    return a[2], a[1], a[0]

def Sphericity(particleList):
    
    l1, l2, l3 = GetEvals(particleList)

    return 1.5*(l2 + l3)

def Aplanarity(particleList):

    l1, l2, l3 = GetEvals(particleList)

    return 1.5*(l3)
    

