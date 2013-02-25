#!/usr/bin/env python


SFb_error = [[20,   2*0.0554504],
             [30,   0.0554504],
             [40,   0.0209663],
             [50,   0.0207019],
             [60,   0.0230073],
             [70,   0.0208719],
             [80,   0.0200453],
             [100,  0.0264232],
             [120,  0.0240102],
             [160,  0.0229375],
             [210,  0.0184615],
             [260,  0.0216242],
             [320,  0.0248119],
             [400,  0.0465748],
             [500,  0.0474666],
             [600,  0.0718173],
             [800,  0.0717567],
             [99999,2*0.0717567],]

def BtagSF(jetPt, syst=''):

    error = 0.0
    if syst == 'Up':
        for val in SFb_error:
            if jetPt < val[0]:
                error = val[1]
                break
    if syst == 'Down':
        for val in SFb_error:
            if jetPt < val[0]:
                error = -1*val[1]
                break

    if syst == 'Data':
        return 1.

    if jetPt < 20:
        x = 20
    elif jetPt > 800:
        x = 800
    else:
        x = jetPt
    
    SFb = 0.726981*((1.+(0.253238*x))/(1.+(0.188389*x))) + error

    return SFb

