import FWCore.ParameterSet.Config as cms

process = cms.Process("SingleTop")

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    FailPath = cms.untracked.vstring('ProductNotFound','Type Mismatch')
    )


# conditions ------------------------------------------------------------------

print "test "

#process.load("Configuration.StandardSequences.MixingNoPileUp_cff")
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff") ### real data
#process.load("Configuration.StandardSequences.MagneticField_cff") ### real data

#ChannelName = "TTBarV4"
ChannelName = "TChannel"

isData = False
#isData = True

#process.GlobalTag.globaltag = cms.string('START53_V11::All')
process.GlobalTag.globaltag = cms.string('START53_V7F::All')
#process.GlobalTag.globaltag = cms.string('START311_V2::All')

#from Configuration.PyReleaseValidation.autoCond import autoCond
#process.GlobalTag.globaltag = autoCond['startup']
process.load("TopQuarkAnalysis.SingleTop.SingleTopSequences_cff") 
process.load("SelectionCuts_Skim_cff")################<----------
process.load("PhysicsTools.PatAlgos.patSequences_cff") 


#process.load("TopQuarkAnalysis.SingleTop.SingleTopFilters_cfi")


import HLTrigger.HLTfilters.triggerResultsFilter_cfi as triggerFilter
#process.HLTFilterResult  = triggerFilter.triggerResultsFilter.clone(
process.HLTFilterMu2012  = triggerFilter.triggerResultsFilter.clone(
    hltResults = cms.InputTag( "TriggerResults","","HLT"),
    triggerConditions = ["HLT_IsoMu24_eta2p1_v*"],
    l1tResults = '',
    throw = False
    )

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('dummy.root'),
                               outputCommands = cms.untracked.vstring(""),
                               )


# Get a list of good primary vertices, in 42x, these are DAF vertices
#from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector

process.goodOfflinePrimaryVertices = cms.EDFilter( "PrimaryVertexObjectFilter" ,
                                                   filterParams = cms.PSet( minNdof = cms.double( 4. ) , maxZ = cms.double( 24. ) , maxRho = cms.double( 2. ) ) ,
                                                   filter = cms.bool( True) , src = cms.InputTag( 'offlinePrimaryVertices' ) )



from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
process.kt6PFJetsForIsolation = kt4PFJets.clone( rParam = 0.6, doRhoFastjet = True )
process.kt6PFJetsForIsolation.Rho_EtaMax = cms.double(2.5)

process.patElectrons.addElectronID = cms.bool(True)
process.patElectrons.electronIDSources = process.electronIDSources

#process.patElectrons.usePV = cms.bool(False)
#process.patMuons.usePV = cms.bool(False)



# set the dB to the beamspot
#process.patMuons.usePV = cms.bool(False)
#process.patElectrons.usePV = cms.bool(False)

postfix = ""

# Configure PAT to use PF2PAT instead of AOD sources
from PhysicsTools.PatAlgos.tools.pfTools import *
from PhysicsTools.PatAlgos.tools.trigTools import *
Postfix = ""
runOnMC = True
jetAlgoName = "AK5"
print "test2.2"
usePF2PAT(process, runPF2PAT=True, jetAlgo=jetAlgoName, runOnMC=runOnMC, postfix=Postfix, jetCorrections=('AK5PFchs',['L1FastJet','L2Relative','L3Absolute']), pvCollection=cms.InputTag('goodOfflinePrimaryVertices'),  typeIMetCorrections=True)
#usePF2PAT(process, runPF2PAT=True, jetAlgo=jetAlgoName, runOnMC=runOnMC, postfix=Postfix, jetCorrections=('AK5PFchs',['L1FastJet','L2Relative','L3Absolute']), pvCollection=cms.InputTag('offlinePrimaryVertices'),  typeIMetCorrections=True)
#          jetCorrections=('AK5PFchs', jetCorrections)


                    
switchOnTriggerMatchEmbedding(process,triggerMatchers = ['PatMuonTriggerMatchHLTIsoMu24','PatJetTriggerMatchHLTIsoMuBTagIP'])



