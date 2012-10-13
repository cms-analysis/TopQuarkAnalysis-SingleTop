#!/usr/bin/env python                                                                                                                  

from ROOT import *

#filenames = ['edmntuple_tWTest_OUTPUT.root']

fileName = TFile('ntuple_SysTrees_TWChannel.root')

fileName.cd('TreesDileptontW')

tWtree = gROOT.FindObject('TWChannel_noSyst')

Channel = ['emu', 'mumu', 'ee']

LepSelection = [0,0,0]
LepVeto = [0,0,0]
mllCut = [0,0,0]
MetCut = [0,0,0]
OneJet = [0,0,0]
JetBtag = [0,0,0]
HtCut = [0,0,0]

print tWtree.GetEntries()

for event in tWtree:
    #Get Muon objects
    muonPt = event.muonPt
    muonEta = event.muonEta
    muonPhi = event.muonPhi
    muonE = event.muonE
    muonCharge = event.muonCharge
    muonRelIso = event.muonRelIso

    #Get Electron objects
    electronPt = event.electronPt
    electronEta = event.electronEta
    electronPhi = event.electronPhi
    electronE = event.electronE
    electronCharge = event.electronCharge
    electronRelIso = event.electronRelIso
    electronPVDz = event.electronPVDz
    electronPVDxy = event.electronPVDxy
    electronMVATrigV0 = event.electronMVATrigV0
    electronTrackerExpectedInnerHits = event.electronTrackerExpectedInnerHits
    electronSuperClusterEta = event.electronSuperClusterEta

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
                if muonRelIso[i] < 0.2:
                    goodMuonidx.append(i)
                    isTightMuon = True
        if not isTightMuon:
            if muonPt[i] > 10:
                if abs(muonEta[i]) < 2.5:
                    if muonRelIso[i] < 0.2:
                        looseMuonidx.append(i)

    for i in range(len(electronPt)):
        isTightElectron = False
        if electronPt[i] > 10:
            if abs(electronEta[i]) < 2.5:
                if electronPVDxy[i] < 0.04:
                    if electronMVATrigV0[i] >= 0. and electronMVATrigV0[i] <= 1.0:
                        if electronRelIso[i] < 0.15:
                            if electronTrackerExpectedInnerHits[i] <= 1:
                                goodEleidx.append(i)
                                isTightElectron = True
        if not isTightElectron:
            if electronPt[i] > 10:
                if abs(electronEta[i]) < 2.5:
                    if electronSuperClusterEta < 1.442 or electronSuperClusterEta > 1.5660:
                        if electronRelIso[i] < 0.15:
                            looseEleidx.append(i)

    nLooseLeptons = len(looseEleidx) + len(looseMuonidx)

    ModeIdx = -1

    lepton0 = TLorentzVector()
    lepton1 = TLorentzVector()

    print len(goodMuonidx), len(goodEleidx), ModeIdx

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
    
    LepSelection[ModeIdx] += 1

    
    if nLooseLeptons != 0:
        continue

    LepVeto[ModeIdx] += 1


    mll = (lepton0 + lepton1).M()

    if mll < 20:
        continue

    if ModeIdx > 0:
        if mll < 101 and mll > 81:
            continue

    
    mllCut[ModeIdx] += 1

    MetPt = event.MetPt
    MetPhi = event.MetPhi

    if MetPt < 30:
        continue

    MetCut[ModeIdx] += 1

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

    OneJet[ModeIdx] += 1

    jetIdx = goodJetIdx[0]

    if jetCSV[jetIdx] < 0.679:
        continue

    JetBtag[ModeIdx] += 1


    jet = TLorentzVector()
    jet.SetPtEtaPhiE(jetPt[jetIdx],jetEta[jetIdx], jetPhi[jetIdx], jetE[jetIdx])

    Ht = (lepton0 + lepton1 + MET + jet).Pt()

    if ModeIdx == 0 and Ht< 150:
        continue

    HtCut[ModeIdx] += 1
    
    


for i in range(3):
    print '----------------------------'
    print Channel[i] + ' Channel'
    print 'Lepton Selection '+ str(LepSelection[i])
    print 'Lepton Veto      '+ str(LepVeto[i])
    print 'Mll Cut          '+ str(mllCut[i])
    print 'Met Cut          '+ str(MetCut[i])
    print 'One Jet          '+ str(OneJet[i])
    print 'Btagged          '+ str(JetBtag[i])
    print 'Ht Cut           '+ str(HtCut[i])

print '----------------------------'
