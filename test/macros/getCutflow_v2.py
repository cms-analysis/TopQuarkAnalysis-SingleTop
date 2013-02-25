#!/usr/bin/env python                                                                                                                  

#Uses random numbers for btagging scale factors

from ROOT import *

import sys

from EventShapeVariables import *        
from BtagSF import *
from fileLoadDict_storeUser import fileLists

import random
import os

if len(sys.argv) == 2:
    ChanName = sys.argv[1]
    if not ChanName in fileLists:
        print 'Unknown Channel, please check list in fileLoadDict.py'
        sys.exit(0)
    systName = "noSyst"
elif len(sys.argv) == 3:
    ChanName = sys.argv[1]
    if not ChanName in fileLists:
        print 'Unknown Channel, please check list in fileLoadDict.py'
        sys.exit(0)
    systName = sys.argv[2]
    if not systName in allowedSystNames:
        print 'Unknown Systematic:', systName
        sys.exit(0)
else:
    print 'Please specificy a channel as the arguement'
    sys.exit(0)

RunA = True
RunB = True
RunC = True

numJets = 1
numBtags = 1

METmllCutsInEMu = True

fileVersion = 'v2'

useLeptonSF = True

#Input actual luminosities for runA, B, Crereco, and Cprompt for each channel from data

isData = False

SFsyst = ''

if 'Data' in ChanName:
    SFsyst = 'Data'
    isData = True


TrueLumis = [[808.472+82.136,4398.,495.003,6397.],
             [808.472+82.136,4411.,495.003,6397.],
             [808.472+82.136,4446.,485.574,6397.]]


#The values used from SingleTopPSetsSummer_tW for the luminosities of run A, B, Crereco, and Cprompt
UsedLumis = [15000.,15000.,15000.,15000.]

#Lepton Scale Factors
lepSF = [0.936,0.962,0.950]
lepSFUnc = [0.011,0.012,0.014]
        

#Branch variables for TMVA tree



temp = ''

if 'SF' in systName:
    temp = systName
    systName = 'noSyst'

if 'PDF' in systName:
    temp = systName
    systName = 'noSyst'

fchain = TChain('TreesDileptontW/'+fileLists[ChanName][0]+'_'+systName)

fchain.SetCacheSize(20*1024*1024)

if 'SF' in temp:
    systName = temp    

if 'PDF' in temp:
    systName = temp    

for file in fileLists[ChanName][1]:
    fchain.Add(file)

Channel = ['emu', 'mumu', 'ee']

evtCount = 0.
percent = 0.0
progSlots = 25.
nEvents = fchain.GetEntries()*1.

print nEvents

#Bins 0-LepSel, 1-LepVeto, 2-mll, 3-MET, 4-jet, 5-bjet, 6-loosejetVeto, 7-ptsys, 8-ht

CutflowHists = [[TH1F("emuCutflow1j1t","",9,0,9), TH1F("mumuCutflow1j1t","",9,0,9), TH1F("eeCutflow1j1t","",9,0,9)],
                [TH1F("emuCutflow2j1t","",9,0,9), TH1F("mumuCutflow2j1t","",9,0,9), TH1F("eeCutflow2j1t","",9,0,9)],
                [TH1F("emuCutflow2j2t","",9,0,9), TH1F("mumuCutflow2j2t","",9,0,9), TH1F("eeCutflow2j2t","",9,0,9)]]

#CutflowHists = [TH1F("emuCutflow1j1t","",9,0,9), TH1F("mumuCutflow1j1t","",9,0,9), TH1F("eeCutflow1j1t","",9,0,9)]

CutflowHists[0][0].Sumw2()
CutflowHists[0][1].Sumw2()
CutflowHists[0][2].Sumw2()
CutflowHists[1][0].Sumw2()
CutflowHists[1][1].Sumw2()
CutflowHists[1][2].Sumw2()
CutflowHists[2][0].Sumw2()
CutflowHists[2][1].Sumw2()
CutflowHists[2][2].Sumw2()

