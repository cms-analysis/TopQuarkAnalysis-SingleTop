import FWCore.ParameterSet.Config as cms

process = cms.Process("SingleTop")

## Load additional RECO config
process.load("Configuration.StandardSequences.MixingNoPileUp_cff")
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff") ### real data
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string('GR_R_38X_V11::All') #TAG FOR 382

process.load("TopQuarkAnalysis.SingleTop.SingleTopSequences_cff") 
process.load("SelectionCuts_top_group_control_samples_v3_cff")

from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
from PhysicsTools.PatAlgos.tools.jetTools import *
from PhysicsTools.PatAlgos.tools.metTools import *
from PhysicsTools.PatAlgos.tools.coreTools import *

#Path for the module that produces the tree for analysis 

# turn off MC matching for the process
removeMCMatching(process, ['All'])

# add PF

addJetCollection(process,
                   cms.InputTag('ak5PFJets'),
                   'AK5',
                   'PF',
                   doJTA=True,
                   doBTagging=True,
                   jetCorrLabel=('AK5','PF'),
                   doType1MET=True,
                   doJetID      = True,
                   jetIdLabel   = "ak5"
                  )

# add JPT
process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
process.load('RecoJets.Configuration.RecoJPTJets_cff')


addJetCollection(process,cms.InputTag('JetPlusTrackZSPCorJetAntiKt5'),
                                  'AK5', 'JPT',
                                  doJTA        = True,
                                  doBTagging   = True,
                                  jetCorrLabel = ('AK5','JPT'),
                                  doType1MET   = False,
                                  doL1Cleaning = False,
                                  doL1Counters = True,
                                  genJetCollection = cms.InputTag("ak5GenJets"),
                                  doJetID      = True,
                                  jetIdLabel   = "ak5"
                                  )

# corrections:
patJetCorrFactors.corrSample = cms.string("Spring10") 
switchJECSet( process, "Spring10")


addTcMET(process, 'TC')
addPfMET(process, 'PF')


process.pathPreselection = cms.Path(
    process.recoJPTJets +
    process.patDefaultSequence 
    )


process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1065) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring (

#    'file:/tmp/oiorio/94659715-5F91-DF11-BBCD-001D09F2AF96.root'
#'rfio:/castor/cern.ch/cms/store/data/Run2010A/Mu/RECO/v4/000/140/331/94659715-5F91-DF11-BBCD-001D09F2AF96.root'

#    'file:/tmp/oiorio/3C6D0701-4AA0-DF11-8437-0030487CD184.root',

    'rfio:/castor/cern.ch/user/o/oiorio/SingleTop/Candidates/Event_142928_446_107153746.root'
    #'rfio:/castor/cern.ch/cms/store/data/Run2010A/EG/RECO/v4/000/142/311/3C6D0701-4AA0-DF11-8437-0030487CD184.root',

#'rfio:/castor/cern.ch/user/g/giamman/singletop/sync/F81B1889-AF4B-DF11-85D3-001A64789DF4.root',


),
duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
#eventsToProcess = cms.untracked.VEventRange("140331:257717658-140331:1257717800"),
)

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    FailPath = cms.untracked.vstring('ProductNotFound','Type Mismatch')
    )

process.preselectedElectrons.isData = cms.untracked.bool(True)
process.topElectrons.isData = cms.untracked.bool(True)
#process.topElectronsPF.isData = cms.untracked.bool(True)

#process.electronIDIso.isData = cms.untracked.bool(True)
#process.electronIDAntiIso.isData = cms.untracked.bool(True)

process.preselectedJets.src = cms.InputTag("patJetsAK5JPT")

# good vertices
process.PVFilter.cut = cms.string("!isFake && ndof > 4 && abs(z) <= 24 && position.Rho <= 2")