process.pfPileUp.Enable = True
process.load("CMGTools.External.pujetidsequence_cff")

process.pfPileUp.checkClosestZVertex = cms.bool(False)

# NOT for gsfElectrons
#process.patElectrons.isolationValues = cms.PSet(
#    pfChargedHadrons = cms.InputTag("elPFIsoValueCharged03PFId"),
#    pfChargedAll = cms.InputTag("elPFIsoValueChargedAll03PFId"),
#    pfPUChargedHadrons = cms.InputTag("elPFIsoValuePU03PFId"),
#    pfNeutralHadrons = cms.InputTag("elPFIsoValueNeutral03PFId"),
#    pfPhotons = cms.InputTag("elPFIsoValueGamma03PFId")
#    )

print " test 0 " 
process.pfIsolatedMuons.combinedIsolationCut = cms.double(0.2)
process.pfIsolatedElectrons.combinedIsolationCut = cms.double(0.2)

#process.pfIsolatedMuons.isolationCut = cms.double(0.2)
#process.pfIsolatedElectrons.isolationCut = cms.double(0.2)

process.pfIsolatedElectrons.isolationValueMapsCharged = cms.VInputTag(cms.InputTag("elPFIsoValueCharged03PFId"))
process.pfIsolatedElectrons.deltaBetaIsolationValueMap = cms.InputTag("elPFIsoValuePU03PFId")
process.pfIsolatedElectrons.isolationValueMapsNeutral = cms.VInputTag(cms.InputTag("elPFIsoValueNeutral03PFId"), cms.InputTag("elPFIsoValueGamma03PFId"))

process.patElectrons.isolationValues = cms.PSet( pfChargedHadrons = cms.InputTag("elPFIsoValueCharged03PFId"), pfChargedAll = cms.InputTag("elPFIsoValueChargedAll03PFId"), pfPUChargedHadrons = cms.InputTag("elPFIsoValuePU03PFId"), pfNeutralHadrons = cms.InputTag("elPFIsoValueNeutral03PFId"), pfPhotons = cms.InputTag("elPFIsoValueGamma03PFId") )



#applyPostfix(process,"pfIsolatedElectrons",postfix).combinedIsolationCut = cms.double(0.2)#

#applyPostfix(process,"pfIsolatedMuons",postfix).isolationCut = cms.double(0.2)
#applyPostfix(process,"pfIsolatedElectrons",postfix).isolationCut = cms.double(0.2)

#
process.patseq = cms.Sequence(
#    process.patElectronIDs +
    process.goodOfflinePrimaryVertices *
    process.patElectronIDs *
    process.kt6PFJetsForIsolation *
    getattr(process,"patPF2PATSequence"+postfix) #*    +process.triggerMatchingSequence
#    process.producePatPFMETCorrections
#    getattr(process,"patPF2PATSequence"+postfixQCD) 
    )


#print " test 1 " 
process.pfIsolatedMuonsZeroIso = process.pfIsolatedMuons.clone(combinedIsolationCut =  cms.double(float("inf")),
                                                               isolationCut =  cms.double(float("inf")),
                                                               )
#
process.patMuonsZeroIso = process.patMuons.clone(pfMuonSource = cms.InputTag("pfIsolatedMuonsZeroIso"))#, genParticleMatch = cms.InputTag("muonMatchZeroIso"))
# use pf isolation, but do not change matching
tmp = process.muonMatch.src
adaptPFMuons(process, process.patMuonsZeroIso, "")
process.muonMatch.src = tmp
process.muonMatchZeroIso = process.muonMatch.clone(src = cms.InputTag("pfIsolatedMuonsZeroIso"))

process.pfIsolatedElectronsZeroIso = process.pfIsolatedElectrons.clone(combinedIsolationCut = cms.double(float("inf")),
                                                                       isolationCut =  cms.double(float("inf")),
                                                                       )
process.patElectronsZeroIso = process.patElectrons.clone(pfElectronSource = cms.InputTag("pfIsolatedElectronsZeroIso"))
#adaptPFElectrons(process, process.patElectronsZeroIso, "")


