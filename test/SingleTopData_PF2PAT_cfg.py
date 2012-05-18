import FWCore.ParameterSet.Config as cms

process = cms.Process("SingleTop")

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    FailPath = cms.untracked.vstring('ProductNotFound','Type Mismatch')
    )

#process.MessageLogger.cerr.FwkReport.reportEvery = 100

#from PhysicsTools.PatAlgos.tools.cmsswVersionTools import run36xOn35xInput


# conditions ------------------------------------------------------------------

print "test "

#process.load("Configuration.StandardSequences.MixingNoPileUp_cff")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff") ### real data

ChannelName = "Data"

process.GlobalTag.globaltag = cms.string('GR_R_52_V7::All')
#process.GlobalTag.globaltag = cms.string('START311_V2::All')

#from Configuration.PyReleaseValidation.autoCond import autoCond
#process.GlobalTag.globaltag = autoCond['startup']
process.load("TopQuarkAnalysis.SingleTop.SingleTopSequences_cff") 
process.load("SelectionCuts_Skim_cff")################<----------

#From <<ysicsTools.PatAlgos.tools.cmsswVersionTools import *
#run42xOn3yzMcInput(process)
#run36xOn35xInput(process)
#process.load("PhysicsTools.PatAlgos.patSequences_cff")

# Get a list of good primary vertices, in 42x, these are DAF vertices
from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
process.goodOfflinePrimaryVertices = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams = pvSelector.clone( minNdof = cms.double(4.0), maxZ = cms.double(24.0) ),
    src=cms.InputTag('offlinePrimaryVertices')
    )

# require physics declared
#process.load('HLTrigger.special.hltPhysicsDeclared_cfi')
#process.hltPhysicsDeclared.L1GtReadoutRecordTag = 'gtDigis'

#dummy output

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('dummy.root'),
                               outputCommands = cms.untracked.vstring(""),
                               )

#mytrigs=["HLT_Mu9"]
mytrigs=["*"]
print "test2"
from HLTrigger.HLTfilters.hltHighLevel_cfi import *
#if mytrigs is not None :
#    process.hltSelection = hltHighLevel.clone(TriggerResultsTag = 'TriggerResults::HLT', HLTPaths = mytrigs)
#    process.hltSelection.throw = False

#
#    getattr(process,"pfNoElectron"+postfix)*process.kt6PFJets 

                                 

# set the dB to the beamspot
process.patMuons.usePV = cms.bool(False)
process.patElectrons.usePV = cms.bool(False)

print "test2.1"
jetCorrections=['L1FastJet','L2Relative','L3Absolute','L2L3Residual']
  
# Configure PAT to use PF2PAT instead of AOD sources
# this function will modify the PAT sequences. It is currently 
# not possible to run PF2PAT+PAT and standart PAT at the same time
from PhysicsTools.PatAlgos.tools.pfTools import *
Postfix = ""
postfix = ""
runOnMC = False
jetAlgoName = "AK5"
print "test2.2"
usePF2PAT(process, runPF2PAT=True, jetAlgo=jetAlgoName, runOnMC=runOnMC, postfix=Postfix,jetCorrections=('AK5PFchs', jetCorrections),outputModules = None)
process.pfPileUp.Enable = True
print "test2.3"
process.pfPileUp.checkClosestZVertex = cms.bool(False)
process.pfPileUp.Vertices = cms.InputTag('goodOfflinePrimaryVertices')
process.pfJets.doAreaFastjet = True
process.pfJets.doRhoFastjet = False


#process.pfJets.Rho_EtaMax =  cms.double(4.4)


#Compute the mean pt per unit area (rho) from the
#PFchs inputs
from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
process.kt6PFJets = kt4PFJets.clone(
    rParam = cms.double(0.6),
    src = cms.InputTag('pfNoElectron'+postfix),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True),
#    voronoiRfact = cms.double(0.9),
#    Rho_EtaMax =  cms.double(4.4)
    )


print "test3"


process.patJetCorrFactors.rho = cms.InputTag("kt6PFJets", "rho")

coneOpening = cms.double(0.4)
defaultIsolationCut = cms.double(0.2)

#coneOpening = process.coneOpening
#defaultIsolationCut = process.coneOpening

