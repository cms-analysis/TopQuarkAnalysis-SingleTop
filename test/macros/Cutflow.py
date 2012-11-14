#!/usr/bin/env python                                                                                                                  

from ROOT import *

import sys

dumpEvtNum = False

if len(sys.argv) > 1:
    if '-evtDump' in sys.argv:
        print 'Dumping event numbers'
        dumpEvtNum = True

#filenames = ['../output/ntuple_SystTrees_TWChannel.root']

fileName = TFile('../output/ntuple_SysTrees_TWChannel.root')

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

emuStart = 0
mumuStart = 0
eeStart = 0

if dumpEvtNum:
    lepSelDump = [open('eventDumps/Danny/lepSelDump_emu.txt','w'),open('eventDumps/Danny/lepSelDump_mumu.txt','w'),open('eventDumps/Danny/lepSelDump_ee.txt','w')]
    lepVetoDump = [open('eventDumps/Danny/lepVetoDump_emu.txt','w'),open('eventDumps/Danny/lepVetoDump_mumu.txt','w'),open('eventDumps/Danny/lepVetoDump_ee.txt','w')]
    mllCutDump = [open('eventDumps/Danny/mllCutDump_emu.txt','w'),open('eventDumps/Danny/mllCutDump_mumu.txt','w'),open('eventDumps/Danny/mllCutDump_ee.txt','w')]
    metCutDump = [open('eventDumps/Danny/metCutDump_emu.txt','w'),open('eventDumps/Danny/metCutDump_mumu.txt','w'),open('eventDumps/Danny/metCutDump_ee.txt','w')]
    oneJetDump = [open('eventDumps/Danny/oneJetDump_emu.txt','w'),open('eventDumps/Danny/oneJetDump_mumu.txt','w'),open('eventDumps/Danny/oneJetDump_ee.txt','w')]


evtCount = 0.
percent = 0.0
progSlots = 25.
nEvents = tWtree.GetEntries()*1.


for event in tWtree:

    evtCount += 1.
    if evtCount/nEvents > percent:
        i = int(percent*progSlots)
        progress = '0%[' + '-' * i + ' ' * (int(progSlots)-i) + ']100%\r'
        sys.stdout.write(progress)
        sys.stdout.flush()
        percent += 1./progSlots

    
    runNum = event.runNum
    lumiNum = event.lumiNum
    eventNum = event.eventNum

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

    if len(electronPt) > 0 and len(muonPt) > 0:
        emuStart += 1
    if len(electronPt) > 1:
        eeStart += 1
    if len(muonPt) > 1:
        mumuStart += 1

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
                    if abs(electronPVDxy[i]) < 0.04: #####ADJUSTMENT
                        if electronMVATrigV0[i] >= 0. and electronMVATrigV0[i] <= 1.0: #####ADJUSTMENT
                            if electronRhoCorrectedRelIso[i] < 0.15: #####ADJUSTMENT
                                if electronTrackerExpectedInnerHits[i] <= 1:
                                    goodEleidx.append(i)
                                    isTightElectron = True

        if not isTightElectron:
            if electronPt[i] > 20:
                if abs(electronEta[i]) < 2.5:
                    #                    if electronSuperClusterEta < 1.442 or electronSuperClusterEta > 1.5660:
                    if electronMVATrigV0[i] >= 0. and electronMVATrigV0[i] <= 1.0: #####ADJUSTMENT
                        if electronRhoCorrectedRelIso[i] < 0.15: #####ADJUSTMENT
                            looseEleidx.append(i)

    nLooseLeptons = len(looseEleidx) + len(looseMuonidx)

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

    if totalCharge != 0:
        print "Charge Issue???"
        continue
    
    LepSelection[ModeIdx] += 1

    if dumpEvtNum:
        lepSelDump[ModeIdx].write(str(runNum) + "\t" + str(lumiNum) + "\t" + str(eventNum) +"\n")
    
    if nLooseLeptons != 0:
        continue

    LepVeto[ModeIdx] += 1

    if dumpEvtNum:
        lepVetoDump[ModeIdx].write(str(runNum) + "\t" + str(lumiNum) + "\t" + str(eventNum) +"\n")


    mll = (lepton0 + lepton1).M()

    if mll < 20:
        continue

    if ModeIdx > 0:
        if mll < 101 and mll > 81:
            continue

    
    mllCut[ModeIdx] += 1

    if dumpEvtNum:
        mllCutDump[ModeIdx].write(str(runNum) + "\t" + str(lumiNum) + "\t" + str(eventNum) +"\n")


    MetPt = event.MetPt
    MetPhi = event.MetPhi

    if MetPt < 30 and not ModeIdx == 0:
        continue

    MetCut[ModeIdx] += 1

    if dumpEvtNum:
        metCutDump[ModeIdx].write(str(runNum) + "\t" + str(lumiNum) + "\t" + str(eventNum) +"\n")


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

    if dumpEvtNum:
        oneJetDump[ModeIdx].write(str(runNum) + "\t" + str(lumiNum) + "\t" + str(eventNum) +"\n")


    jetIdx = goodJetIdx[0]

    if jetCSV[jetIdx] < 0.679:
        continue

    JetBtag[ModeIdx] += 1


    jet = TLorentzVector()
    jet.SetPtEtaPhiE(jetPt[jetIdx],jetEta[jetIdx], jetPhi[jetIdx], jetE[jetIdx])

    Ptsys = (lepton0 + lepton1 + MET + jet).Pt()

    Ht = lepton0.Pt() + lepton1.Pt() + MET.Pt() + jet.Pt()

    if ModeIdx == 0 and Ht< 60:
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

print emuStart
print mumuStart
print eeStart