#print " test 2 " 



process.ZeroIsoLeptonSequence = cms.Sequence(
         process.pfIsolatedMuonsZeroIso +
#         process.muonMatchZeroIso +
         process.patMuonsZeroIso +
         process.pfIsolatedElectronsZeroIso +
         process.patElectronsZeroIso
         )



#print " test 3 " 


#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(200) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring (
#"file:/tmp/oiorio/Sync_File_TTBar.root",
#"file:/tmp/oiorio/Synch_File_TbarChannel.root",
#"file:/tmp/oiorio/T_t-channel_Synch.root",
"file:/afs/cern.ch/work/o/oiorio/public/xFrancescoFab/T_t-channel_Synch.root"
#"file:/tmp/oiorio/edmntuple_sync2012_T_t_withPVCleaning.root"
),
#eventsToProcess = cms.untracked.VEventRange('1:3107635-1:3107635'),
duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)


if isData:
    process.looseElectrons.isData = cms.untracked.bool(True)
    process.looseElectronsEle.isData = cms.untracked.bool(True)
    process.tightElectrons.isData = cms.untracked.bool(True)
    process.tightElectronsZeroIso.isData = cms.untracked.bool(True)


#process.selectedPatJetsTriggerMatch.cut = cms.string("numberOfDaughters()>1 & pt()> 40 && abs(eta())<4.7 " +
#                         " & ((abs(eta())>=2.4) || ( chargedHadronEnergyFraction() > 0 & chargedMultiplicity()>0 & chargedEmEnergyFraction()<0.99))"+
#                        " & neutralEmEnergyFraction() < 0.99 & neutralHadronEnergyFraction() < 0.99 "  )#





process.selection = cms.Path (
    process.HLTFilterMu2012 *
    process.goodOfflinePrimaryVertices 
    )

process.pathPreselection = cms.Path(
    process.HLTFilterMu2012 *
    process.patseq + process.puJetIdSqeuence + process.puJetIdSqeuenceChs *
    process.ZeroIsoLeptonSequence *
    process.basePath +
    process.preselection + 
    process.nTuplesSkim 

    #+  process.producePatPFMETCorrections
    )

#process.baseLeptonSequence = cms.Path(
#    process.HLTFilterMu2012 *
 #   process.goodOfflinePrimaryVertices *
 #   )




doMCTruth = True 
#doMCTruth = False
#print " test 4 " 

if isData: doMCTruth = False  

from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import saveNTuplesSkimLoose
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import saveNTuplesSkimMu

process.nTupleAllJets.src = cms.InputTag("selectedPatJets")
process.topJetsPF.src = cms.InputTag("selectedPatJets")
process.topJetsPF.removeOverlap = cms.untracked.bool(False)


savePatTupleSkimLoose = cms.untracked.vstring(
    'drop *',

    'keep patMuons_selectedPatMuons_*_*',
    'keep patMuons_selectedPatMuonsTriggerMatch_*_*',
    'keep patJets_selectedPatJetsTriggerMatch_*_*',

    'keep patElectrons_selectedPatElectrons_*_*',
    'keep patJets_selectedPatJets_*_*',
    'keep patMETs_patMETs_*_*',
    'keep *_patPFMet_*_*',
    'keep *_patType1CorrectedPFMet_*_*',
    'keep *_PVFilterProducer_*_*',

    'keep *_kt6PFJetsForIsolation_rho_*',

    'keep patJets_topJetsPF_*_*',
    'keep patMuons_looseMuons_*_*',
    'keep *_looseElectrons_*_*',
    'keep patMuons_tightMuons_*_*',
    'keep patMuons_tightMuonsTest_*_*',
    'keep *_tightElectrons_*_*',

    "keep *_TriggerResults_*_*",#Trigger results
    "keep *_PatMuonTriggerMatchHLTIsoMu24_*_*",#Trigger matches
    "keep *_patTrigger_*_*",
    "keep *_patTriggerEvent_*_*",

    'keep *_PDFInfo_*_*',

    'keep *_patElectronsZeroIso_*_*',
    'keep *_patMuonsZeroIso_*_*',
    'keep *_kt6PFJetsCentral_*_*',
    'keep *_PVFilterProducer_*_*',
    
    'keep *_cFlavorHistoryProducer_*_*',
    'keep *_bFlavorHistoryProducer_*_*',
    "keep *_puJetId_*_*", # input variables
    "keep *_puJetMva_*_*", # final MVAs and working point flags
    "keep *_puJetIdChs_*_*", # input variables
    "keep *_puJetMvaChs_*_*", # final MVAs and working point flags

    'keep *_pfNoMuon_*_*',
    'keep *_pfIsolatedElectrons_*_*',
    'keep *_pfNoElectron_*_*',
    'keep *_pfNoTau_*_*',
    'keep *_pfTaus_*_*',
    'keep *_pfNoTau_*_*',
    'keep *_pfJets_*_*',

    )




