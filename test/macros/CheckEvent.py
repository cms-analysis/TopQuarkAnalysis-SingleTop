#!/usr/bin/env python                                                                                                                  

from ROOT import *

import sys

printSkim = True
printLepSel = False

#EventNumsFile = open('eventDumps/diff/RebecasNotMine_lepSel_emu.txt')
#EventNumsFile = open('eventDumps/diff/RebecasNotMine_lepVeto_emu.txt')
#EventNumsFile = open('eventDumps/diff/MineNotRebecas_lepVeto_mumu.txt')
#EventNumsFile = open('eventDumps/diff/DuncansNotMine_lepSel_mumu.txt')
#EventNumsFile = open('eventDumps/diff/MineNotDuncans_lepSel_mumu.txt')
#EventNumsWanted = EventNumsFile.readlines()

# for i in range(len(EventNumsWanted)):
#     EventNumsWanted[i] = int(EventNumsWanted[i].split()[2])

EventNumsWanted = [288,149520,6952,4987,102152]  # A way to bypass the files, and pick specific events

EventsLeft = EventNumsWanted[:]

fileName = TFile('../output/ntuple_SysTrees_TWChannel.root')

fileName.cd('TreesDileptontW')

tWtree = gROOT.FindObject('TWChannel_noSyst')


print tWtree.GetEntries()


evtCount = 0.
percent = 0.0
progSlots = 25.
nEvents = tWtree.GetEntries()*1.


foundEvents = 0

