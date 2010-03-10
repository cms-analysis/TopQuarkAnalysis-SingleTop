import FWCore.ParameterSet.Config as cms

process = cms.Process("SingleTop")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring (
#    'file:/tmp/oiorio/SingleTopSkim_35_55.root'
#'rfio:/castor/cern.ch/user/o/oiorio/SingleTop/SingleTop_tChan/SingleTop_tChanSkim_351_1.root',
#'rfio:/castor/cern.ch/user/o/oiorio/SingleTop/SingleTop_tChan/SingleTopSkim_35_2.root',
#'rfio:/castor/cern.ch/user/o/oiorio/SingleTop/SingleTop_tChan/SingleTopSkim_35_3.root',
#'rfio:/castor/cern.ch/user/o/oiorio/SingleTop/SingleTop_tChan/SingleTopSkim_35_4.root',
'rfio:/castor/cern.ch/user/o/oiorio/SingleTop/SingleTop_tChan/Events_35_1.root',

),
duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)

process.MessageLogger = cms.Service("MessageLogger")

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
    )

## Load additional RECO config
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.GlobalTag.globaltag = cms.string('MC_3XY_V9B::All') #TAG FOR 3_3_X
#process.GlobalTag.globaltag = cms.string('MC_3XY_V15::All') #TAG FOR  3_5
process.GlobalTag.globaltag = cms.string('MC_3XY_V25::All') #TAG FOR  3_5
process.load("Configuration.StandardSequences.MagneticField_cff")

#Loading Pat Sequences
process.load("PhysicsTools.PatAlgos.patSequences_cff")

#Apply correction factors for jets
process.patJetCorrFactors.corrSample = 'Summer09_7TeV'
#Apply MET correction factors
process.load("JetMETCorrections.Configuration.L2L3Corrections_Summer09_7TeV_cff")


#Path for the module that produces the tree for analysis 
process.pathPreselection = cms.Path(
   process.patDefaultSequence    )


#Here we load all modules and cuts: we can edit the cuts from there
#or load a new file that is a copy of this
process.load("TopQuarkAnalysis.SingleTop.SingleTopModules_cff")
#You can use this if you launch cmsRun from the same directory as the file
#SelectionCuts_cff
#process.load("SelectionCuts_cff")


# Reduce verbosity
#process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(10)

process.printTree = cms.EDAnalyzer("ParticleListDrawer",
                                   maxEventsToPrint = cms.untracked.int32(15),
                                   printVertex=cms.untracked.bool(False),
                                   src = cms.InputTag("genParticles")
                                   )

### HLT filter ###
import HLTrigger.HLTfilters.hltHighLevel_cfi
process.hltFilter = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
process.hltFilter.HLTPaths = ['HLT_IsoMu15', 'HLT_Ele15_SW_EleId_L1R']

#TFile for histograms production

#process.TFileService = cms.Service("TFileService", fileName = cms.string('SingleTopHistograms_tChan_test.root') )

#Production step: all collections are created
process.singleTopCollectionsProduction = cms.Sequence(
    process.preselectedElectrons *
    process.preselectedMuons *
    process.preselectedJets *
    process.preselectedMETs *

    process.topElectrons *
    process.topMuons *
    process.topJets *

    process.bJets *
    process.forwardJets *
    process.antiBJets *
    process.MCTruthParticles *
    process.recoTops 
    )

#Selection step: counting the events that survive the cuts
process.Selection = cms.Sequence(

#Counting leptons that survive the cuts, imposing there is just 1 Lepton
    process.countLeptons *

#Ntuples after those cuts
    process.singleTopBJets *
    process.singleTopForwardJets *
    process.singleTopPreJetsCutsElectrons *
    process.singleTopPreJetsCutsMuons * 
    process.singleTopPreJetsCutsTops * 

#Jets counting part
    process.countJets *    
    process.countBTags *
    process.countAntiBTags *
    process.countForwardJets *    

#Plots after jets cuts
    process.singleTopFinalElectrons *
    process.singleTopFinalMuons *
    process.singleTopFinalTops

#    process.final_cuts_top_histos # histograms after all cuts
    )

#Path
process.overallPath = cms.Path(
    process.singleTopCollectionsProduction *
    process.Selection
    )

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

#To run on 31X MC Production 
from TopQuarkAnalysis.SingleTop.SingleTopVersionTools_cff import *
run35xOn31xMC( process,
               jetSrc = cms.InputTag("antikt5CaloJets"),
               jetIdTag = "antikt5")


## Output module configuration
process.skim = cms.OutputModule("PoolOutputModule",
   fileName = cms.untracked.string('testVeryTightSkim.root'),
   
   # save only events passing the full path
   SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('overallPath') ),
     outputCommands = cms.untracked.vstring(
    'drop *',

#Ntuples

    'keep *_singleTopBJets_*_*',
    'keep *_singleTopForwardJets_*_*',
    'keep *_singleTopPreJetsCutsElectrons_*_*',
    'keep *_singleTopPreJetsCutsMuons_*_*',

    'keep *_singleTopFinalTops_*_*',
    'keep *_singleTopFinalElectrons_*_*',
    
#Skimmed collections

    'keep *_preselectedMuons_*_*',
    'keep *_preselectedElectrons_*_*',

    'keep *_topMuons_*_*',
    'keep *_topElectrons_*_*',

    'keep *_preselectedJets_*_*',

    'keep *_topJets_*_*',
    'keep *_bJets_*_*',
    'keep *_antiBJets_*_*',
    'keep *_forwardJets_*_*',

    'keep *_preselectedMETs_*_*',

    'keep *_recoTops__*',
    
#MC Info
    'keep *_generator_*_*',  
#    'keep *_genEventWeight_*_*',  
#    'keep GenEventInfoProduct_*_*_*',  
    'keep *_MCTruthParticles_*_*',

    )

)

process.ntuples = cms.OutputModule("PoolOutputModule",
        fileName = cms.untracked.string('NtuplesMC.root'),
     outputCommands = cms.untracked.vstring(
    'drop *',


#MC info
    'keep *_generator_*_*',  

#Ntuples


    'keep *_singleTopBJets_*_*',
    'keep *_singleTopForwardJets_*_*',
    'keep *_singleTopPreJetsCutsElectrons_*_*',
    'keep *_singleTopPreJetsCutsMuons_*_*',
    'keep *_singleTopPreJetsCutsTops_*_*',

    'keep *_singleTopFinalTops_*_*',
    'keep *_singleTopFinalElectrons_*_*',
    'keep *_singleTopFinalMuons_*_*',

)

)


#Save the skims
process.outpath = cms.EndPath( process.skim)

