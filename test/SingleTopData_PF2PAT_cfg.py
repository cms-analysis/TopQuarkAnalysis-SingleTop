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

process.load("TopQuarkAnalysis.SingleTop.SingleTopSequences_cff") 
process.load("SelectionCuts_Skim_cff")################<----------

# Get a list of good primary vertices, in 42x, these are DAF vertices
from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
process.goodOfflinePrimaryVertices = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams = pvSelector.clone( minNdof = cms.double(4.0), maxZ = cms.double(24.0), maxRho = cms.double(2.)  ),
    src=cms.InputTag('offlinePrimaryVertices')
    )

process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('dummy.root'),
                               outputCommands = cms.untracked.vstring(""),
                               )

jetCorrections=['L1FastJet','L2Relative','L3Absolute','L2L3Residual']

postfix = ""

#Compute the mean pt per unit area (rho) from the
#PFchs inputs
from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
process.kt6PFJets = kt4PFJets.clone(
    rParam = cms.double(0.6),
    src = cms.InputTag('pfNoElectron'+postfix),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True),
    )

# Configure PAT to use PF2PAT instead of AOD sources
# this function will modify the PAT sequences. It is currently 
# not possible to run PF2PAT+PAT and standart PAT at the same time
from PhysicsTools.PatAlgos.tools.pfTools import *
Postfix = ""
runOnMC = False
jetAlgoName = "AK5"
usePF2PAT(process, runPF2PAT=True, jetAlgo=jetAlgoName, runOnMC=runOnMC, postfix=Postfix,jetCorrections=('AK5PFchs', jetCorrections),outputModules = None)

process.patElectrons.useParticleFlow = False
process.eleIsoSequence = setupPFElectronIso(process, 'gsfElectrons', "PFIso"+postfix)
adaptPFIsoElectrons( process, process.patElectrons, "PFIso"+postfix)
getattr(process,'patDefaultSequence'+postfix).replace( getattr(process,"patElectrons"+postfix),
                                                       process.pfParticleSelectionSequence +
                                                       process.eleIsoSequence +
                                                       getattr(process,"patElectrons"+postfix)
                                                       )
           
#useGsfElectrons(process,postfix)

#process.pfPileUp.Enable = True
#process.pfPileUp.checkClosestZVertex = cms.bool(False)
#process.pfPileUp.Vertices = cms.InputTag('goodOfflinePrimaryVertices')
#process.pfJets.doAreaFastjet = True
#process.pfJets.doRhoFastjet = False

# set the dB to the beamspot
process.patMuons.usePV = cms.bool(False)
process.patElectrons.usePV = cms.bool(False)



#Muons

#Electrons
process.pfIsolatedElectrons.isolationValueMapsCharged = cms.VInputTag( cms.InputTag("elPFIsoValueCharged03PFId"),    )
process.pfIsolatedElectrons.isolationValueMapsNeutral = cms.VInputTag( cms.InputTag("elPFIsoValueNeutral03PFId"),  cms.InputTag("elPFIsoValueGamma03PFId")  )
process.pfIsolatedElectrons.deltaBetaIsolationValueMap = cms.InputTag("elPFIsoValuePU03PFId")


print "test4"

#Residuals (Data)
print "test5"

process.patseq = cms.Sequence(
#  process.patElectronIDs +
    process.goodOfflinePrimaryVertices *
    process.patElectronIDs *
    getattr(process,"patPF2PATSequence"+postfix) #*
#    patPF2PATSequence
#    process.producePatPFMETCorrections
#    getattr(process,"patPF2PATSequence"+postfixQCD) 
    )

print "test6"

process.pfIsolatedMuonsZeroIso = process.pfIsolatedMuons.clone(combinedIsolationCut =  cms.double(float("inf")))
process.patMuonsZeroIso = process.patMuons.clone(pfMuonSource = cms.InputTag("pfIsolatedMuonsZeroIso"))#, genParticleMatch = cms.InputTag("muonMatchZeroIso"))
# use pf isolation, but do not change matching
#tmp = process.muonMatch.src
#adaptPFMuons(process, process.patMuonsZeroIso, "")
print "test7"
#process.muonMatch.src = tmp
#process.muonMatchZeroIso = process.muonMatch.clone(src = cms.InputTag("pfIsolatedMuonsZeroIso"))
print "test8"


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

getattr(process,"pfNoTau"+postfix).enable = False


process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring (
#"rfio:/castor/cern.ch/user/o/oiorio/SingleTop/2012/MC2012/Synch/Data/SingleMu.root",
"rfio:/castor/cern.ch/user/o/oiorio/SingleTop/2012/MC2012/Synch/Data/SingleEle.root"
),
duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)


process.countLeptons.doQCD = cms.untracked.bool(False)

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

