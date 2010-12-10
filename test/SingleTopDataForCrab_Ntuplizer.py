import FWCore.ParameterSet.Config as cms

process = cms.Process("SingleTop")

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    FailPath = cms.untracked.vstring('ProductNotFound','Type Mismatch')
    )


# conditions ------------------------------------------------------------------

process.load("Configuration.StandardSequences.MixingNoPileUp_cff")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff") ### real data
#process.GlobalTag.globaltag = cms.string("GR_R_35X_V6::All")
#process.GlobalTag.globaltag = cms.string('GR_R_38X_V11::All') #TAG FOR  382
#process.GlobalTag.globaltag = cms.string("GR_R_38X_V11::All")
from Configuration.PyReleaseValidation.autoCond import autoCond
process.GlobalTag.globaltag = autoCond['startup']



process.load("TopQuarkAnalysis.SingleTop.SingleTopSequences_cff") 
process.load("SelectionCuts_top_group_control_samples_v3_cff")



# set the dB to the beamspot
process.patMuons.usePV = cms.bool(False)
process.patElectrons.usePV = cms.bool(False)


from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
from PhysicsTools.PatAlgos.tools.jetTools import *
from PhysicsTools.PatAlgos.tools.metTools import *
from PhysicsTools.PatAlgos.tools.coreTools import *

print "test0 "

#Path for the module that produces the tree for analysis 


#add ak5GenJets

process.load("RecoJets.Configuration.GenJetParticles_cff")
process.load("RecoJets.JetProducers.ak5GenJets_cfi")



# set default collection
switchJetCollection( process,
                     jetCollection=cms.InputTag('ak5CaloJets'),
###MC:                     jetCorrLabel=('AK5Calo', ['L2Relative', 'L3Absolute']))
                     jetCorrLabel=('AK5Calo', ['L2Relative', 'L3Absolute', 'L2L3Residual']))

# turn off MC matching for the process
removeMCMatching(process, ['All'],"",False)

#from PhysicsTools.PatAlgos.tools.cmsswVersionTools import *
#run36xOn35xInput(process)

# add PF
addJetCollection(process,
                   cms.InputTag('ak5PFJets'),
                   'AK5',
                   'PF',
                   doJTA=True,
                   doBTagging=True,
                   jetCorrLabel=('AK5PF', cms.vstring(['L2Relative', 'L3Absolute'])),#('AK5','PF'),
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
                                  jetCorrLabel = ('AK5JPT', cms.vstring(['L2Relative', 'L3Absolute'])),#('AK5','JPT'),
                                  doType1MET   = False,
                                  doL1Cleaning = False,
                                  doL1Counters = True,
                                  genJetCollection = cms.InputTag("ak5GenJets"),
                                  doJetID      = True,
                                  jetIdLabel   = "ak5"
                                  )


addTcMET(process, 'TC')
addPfMET(process, 'PF')

############################

process.pathPreselection = cms.Path(
    process.patElectronIDs +
    process.patDefaultSequence 
    )


#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1065) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring (

    'file:/tmp/oiorio/94659715-5F91-DF11-BBCD-001D09F2AF96.root'
#'rfio:/castor/cern.ch/cms/store/data/Run2010A/Mu/RECO/v4/000/140/331/94659715-5F91-DF11-BBCD-001D09F2AF96.root'

#    'file:/tmp/oiorio/3C6D0701-4AA0-DF11-8437-0030487CD184.root',

#    'rfio:/castor/cern.ch/user/o/oiorio/SingleTop/Candidates/Event_142928_446_107153746.root'
    #'rfio:/castor/cern.ch/cms/store/data/Run2010A/EG/RECO/v4/000/142/311/3C6D0701-4AA0-DF11-8437-0030487CD184.root',

#'rfio:/castor/cern.ch/user/g/giamman/singletop/sync/F81B1889-AF4B-DF11-85D3-001A64789DF4.root',


),
duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
#eventsToProcess = cms.untracked.VEventRange("140331:257717658-140331:1257717800"),
)

process.preselectedElectrons.isData = cms.untracked.bool(True)
process.topElectrons.isData = cms.untracked.bool(True)
#process.topElectronsPF.isData = cms.untracked.bool(True)

#process.electronIDIso.isData = cms.untracked.bool(True)
#process.electronIDAntiIso.isData = cms.untracked.bool(True)


process.preselectedJets.src = cms.InputTag("patJetsAK5JPT")


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

#
process.topMuons.useJetVeto = cms.untracked.bool(False)
process.topJetsPF.ptCut = cms.untracked.double(20.)
process.topJetsAntiIsoPF.ptCut = cms.untracked.double(20.)