#Muons
#applyPostfix(process,"isoValMuonWithNeutral",postfix).deposits[0].deltaR = coneOpening
#applyPostfix(process,"isoValMuonWithCharged",postfix).deposits[0].deltaR = coneOpening
#applyPostfix(process,"isoValMuonWithPhotons",postfix).deposits[0].deltaR = coneOpening
##electrons
process.pfIsolatedElectrons.isolationValueMapsCharged = cms.VInputTag( cms.InputTag("elPFIsoValueCharged03PFId"),    )
process.pfIsolatedElectrons.isolationValueMapsNeutral = cms.VInputTag( cms.InputTag("elPFIsoValueNeutral03PFId"),  cms.InputTag("elPFIsoValueGamma03PFId")  )
process.pfIsolatedElectrons.deltaBetaIsolationValueMap = cms.InputTag("elPFIsoValuePU03PFId")
#applyPostfix(process,"isoValElectronWithNeutral",postfix).deposits[0].deltaR = coneOpening
#applyPostfix(process,"isoValElectronWithCharged",postfix).deposits[0].deltaR = coneOpening
#applyPostfix(process,"isoValElectronWithPhotons",postfix).deposits[0].deltaR = coneOpening
#
#applyPostfix(process,"pfIsolatedMuons",postfix).combinedIsolationCut = defaultIsolationCut
#applyPostfix(process,"pfIsolatedElectrons",postfix).combinedIsolationCut = defaultIsolationCut

#applyPostfix(process,"pfIsolatedMuons",postfix).combinedIsolationCut = cms.double(0.125)
#applyPostfix(process,"pfIsolatedElectrons",postfix).combinedIsolationCut = cms.double(0.125)

#postfixQCD = "ZeroIso"


print "test4"

# Add the PV selector and KT6 producer to the sequence
getattr(process,"patPF2PATSequence"+postfix).replace(
    getattr(process,"pfNoElectron"+postfix),
    getattr(process,"pfNoElectron"+postfix)*process.kt6PFJets )

#Residuals (Data)
#process.patPFJetMETtype1p2Corr.jetCorrLabel = 'L2L3Residual'

process.patseq = cms.Sequence(
#    process.patElectronIDs +
    process.goodOfflinePrimaryVertices *
    process.patElectronIDs *
    getattr(process,"patPF2PATSequence"+postfix) #*
#    process.producePatPFMETCorrections
#    getattr(process,"patPF2PATSequence"+postfixQCD) 
    )


process.pfIsolatedMuonsZeroIso = process.pfIsolatedMuons.clone(combinedIsolationCut =  cms.double(float("inf")))
process.patMuonsZeroIso = process.patMuons.clone(pfMuonSource = cms.InputTag("pfIsolatedMuonsZeroIso"), genParticleMatch = cms.InputTag("muonMatchZeroIso"))
# use pf isolation, but do not change matching
tmp = process.muonMatch.src
adaptPFMuons(process, process.patMuonsZeroIso, "")
process.muonMatch.src = tmp
process.muonMatchZeroIso = process.muonMatch.clone(src = cms.InputTag("pfIsolatedMuonsZeroIso"))

process.pfIsolatedElectronsZeroIso = process.pfIsolatedElectrons.clone(combinedIsolationCut = cms.double(float("inf")))
process.patElectronsZeroIso = process.patElectrons.clone(pfElectronSource = cms.InputTag("pfIsolatedElectronsZeroIso"))
#adaptPFElectrons(process, process.patElectronsZeroIso, "")

#Add the PF type 1 corrections to MET
#process.load("PhysicsTools.PatUtils.patPFMETCorrections_cff")
#process.selectedPatJetsForMETtype1p2Corr.src = cms.InputTag('selectedPatJets')
#process.selectedPatJetsForMETtype2Corr.src = cms.InputTag('selectedPatJets')
#process.patPFJetMETtype1p2Corr.type1JetPtThreshold = cms.double(10.0)
#process.patPFJetMETtype1p2Corr.skipEM = cms.bool(False)
#process.patPFJetMETtype1p2Corr.skipMuons = cms.bool(False)

#process.patPF2PATSequence.remove(process.patPF2PATSequence.FastjetJetProducer)

process.pathPreselection = cms.Path(
        process.patseq #+  process.producePatPFMETCorrections
        )


process.ZeroIsoLeptonSequence = cms.Path(
         process.pfIsolatedMuonsZeroIso +
#         process.muonMatchZeroIso +
         process.patMuonsZeroIso +
         process.pfIsolatedElectronsZeroIso +
         process.patElectronsZeroIso
         )