for event in tWtree:

    evtCount += 1.
    if evtCount/nEvents > percent:
        i = int(percent*progSlots)
        progress = '0%[' + '-' * i + ' ' * (int(progSlots)-i) + ']100%\r'
        sys.stdout.write(progress)
        sys.stdout.flush()
        percent += 1./progSlots

    if event.eventNum in EventNumsWanted:
        print "-------------------------------"
        print event.runNum, event.lumiNum, event.eventNum
        print "-------------------------------"
    else:
        continue

    
    runNum = event.runNum
    lumiNum = event.lumiNum
    eventNum = event.eventNum

    EventsLeft.remove(eventNum)


    #Get Muon objects
    muonPt = event.muonPt
    muonEta = event.muonEta
    muonPhi = event.muonPhi
    muonE = event.muonE
    muonCharge = event.muonCharge
    muonRelIso = event.muonRelIso
    muonDeltaCorrectedRelIso = event.muonDeltaCorrectedRelIso
    muonChargedHadronIso = event.muonChargedHadronIso
    muonNeutralHadronIso = event.muonNeutralHadronIso
    muonPhotonIso = event.muonPhotonIso
    muonPUChargedHadronIso = event.muonPUChargedHadronIso
    muonSumChargedHadronPtR04 = event.muonSumChargedHadronPtR04
    muonSumNeutralHadronEtR04 = event.muonSumNeutralHadronEtR04
    muonSumPhotonEtR04 = event.muonSumPhotonEtR04
    muonSumPUPtR04 = event.muonSumPUPtR04

    #Get Electron objects
    electronPt = event.electronPt
    electronECALPt = event.electronECALPt
    electronEta = event.electronEta
    electronPhi = event.electronPhi
    electronE = event.electronE
    electronCharge = event.electronCharge
    electronRelIso = event.electronRelIso
    electronRhoCorrectedRelIso = event.electronRhoCorrectedRelIso
    electronDeltaCorrectedRelIso = event.electronDeltaCorrectedRelIso
    electronPVDz = event.electronPVDz
    electronPVDxy = event.electronPVDxy
    electronMVATrigV0 = event.electronMVATrigV0
    electronMVANonTrigV0 = event.electronMVANonTrigV0
    electronTrackerExpectedInnerHits = event.electronTrackerExpectedInnerHits
    electronSuperClusterEta = event.electronSuperClusterEta
    electronDB = event.electronDB
    electronChargedHadronIso = event.electronChargedHadronIso
    electronNeutralHadronIso = event.electronNeutralHadronIso
    electronPhotonIso = event.electronPhotonIso
    electronPassConversionVeto = event.electronPassConversionVeto

    rho = event.ktJetsForIsoRho
    
    if printSkim:
        print "Skim level: "
        print "electrons:",len(electronPt)
        print "muons:",len(muonPt)
        
        for i in range(len(electronPt)):
            print "electron", i
            print "pt:",electronPt[i]
            print "ECAL pt:",electronECALPt[i]
            print "eta:",electronEta[i]
            print "RelIso:",electronRelIso[i]
            print "RhoCorr:",electronRhoCorrectedRelIso[i]
            print "DeltaCorr:",electronDeltaCorrectedRelIso[i]
            print "DB", electronDB[i]
            print "PVDxy", electronPVDxy[i]
            print "MVATrigV0:", electronMVATrigV0[i]
            print "MVANonTrigV0:", electronMVANonTrigV0[i]
            print "InnerHits:", electronTrackerExpectedInnerHits[i]
            print "CHIso:", electronChargedHadronIso[i]
            print "NHIso:", electronNeutralHadronIso[i]
            print "PhIso:", electronPhotonIso[i]
            print "Rho:", rho
            print "PassConvVeto:", electronPassConversionVeto[i]
            print
            
        for i in range(len(muonPt)):
            print "muon", i
            print "pt:",muonPt[i]
            print "eta:",muonEta[i]
            print "RelIso:",muonRelIso[i]
            print "DeltaCorr:",muonDeltaCorrectedRelIso[i]
            print "CHIso:", muonChargedHadronIso[i]
            print "NHIso:", muonNeutralHadronIso[i]
            print "PhIso:", muonPhotonIso[i]    
            print "PUCHIso:", muonPUChargedHadronIso[i]
            print "CalcRelIso:", (muonChargedHadronIso[i] + muonNeutralHadronIso[i] + muonPhotonIso[i])/muonPt[i]
            print "CalcdBetaRelIso:", (muonChargedHadronIso[i] + max(muonNeutralHadronIso[i] + muonPhotonIso[i] - 0.5*muonPUChargedHadronIso[0],0.0))/muonPt[i]        
            print "muonSumChargedHadronPtR04:", muonSumChargedHadronPtR04[i]
            print "muonSumNeutraHadronEtR04:", muonSumNeutralHadronEtR04[i]
            print "muonSumPhotonEtR04:", muonSumPhotonEtR04[i]
            print "muonSumPUPtR04:", muonSumPUPtR04[i]
            print "ReCalcBetRelIso:", (muonSumChargedHadronPtR04[i] + max(muonSumNeutralHadronEtR04[i] + muonSumPhotonEtR04[i] - 0.5*muonSumPUPtR04[i],0.0))/muonPt[i]
            
            print "FloatReCalcBetRelIso:", ( float(muonSumChargedHadronPtR04[i]) + max(float(muonSumNeutralHadronEtR04[i]) + float(muonSumPhotonEtR04[i]) - 0.5*float(muonSumPUPtR04[i]),0.0))/float(muonPt[i])
            print

            

    goodMuonidx = list()
    goodEleidx = list()
    looseMuonidx = list()
    looseEleidx = list()

    # print 'Total Leptons ', (len(muonPt)+len(electronPt))
    # print 'Muons ', len(muonPt)
    # print 'Electrons ', len(electronPt)

    for i in range(len(muonPt)):
        isTightMuon = False
        if muonPt[i] > 20:
            if abs(muonEta[i]) < 2.4:
                if muonDeltaCorrectedRelIso[i] < 0.2:
                    goodMuonidx.append(i)
                    isTightMuon = True
        if not isTightMuon:
            if muonPt[i] > 10:
                if abs(muonEta[i]) < 2.5:
                    if muonDeltaCorrectedRelIso[i] < 0.2:
                        looseMuonidx.append(i)

    for i in range(len(electronPt)):
        isTightElectron = False
        if electronPassConversionVeto[i]:
            if electronPt[i] > 20:
                if abs(electronEta[i]) < 2.5:
                    #if abs(electronPVDxy[i]) < 0.04:
                    if abs(electronDB[i]) < 0.04:
                        #if electronMVATrigV0[i] >= 0. and electronMVATrigV0[i] <= 1.0:
                        if electronMVANonTrigV0[i] >= 0. and electronMVANonTrigV0[i] <= 1.0:
                            #if electronRhoCorrectedRelIso[i] < 0.15:
                            if electronDeltaCorrectedRelIso[i] < 0.15:
                                if electronTrackerExpectedInnerHits[i] <= 1:
                                    goodEleidx.append(i)
                                    isTightElectron = True

        if not isTightElectron:
            if electronPassConversionVeto[i]:
                if electronPt[i] > 15:
                    if abs(electronEta[i]) < 2.5:
                        #                    if electronSuperClusterEta < 1.442 or electronSuperClusterEta > 1.5660:
                        #if electronMVATrigV0[i] >= 0. and electronMVATrigV0[i] <= 1.0:
                        if electronMVANonTrigV0[i] >= 0. and electronMVANonTrigV0[i] <= 1.0:
                            #if electronRhoCorrectedRelIso[i] < 0.20:
                            if electronDeltaCorrectedRelIso[i] < 0.15:
                                looseEleidx.append(i)