process.demo = cms.EDAnalyzer('SimpleEventDumper',
                              verticesSource = cms.InputTag("PVFilter"),
                              electronSource = cms.InputTag("cleanPatElectrons"),
                              muonSource     = cms.InputTag("patMuons"),
                              patmetSource = cms.InputTag("patMETs"),
                              calometSource = cms.InputTag("met"), #uncorrected
                              pfmetSource = cms.InputTag("pfMet"),
                              tcmetSource = cms.InputTag("tcMet"),
                              patjetSource = cms.InputTag("patJets"),
                              pfjetSource = cms.InputTag("ak5PFJets"), #uncorrected
                              pfpatjetSource = cms.InputTag("patJetsAK5PF"), #corrected, and possibility to access b-tagging for it
                              jptjetSource = cms.InputTag("patJetsAK5JPT"),
                              lep_pt_min = cms.double(10),
                              mt_min = cms.double(20),
                              jet_pt_min = cms.double(20),
                              useL5corr = cms.bool(False),
                              useL5corr_including_gluons = cms.bool(False),#

                              imgSolStrategy = cms.int32(1), #0: ignore Img part; 1: adjust MT to MW (as TOP-09-005)
                             )

process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","HLT")


process.hltFilterPhoton20 = process.hltFilter.clone(HLTPaths = (
    'HLT_Ele15_SW_L1R',
    'HLT_Ele15_SW_L1R',
#    'HLT_Ele10_LW_L1R',
#    'HLT_Ele10_LW_L1R'
    ))

process.hltFilterSummary = cms.EDFilter("HLTSummaryFilter",
                                         summary = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
#                                         member = cms.InputTag("hltL1NonIsoHLTNonIsoSingleElectronLWEt10PixelMatchFilter","","HLT"),
                                       member = cms.InputTag("hltL1NonIsoHLTNonIsoSingleElectronEt15PixelMatchFilter","","HLT"),
                                        cut = cms.string(""),
                                        minN = cms.int32(1),
                                        )

#process.hltFilterPhoton20.eventSetupPathsKey = cms.string("hltL1NonIsoHLTNonIsoSingleElectronEt15PixelMatchFilter")

#process.hltFilter.HLTPaths = ['HLT_Mu15_v1']#,'HLT_Ele15_LW_L1R']

#Process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","HLT")

#process.hltFilterPhoton20.summary = cms.InputTag("hltTriggerSummaryAOD","","HLT")
#process.hltFilterPhoton20.member = cms.InputTag("HLT_Photon20_Cleaned_L1R","","HLT")

#process.hltFilterPhoton20 = process.hltFilterDev.clone(HLTPaths = ('HLT_Photon20_Cleaned_L1R','HLT_Photon20_Cleaned_L1R'))
#process.hltFilterPhoton20.HLTPathsPrescales = cms.vuint32(1,1)
#hltFilterPhoton20.member = cms.InputTag("hltL1NonIsoHLTNonIsoSinglePhotonEt10HcalIsolFilter","","HLT")
#hltFilterPhoton20.cut = cms.string("pt> 20")
#hltFilterPhoton20.minN = cms.int32(1)

process.baseLeptonSequence = cms.Path(
    process.basePath
    )

#Muon control samples

#process.PathTSampleMuonPF = cms.Path(
#    process.TSampleMuonPF *
#    process.demo
#    )

#process.PathTSampleMuonPFQCD = cms.Path(
#    process.QCDSampleMuonPF *
#    process.demo
#    )

###Electron control samples

process.PathTSampleElectronPF = cms.Path(
    process.hltFilterPhoton20 *
    process.hltFilterSummary *
    process.TSampleElectronPF *
    process.demo
    )

process.PathTSampleElectronPFQCD = cms.Path(
    process.hltFilterPhoton20 *
    process.hltFilterSummary *
    process.QCDSampleElectronPF *
    process.demo
    )


#process.PathTSampleElectronPFQCD = cms.Path(
#    process.TSampleElectronAntiIso *
#    process.QCDSampleElectron *
#    process.QCDSampleElectronPF *
#    process.PathElectronsAntiIso *
#    process.demo
#    )




