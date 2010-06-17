import FWCore.ParameterSet.Config as cms

process = cms.Process("SingleTop")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring (

#    'rfio:/castor/cern.ch/cms/store/data/Commissioning10/MinimumBias/RECO/Apr15Skim_356_PreProduction_SD_Mu-v2/0011/90ACEF66-2E49-DF11-8B3C-00261894396B.root',
        #'rfio:/castor/cern.ch/user/o/oiorio/SingleTop/SingleTop_tChan/Events_35_1.root',

),
duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)




## Load additional RECO config
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.GlobalTag.globaltag = cms.string('MC_3XY_V9B::All') #TAG FOR 3_3_X
#process.GlobalTag.globaltag = cms.string('MC_3XY_V15::All') #TAG FOR  3_5
#process.GlobalTag.globaltag = cms.string('MC_3XY_V25::All') #TAG FOR  3_5
process.GlobalTag.globaltag = cms.string('GR_R_36X_V11A::All') #TAG FOR  Data 27May
#process.GlobalTag.globaltag = cms.string('GR_R_37X_V5A::All') #TAG FOR  Data 27May
process.load("Configuration.StandardSequences.MagneticField_cff")



from PhysicsTools.PatAlgos.patTemplate_cfg import *

#Loading Pat Sequences

#process.load("PhysicsTools.PatAlgos.patSequences_cff")



#Loading Pat Sequences + various stuff
process.load("TopQuarkAnalysis.SingleTop.SingleTopSequences_cff") 


#process.patElectrons.pfElectronSource= cms.InputTag("particleFlow","electrons")
#process.patMuons.pfMuonSource = cms.InputTag("particleFlow","muons")
#process.patElectrons.pfElectronSource= ""
#process.patMuons.pfMuonSource = cms.InputTag("particleFlow","muons")

from PhysicsTools.PatAlgos.tools.coreTools import *

#Loading Pf Algorythms
process.load("PhysicsTools.PFCandProducer.PF2PAT_cff")


from PhysicsTools.PatAlgos.patTemplate_cfg import *
from PhysicsTools.PatAlgos.tools.pfTools import *

print "test0"

postfix = "PFlow"
usePF2PAT(process,runPF2PAT=True,jetAlgo='AK5',runOnMC=False,postfix=postfix)

print "test1"

getattr(process, "patElectrons" + postfix).embedGenMatch=False
getattr(process, "patMuons" + postfix).embedGenMatch=False

print "test2"

# turn off MC matching for the process
removeMCMatching(process,
                 ['All'])

#bJetsCut = cms.string('bDiscriminator("trackCountingHighPurBJetTags") > 2.36 && pt > 30')

#print "test3"


process.patPFBJets = cms.EDFilter("PATJetSelector",
                                 src = cms.InputTag("patJetsPFlow"),
#                                  src = cms.InputTag("pfNoTauPFlow"),
                                  #                                  cut = bJetsCut
                                 )


process.patPFElectrons = process.patElectrons.clone(pfElectronSource = cms.InputTag("particleFlow","electrons"), useParticleFlow = cms.bool(True))
process.patPFMuons = process.patMuons.clone(pfMuonSource = cms.InputTag("particleFlow","muons"),useParticleFlow = cms.bool(False))

#process.patJets.addJetCorrFactors = cms.bool(False)
 
#Path for the module that produces the tree for analysis 
process.pathPreselection = cms.Path(
   process.patElectronIDs +
   process.patDefaultSequence +
   getattr(process,"patPF2PATSequence"+postfix) 
#   process.makeNewPatElectrons
   #   process.patPFElectrons +
   #   process.patJetsPFlow +
#   process.patPFBJets +
#      process.patPFElectrons +
#      process.patPFMuons 

  )


#Here we load all modules and cuts: we can edit the cuts from there
#or load a new file that is a copy of this
#process.load("TopQuarkAnalysis.SingleTop.SingleTopModules_cff")
#You can use this if you launch cmsRun from the same directory as the file
#SelectionCuts_cff
#process.load("SelectionCuts_top_group_cff")

#process.bJets.cut = bJetsCut


# Reduce verbosity
#process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)



#TFile for histograms production

#process.TFileService = cms.Service("TFileService", fileName = cms.string('SingleTopHistograms_tChan_test.root') )



readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()

readFiles.extend( [
    #'file:/tmp/oiorio/90ACEF66-2E49-DF11-8B3C-00261894396B.root',
#    'rfio:/castor/cern.ch/cms/store/data/Commissioning10/MinimumBias/RAW-RECO/Apr20Skim_GOODCOLL-v1/0179/FEF8B706-254E-DF11-9304-0026189437FE.root'

    #'file:/tmp/oiorio/90ACEF66-2E49-DF11-8B3C-00261894396B.root',
#'file:ExpressPhysics_Run2010A-Express-v2_FEVT_136100_922_273730582.root',
#'file:/tmp/oiorio/DataMiniSkim_1_1.root',
    #'rfio:/castor/cern.ch/user/o/oiorio/SingleTop/SingleTop_tChan/Events_35_1.root',
    'rfio:/castor/cern.ch/user/o/oiorio/SingleTop/SubSkims/Data/Loose/DataMiniSkim_1_1.root',
    #Production step: all collections are created
        ] );

#from getLFNsForSite_cff import *

process.source.fileNames = readFiles
#process.source.lumisToProcess = cms.untracked.VLuminosityBlockRange()


process.hltFilter.HLTPaths = ['HLT_Mu9', 'HLT_Photon10_L1R']

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )


process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    FailPath = cms.untracked.vstring('ProductNotFound')
    )


#process.MessageLogger.debugModules = cms.untracked.vstring("*")
#process.MessageLogger.cout = cms.untracked.PSet( threshold = cms.untracked.string("ERROR"), ) 
#process.MessageLogger.destinations = cms.untracked.vstring("cout")


                                        
#process.load("SelectionCuts_top_group_loose_control_samples_cff")

    
process.recoTopsPF = process.recoTops.clone(jetsSource = cms.InputTag("patPFBJets"))
process.recoTopsPF.METsSource = cms.InputTag("patMETsPFlow")
process.recoTopsPFAll = process.recoTopsPF.clone(
#    electronsSource = cms.InputTag("patElectronsPFlow"),
#    muonsSource = cms.InputTag("patMuonsPFlow"),
    electronsSource = cms.InputTag("patPFElectrons"),
    muonsSource = cms.InputTag("patPFMuons"),
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
                   fileName = cms.untracked.string('DataControlSamples.root'),
                                           

   
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

#    'keep *_patPFMETs_*_*',
#    'keep *_pfJets_*_*',
#    'keep *_patPFElectrons_*_*',
#    'keep *_patPFMuons_*_*',
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

process.qcdIsoControlSamples = cms.OutputModule('PoolOutputModule',
 SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
#    'PathAllNonTTBarSampleMuon',
#    'PathAllNonTTBarAntiIsoSampleMuon',
    'PathIsoMuons',
    'PathAntiIsoMuons',
    'PathIsoElectrons',
    'PathAntiIsoElectrons',
    ) ),
 
# fileName = cms.untracked.string('rfio:/castor/cern.ch/user/o/oiorio/SingleTop/SubSkims/QCDIsoControlSamples1.root'),
fileName = cms.untracked.string('DataIsoControlSamples.root'),
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
    'keep *_patJetsPFlow_*_*',

    )

 )

process.outpath = cms.EndPath(
    process.allControlSamples
    +
    process.qcdIsoControlSamples
    )
