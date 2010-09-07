import FWCore.ParameterSet.Config as cms

process = cms.Process("SingleTop")

## Load additional RECO config
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.GlobalTag.globaltag = cms.string('START36_V9::All') #TAG FOR  Data 27May
process.GlobalTag.globaltag = cms.string('START36_V9::All') #TAG FOR  Data 27May
#process.GlobalTag.globaltag = cms.string('GR_R_37X_V5A::All') #TAG FOR  Data 27May
process.load("Configuration.StandardSequences.MagneticField_cff")



from PhysicsTools.PatAlgos.patTemplate_cfg import *


#Loading Pat Sequences


#Loading SingleTop Sequences + other functions
process.load("TopQuarkAnalysis.SingleTop.SingleTopSequences_cff") 


process.load("SelectionCuts_top_group_control_samples_v3_cff")


from PhysicsTools.PatAlgos.tools.coreTools import *
from PhysicsTools.PatAlgos.tools.metTools import *

#Loading Pf Algorythms
process.load("PhysicsTools.PFCandProducer.PF2PAT_cff")

from PhysicsTools.PatAlgos.patTemplate_cfg import *
from PhysicsTools.PatAlgos.tools.pfTools import *


removeMCMatching(process,
                 ['All'])


from PhysicsTools.PatAlgos.tools.cmsswVersionTools import *


run36xOn35xInput(process)


process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
process.load("RecoJets.Configuration.RecoJPTJets_cff")


#Path for the module that produces the tree for analysis 

addTcMET(process, 'TC')
addPfMET(process, 'PF')

postfix = "PFlow"
usePF2PAT(process,runPF2PAT=True,jetAlgo='AK5',runOnMC=True,postfix=postfix)


getattr(process, "patElectrons" + postfix).embedGenMatch=False
getattr(process, "patMuons" + postfix).embedGenMatch=False

                                     
addJetCollection(process,cms.InputTag("JetPlusTrackZSPCorJetAntiKt5"),
                 'AK5', 'JPT',
                 doJTA = True,
                 doBTagging = True,
                 jetCorrLabel = ('AK5','JPT'),
                 doType1MET = False ,
                 doL1Cleaning = False,
                 doL1Counters = True,
                 genJetCollection = cms.InputTag("ak5GenJets"),
                 doJetID = True,
                 jetIdLabel = "ak5"             
                 )

switchJetCollection(process,
                    cms.InputTag("JetPlusTrackZSPCorJetAntiKt5"),
                    jetIdLabel = "ak5",
                    doJTA = True,
                    doBTagging = True,
                    jetCorrLabel = ('AK5','JPT'),
                    doType1MET = False,
                    genJetCollection = cms.InputTag("ak5GenJets"),
                    doJetID = True,
                    )



process.pathPreselection = cms.Path(
    process.recoJPTJets +
    process.patDefaultSequence     )


process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(300) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring (

    'file:/tmp/oiorio/F81B1889-AF4B-DF11-85D3-001A64789DF4.root'

#'rfio:/castor/cern.ch/user/g/giamman/singletop/sync/F81B1889-AF4B-DF11-85D3-001A64789DF4.root',


),
duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    FailPath = cms.untracked.vstring('ProductNotFound','Type Mismatch')
    )


process.baseLeptonSequence = cms.Path(
    process.basePath
    )

#Muon control samples

process.PathTSampleMuon = cms.Path(
    process.TSampleMuon
    )

###Electron control samples
process.PathTSampleElectron = cms.Path(
    process.TSampleElectron
    )




## Output module configuration
process.allControlSamples = cms.OutputModule("PoolOutputModule",
#                                fileName = cms.untracked.string('rfio:/CST/cern.ch/user/o/oiorio/SingleTop/SubSkims/WControlSamples1.root'),
                   fileName = cms.untracked.string('test.root'),
                                           

     outputCommands = cms.untracked.vstring(
    'drop *',


    'keep *_patMETsPFlow_*_*',
    'keep *_patMETsTC_*_*',
    'keep *_patMETsPF_*_*',

    'keep *_patJetsPFlow_*_*',
    'keep *_patJetsPFlow_*_*',
    'keep *_cleanPatJets_*_*',
    'keep *_patElectronsPFlow_*_*',
    'keep *_patMuonsPFlow_*_*',
#Skimmed collections

    'keep *_TriggerResults_*_*',

#Skimmed collections

    'keep *_topMuons_*_*',
    'keep *_topElectrons_*_*',



#FIXME JUST TO KEEP REASONABLE SIZE

    'keep *_topJets_*_*',
    'keep *_topJetsPF_*_*',
#    'keep *_bJets_*_*',
#    'keep *_forwardJets_*_*',

    'keep *_preselectedMETs_*_*',
#    'keep *_preselectedJets_*_*',

    'keep *_singleTopObservablesTSample_*_*',    
    'keep *_singleTopObservablesWSample_*_*',    
    'keep *_singleTopObservablesTTBarSample_*_*',    
    'keep *_singleTopObservablesAntiIso_*_*',    
    'keep *_singleTopObservablesWSampleAntiIso_*_*',    


#MC Info
    'keep *_generator_*_*',  
#    'keep *_genEventWeight_*_*',  
#    'keep GenEventInfoProduct_*_*_*',  
#    'keep *_MCTruthParticles_*_*',

    )

)


process.tSampleMu =  process.allControlSamples.clone(
    fileName = cms.untracked.string('MCTChanSampleMu.root'),
    
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
    'PathTSampleMuon',
#    'PathTSampleElectron',
    )
)
)

process.tSampleEle =  process.allControlSamples.clone(
    fileName = cms.untracked.string('MCTChanSampleEle.root'),
    
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
#    'PathTSampleMuon',
    'PathTSampleElectron',
    )
)
)


process.outpath = cms.EndPath(
    process.tSampleMu + 
    process.tSampleEle 
    )