#print " test 5 " 

#doMCTruth= False
if doMCTruth:
    process.MCTruth = cms.Path (
        process.HLTFilterMu2012 *
        process.MCTruthParticles
        + process.nTuplesSkimMCTruth
        )
    
    savePatTupleSkimLoose.append('keep *_MCTruthParticles_*_*')

    saveNTuplesSkimLoose.append('keep  floats_MCTruthParticles_*_*')
    saveNTuplesSkimLoose.append('keep  ints_MCTruthParticles_*_*')
    saveNTuplesSkimLoose.append('keep  floats_singleTopMCLeptons_*_*')
    saveNTuplesSkimLoose.append('keep  floats_singleTopMCQuarks_*_*')
    saveNTuplesSkimLoose.append('keep  floats_singleTopMCNeutrinos_*_*')
    saveNTuplesSkimLoose.append('keep  floats_singleTopMCBQuarks_*_*')
    saveNTuplesSkimLoose.append('keep  floats_singleTopMCTops_*_*')
    saveNTuplesSkimLoose.append('keep  floats_singleTopMCTopsW_*_*')
    saveNTuplesSkimLoose.append('keep  floats_singleTopMCTopsBQuark_*_*')
    saveNTuplesSkimLoose.append('keep  floats_singleTopMCTopsLepton_*_*')
    saveNTuplesSkimLoose.append('keep  floats_singleTopMCTopsNeutrino_*_*')
    saveNTuplesSkimLoose.append('keep  floats_singleTopMCTopsQuark_*_*')
    saveNTuplesSkimLoose.append('keep  floats_singleTopMCTopsQuarkBar_*_*')


#process.out.extend(["keep *_puJetId_*_*", # input variables
#                    "keep *_puJetMva_*_*" # final MVAs and working point flags
#                    ])

#process.saveNTuplesSkimLoose.append()

## Output module configuration
process.singleTopNTuple = cms.OutputModule("PoolOutputModule",
#                                fileName = cms.untracked.string('rfio:/CST/cern.ch/user/o/oiorio/SingleTop/SubSkims/WControlSamples1.root'),
#                   fileName = cms.untracked.Bstring('/tmp/oiorio/edmntuple_tchannel_big.root'),
                   fileName = cms.untracked.string('edmntuple_mu'+ChannelName+'.root'),
                                             
                   SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('selection')),
                   outputCommands = saveNTuplesSkimLoose,
#                   outputCommands = savePatTupleSkimLoose
#                   outputCommands = saveNTuplesSkimLoose,
)

process.singleTopPatTuple = cms.OutputModule("PoolOutputModule",
#                                fileName = cms.untracked.string('rfio:/CST/cern.ch/user/o/oiorio/SingleTop/SubSkims/WControlSamples1.root'),
                   fileName = cms.untracked.string('/tmp/oiorio/pattuple_smalptcut'+ChannelName+'.root'),


                   SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('selection')),
                   outputCommands = savePatTupleSkimLoose
                                             )
process.singleTopNTuple.dropMetaData = cms.untracked.string("ALL")

process.outpath = cms.EndPath(
    process.singleTopNTuple +
    process.singleTopPatTuple 
    )

