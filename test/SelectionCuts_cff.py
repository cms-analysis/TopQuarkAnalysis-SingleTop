import FWCore.ParameterSet.Config as cms
from TopQuarkAnalysis.SingleTop.SingleTopProducers_cff import *
from TopQuarkAnalysis.SingleTop.SingleTopSelectors_cff import *

from TopQuarkAnalysis.SingleTop.SingleTopHistogrammers_cff import *
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import *




#### Set the cuts values ####

### Cuts for the kinematic variables, and ID and b-tagging###

#Muons, electrons and jets kinematic and ID cuts
muonCuts = cms.string("pt > 20 & abs(eta) < 2.1 & muonID('GlobalMuonPromptTight') > 0")
electronCuts = cms.string("pt > 20 & abs(eta) < 2.4 & electronID('eidRobustTight') > 0")

jetCuts = cms.string('pt >  20 & abs(eta) < 5.0')

#Cuts on the isolation of the leptons
eleIsoCut = cms.string('pt/(pt + trackIso + caloIso) >  0.95')
muIsoCut = cms.string('pt/(pt + trackIso + caloIso) > 0.95')

#Jets cleaning part: very tight cut requiring no overlaps with electrons and muons!
photonsCut = cms.string('pt/(pt+ caloIso) > 0.9')

#Apply  selection to clean jets from electrons
jetTightCut = cms.string('!hasOverlaps("myElectrons") & !hasOverlaps("myPhotons")')

#Cut to define forward jets 
forwardJetsCut = cms.string('(eta > 2.5) || (eta < -2.5)')

#Cuts for b-tagging
bJetsCut = cms.string('bDiscriminator("trackCountingHighPurBJetTags") > 5.36') # & pt > 30')

#Cuts for anti-b tagging algorythm
antiBJetsCut = cms.string('bDiscriminator("trackCountingHighEffBJetTags") < 1.47') 

#Cuts on the transverse mass of the W from top decay
#transverseWMassCut = cms.untracked.double(50)
transverseWMassCut = cms.untracked.double(0)

### Cuts for the number of objects: counting how many of them survive the cuts ###

#Number of leptons that survive all the cuts ( kin + iso + ID )
minLeptons = cms.int32(1)
maxLeptons = cms.int32(1)

#Number of jets that survive kinematic cuts ( kin )
minJets = cms.uint32(2)
maxJets = cms.uint32(2)

#Number of b-tagged jets ( kin + b-tag algo )
minBTags = cms.uint32(1)
maxBTags = cms.uint32(1)

#Number of anti-b-tagged jets ( kin + NOT anti-b-tag algo)
minNonBTags = cms.uint32(0)
maxNonBTags = cms.uint32(9999)

#Number of forward jets ( kin + fwd jets cut )
minFwdJets = cms.uint32(1)
maxFwdJets= cms.uint32(1)

#Detailed request for number of leptons ( not used in standard analysis )
minMuons = cms.uint32(0)
maxMuons = cms.uint32(9999)

minElectrons = cms.uint32(0)
maxElectrons = cms.uint32(9999)



### MC details that do not influence the selection  ###

#Check to see if it is signal channel ( MC only )
isMCSingleTopTChannel = cms.untracked.bool(True)
#isMCSingleTopTChannel = cms.untracked.bool(False)




#### Put the cuts in the modules ####

#Preselection
preselectedMuons.cut = muonCuts
preselectedElectrons.cut = electronCuts
preselectedJets.cut = jetCuts

#selection: Leptons 
topElectrons.cut =  eleIsoCut
topMuons.cut = muIsoCut

#selection: Jets
topJets.finalCut = jetTightCut

#selection: jets peculiar collections
forwardJets.cut = forwardJetsCut
bJets.cut = bJetsCut 
antiBJets.cut =antiBJetsCut


#MCTruth
MCTruthParticles.isSingleTopTChan = isMCSingleTopTChannel

#WMass
selectSingleTops.transverseWMassCut = transverseWMassCut

#Counting
countMuons.minNumber = minMuons
countMuons.maxNumber = maxMuons

countElectrons.minNumber = minElectrons
countElectrons.maxNumber = maxElectrons

countJets.minNumber = minJets
countJets.maxNumber = maxJets

countBTags.minNumber = minBTags
countBTags.maxNumber = maxBTags

countAntiBTags.minNumber = minNonBTags
countAntiBTags.maxNumber = maxNonBTags

countForwardJets.minNumber = minFwdJets
countForwardJets.maxNumber = maxFwdJets

countLeptons.minNumber = minLeptons
countLeptons.maxNumber = maxLeptons



topJets.checkOverlaps = cms.PSet(
    myElectrons = cms.PSet(
#    src = cms.InputTag('cleanPatElectrons'),
    src = cms.InputTag('topElectrons'),
    #   algorithm = cms.string('bySuperClusterSeed'),
    preselection = cms.string(""),
    algorithm = cms.string('byDeltaR'),
    deltaR = cms.double(0.5),
    checkRecoComponents = cms.bool(False),
    pairCut =cms.string(""),
    requireNoOverlaps = cms.bool(False),
    ),
   
    myPhotons = cms.PSet(
    src = cms.InputTag('cleanPatPhotons'),
    #preselection = cms.string(""),#"pt > 0 & pt/(pt+caloIso) > 0.8"),
    preselection = photonsCut,
    #   algorithm = cms.string('bySuperClusterSeed'),
    algorithm = cms.string('byDeltaR'),
    deltaR = cms.double(0.5), 
    checkRecoComponents = cms.bool(False),
    pairCut =cms.string(""),
   requireNoOverlaps = cms.bool(False),
    ),
    )
