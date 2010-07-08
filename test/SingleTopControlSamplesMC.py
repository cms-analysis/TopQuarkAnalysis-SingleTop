import FWCore.ParameterSet.Config as cms

process = cms.Process("SingleTop")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring (
    'rfio:/castor/cern.ch/user/g/giamman/test/D817160F-BAEB-DE11-BE9F-00E0814896BE.root'#signal file, from /SingleTop_tChannel-madgraph/Summer09-MC_31X_V3_7TeV-v2/GEN-SIM-RECO
),
duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)




## Load additional RECO config
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")


process.GlobalTag.globaltag = cms.string('START36_V9::All') #TAG FOR  Data 27May


#process.GlobalTag.globaltag = cms.string('GR_R_37X_V5A::All') #TAG FOR  Data 27May
process.load("Configuration.StandardSequences.MagneticField_cff")




from PhysicsTools.PatAlgos.patTemplate_cfg import *

#Loading Pat Sequences

#Loading Pat Sequences + various stuff
process.load("TopQuarkAnalysis.SingleTop.SingleTopSequences_cff") 


process.load("SelectionCuts_top_group_control_samples_v2_cff")

print "loadedcuts"


from PhysicsTools.PatAlgos.tools.coreTools import *

#Loading Pf Algorythms
process.load("PhysicsTools.PFCandProducer.PF2PAT_cff")

from PhysicsTools.PatAlgos.patTemplate_cfg import *
from PhysicsTools.PatAlgos.tools.pfTools import *


removeMCMatching(process,
                 ['All'])


from PhysicsTools.PatAlgos.tools.cmsswVersionTools import *


run36xOn35xInput(process)


process.patJets.jetSource = cms.InputTag("ak5CaloJets")

postfix = "PFlow"
#usePF2PAT(process,runPF2PAT=True,jetAlgo='AK5',runOnMC=True,postfix=postfix)

print "test1"

#getattr(process, "patElectrons" + postfix).embedGenMatch=False
#getattr(process, "patMuons" + postfix).embedGenMatch=False


process.patPFMETs = process.patMETs.clone(metSource = cms.InputTag("pfMET"))
process.patPFElectrons = process.patElectrons.clone(pfElectronSource = cms.InputTag("particleFlow","electrons"), useParticleFlow = cms.bool(True))
process.patPFMuons = process.patMuons.clone(pfMuonSource = cms.InputTag("particleFlow","muons"),useParticleFlow = cms.bool(False))

#Path for the module that produces the tree for analysis 

process.pathPreselection = cms.Path(
   process.patElectronIDs +
   process.patDefaultSequence +
   process.PF2PAT +
   process.pfMET +
   process.patPFMETs +#+ +
#   getattr(process,"patPF2PATSequence"+postfix) 
#   process.makeNewPatElectrons
      process.patPFElectrons +
   #   process.patJetsPFlow +
#   process.patPFBJets +
#      process.patPFElectrons +
      process.patPFMuons)


readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()

readFiles.extend( [
    'rfio:/castor/cern.ch/user/o/oiorio/SingleTop/SubSkims/MC/Loose/Events_1_1.root',
    #    'file:/tmp/oiorio/Events_1_1.root',
    #Production step: all collections are created
        ] );

#from getLFNsForSite_cff import *


process.source.fileNames = readFiles
#process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange()


process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )


process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    FailPath = cms.untracked.vstring('ProductNotFound','Type Mismatch')
    )


process.baseLeptonSequence = cms.Path(
    process.basePath
    )


#Iso Paths 
process.PathIsoMuons = cms.Path(
    process.IsoMuons
    )


process.PathIsoElectrons = cms.Path(
    process.IsoElectrons
    )


#AntiIso Paths
process.PathAntiIsoMuons = cms.Path(
    process.AntiIsoMuons
    )

process.PathAntiIsoElectrons = cms.Path(
    process.AntiIsoElectrons
    )

#Muon control samples

process.PathTSampleMuon = cms.Path(
    process.TSampleMuon
    )
process.PathWSampleMuon = cms.Path(
    process.WSampleMuon
    )
process.PathTTBarSampleMuon = cms.Path(
    process.TTBarSampleMuon
    )
process.PathQCDSampleMuon = cms.Path(
    process.QCDSampleMuon
    )
process.PathQCDWSampleMuon = cms.Path(
    process.QCDWSampleMuon
    )

###Electron control samples
process.PathTSampleElectron = cms.Path(
    process.TSampleElectron
    )
process.PathWSampleElectron = cms.Path(
    process.WSampleElectron
    )
process.PathTTBarSampleElectron = cms.Path(
    process.TTBarSampleElectron
    )
process.PathQCDSampleElectron = cms.Path(
    process.QCDSampleElectron
    )
process.PathQCDWSampleElectron = cms.Path(
    process.QCDWSampleElectron
    )




