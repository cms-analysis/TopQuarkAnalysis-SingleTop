#!/usr/bin/env python

metbins = [    10,     20,      30,     40,      50,      60,    9999]
sf =     [[0.8799, 0.9257, 0.99445, 1.0721, 1.14595, 1.21935, 1.20315],
          [0.8856, 0.9398, 1.0142,  1.1017, 1.1839,  1.2458,  1.2872],
          [0.8742, 0.9116, 0.9747,  1.0425, 1.1080,  1.1929,  1.1191]]

        
def ZjetSF(met,mode):
    for i in range(len(metbins)):
        if met < metbins[i]:
            return sf[mode][i]

    return 1.

