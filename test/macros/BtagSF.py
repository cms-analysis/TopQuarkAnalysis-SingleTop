#!/usr/bin/env python


SFb_error = [[20,   2*0.0484285],
             [30,   0.0484285],
             [40,   0.0126178],
             [50,   0.0120027],
             [60,   0.0141137],
             [70,   0.0145441],
             [80,   0.0131145],
             [100,  0.0168479],
             [120,  0.0160836],
             [160,  0.0126209],
             [210,  0.0136017],
             [260,  0.019182],
             [320,  0.0198805],
             [400,  0.0386531],
             [500,  0.0392831],
             [600,  0.0481008],
             [800,  0.0474291],
             [99999,2*0.0474291]]


def BtagSF(jetPt, syst=0):

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


    if jetPt < 20:
        x = 20
    elif jetPt > 800:
        x = 800
    else:
        x = jetPt
    
    SFb = 0.981149*((1.+(-0.000713295*x))/(1.+(-0.000703264*x))) + error

    return SFb

    
