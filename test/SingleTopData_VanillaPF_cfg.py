import FWCore.ParameterSet.Config as cms

process = cms.Process("SingleTop")


process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    FailPath = cms.untracked.vstring('ProductNotFound','Type Mismatch')
    )


# conditions ------------------------------------------------------------------

print "test02 "

#process.load("Configuration.StandardSequences.MixingNoPileUp_cff")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff") ### real data

print "test03 "

#process.GlobalTag.globaltag = cms.string("GR_R_35X_V6::All")
#process.GlobalTag.globaltag = cms.string('GR_R_38X_V11::All') #TAG FOR  382
#process.GlobalTag.globaltag = cms.string("GR_R_38X_V11::All")
#process.GlobalTag.globaltag = cms.string("START311_V2::All")
process.GlobalTag.globaltag = cms.string('GR_R_311_V2::All')

print "test04 "

#from Configuration.PyReleaseValidation.autoCond import autoCond
#process.GlobalTag.globaltag = autoCond['startup']
process.load("TopQuarkAnalysis.SingleTop.SingleTopSequences_cff") 
process.load("SelectionCuts_top_group_control_samples_v3_cff")

print "test05 "

# set the dB to the beamspot
process.patMuons.usePV = cms.bool(False)
process.patElectrons.usePV = cms.bool(False)

print "test06 "

from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
from PhysicsTools.PatAlgos.tools.jetTools import *
from PhysicsTools.PatAlgos.tools.metTools import *
from PhysicsTools.PatAlgos.tools.coreTools import *

print "test0 "

#Path for the module that produces the tree for analysis 


#add ak5GenJets


print "test00 "


# set default collection
#switchJetCollection( process,
#                     jetCollection=cms.InputTag('ak5CaloJets'),
#                     jetCorrLabel=('AK5','Calo'),)# ['L2Relative', 'L3Absolute']))
# data: jetCorrLabel=('AK5Calo', ['L2Relative', 'L3Absolute', 'L2L3Residual']))


# Jet energy corrections to use: 
inputJetCorrLabel = ('AK5PF', ['L1Offset', 'L2Relative', 'L3Absolute', 'L2L3Residual'])

# add pf met
removeMCMatching(process, ['All'],"",False)



# Add PF jets
switchJetCollection(process,cms.InputTag('ak5PFJets'),
                 doJTA        = True,
                 doBTagging   = True,
                 jetCorrLabel = inputJetCorrLabel,
                 doType1MET   = True,
                 genJetCollection=cms.InputTag("ak5GenJets"),
                 doJetID      = True,
                 outputModule = "",   
                 ) 

process.patJets.addTagInfos = True
process.patJets.tagInfoSources  = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAOD"),
    )

# Apply loose PF jet ID
from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector
process.goodPatJets = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                   filterParams = pfJetIDSelector.clone(),
                                   src = cms.InputTag("selectedPatJets"),
                                   filter = cms.bool(True)
                                   )



# require physics declared
process.load('HLTrigger.special.hltPhysicsDeclared_cfi')
process.hltPhysicsDeclared.L1GtReadoutRecordTag = 'gtDigis'


print "test003"

# require scraping filter
process.scrapingVeto = cms.EDFilter("FilterOutScraping",
                                    applyfilter = cms.untracked.bool(True),
                                    debugOn = cms.untracked.bool(False),
                                    numtrack = cms.untracked.uint32(10),
                                    thresh = cms.untracked.double(0.2)
                                    )
# HB + HE noise filtering
process.load('CommonTools/RecoAlgos/HBHENoiseFilter_cfi')

#mytrigs=["HLT_Mu9"]
mytrigs=["*"]

from HLTrigger.HLTfilters.hltHighLevel_cfi import *
if mytrigs is not None :
    process.hltSelection = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths = mytrigs)
    process.hltSelection.throw = False


print "test000 "

# add JPT
process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
#process.load('RecoJets.Configuration.RecoJPTJets_cff')

#addJetCollection(process,cms.InputTag('JetPlusTrackZSPCorJetAntiKt5'),
#                                  'AK5', 'JPT',
#                                  doJTA        = True,
#                                  doBTagging   = True,
#                                  jetCorrLabel = ('AK5','JPT'),# cms.vstring(['L2Relative', 'L3Absolute'])),#('AK5','JPT'),
#                                  doType1MET   = False,
#                                  doL1Cleaning = False,
#                                  doL1Counters = True,
#                                  genJetCollection = cms.InputTag("ak5GenJets"),
#                                 doJetID      = True,
#                                  jetIdLabel   = "ak5"
#                                  )

addTcMET(process, 'TC')
addPfMET(process, 'PF')


print "test1 "


print "test2 "


print "test2.1 "




process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi")
#process.cFlavorHistoryProducer.matchedSrc = cms.InputTag("antikt5GenJets")
#process.bFlavorHistoryProducer.matchedSrc = cms.InputTag("antikt5GenJets")



# Taus are currently broken in 4.1.x
removeSpecificPATObjects( process, ['Taus'],False )
process.patDefaultSequence.remove( process.patTaus )
process.patDefaultSequence.remove( process.selectedPatTaus )
process.patDefaultSequence.remove( process.cleanPatTaus )


process.pathPreselection = cms.Path(

#    process.recoJPTJets +
    process.patElectronIDs +
    process.patDefaultSequence #+
#    process.PF2PAT
    )



#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring (

