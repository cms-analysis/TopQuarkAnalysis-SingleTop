import FWCore.ParameterSet.Config as cms

process = cms.Process("SingleTop")

## Load additional RECO config
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
#process.GlobalTag.globaltag = cms.string('START36_V9::All') #TAG FOR  Data 27May
#process.GlobalTag.globaltag = cms.string('START38_V10::All') #TAG FOR  Data 27May
#process.GlobalTag.globaltag = cms.string('GR_R_37X_V5A::All') #TAG FOR  Data 27May
process.GlobalTag.globaltag = cms.string('GR_R_38X_V11::All') #TAG FOR 382
process.load("Configuration.StandardSequences.MagneticField_cff")

process.load("TopQuarkAnalysis.SingleTop.SingleTopSequences_cff") 
process.load("SelectionCuts_top_group_control_samples_v3_cff")

from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
from PhysicsTools.PatAlgos.tools.jetTools import *
from PhysicsTools.PatAlgos.tools.metTools import *
from PhysicsTools.PatAlgos.tools.coreTools import *

#Path for the module that produces the tree for analysis 

# turn off MC matching for the process
removeMCMatching(process, ['All'])


#add ak5GenJets

process.load("RecoJets.Configuration.GenJetParticles_cff")
process.load("RecoJets.JetProducers.ak5GenJets_cfi")

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


#from PhysicsTools.PatAlgos.tools.cmsswVersionTools import *
#run36xOn35xInput(process)


process.pathPreselection = cms.Path(
    process.recoJPTJets +
    process.patDefaultSequence     )


#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring (

    'file:/tmp/oiorio/F81B1889-AF4B-DF11-85D3-001A64789DF4.root'

#'rfio:/castor/cern.ch/user/g/giamman/singletop/sync/F81B1889-AF4B-DF11-85D3-001A64789DF4.root',
#    'file:/tmp/oiorio/TChanFile2_1_1_L7h.root',
#    'file:/tmp/oiorio/TChanFile_1_1_xtA.root',
#    'file:/tmp/oiorio/EMEnrichedFile_1_1_CWt.root',
#   'file:/tmp/oiorio/WJets_File_Tauola_1_1_2nU.root',

),
duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    FailPath = cms.untracked.vstring('ProductNotFound','Type Mismatch')
    )

process.preselectedJets.src = cms.InputTag("patJetsAK5JPT")
process.preselectedMETs.src = cms.InputTag("patMETsTC")

process.bJets.cut = cms.string('bDiscriminator("trackCountingHighPurBJetTags") < 3.41 && (bDiscriminator("trackCountingHighEffBJetTags") > 1.7 || abs(eta) >2.5)')#process.


process.bJetsPF.cut = cms.string('')
process.forwardJetsPF.cut = cms.string('')

process.bJetsAntiIsoPF.cut = cms.string('')
process.forwardJetsAntiIsoPF.cut = cms.string('')

process.countBTagsPF.minNumber = cms.uint32(0)
process.countBTagsPF.maxNumber = cms.uint32(15)
process.countForwardJetsPF.minNumber = cms.uint32(0)
process.countForwardJetsPF.maxNumber = cms.uint32(15)
process.countJetsPF.minNumber = cms.uint32(0)
process.countJetsPF.maxNumber = cms.uint32(15)

process.countBTagsAntiIsoPF.minNumber = cms.uint32(0)
process.countBTagsAntiIsoPF.maxNumber = cms.uint32(15)
process.countForwardJetsAntiIsoPF.minNumber = cms.uint32(0)
process.countForwardJetsAntiIsoPF.maxNumber = cms.uint32(15)
process.countJetsAntiIsoPF.minNumber = cms.uint32(0)
process.countJetsAntiIsoPF.maxNumber = cms.uint32(15)

#process.topMuons.jetsSrc = cms.InputTag("topJets")
process.topMuons.useJetVeto = cms.untracked.bool(False)
process.topJetsPF.ptCut = cms.untracked.double(20.)
process.topJetsAntiIsoPF.ptCut = cms.untracked.double(20.)



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

