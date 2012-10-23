#!/usr/bin/env python                                                                                                                  

from ROOT import *
from separation import *

f = TFile("histos.root")

Vars = ['ptjet',
        'ptlep0',
        'ptlep1',
        'jetCSV',
        'ht',
        'htNoMet',
        'msys',
        'mjll',
        'mjl0',
        'mjl1',
        'ptsys',
        'ptjll',
        'ptjl0',
        'ptjl1',
        'ptleps',
        'ptsys_ht',
        'ptjet_ht',
        'ptlep0_ht',
        'ptlep1_ht',
        'ptleps_ht',
        'htleps_ht',
        'NlooseJet15Central',
        'NlooseJet15Forward',
        'NlooseJet20Central',
        'NlooseJet20Forward',
        'NlooseJet25Central',
        'NlooseJet25Forward',
        'NtightJetForward',
        'unweightedEta_Avg',
        'unweightedEta_Vecjll',
        'unweightedEta_Vecsys',
        'unweightedPhi_Avg',
        'unweightedPhi_Vecjll',
        'unweightedPhi_Vecsys',
        'avgEta',
        'sysEta',
        'jllEta',
        'dRleps',
        'dRjlmin',
        'dRjlmax',
        'dPhileps',
        'dPhijlmin',
        'dPhijlmax',
        'met',
#        'flavourJet',
        'etajet',
        'etalep0',
        'etalep1',
        'phijet',
        'philep0',
        'philep1',
        'phimet',
        'sumeta2',
        'loosejetPt',
        'loosejetCSV',
#        'loosejetFlavour',
        'centralityJLL',
        'centralityJLLM',
        'centralityJLLWithLoose',
        'centralityJLLMWithLoose',
        'sphericityJLL',
        'sphericityJLLM',
        'sphericityJLLWithLoose',
        'sphericityJLLMWithLoose',
        'aplanarityJLL',
        'aplanarityJLLM',
        'aplanarityJLLWithLoose',
        'aplanarityJLLMWithLoose',
        ]

sepValues = list()
print
print

for var in Vars:
    sepValues.append([var,separation(f.Get("TWDilepton_"+var),f.Get("TTBarDilepton_"+var))])

sepValuesSorted = sorted(sepValues, key = lambda temp: temp[1], reverse = True)

for sep in sepValuesSorted:
    print sep[0], '&', "{0:0.5f}".format(sep[1])
    

print
print "Btagged Loose"
print

sepValues = list()

for var in Vars:
    sepValues.append([var,separation(f.Get("TWDilepton_BtaggedL_"+var),f.Get("TTBarDilepton_BtaggedL_"+var))])

sepValuesSorted = sorted(sepValues, key = lambda temp: temp[1], reverse = True)


for sep in sepValuesSorted:
    print sep[0], '&', "{0:0.5f}".format(sep[1])

print
print "Btagged Medium"
print

sepValues = list()

for var in Vars:
    sepValues.append([var,separation(f.Get("TWDilepton_BtaggedM_"+var),f.Get("TTBarDilepton_BtaggedM_"+var))])

sepValuesSorted = sorted(sepValues, key = lambda temp: temp[1], reverse = True)


for sep in sepValuesSorted:
    print sep[0], '&', "{0:0.5f}".format(sep[1])

print
print "Btagged Tight"
print

sepValues = list()

for var in Vars:
    sepValues.append([var,separation(f.Get("TWDilepton_BtaggedT_"+var),f.Get("TTBarDilepton_BtaggedT_"+var))])

sepValuesSorted = sorted(sepValues, key = lambda temp: temp[1], reverse = True)


for sep in sepValuesSorted:
    print sep[0], '&', "{0:0.5f}".format(sep[1])


c = TCanvas()

for var in Vars:
    s = f.Get("TWDilepton_"+var)
    b = f.Get("TTBarDilepton_"+var)
    b.SetLineColor(kRed)
    s.DrawNormalized()
    b.DrawNormalized("same")
    c.SaveAs("~/tempPlots/"+var+".png")

    s = f.Get("TWDilepton_BtaggedL_"+var)
    b = f.Get("TTBarDilepton_BtaggedL_"+var)
    b.SetLineColor(kRed)
    s.DrawNormalized()
    b.DrawNormalized("same")
    c.SaveAs("~/tempPlots/BtaggedLoose/"+var+".png")

    s = f.Get("TWDilepton_BtaggedM_"+var)
    b = f.Get("TTBarDilepton_BtaggedM_"+var)
    b.SetLineColor(kRed)
    s.DrawNormalized()
    b.DrawNormalized("same")
    c.SaveAs("~/tempPlots/BtaggedMedium/"+var+".png")

    s = f.Get("TWDilepton_BtaggedT_"+var)
    b = f.Get("TTBarDilepton_BtaggedT_"+var)
    b.SetLineColor(kRed)
    s.DrawNormalized()
    b.DrawNormalized("same")
    c.SaveAs("~/tempPlots/BtaggedTight/"+var+".png")