## Output module configuration
process.allControlSamples = cms.OutputModule("PoolOutputModule",
#                                fileName = cms.untracked.string('rfio:/CST/cern.ch/user/o/oiorio/SingleTop/SubSkims/WControlSamples1.root'),
                   fileName = cms.untracked.string('test.root'),
                                           

  
     outputCommands = cms.untracked.vstring(
    'drop *',


#    'keep *_patMETsPFlow_*_*',
    'keep *_patMETsTC_*_*',
    'keep *_patMETsPF_*_*',

#    'keep *_patJetsPF_*_*',
#    'keep *_patJetsPF_*_*',
#    'keep *_cleanPatJets_*_*',
#    'keep *_patElectronsPFlow_*_*',
#    'keep *_patMuonsPFlow_*_*',
#Skimmed collections

#    'keep *_TriggerResults_*_*',

#Skimmed collections

    'keep *_topMuons_*_*',
    'keep *_topElectrons_*_*',

    'keep *_topMuonsAntiIso_*_*',
    'keep *_topElectronsAntiIso_*_*',

    
    'keep *_cFlavorHistoryProducer_*_*',
    'keep *_bFlavorHistoryProducer_*_*',

#Fixme JUST TO KEEP REASONABLE SIZE

    'keep *_topJetsAntiIsoPF_*_*',
#    'keep *_topJets_*_*',


    'keep *_topJetsPF_*_*',
    'keep *_bJetsPF_*_*',
    'keep *_forwardJetsPF_*_*',
    'keep *_bJetsAntiIsoPF_*_*',
    'keep *_forwardJetsAntiIsoPF_*_*',

    'keep recoNamedCompositeCandidates_recoTopsPF_*_*',
    'keep recoNamedCompositeCandidates_recoTopsAntiIsoPF_*_*',


#    'keep *_preselectedMETs_*_*',
#    'keep *_preselectedJets_*_*',

#    'keep *_singleTopObservablesTSample_*_*',    
#    'keep *_singleTopObservablesWSample_*_*',    
#    'keep *_singleTopObservablesTTBarSample_*_*',    
#    'keep *_singleTopObservablesAntiIso_*_*',    
#    'keep *_singleTopObservablesWSampleAntiIso_*_*',    


#MC Info
 #'keep *_generator_*_*',  
#    'keep *_genEventWeight_*_*',  
#    'keep GenEventInfoProduct_*_*_*',  
#    'keep *_MCTruthParticles_*_*',

    )

)


process.tSampleMu =  process.allControlSamples.clone(
    fileName = cms.untracked.string('DataTChanSampleMu_145762_147196.root'),
#    fileName = cms.untracked.string('DataTChanSampleMu_147196_148058.root'),
#    fileName = cms.untracked.string('DataTChanSampleMu_132240_144114.root'),
                                    
 
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
    'PathTSampleMuonPF',
#    'PathTSampleElectron',
    )
)
)

process.tSampleMuAntiIso =  process.allControlSamples.clone(
    fileName = cms.untracked.string('DataQCDChanSampleMu_145762_147196.root'),
#    fileName = cms.untracked.string('DataQCDChanSampleMu_147196_148058.root'),
#    fileName = cms.untracked.string('DataQCDChanSampleMu_132240_144114.root'),

    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
    'PathTSampleMuonPFQCD',
#    'PathTSampleElectron',
    )
)
)

process.tSampleEle =  process.allControlSamples.clone( 
#    fileName = cms.untracked.string('DataTChanSampleEle_132440_140040.root'),
    fileName = cms.untracked.string('DataTChanSampleEle_132440_140040.root'),
#    fileName = cms.untracked.string('DataTChanSampleEle_143963_146427.root'),
#    fileName = cms.untracked.string('DataTChanSampleEle_146428_147116.root'),
#    fileName = cms.untracked.string('DataTChanSampleEle_147117_148058.root'),
   
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
#    'PathTSampleMuon',
    'PathTSampleElectronPF',
    )
)
)
process.tSampleEleAntiIso =  process.allControlSamples.clone(
#   fileName = cms.untracked.string('DataQCDChanSampleEle_132440_140040.root'),
  fileName = cms.untracked.string('DataQCDChanSampleEle_132440_140040.root'),
#  fileName = cms.untracked.string('DataQCDChanSampleEle_143963_146427.root'),
#  fileName = cms.untracked.string('DataQCDChanSampleEle_146428_147116.root'),
#  fileName = cms.untracked.string('DataQCDChanSampleEle_147117_148058.root'),

    
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
#    'PathTSampleMuon',
    'PathTSampleElectronPFQCD',
    )
)
)


process.outpath = cms.EndPath(
    #process.tSampleMu + 
    #process.tSampleMuAntiIso  
    process.tSampleEleAntiIso +
    process.tSampleEle 
    )

