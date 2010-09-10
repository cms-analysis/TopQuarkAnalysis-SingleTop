import FWCore.ParameterSet.Config as cms

from TopQuarkAnalysis.SingleTop.SingleTopProducers_cff import *
from TopQuarkAnalysis.SingleTop.SingleTopSelectors_cff import *

#from TopQuarkAnalysis.SingleTop.SingleTopHistogrammers_cff import *
#from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import *

from TopQuarkAnalysis.SingleTop.SingleTopControlSamplesProducers_cff import *


#### Set the cuts values ####

### Cuts for the kinematic variables, and ID and b-tagging###

#Muons, electrons and jets kinematic and ID cuts
muLooseCut = cms.string("isGlobalMuon & pt > 10 & abs(eta) < 2.5 & (isolationR03.sumPt + isolationR03.emEt + isolationR03.hadEt)/pt < 0.2")
eleLooseCut = cms.string("et > 15 & abs(eta) < 2.5 & (dr03TkSumPt + dr03EcalRecHitSumEt + dr03HcalTowerSumEt)/et < 0.2 ")

ele2ndEleCuts = cms.string("et > 20 & abs(eta) < 2.5 & (dr03TkSumPt + dr03EcalRecHitSumEt + dr03HcalTowerSumEt)/et < 1.0 ")

#Cuts on the isolation of the leptons
eleTightCut = cms.string("et>30  & abs(eta)<2.5  & gsfTrack().trackerExpectedHitsInner.numberOfHits == 0 & (dr03TkSumPt + dr03EcalRecHitSumEt + dr03HcalTowerSumEt)/et < 0.1 & dB < 0.02 && ( abs(superCluster.eta)> 1.5660 || abs(superCluster.eta)<14442)")

muTightCut = cms.string("pt > 20 & isGlobalMuon & isTrackerMuon & abs(eta) < 2.1 & muonID('GlobalMuonPromptTight') > 0 & (isolationR03.sumPt + isolationR03.emEt + isolationR03.hadEt)/pt < 0.1 & dB < 0.02 ") 

jetCut = cms.string('pt >  30 & abs(eta) < 5.0')# & jetID().fHPD < 0.98 & jetID().n90Hits > 1 ')

#Jets cleaning part: very tight cut requiring no overlaps with electrons and muons!
photonsCut = cms.string('pt/(pt+ caloIso) > 0.9')

#Apply  selection to clean jets from electrons
jetTightCut = cms.string('pt > 30 && abs(eta)<5 &&!hasOverlaps("myElectrons") && !hasOverlaps("myMuons") & emEnergyFraction > 0.01 & (abs(eta) > 2.4 || ( jetID().n90Hits > 1 & jetID().fHPD < 0.98)) ')

jetTightCutPF = cms.string("pt > 30 && abs(eta)<5 &&!hasOverlaps('myElectrons') && !hasOverlaps('myMuons') && numberOfDaughters > 1 && neutralHadronEnergyFraction < 1 & neutralEmEnergyFraction < 1 & (abs(eta)> 2.4 || ( chargedHadronEnergyFraction > 0 & chargedMultiplicity > 0) )")
#jetTightCut = cms.string('pt > 30')

#Cut to define forward jets 
forwardJetsCut = cms.string('(eta > 2.5) || (eta < -2.5)')

#Cuts for b-tagging
bJetsCut = cms.string('bDiscriminator("trackCountingHighPurBJetTags") > 3.41 && pt > 30')

#Cuts for anti-b tagging algorythm
antiBJetsCut = cms.string('bDiscriminator("trackCountingHighEffBJetTags") < 1.7 && pt > 30') 



### Cuts for the number of objects: counting how many of them survive the cuts ###

#Number of leptons that survive all the cuts ( kin + iso + ID )
minLeptons = cms.int32(1)
maxLeptons = cms.int32(1)

#Number of jets that survive kinematic cuts ( kin )
minJets = cms.uint32(2)
maxJets = cms.uint32(3)