#process.looseLeptonSequence.remove(process.muonMatchLoose)



#getattr(process,"pfNoPileUp"+postfix).enable = True
#getattr(process,"pfNoMuon"+postfix).enable = True
#getattr(process,"pfNoElectron"+postfix).enable = True
#getattr(process,"pfNoTau"+postfix).enable = False
#Getattr (process,"pfNoJet"+postfix).enable = True 



process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring (
#'file:/tmp/oiorio/2E336374-1286-E111-AB01-001D09F24D67.root',
'file:/tmp/oiorio/SingleEle.root',
#'/tmp/oiorio/SingleMu.root',
#'file:/tmp/oiorio/FE4EF257-A3AB-E011-9698-00304867915A.root',
#'file:/tmp/oiorio/50A31B1A-8AAB-E011-835B-0026189438F5.root'
#'file:/tmp/oiorio/WJetsSmallFile_1_1_nb1.root',
#'file:/tmp/oiorio/00012F91-72E5-DF11-A763-00261834B5F1.root',
),
duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)


#process.TFileService = cms.Service("TFileService", fileName = cms.string("/tmp/oiorio/"+ChannelName+"_pt_bmode.root"))
#process.TFileService = cms.Service("TFileService", fileName = cms.string("pileupdistr_"+ChannelName+".root"))

#process.pileUpDumper = cms.EDAnalyzer("SingleTopPileUpDumper",
#                                      channel = cms.string(ChannelName),
#                                      )


#process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","REDIGI38X")
#process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","REDIGI37X")
#process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","REDIGI")
#process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","REDIGI311X")
#process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","HLT")
#process.hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","HLT")
#process.hltFilter.HLTPaths = mytrigs
    
    
#process.countLeptons.doQCD = cms.untracked.bool(False)

process.baseLeptonSequence = cms.Path(
#    process.pileUpDumper +
    process.basePathData
    )
#    
process.selection = cms.Path (
    process.preselection +
    process.nTuplesSkim
    )
    
        
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import saveNTuplesSkimLoose
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import saveNTuplesSkimMu
    
savePatTupleSkimLoose = cms.untracked.vstring(
    'drop *',

    'keep patMuons_selectedPatMuons_*_*',
    'keep patElectrons_selectedPatElectrons_*_*',
    'keep patJets_selectedPatJets_*_*',
    'keep patMETs_patMETs_*_*',
    'keep *_patPFMet_*_*',
    'keep *_patType1CorrectedPFMet_*_*',
    'keep *_PVFilterProducer_*_*',

    'keep patJets_topJetsPF_*_*',
    'keep patMuons_looseMuons_*_*',
    'keep *_looseElectrons_*_*',
    'keep patMuons_tightMuons_*_*',
    'keep *_tightElectrons_*_*',

    'keep *_PDFInfo_*_*',

    'keep *_patElectronsZeroIso_*_*',
    'keep *_patMuonsZeroIso_*_*',
    'keep *_kt6PFJetsCentral_*_*',
    'keep *_PVFilterProducer_*_*',
    
    'keep *_cFlavorHistoryProducer_*_*',
    'keep *_bFlavorHistoryProducer_*_*',
    )

## Output module configuration
process.singleTopNTuple = cms.OutputModule("PoolOutputModule",
#                                fileName = cms.untracked.string('rfio:/CST/cern.ch/user/o/oiorio/SingleTop/SubSkims/WControlSamples1.root'),
#                   fileName = cms.untracked.Bstring('/tmp/oiorio/edmntuple_tchannel_big.root'),
                   fileName = cms.untracked.string('/tmp/oiorio/edmntuple_'+ChannelName+'.root'),
                                             
#                   SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('selection')),
                   outputCommands = saveNTuplesSkimLoose,
)

process.singleTopPatTuple = cms.OutputModule("PoolOutputModule",
#                                fileName = cms.untracked.string('rfio:/CST/cern.ch/user/o/oiorio/SingleTop/SubSkims/WControlSamples1.root'),
                   fileName = cms.untracked.string('/tmp/oiorio/pattuple_'+ChannelName+'.root'),


#                   SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('selection')),
                   outputCommands = savePatTupleSkimLoose
)
process.singleTopNTuple.dropMetaData = cms.untracked.string("ALL")

process.outpath = cms.EndPath(
   process.singleTopNTuple +
   process.singleTopPatTuple 
    )