process.singleTopObservablesTSamplePF = cms.EDProducer(
    'TopCosThetaStarDumperData',
    jetsSource = cms.InputTag('boostedForwardJetsPF'), 
    topsSource = cms.InputTag('boostedTopsPF'), 
    tChanSource = cms.InputTag('recoTChanEventsPF'),
    )


process.singleTopObservablesAntiIso = process.singleTopObservablesTSamplePF.clone(
    jetsSource = cms.InputTag('boostedForwardJetsAntiIsoTops'),
    topsSource = cms.InputTag('boostedTopsAntiIsoTops'),
    tChanSource = cms.InputTag('recoTChanEventsAntiIso'), 
   
    )



# good vertices
process.PVFilter.cut = cms.string("!isFake && ndof > 4 && abs(z) <= 24 && position.Rho <= 2")

process.demo = cms.EDAnalyzer('SimpleEventDumper',
#                              verticesSource = cms.InputTag("PVFilter"),
                              verticesSource = cms.InputTag("offlinePrimaryVertices"),
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
process.hltFilter.HLTPaths = ['HLT_Mu9']

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

process.PathTSampleMuonPF = cms.Path(
    process.TSampleMuonPF *
    process.nTuples *
    process.demo
    )

process.PathTSampleMuonPFQCD = cms.Path(
    process.QCDSampleMuonPF *
    process.nTuplesAntiIso *
    process.demo
    )

###Electron control samples

#process.PathTSampleElectronPF = cms.Path(
#    process.hltFilterPhoton20 *
#    process.hltFilterSummary *
#    process.TSampleElectronPF *
#    process.nTuples *
#    process.demo
#    )

#process.PathTSampleElectronPFQCD = cms.Path(
#    process.hltFilterPhoton20 *
#    process.hltFilterSummary *
#    process.QCDSampleElectronPF *
#    process.nTuplesAntiIso *
#    process.demo
#    )


#process.PathTSampleElectronPFQCD = cms.Path(
#    process.TSampleElectronAntiIso *
#    process.QCDSampleElectron *
#    process.QCDSampleElectronPF *
#    process.PathElectronsAntiIso *
#    process.demo
#    )


from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import saveNTuplesMu
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import saveNTuplesEle
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import saveNTuplesMuAntiIso
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import saveNTuplesEleAntiIso


## Output module configuration
process.allControlSamples = cms.OutputModule("PoolOutputModule",
#                                fileName = cms.untracked.string('rfio:/CST/cern.ch/user/o/oiorio/SingleTop/SubSkims/WControlSamples1.root'),
                   fileName = cms.untracked.string('test.root'),
                                           
     outputCommands = saveNTuplesMu,
)


process.tSampleMu =  process.allControlSamples.clone(
#    fileName = cms.untracked.string('DataTChanSampleMu_144115_147195.root'),
#    fileName = cms.untracked.string('DataTChanSampleMu_145762_147196.root'),
#    fileName = cms.untracked.string('DataTChanSampleMu_147196_148058.root'),
    fileName = cms.untracked.string('DataTChanSampleMu_132440_144114.root'),

    outputCommands = saveNTuplesMu,
                                    
 
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
    'PathTSampleMuonPF',
#    'PathTSampleElectron',
    )


)
)

process.tSampleMuAntiIso =  process.allControlSamples.clone(
#    fileName = cms.untracked.string('DataQCDChanSampleMu_147196_149442.root'),
#    fileName = cms.untracked.string('DataQCDChanSampleMu_144115_147195.root'),
#    fileName = cms.untracked.string('DataQCDChanSampleMu_145762_147196.root'),
#    fileName = cms.untracked.string('DataQCDChanSampleMu_147196_148058.root'),
    fileName = cms.untracked.string('DataQCDChanSampleMu_132440_144114.root'),
    outputCommands = saveNTuplesMuAntiIso,
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
    'PathTSampleMuonPFQCD',
    #    'PathTSampleElectron',
    )
                                         ),
)

process.tSampleEle =  process.allControlSamples.clone( 
#    fileName = cms.untracked.string('DataTChanSampleEle_132440_140040.root'),
    fileName = cms.untracked.string('DataTChanSampleEle_132440_140040.root'),
#    fileName = cms.untracked.string('DataTChanSampleEle_143963_146427.root'),
#    fileName = cms.untracked.string('DataTChanSampleEle_146428_147116.root'),
#    fileName = cms.untracked.string('DataTChanSampleEle_147117_148058.root'),
    outputCommands = saveNTuplesEle,
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

  outputCommands = saveNTuplesEleAntiIso,
  SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
#    'PathTSampleMuon',
    'PathTSampleElectronPFQCD',
    )
                                      ),
)


process.outpath = cms.EndPath(
    process.tSampleMu + 
    process.tSampleMuAntiIso  
#    process.tSampleEleAntiIso +
#    process.tSampleEle 
    )