process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi")
#process.cFlavorHistoryProducer.matchedSrc = cms.InputTag("antikt5GenJets")
#process.bFlavorHistoryProducer.matchedSrc = cms.InputTag("antikt5GenJets")

process.PathFlavor = cms.Path(
    process.genParticlesForJets *
    process.ak5GenJets *
    process.cFlavorHistoryProducer *
    process.bFlavorHistoryProducer
    )


process.WLightFilter = process.flavorHistoryFilter.clone(pathToSelect = cms.int32(11))
process.WccFlter = process.flavorHistoryFilter.clone(pathToSelect = cms.int32(6))
process.WbbFilter = process.flavorHistoryFilter.clone(pathToSelect = cms.int32(5))

process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","REDIGI38X")
#process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","REDIGI37X")
#process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","REDIGI")
#process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","HLT")

#process.bJetsPF = cms.EDProducer("SingleTopBJetsProducer",
#                               src = cms.InputTag("topJetsPF"),
##                               bThreshold = cms.untracked.double(-999),
#                               veto = cms.untracked.bool(False),
#                               )

#process.forwardJetsPF = cms.EDProducer("SingleTopBJetsProducer",
#                               src = cms.InputTag("topJetsPF"),
# #                              bThreshold = cms.untracked.double(-999),
#                               veto = cms.untracked.bool(True),
#                               )

#part for W + jets
#process.PathWLight = cms.Path(
#    process.WLightFilter 
#    )
#
#process.PathWcc = cms.Path(
#    process.WccFlter 
#    )

#process.PathWbb = cms.Path(
#    process.WbbFilter 
#    )

#process.countJetsNonTTBarAntiIso.minNumber = cms.uint32(0)

process.baseLeptonSequence = cms.Path(
    process.basePath
    )

#Muon control samples

process.PathTSampleMuonPF = cms.Path(
    process.TSampleMuonPF *
    process.nTuples *
    process.demo
    )

#process.PathTSampleMuon = cms.Path(
#    process.TSampleMuon *
#    process.nTuples *
#    process.demo
#    )

process.PathTSampleMuonPFQCD = cms.Path(
    process.QCDSampleMuonPF *
    process.nTuplesAntiIso *
    process.demo
    )

###Electron control samples

process.PathTSampleElectronPF = cms.Path(
    process.TSampleElectronPF *
    process.nTuples *
    process.demo
    )


process.PathTSampleElectronPFQCD = cms.Path(
#    process.TSampleElectronAntiIso *
#    process.QCDSampleElectron *
    process.QCDSampleElectronPF *
#    process.PathElectronsAntiIso *
    process.nTuplesAntiIso *
    process.demo
    )
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import saveNTuplesMu
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import saveNTuplesEle

from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import saveNTuplesMuAntiIso
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import saveNTuplesEleAntiIso