## Output module configuration
process.allControlSamples = cms.OutputModule("PoolOutputModule",
#                                fileName = cms.untracked.string('rfio:/CST/cern.ch/user/o/oiorio/SingleTop/SubSkims/WControlSamples1.root'),
                   fileName = cms.untracked.string('MCControlSamplesQCD_New.root'),
                                           

   
     # save only events passing the full path
     SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
    'PathTSampleMuon',
    'PathWSampleMuon',
    'PathTTBarSampleMuon',
    'PathQCDSampleMuon',
    'PathQCDWSampleMuon',
    'PathTSampleElectron',
    'PathWSampleElectron',
    'PathTTBarSampleElectron',
    'PathQCDSampleElectron',
    'PathQCDWSampleElectron',

                                                                     ) ),
     outputCommands = cms.untracked.vstring(
    'drop *',


    'keep *_patMETsPFlow_*_*',
    'keep *_pfJets_*_*',
    'keep *_patJetsPFlow_*_*',
    'keep *_patElectronsPFlow_*_*',
    'keep *_patMuonsPFlow_*_*',
#Skimmed collections

    'keep *_TriggerResults_*_*',

    'keep *_patPFMETs_*_*',
    'keep *_pfJets_*_*',
    'keep *_patPFElectrons_*_*',
    'keep *_patPFMuons_*_*',
#    'keep *_pfPhotons_*_*',

#Skimmed collections

#    'keep *_preselectedMuons_*_*',
#    'keep *_preselectedElectrons_*_*',



#FIXME JUST TO KEEP REASONABLE SIZE
#    'Keep *_topMuons_*_*',
#    'keep *_topElectrons_*_*',

#    'keep *_preselectedJets_*_*',

#    'keep *_topJets_*_*',
    'keep *_bJets_*_*',
#    'keep *_antiBJets_*_*',
    'keep *_forwardJets_*_*',

    'keep *_preselectedMETs_*_*',

    'keep *_pseudoBJets_*_*',


#    'keep *_topMuonsAntiIso_*_*',
#    'keep *_topElectronsAntiIso_*_*',

    'keep *_recoTopsAntiIso__*',
#    'keep *_topJetsAntiIso_*_*',
    'keep *_bJetsAntiIso_*_*',
#    'keep *_antiBJetsAntiIso_*_*',
    'keep *_forwardJetsAntiIso_*_*',



    'keep *_recoTops__*',
#    'keep *_boostedTops__*',
#    'keep *_boostedForwardJets_*_*',

    'keep *_recoTopsWSamplePseudoBTags__* ',
#    'keep *_boostedTopsWSamplePseudoBTagsTops__*', 
#    'keep *_boostedForwardJetsWSamplePseudoBTagsTops_*_*', 


    'keep *_recoTopsWSamplePseudoBTagsAntiIso__* ',


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


process.isoControlSamples = cms.OutputModule('PoolOutputModule',


                                                SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
    'PathIsoMuons',
    'PathAntiIsoMuons',
    'PathIsoElectrons',
    'PathAntiIsoElectrons',
    ) ),
 
                                                # fileName = cms.untracked.string('rfio:/castor/cern.ch/user/o/oiorio/SingleTop/SubSkims/QCDIsoControlSamples1.root'),
                                                fileName = cms.untracked.string('MCIsoControlSamplesQCD_New.root'),
#fileName = cms.untracked.string('test.root'),


     outputCommands = cms.untracked.vstring(
    'drop *',

    'keep *_patMETs_*_*',
    'keep *_patJets_*_*',

#    'keep *_patMETs_*_*',
#    'keep *_patMETs_*_*',

    'keep *_topMuonsAntiIso_*_*',
    'keep *_topElectronsAntiIso_*_*',

    'keep *_topMuons_*_*',
    'keep *_topElectrons_*_*',

    'keep *_topJets_*_*',
    'keep *_topJetsAntiIso_*_*',
    'keep *_patJetsPFlow_*_*',


    'keep *_preselectedMETs_*_*',
    'keep *_patMETsPFlow_*_*',

    'keep *_patPFMETs_*_*',
    'keep *_pfJets_*_*',
    'keep *_patPFElectrons_*_*',
    'keep *_patPFMuons_*_*',


    )

)

process.tSample =  process.allControlSamples.clone(
    fileName = cms.untracked.string('MCTChanSample_New.root'),
    
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
    'PathTSampleMuon',
    'PathTSampleElectron',
    )
                                         ))

process.wSample =  process.allControlSamples.clone(
    fileName = cms.untracked.string('MCWSample_New.root'),
    
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
    'PathWSampleMuon',
    'PathWSampleElectron',
    )
))

process.ttbarSample =  process.allControlSamples.clone(
    fileName = cms.untracked.string('MCTTBarSample_New.root'),
    
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
    'PathTTBarSampleMuon',
    'PathTTBarSampleElectron',
    )
))

process.outpath = cms.EndPath(
    process.tSample +
    process.wSample +
    process.ttbarSample +
    process.isoControlSamples
    )