for event in fchain:

    evtCount += 1.
    if evtCount/nEvents > percent:
        i = int(percent*progSlots)
        progress = '0%[' + '-' * i + ' ' * (int(progSlots)-i) + ']100%\r'
        sys.stdout.write(progress)
        sys.stdout.flush()
        percent += 1./progSlots

    evtWeightA = event.weightA
    evtWeightB = event.weightB
    evtWeightCrereco = event.weightCrereco
    evtWeightCprompt = event.weightCprompt
    evtPUWeightA = event.PUWeightA
    evtPUWeightB = event.PUWeightB
    evtPUWeightCrereco = event.PUWeightCrereco
    evtPUWeightCprompt = event.PUWeightCprompt


    if isData:
        weight = 1.

    #Get Muon objects
    muonPt = event.muonPt
    muonEta = event.muonEta
    muonPhi = event.muonPhi
    muonE = event.muonE
    muonCharge = event.muonCharge
    muonRelIso = event.muonRelIso
    muonDeltaCorrectedRelIso = event.muonDeltaCorrectedRelIso

    #Get Electron objects
    electronPt = event.electronPt
    electronEta = event.electronEta
    electronPhi = event.electronPhi
    electronE = event.electronE
    electronCharge = event.electronCharge
    electronRelIso = event.electronRelIso
    electronRhoCorrectedRelIso = event.electronRhoCorrectedRelIso
    electronDeltaCorrectedRelIso = event.electronDeltaCorrectedRelIso
    electronPVDz = event.electronPVDz
    electronPVDxy = event.electronPVDxy
    electronDB = event.electronDB
    electronMVATrigV0 = event.electronMVATrigV0
    electronMVANonTrigV0 = event.electronMVANonTrigV0
    electronTrackerExpectedInnerHits = event.electronTrackerExpectedInnerHits
    electronSuperClusterEta = event.electronSuperClusterEta
    electronECALPt = event.electronECALPt
    electronPassConversionVeto = event.electronPassConversionVeto

    goodMuonidx = list()
    goodEleidx = list()
    looseMuonidx = list()
    looseEleidx = list()

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
                    if abs(electronPVDxy[i]) < 0.04:
                        if electronMVATrigV0[i] >= 0. and electronMVATrigV0[i] <= 1.0:
                            if electronRhoCorrectedRelIso[i] < 0.15: #####ADJUSTMENT
                                if electronTrackerExpectedInnerHits[i] <= 1:
                                    goodEleidx.append(i)
                                    isTightElectron = True
        if not isTightElectron:
            if electronPt[i] > 15:
                if abs(electronEta[i]) < 2.5:
                    if electronMVATrigV0[i] >= 0. and electronMVATrigV0[i] <= 1.0: #####ADJUSTMENT
                        if electronRhoCorrectedRelIso[i] < 0.15: #####ADJUSTMENT
                            looseEleidx.append(i)
    nLooseLeptons = len(looseEleidx) + len(looseMuonidx)

    ModeIdx = -1

    lepton0 = TLorentzVector()
    lepton1 = TLorentzVector()

    if len(goodMuonidx) == 1 and len(goodEleidx) == 1:
        ModeIdx = 0
        i = goodMuonidx[0]
        j = goodEleidx[0]
        lepton0.SetPtEtaPhiE(muonPt[i],muonEta[i],muonPhi[i],muonE[i])
        lepton1.SetPtEtaPhiE(electronPt[j],electronEta[j],electronPhi[j],electronE[j])
        totalCharge = muonCharge[i]+electronCharge[j]
        chargeMult = muonCharge[i]*electronCharge[j]
    elif len(goodMuonidx) == 2 and len(goodEleidx) == 0:
        ModeIdx = 1
        i = goodMuonidx[0]
        j = goodMuonidx[1]
        lepton0.SetPtEtaPhiE(muonPt[i],muonEta[i],muonPhi[i],muonE[i])
        lepton1.SetPtEtaPhiE(muonPt[j],muonEta[j],muonPhi[j],muonE[j])
        totalCharge = muonCharge[i]+muonCharge[j]
        chargeMult = muonCharge[i]*muonCharge[j]
    elif len(goodMuonidx) == 0 and len(goodEleidx) == 2:
        ModeIdx = 2
        i = goodEleidx[0]
        j = goodEleidx[1]
        lepton0.SetPtEtaPhiE(electronPt[i],electronEta[i],electronPhi[i],electronE[i])
        lepton1.SetPtEtaPhiE(electronPt[j],electronEta[j],electronPhi[j],electronE[j])
        totalCharge = electronCharge[i]+electronCharge[j]
        chargeMult = electronCharge[i]*electronCharge[j]
    else: 
        continue  

    if chargeMult > 0:
        continue


    extraMultipliers = lepSF[ModeIdx]

    weightA      = extraMultipliers*evtWeightA*evtPUWeightA*TrueLumis[ModeIdx][0]/UsedLumis[0]

    weightB      = extraMultipliers*evtWeightB*evtPUWeightB*TrueLumis[ModeIdx][1]/UsedLumis[1]

    weightC      = extraMultipliers*evtWeightCrereco*evtPUWeightCrereco*TrueLumis[ModeIdx][2]/UsedLumis[2]

    weightC     += extraMultipliers*evtWeightCprompt*evtPUWeightCprompt*TrueLumis[ModeIdx][3]/UsedLumis[3]

    weight = weightA + weightB + weightC
    

    CutflowHists[0][ModeIdx].Fill(0.5,weight)
    CutflowHists[1][ModeIdx].Fill(0.5,weight)
    CutflowHists[2][ModeIdx].Fill(0.5,weight)

    if totalCharge != 0:
        print "Charge Issue???"
        continue

    if nLooseLeptons != 0:
        continue

    CutflowHists[0][ModeIdx].Fill(1.5,weight)
    CutflowHists[1][ModeIdx].Fill(1.5,weight)
    CutflowHists[2][ModeIdx].Fill(1.5,weight)


    mll = (lepton0 + lepton1).M()

    if mll < 20:
        continue



    inZpeak = False
    if not METmllCutsInEMu:
        if ModeIdx > 0:
            if mll < 101 and mll > 81:
                continue
    else:
        if mll < 101 and mll > 81:
            continue

    CutflowHists[0][ModeIdx].Fill(2.5,weight)
    CutflowHists[1][ModeIdx].Fill(2.5,weight)
    CutflowHists[2][ModeIdx].Fill(2.5,weight)


    MetPt = event.MetPt
    MetPhi = event.MetPhi

    if not METmllCutsInEMu:
        if ModeIdx>0 and MetPt<50:
            continue
    else:
        if MetPt<50:
            continue

    CutflowHists[0][ModeIdx].Fill(3.5,weight)
    CutflowHists[1][ModeIdx].Fill(3.5,weight)
    CutflowHists[2][ModeIdx].Fill(3.5,weight)


    MET = TLorentzVector()
    MET.SetPtEtaPhiE(MetPt, 0, MetPhi, MetPt)

    jetPt = event.jetPt
    jetPhi = event.jetPhi
    jetEta = event.jetEta
    jetE = event.jetE
    jetCSV = event.jetCSV
    jetNumDaughters = event.jetNumDaughters
    jetCHEmEn = event.jetCHEmEn
    jetCHHadEn = event.jetCHHadEn
    jetCHMult = event.jetCHMult
    jetNeuEmEn = event.jetNeuEmEn
    jetNeuHadEn = event.jetNeuHadEn


    goodJetIdx = list()
    btaggedTightJetIdx = list()
    looseJet20Idx = list()
    btaggedLooseJet20Idx = list()


    for i in range(len(jetPt)):
        isTightJet = False
        jetID = False        
        btagSF_ = BtagSF(jetPt[i],SFsyst)
        if btagSF_ > 1:
            print btagSF_, jetPt[i]
        if jetNumDaughters[i] > 1:
            if jetNeuHadEn[i] < 0.99:
                if jetNeuEmEn[i] < 0.99:
                    if abs(jetEta[i]) > 2.5:
                        jetID = True
                    else:
                        if jetCHEmEn[i] < 0.99:
                            if jetCHHadEn[i] > 0:
                                if jetCHMult[i] > 0:
                                    jetID = True
        if jetPt[i] > 30:
            if abs(jetEta[i]) < 2.5:
                if jetID:
                    tJet = TLorentzVector()
                    tJet.SetPtEtaPhiE(jetPt[i],jetEta[i],jetPhi[i],jetE[i])
                    if min(lepton0.DeltaR(tJet),lepton1.DeltaR(tJet)) > 0.3:
                        goodJetIdx.append(i)
                        isTightJet = True
                        if jetCSV[i] > 0.679:
                            if random.random() < btagSF_ or isData:
                                btaggedTightJetIdx.append(i)

        if not isTightJet:
            if jetID:
                if jetPt[i] > 20:
                    looseJet20Idx.append(i)
                    if jetCSV[i] > 0.679:
                        if random.random() < btagSF_ or isData:
                            btaggedLooseJet20Idx.append(i)

    if len(goodJetIdx) == 1:
        CutflowHists[0][ModeIdx].Fill(4.5,weight)
    elif len(goodJetIdx) == 2:
        CutflowHists[1][ModeIdx].Fill(4.5,weight)
        CutflowHists[2][ModeIdx].Fill(4.5,weight)
    else:
        continue

    region = -1
    if len(btaggedTightJetIdx) == 1:
        if len(goodJetIdx) == 1:
            CutflowHists[0][ModeIdx].Fill(5.5,weight)
            region = 0
        elif len(goodJetIdx) == 2:
            CutflowHists[1][ModeIdx].Fill(5.5,weight)
            region = 1
        else:
            continue
    elif len(btaggedTightJetIdx) == 2:
        if len(goodJetIdx) == 2:
            CutflowHists[2][ModeIdx].Fill(5.5,weight)
            region = 2
        else:
            continue
    else:
        continue


    jetIdx = goodJetIdx[0]

    jet = TLorentzVector()
    jet.SetPtEtaPhiE(jetPt[jetIdx],jetEta[jetIdx], jetPhi[jetIdx], jetE[jetIdx])

    system = lepton0 + lepton1 + MET + jet 
    Ht = lepton0.Pt() + lepton1.Pt() + MET.Pt() + jet.Pt()

    


if not os.path.exists('cutFlows/'+fileVersion):
    command = 'mkdir cutFlows/'+fileVersion
    os.system(command)

outFileName = 'cutFlows/'+fileVersion+'/'+fileLists[ChanName][2]

print
print outFileName
outputFile = TFile(outFileName,"RECREATE")

CutflowHists[0][0].Write()
CutflowHists[0][1].Write()
CutflowHists[0][2].Write()
CutflowHists[1][0].Write()
CutflowHists[1][1].Write()
CutflowHists[1][2].Write()
CutflowHists[2][0].Write()
CutflowHists[2][1].Write()
CutflowHists[2][2].Write()