#Number of b-tagged jets ( kin + b-tag algo )
minBTags = cms.uint32(1)
maxBTags = cms.uint32(1)

#Number of anti-b-tagged jets ( kin + NOT anti-b-tag algo)
minNonBTags = cms.uint32(1)
maxNonBTags = cms.uint32(1)

#Number of forward jets ( kin + fwd jets cut )
minFwdJets = cms.uint32(1)
maxFwdJets= cms.uint32(1)

#Detailed request for number of leptons ( not used in standard analysis )
minMuons = cms.uint32(1)
maxMuons = cms.uint32(1)


minElectrons = cms.uint32(1)
maxElectrons = cms.uint32(1)




topJets.checkOverlaps = cms.PSet(
    myElectrons = cms.PSet(
    src = cms.InputTag('topElectrons'),
#    #   algorithm = cms.string('bySuperClusterSeed'),
    preselection = cms.string(""),
    algorithm = cms.string('byDeltaR'),
    deltaR = cms.double(0.3),
    checkRecoComponents = cms.bool(False),
    pairCut =cms.string(""),
    requireNoOverlaps = cms.bool(False),
    ),

    myMuons = cms.PSet(
    src = cms.InputTag('topMuons'),
#    #   algorithm = cms.string('bySuperClusterSeed'),
    preselection = cms.string(""),
    algorithm = cms.string('byDeltaR'),
    deltaR = cms.double(0.3),
    checkRecoComponents = cms.bool(False),
    pairCut =cms.string(""),
    requireNoOverlaps = cms.bool(False),
    ),

)



### MC details that do not influence the selection  ###




#Check to see if it is signal channel ( MC only )
#isMCSingleTopTChannel = cms.untracked.bool(True)
isMCSingleTopTChannel = cms.untracked.bool(False)


#### Put the cuts in the modules ####
looseElectrons.cut = ele2ndEleCuts
#Preselection
preselectedMuons.cut = muLooseCut
preselectedElectrons.cut = eleLooseCut
preselectedJets.finalCut = jetTightCut

#looseMuons.cut = muLooseCut
#looseElectrons.cut = eleLooseCut

#selection: Leptons 
topElectrons.cut =  eleTightCut
topMuons.cut = muTightCut

#Selection : Jets
topJets.cut = jetTightCut
topJetsPF.cut = jetTightCutPF

#selection: jets peculiar collections
forwardJets.cut = forwardJetsCut
bJets.cut = bJetsCut 
antiBJets.cut =antiBJetsCut

forwardJetsPF.cut = forwardJetsCut
bJetsPF.cut = bJetsCut 


countMuons.minNumber = minMuons
countMuons.maxNumber = maxMuons

countMuonsPF.minNumber = minMuons
countMuonsPF.maxNumber = maxMuons

countElectrons.minNumber = minElectrons
countElectrons.maxNumber = maxElectrons



countMuonsAntiIso.minNumber = minMuons
countMuonsAntiIso.maxNumber = maxMuons
#countMuons.verbose = cms.untracked.bool(True)


countElectronsAntiIso.minNumber = minElectrons
countElectronsAntiIso.maxNumber = maxElectrons


countJets.minNumber = minJets
countJets.maxNumber = maxJets

countBTags.minNumber = minBTags
countBTags.maxNumber = maxBTags

countBTagsPF.minNumber = minBTags
countBTagsPF.maxNumber = maxBTags

countAntiBTags.minNumber = minNonBTags
countAntiBTags.maxNumber = maxNonBTags

countForwardJets.minNumber = minFwdJets
countForwardJets.maxNumber = maxFwdJets

countForwardJetsPF.minNumber = minFwdJets
countForwardJetsPF.maxNumber = maxFwdJets

countLeptons.minNumber = minLeptons
countLeptons.maxNumber = maxLeptons

countJetsPF.minNumber = cms.uint32(2)
countJetsPF.maxNumber = cms.uint32(2)

############Control samples part

#Control samples anti-iso cuts:

