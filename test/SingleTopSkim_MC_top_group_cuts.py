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
#'file:/tmp/oiorio/Events_35_1.root',

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
#Loading Pf Algorythms
process.load("PhysicsTools.PFCandProducer.PF2PAT_cff")

#Apply correction factors for jets
process.patJetCorrFactors.corrSample = 'Summer09_7TeV'
#Apply MET correction factors
process.load("JetMETCorrections.Configuration.L2L3Corrections_Summer09_7TeV_cff")


#Path for the PF algorythms:
process.pathPF = cms.Path(
    process.pfMET +#Particle Flow MET
    process.pfNoPileUpSequence +
    process.pfAllNeutralHadrons +
    process.pfAllChargedHadrons +
    process.pfAllPhotons +
    process.pfMuonSequence +
    process.pfNoMuon +
    process.pfElectronSequence +
    process.pfNoElectron +
    process.pfJetSequence +
    process.pfNoJet 
    #process.PF2PAT #Particle Flow Objects
     )


#Get PAT MET From PF 

#process.patPFPhotons = process.patPhotons.clone(photonSource = cms.InputTag("pfAllPhotons"))

#process.ic5PFJetTracksAssociatorAtVertex.jets = cms.InputTag("pfJets") 
#process.patPFJets = process.patJets.clone(jetSource = cms.InputTag("pfJets"),embedPFCandidates = cms.bool(True))
process.patPFMETs = process.patMETs.clone(metSource = cms.InputTag("pfMET"))
process.patPFElectrons = process.patElectrons.clone(useParticleFlow = cms.bool(True))
process.patPFMuons = process.patMuons.clone(useParticleFlow = cms.bool(True))

#process.patPFElectrons = process.patMETs.clone(jetSource = cms.InputTag("pfIsolatedElectrons"))
#process.patPFMuons = process.patMETs.clone(muonSource = cms.InputTag("pfIsolatedMuons"))


#Path for the module that produces the tree for analysis 
process.pathPreselection = cms.Path(
   process.patDefaultSequence +
   process.patPFMETs +
   process.patPFElectrons #+
 #  process.ic5PFJetTracksAssociatorAtVertex +
 #  process.patPFJets #+
#   process.patPFPhotons 
  )


#Here we load all modules and cuts: we can edit the cuts from there
#or load a new file that is a copy of this
#process.load("TopQuarkAnalysis.SingleTop.SingleTopModules_cff")
#You can use this if you launch cmsRun from the same directory as the file
#SelectionCuts_cff
process.load("SelectionCuts_top_group_cff")


# Reduce verbosity
#process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(10)

### HLT filter ###
import HLTrigger.HLTfilters.hltHighLevel_cfi
process.hltFilter = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
#process.hltFilter.HLTPaths = ['HLT_Mu9', 'HLT_Ele15_LW_L1R']
process.hltFilter.HLTPaths = ['HLT_Mu9','HLT_Ele15_SW_EleId_L1R']
process.hltFilter.andOr = cms.bool(True) 


#TFile for histograms production

#process.TFileService = cms.Service("TFileService", fileName = cms.string('SingleTopHistograms_tChan_test.root') )

#Production step: all collections are created

process.baseSequence = cms.Sequence(
    process.hltFilter *
    process.PVFilter *
    process.preselectedMuons *
    process.preselectedElectrons *
    process.countLeptons *
    process.preselectedJets *
    process.preselectedMETs *

#Production
    process.topMuons *
    process.topElectrons *
       
    process.topJets *
    process.bJets *
    process.antiBJets *
    process.forwardJets *
   
    process.recoTops 
#    process.MCTruthParticles
#    process.recoPFTops *
#    process.boostedTops *
#    process.boostedForwardJets *

#    process.boostedPFTops *
#    process.boostedForwardJetsVsPFTops *
#    process.boostedForwardJetsVsPFTops2 *

    )


process.PathAllMuons = cms.Path(
    process.baseSequence *
    process.countMuons *
    process.countJets *
    process.countBTags *
    process.countForwardJets 
#    process.countAntiBTags 
#    process.positiveMuons 
    )
#    process.negativeMuons 
#    process.negativeElectrons 

process.PathAllElectrons = cms.Path(
    process.baseSequence *
    process.countElectrons *
    process.countJets *
    process.countBTags *
    process.countForwardJets 
#   process.countAntiBTags 
#   process.positiveElectrons 
    )



process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")

#To run on 31X MC Production 
from TopQuarkAnalysis.SingleTop.SingleTopVersionTools_cff import *
run35xOn31xMC( process,
               jetSrc = cms.InputTag("antikt5CaloJets"),
               jetIdTag = "antikt5")


## Output module configuration
process.skim = cms.OutputModule("PoolOutputModule",
                                fileName = cms.untracked.string('TChannelSkim.root'),

#                                fileName = cms.untracked.string('WLNuChanSkim2.root'),
#                                fileName = cms.untracked.string('QCDSkim_fewEvents.root'),
                              #                                fileName = cms.untracked.string('WLNuChanSkim.root'),
   
   # save only events passing the full path
   SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('PathAllMuons','PathAllElectrons') ),
     outputCommands = cms.untracked.vstring(
    'drop *',


    'keep *_TriggerResults_*_*',

    'keep *_patPFMETs_*_*',
    'keep *_pfJets_*_*',
    'keep *_patPFElectrons_*_*',
    'keep *_patPFMuons_*_*',
    'keep *_pfPhotons_*_*',

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

#Save the skims
process.outpath = cms.EndPath( process.skim)