#     for i in range(len(muonPt)):
#         isTightMuon = False
#         if muonPt[i] > 20:
#             if abs(muonEta[i]) < 2.4:
#                 if muonDeltaCorrectedRelIso[i] < 0.2:
#                     goodMuonidx.append(i)
#                     isTightMuon = True
#         if not isTightMuon:
#             if muonPt[i] > 10:
#                 if abs(muonEta[i]) < 2.5:
#                     if muonDeltaCorrectedRelIso[i] < 0.2:
#                         looseMuonidx.append(i)

#     for i in range(len(electronPt)):
#         isTightElectron = False
#         if electronPt[i] > 20:
#             if abs(electronEta[i]) < 2.5:
#                 if abs(electronPVDxy[i]) < 0.04:
#                     if electronMVATrigV0[i] >= 0. and electronMVATrigV0[i] <= 1.0:
#                         if electronRhoCorrectedRelIso[i] < 0.15:
#                             if electronTrackerExpectedInnerHits[i] <= 1:
#                                 goodEleidx.append(i)
#                                 isTightElectron = True
#         if not isTightElectron:
#             if electronPt[i] > 10:
#                 if abs(electronEta[i]) < 2.5:
# #                     if electronSuperClusterEta < 1.442 or electronSuperClusterEta > 1.5660:
# #                         if electronMVATrigV0[i] >= 0. and electronMVATrigV0[i] <= 1.0:
#                             if electronRhoCorrectedRelIso[i] < 0.20:
#                                 looseEleidx.append(i)
                                
    nLooseLeptons = len(looseEleidx) + len(looseMuonidx)


    if printLepSel:
        print 
        print "Lepton Selection:"
        print "electrons:",len(goodEleidx)
        print "muons:",len(goodMuonidx)

        for i in goodEleidx:        
            print "electron", i
#             print "pt:",electronPt[i]
#             print "ECAL pt:",electronECALPt[i]
#             print "eta:",electronEta[i]
#             print "RelIso:",electronRelIso[i]
#             print "RhoCorr:",electronRhoCorrectedRelIso[i]
#             print "DeltaCorr:",electronDeltaCorrectedRelIso[i]
#             print "DB", electronDB[i]
#             print "PVDxy", electronPVDxy[i]
#             print "MVATrigV0:", electronMVATrigV0[i]
#             print "MVANonTrigV0:", electronMVANonTrigV0[i]
#             print "InnerHits:", electronTrackerExpectedInnerHits[i]
#             print "CHIso:", electronChargedHadronIso[i]
#             print "NHIso:", electronNeutralHadronIso[i]
#             print "PhIso:", electronPhotonIso[i]
#             print "Rho:", rho
#             print "PassConvVeto:", electronPassConversionVeto[i]

        for i in goodMuonidx:        
            print "muon", i