## Output module configuration
process.allControlSamples = cms.OutputModule("PoolOutputModule",
#                                fileName = cms.untracked.string('rfio:/CST/cern.ch/user/o/oiorio/SingleTop/SubSkims/WControlSamples1.root'),
                   fileName = cms.untracked.string('test.root'),
                                           

     outputCommands = saveNTuplesMu,
#                                             cms.untracked.vstring(
 #   'drop *',


#    'keep *_patMETsPFlow_*_*',
#    'keep *_patMETsTC_*_*',
#    'keep *_patMETsPF_*_*',

    #    'keep *_patJetsPF_*_*',
#    'keep *_patJetsPF_*_*',
#    'keep *_cleanPatJets_*_*',
#    'keep *_patElectronsPFlow_*_*',
#    'keep *_patMuonsPFlow_*_*',
#Skimmed collections

#    'keep *_TriggerResults_*_*',

#Skimmed collections

###############TOADD
#    'keep *_topMuons_*_*',
#    'keep *_topElectrons_*_*',#
#
#   'keep *_topMuonsAntiIso_*_*',
#    'keep *_topElectronsAntiIso_*_*',

    
#    'keep *_cFlavorHistoryProducer_*_*',
#    'keep *_bFlavorHistoryProducer_*_*',

#    'keep *_boostedEventsPF_*_*',
#    'keep *_boostedEventsAntiIsoPF_*_*',

#Fixme JUST TO KEEP REASONABLE SIZE

#########TOADD
#    'keep *_topJetsAntiIsoPF_*_*',
#    'keep *_topJets_*_*',


#    'keep *_topJetsPF_*_*',
#    'keep *_bJetsPF_*_*',
#    'keep *_forwardJetsPF_*_*',
#    'keep *_bJetsAntiIsoPF_*_*',
#    'keep *_forwardJetsAntiIsoPF_*_*',
#########

#    'keep recoNamedCompositeCandidates_recoTopsPF_*_*',
#    'keep recoNamedCompositeCandidates_recoTopsAntiIsoPF_*_*',


#    'keep *_preselectedMETs_*_*',
#    'keep *_preselectedJets_*_*',
#    'keep *_cFlavorHistoryProducer_*_*',
#    'keep *_bFlavorHistoryProducer_*_*',


#    'keep *_singleTopObservablesTSamplePF_*_*',    
#    'keep floats_nTupleEventsPF_*_*',
#    'keep floats_nTuplePatMETsPF_*_*',
#    'keep floats_nTupleTopJetsPF_*_*',
#    'keep floats_nTupleBJetsPF_*_*',
#    'keep floats_nTupleForwardJetsPF_*_*',
    
#    'keep *_singleTopObservablesWSample_*_*',    
#    'keep *_singleTopObservablesTTBarSample_*_*',    
#    'keep *_singleTopObservablesAntiIso_*_*',    
#    'keep *_singleTopObservablesWSampleAntiIso_*_*',    


#MC Info
 #'keep *_generator_*_*',  
#    'keep *_genEventWeight_*_*',  
#    'keep GenEventInfoProduct_*_*_*',  
#    'keep *_MCTruthParticles_*_*',

  #  )

)


process.tSampleMu =  process.allControlSamples.clone(
    fileName = cms.untracked.string('TSampleMuQCDMu.root'),
    
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
    'PathTSampleMuonPF',
#    'PathTSampleElectron',
    )
)
)


process.tSampleMuAntiIso =  process.allControlSamples.clone(
    fileName = cms.untracked.string('QCDSampleMuQCDMu.root'),
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
    'PathTSampleMuonPFQCD',
#    'PathTSampleElectron',
    )
    ),
    outputCommands = saveNTuplesMuAntiIso
)


process.tSampleEleAntiIso =  process.allControlSamples.clone(
    #    fileName = cms.untracked.string('QCDChanSampleEleCiso95.root'),
#    fileName = cms.untracked.string('QCDSampleEleQCDBCToE_Pt80to170.root'),
    fileName = cms.untracked.string('QCDSampleEleQCDMu.root'),
 
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
    'PathTSampleElectronPFQCD',
    )
  ),
                             
    outputCommands = saveNTuplesEleAntiIso,
    #cms.untracked.vstring(
    #'drop *',#

#    'keep *_cFlavorHistoryProducer_*_*',
#    'keep *_bFlavorHistoryProducer_*_*',#

#    'keep *_singleTopObservablesAntiIsoPF_*_*',
#    'keep floats_nTupleEventsAntiIsoPF_*_*',
#    'keep floats_nTuplePatMETsPF_*_*',
#    'keep floats_nTupleTopJetsPF_*_*',
#    ),

)

process.tSampleEle =  process.allControlSamples.clone(
#    fileName = cms.untracked.string('QCDChanSampleEleCiso95.root'),
fileName = cms.untracked.string('TSampleEleQCDMu.root'),
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
#    'PathTSampleMuon',
    'PathTSampleElectronPF',
#    'PathWLight',
#    'PathWbb',
#    'PathWcc',
   )
),
    outputCommands = saveNTuplesEle,

)
process.outpath = cms.EndPath(
    process.tSampleMu + 
    process.tSampleMuAntiIso #+ 
#    process.tSampleEle +
#    process.tSampleEleAntiIso 
    )

