import FWCore.ParameterSet.Config as cms

from TopQuarkAnalysis.SingleTop.SingleTopProducers_cff import *
from TopQuarkAnalysis.SingleTop.SingleTopSelectors_cff import *

#### Set the cuts values ####

#
muVetoCut = cms.string(" (isGlobalMuon || isTrackerMuon)  & pt > 10 & abs(eta) < 2.5 && userFloat(\"DeltaCorrectedIso\") <0.2 ")

eleVetoCut = cms.string("ecalDrivenMomentum.et > 20 & abs(eta) < 2.5 && userFloat(\"RhoCorrectedIso\") <0.2" )

eleVetoCutMVA = cms.string("abs(eta) < 2.5 && userFloat(\"RhoCorrectedIso\") <0.2" +
                            "&& electronID('mvaTrigV0') >0.0 &&"+
                            " et > 30 &  (abs(superCluster.eta)> 1.5660 || abs(superCluster.eta)<1.4442) ")
                            
#Tight leptons selection criteria
#No isolation or electronID requirement
eleTightCut = cms.string("ecalDrivenMomentum.et > 30  && abs(eta)<2.5  & ( abs(superCluster.eta)> 1.5660 || abs(superCluster.eta)<1.4442) && passConversionVeto")

muTightCut = cms.string("pt > 26 & isGlobalMuon && isPFMuon & abs(eta) < 2.1 && normChi2 < 10 && track.hitPattern.trackerLayersWithMeasurement>5 &&"+
                        "numberOfMatchedStations() > 1 && innerTrack.hitPattern.numberOfValidPixelHits > 0 && " +
                        " globalTrack.hitPattern.numberOfValidMuonHits > 0")

#Isolation cones definitions
#coneOpening = cms.double(0.4)
#defaultIsolationCut = cms.double(0.2)

#eJet definition
jetLooseCut = cms.string("numberOfDaughters()>1 & pt()> 20 && abs(eta())<5 " +
                         " & ((abs(eta())>=2.4) || ( chargedHadronEnergyFraction() > 0 & chargedMultiplicity()>0 & chargedEmEnergyFraction()<0.99))"+
                         " & neutralEmEnergyFraction() < 0.99 & neutralHadronEnergyFraction() < 0.99 "  )



#Requirement on the number of leptons in the event
#Loose: at least 1 tight lepton
minTightLeptons = cms.untracked.int32(1)
maxTightLeptons = cms.untracked.int32(99)

#Number of leptons that survive loose cuts and do not overlap with tight leptons
minVetoLeptons = cms.untracked.int32(0)
maxVetoLeptons = cms.untracked.int32(99)

### MC details that do not influence the selection  ###

#Check to see if it is signal channel ( MC only )
isMCSingleTopTChannel = cms.untracked.bool(False)

#definition: Leptons Veto for bet
vetoElectrons.cut =  eleVetoCut
vetoElectronsMVA.cut =  eleVetoCutMVA
vetoMuons.cut = muVetoCut

tightElectrons.cut =  eleTightCut
tightMuons.cut = muTightCut

tightElectronsZeroIso.cut =  eleTightCut
tightMuonsZeroIso.cut = muTightCut

#definition: Jets Loose
topJetsPF.cut = jetLooseCut

countLeptons.minNumberLoose = minVetoLeptons
countLeptons.maxNumberLoose = maxVetoLeptons

countLeptons.minNumberTight = minTightLeptons
countLeptons.maxNumberTight = maxTightLeptons