#    'file:/tmp/oiorio/F81B1889-AF4B-DF11-85D3-001A64789DF4.root'
#'rfio:/castor/cern.ch/user/g/giamman/singletop/sync/00012F91-72E5-DF11-A763-00261834B5F1.root'
'file:/tmp/oiorio/EC0EE286-FA55-E011-B99B-003048F024F6.root'
#'file:/tmp/oiorio/00012F91-72E5-DF11-A763-00261834B5F1.root'
#'file:/tmp/oiorio/F81B1889-AF4B-DF11-85D3-001A64789DF4.root'
#'rfio:    /castor/cern.ch/user/g/giamman/singletop/sync/F81B1889-AF4B-DF11-85D3-001A64789DF4.root',
#    'file:/tmp/oiorio/TChanFile2_1_1_L7h.root',
#    'file:/tmp/oiorio/TChanFile_1_1_xtA.root',
#    'file:/tmp/oiorio/EMEnrichedFile_1_1_CWt.root',
#   'file:/tmp/oiorio/WJets_File_Tauola_1_1_2nU.root',

),
duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)

#process.preselectedJets.src = cms.InputTag("patJetsAK5PF")
process.preselectedMETs.src = cms.InputTag("patMETsPF")

process.bJets.cut = cms.string('bDiscriminator("trackCountingHighPurBJetTags") < 3.41 && (bDiscriminator("trackCountingHighEffBJetTags") > 1.7 || abs(eta) >2.5)')#process.


print "test3 "

process.topJetsPF.ptCut = cms.untracked.double(20.)
process.topJetsAntiIsoPF.ptCut = cms.untracked.double(20.)



process.demo = cms.EDAnalyzer('SimpleEventDumper',                              
                              verticesSource = cms.InputTag("PVFilterProducer"),
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



process.WLightFilter = process.flavorHistoryFilter.clone(pathToSelect = cms.int32(11))
process.WccFlter = process.flavorHistoryFilter.clone(pathToSelect = cms.int32(6))
process.WbbFilter = process.flavorHistoryFilter.clone(pathToSelect = cms.int32(5))

#process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","REDIGI38X")
#process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","REDIGI37X")
#process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","REDIGI")
process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","HLT")
process.hltFilter.HLTPaths = mytrigs

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
    process.basePathData
    )

#Muon control samples

#process.PathTSampleMuonPF = cms.Path(
#    process.TSampleMuonPF *
#    process.nTuples *
#    process.demo
#    )

#process.PathTSampleMuonPF = cms.Path(
#    process.IsoMuonsSkimPF *
#    process.nTuplesSkim #*
#    process.demo
#    )

#process.PathTSampleMuonPFQCD = cms.Path(
#    process.AntiIsoMuonsSkimPF *
#    process.nTuplesAntiIsoSkim #*
#    process.demo
#    )

###Electron control samples

process.PathTSampleElectronPF = cms.Path(
    process.IsoElectronsSkimPF *
    #    process.TSampleElectronPF *
    process.nTuplesSkim #*
#    process.demo
    )


#process.PathTSampleElectronPFQCD = cms.Path(
#    process.AntiIsoElectronsSkimPF *
#    process.nTuplesAntiIsoSkim #*
#    process.demo
#)

#    process.TSampleElectronAntiIso *
#    process.QCDSampleElectron *
#    process.QCDSampleElectronPF *
#    process.PathElectronsAntiIso *
#    )
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import saveNTuplesSkimMu
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import saveNTuplesSkimEle
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import saveNTuplesSkimMuAntiIso
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import saveNTuplesSkimEleAntiIso


#saveNTuplesSkimMu.append("keep *_topJetsPF_*_*")





## Output module configuration
process.allControlSamples = cms.OutputModule("PoolOutputModule",
#                                fileName = cms.untracked.string('rfio:/CST/cern.ch/user/o/oiorio/SingleTop/SubSkims/WControlSamples1.root'),
                   fileName = cms.untracked.string('test.root'),
                                           
     outputCommands = saveNTuplesSkimMu,
)


process.tSampleMu =  process.allControlSamples.clone(
    fileName = cms.untracked.string('TSampleMuData.root'),
    
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
    'PathTSampleMuonPF',
#    'PathTSampleElectron',
    )
)
)


process.tSampleMuAntiIso =  process.allControlSamples.clone(
    fileName = cms.untracked.string('QCDSampleMuData.root'),
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
    'PathTSampleMuonPFQCD',
#    'PathTSampleElectron',
    )
    ),
    outputCommands = saveNTuplesSkimMuAntiIso,
)


process.tSampleEleAntiIso =  process.allControlSamples.clone(
    #    fileName = cms.untracked.string('QCDChanSampleEleCiso95.root'),
#    fileName = cms.untracked.string('QCDSampleEleQCDBCToE_Pt80to170.root'),
    fileName = cms.untracked.string('QCDSampleEleData.root'),
 
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
    'PathTSampleElectronPFQCD',
    )
  ),
                             
    outputCommands = saveNTuplesSkimEleAntiIso,
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
fileName = cms.untracked.string('TSampleEleData.root'),
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring(
#    'PathTSampleMuon',
    'PathTSampleElectronPF',
#    'PathWLight',
#    'PathWbb',
#    'PathWcc',
   )
),
    outputCommands = saveNTuplesSkimEle,

)
process.outpath = cms.EndPath(
#    process.tSampleMu #+ 
#    process.tSampleMuAntiIso + 
    process.tSampleEle #+
#    process.tSampleEleAntiIso 
    )