#             print "pt:",muonPt[i]
#             print "eta:",muonEta[i]
#             print "RelIso:",muonRelIso[i]
#             print "DeltaCorr:",muonDeltaCorrectedRelIso[i]
#             print "CHIso:", muonChargedHadronIso[i]
#             print "NHIso:", muonNeutralHadronIso[i]
#             print "PhIso:", muonPhotonIso[i]
#             print "PUCHIso:", muonPUChargedHadronIso[i]
#             print "CalcRelIso:", (muonChargedHadronIso[i] + muonNeutralHadronIso[i] + muonPhotonIso[i])/muonPt[i]
#             print "CalcdBetaRelIso:", (muonChargedHadronIso[i] + max(muonNeutralHadronIso[i] + muonPhotonIso[i] - 0.5*muonPUChargedHadronIso[0],0.0))/muonPt[i]        

        print
        print "Loose Leptons",nLooseLeptons
        for i in looseEleidx:
            print "loose electron:", i
        for i in looseMuonidx:
            print "loose muon:", i
        print

    ModeIdx = -1

    lepton0 = TLorentzVector()
    lepton1 = TLorentzVector()

#     if (len(goodMuonidx)+len(goodEleidx)) != 2:
#         print "muons",len(goodMuonidx),"electrons", len(goodEleidx)

    if len(goodMuonidx) == 1 and len(goodEleidx) == 1:
        ModeIdx = 0
        i = goodMuonidx[0]
        j = goodEleidx[0]
        lepton0.SetPtEtaPhiE(muonPt[i],muonEta[i],muonPhi[i],muonE[i])
        lepton1.SetPtEtaPhiE(electronPt[j],electronEta[j],electronPhi[j],electronE[j])
        totalCharge = muonCharge[i]+electronCharge[j]
    elif len(goodMuonidx) == 2 and len(goodEleidx) == 0:
        ModeIdx = 1
        i = goodMuonidx[0]
        j = goodMuonidx[1]
        lepton0.SetPtEtaPhiE(muonPt[i],muonEta[i],muonPhi[i],muonE[i])
        lepton1.SetPtEtaPhiE(muonPt[j],muonEta[j],muonPhi[j],muonE[j])
        totalCharge = muonCharge[i]+muonCharge[j]
    elif len(goodMuonidx) == 0 and len(goodEleidx) == 2:
        ModeIdx = 2
        i = goodEleidx[0]
        j = goodEleidx[1]
        lepton0.SetPtEtaPhiE(electronPt[i],electronEta[i],electronPhi[i],electronE[i])
        lepton1.SetPtEtaPhiE(electronPt[j],electronEta[j],electronPhi[j],electronE[j])
        totalCharge = electronCharge[i]+electronCharge[j]
    else: 
        continue  


    if totalCharge != 0:
        continue
    
    #LepSelection

    
    if nLooseLeptons != 0:
        continue

    #LepVeto

    mll = (lepton0 + lepton1).M()

    if mll < 20:
        continue

    if ModeIdx > 0:
        if mll < 101 and mll > 81:
            continue

    
    #mllCut

    MetPt = event.MetPt
    MetPhi = event.MetPhi

    if MetPt < 30:
        continue

    #MetCut


    MET = TLorentzVector()
    MET.SetPtEtaPhiE(MetPt, 0, MetPhi, MetPt)

    jetPt = event.jetPt
    jetPhi = event.jetPhi
    jetEta = event.jetEta
    jetE = event.jetE
    jetCSV = event.jetCSV


    goodJetIdx = list()

    for i in range(len(jetPt)):
        if jetPt[i] > 30:
            if abs(jetEta[i]) < 2.4:
                goodJetIdx.append(i)

    if len(goodJetIdx) != 1:
        continue

    #OneJet


    jetIdx = goodJetIdx[0]

    if jetCSV[jetIdx] < 0.679:
        continue

    #JetBtag


    jet = TLorentzVector()
    jet.SetPtEtaPhiE(jetPt[jetIdx],jetEta[jetIdx], jetPhi[jetIdx], jetE[jetIdx])

    Ptsys = (lepton0 + lepton1 + MET + jet).Pt()

    Ht = lepton0.Pt() + lepton1.Pt() + MET.Pt() + jet.Pt()

    if ModeIdx == 0 and Ht< 150:
        continue

    #HtCut
        

print EventsLeft
