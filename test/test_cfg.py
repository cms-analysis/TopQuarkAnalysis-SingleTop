import FWCore.ParameterSet.Config as cms

process = cms.Process("SingleTop")

#process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(50))
#process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(__MAX_EVENTS__))
process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring (
    'file:/storage/4/sroecker/SingleTop_tChannel_31x_Summer09_7TeV_GEN-SIM-RECO.root'
    ),
                             duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
                             )
#secondaryFileNames = cms.untracked.vstring (
#)
#)

#skipEvents = cms.untracked.uint32(__SKIP_EVENTS__),

process.MessageLogger = cms.Service("MessageLogger")

# new
process.load("PhysicsTools.PatAlgos.patSequences_cff")

## Load additional RECO config
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.GlobalTag.globaltag = cms.string('IDEAL_V9::All')
process.GlobalTag.globaltag = cms.string('MC_3XY_V25::All')
process.load("Configuration.StandardSequences.MagneticField_cff")


# to run on old MC
#from PhysicsTools.PatAlgos.tools.jetTools import *

#addJetID( process, "antikt5CaloJets", "antikt5" )

#switchJetCollection(process,
#cms.InputTag('antikt5CaloJets'),
#doJTA            = True,
#doBTagging       = True,
#jetCorrLabel     = ('AK5','Calo'),
#doType1MET       = True,
#genJetCollection = cms.InputTag("antikt5GenJets"),
#doJetID = True,
#jetIdLabel = "antikt5"
#)

# SingleTop preselection
process.STPreselection = cms.EDAnalyzer("Preselection",
                                        ResultDir = cms.string('./'),
                                        
                                        EventType = cms.InputTag("SingleTopT"),
                                        #   EventType = cms.InputTag("NoMCInfo"),                                        
                                        ###SingleTopT, SingleTopS, TTBar, WJets or NoMCInfo
                                                                                
                                        #AnaType = cms.InputTag("MCTruth"),
                                        AnaType = cms.InputTag("Presel"),
                                        ### MCTruth: all events / Presel: selected events
                                        
                                        SampleCrossSection = cms.double(242.0),
                                      
                                        MiniTreeName = cms.string('tchan'),
                                      
                                        SampleName = cms.string('CatoCMSTree'),
                                        triggerInfo = cms.bool(True),
                                        
                                        doPresel = cms.bool(True),
					no0jets = cms.bool(True),

                                        metProducer = cms.InputTag("patMETs"),
                                        met_cut_pt = cms.double(-30.0),
                                        
                                        muonProducer = cms.InputTag("selectedPatMuons"),
                                        muon_cut_pt = cms.double(20.0),
                                        muon_cut_eta = cms.double(2.1),
                                        muTriggerTag = cms.string('HLT_Mu15'),
                                        
                                        electronProducer = cms.InputTag("selectedPatElectrons"),
                                        electron_cut_pt = cms.double(20.0),
                                        electron_cut_eta = cms.double(2.4),
                                        eleTriggerTag = cms.string('HLT_Ele15_SW_EleId_L1R'),
                                        
					jet_loosecut_pt = cms.double(20.0),
					jet_tightcut_pt = cms.double(30.0),
                                        jet_cut_eta = cms.double(5.0),
                                        jetProducer = cms.InputTag("selectedPatJets"),
                                        jetAlgo = cms.string('iterativeCone5CaloJets'), 
					#/not used anyway

                                        trackProducer = cms.InputTag("ctfWithMaterialTracks"),
                                        
                                        vertexProducer = cms.InputTag("offlinePrimaryVertices")
                                        ### is it better to use this, or offlinePrimaryVerticesWithBS ?
                                        )


process.TFileService = cms.Service("TFileService", fileName = cms.string('tchan.root') )

### HLT filter ###

import HLTrigger.HLTfilters.hltHighLevel_cfi
process.hltFilter = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltFilter.HLTPaths = ['HLT_IsoMu15', 'HLT_Ele15_SW_EleId_L1R']

### execute ###

process.p = cms.Path(
    process.patDefaultSequence +
    process.STPreselection
    )

from PhysicsTools.PatAlgos.tools.cmsswVersionTools import *
run33xOn31xMC( process,
               jetSrc = cms.InputTag("antikt5CaloJets"),
               jetIdTag = "antikt5")