#Muons, electrons loose:
muLooseAntiIsoCut = cms.string("isGlobalMuon & pt > 10 & abs(eta) < 2.5 & (isolationR03.sumPt + isolationR03.emEt + isolationR03.hadEt)/pt > 0.1")
eleLooseAntiIsoCut = cms.string("et > 15 & abs(eta) < 2.5 & (dr03TkSumPt + dr03EcalRecHitSumEt + dr03HcalTowerSumEt)/et > 0.1 ")

#Muons, electrons tight:
eleTightAntiIsoCut = cms.string("et>30 & abs(eta)<2.5  & (dr03TkSumPt + dr03EcalRecHitSumEt + dr03HcalTowerSumEt)/et > 0.2 & gsfTrack().trackerExpectedHitsInner().numberOfHits == 0 & dB < 0.02")

muTightAntiIsoCut = cms.string("pt > 20 & abs(eta) < 2.1 & muonID('GlobalMuonPromptTight') > 0 & isGlobalMuon & isTrackerMuon & (isolationR03.sumPt + isolationR03.emEt + isolationR03.hadEt)/pt > 0.2 & dB < 0.02") 


#Jet Part
jetAntiIsoTightCut = cms.string('pt > 30 && !hasOverlaps("myElectronsAntiIso") && !hasOverlaps("myElectronsIso") && emEnergyFraction > 0.01 & jetID().n90Hits > 1 & jetID().fHPD < 0.98 ') 
bJetsAntiIso.cut = bJetsCut  
forwardJetsAntiIso.cut = forwardJetsCut


#Check that the jet does not overlap with the high pt Anti-Isolated electrons
topJetsAntiIso.checkOverlaps = cms.PSet(
    myElectronsAntiIso = cms.PSet(
    src = cms.InputTag('topElectronsAntiIso'),
    preselection = cms.string(""),
    algorithm = cms.string('byDeltaR'),
    deltaR = cms .double(0.3),
    checkRecoComponents = cms.bool(False),
    pairCut =cms.string(""),
    requireNoOverlaps = cms.bool(False),
    ),

    myElectronsIso = cms.PSet(
    src = cms.InputTag('preselectedElectrons'),
    preselection = eleTightCut,
    algorithm = cms.string('byDeltaR'),
    deltaR = cms .double(0.3),
    checkRecoComponents = cms.bool(False),
    pairCut =cms.string(""),
    requireNoOverlaps = cms.bool(False),
    ),
)

preselectedMuonsAntiIso.cut = muLooseAntiIsoCut
preselectedElectronsAntiIso.cut = eleLooseAntiIsoCut


topMuonsAntiIso.finalCut = muTightAntiIsoCut
topElectronsAntiIso.finalCut = eleTightAntiIsoCut

topJetsAntiIso.finalCut = jetAntiIsoTightCut

countLeptonsAntiIso.minNumber = cms.int32(1) 
countLeptonsAntiIso.maxNumber = cms.int32(1) 

vetoLeptonsIso.minNumber = cms.int32(0) 
vetoLeptonsIso.maxNumber = cms.int32(0) 


countJetsAntiIso.minNumber = cms.uint32(2)
countJetsAntiIso.maxNumber = cms.uint32(3) 

countJetsTTBar.minNumber = cms.uint32(3)
countJetsTTBar.maxNumber = cms.uint32(3) 

countJetsNonTTBar.minNumber = cms.uint32(2)
countJetsNonTTBar.maxNumber = cms.uint32(2) 

countJetsNonTTBarAntiIso.minNumber = cms.uint32(2)
countJetsNonTTBarAntiIso.maxNumber = cms.uint32(2) 


countJetsTTBarAntiIso.minNumber = cms.uint32(3)
countJetsTTBarAntiIso.maxNumber = cms.uint32(3) 
#
countWSamplePseudoBTags.minNumber =minBTags
countWSamplePseudoBTags.maxNumber =maxBTags

countWSamplePseudoBTagsAntiIso.minNumber = minBTags
countWSamplePseudoBTagsAntiIso.maxNumber = maxBTags
