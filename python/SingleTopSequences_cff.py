import FWCore.ParameterSet.Config as cms

from TopQuarkAnalysis.SingleTop.SelectionCuts_Skim_cff import *

from PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi import *

from PhysicsTools.PatAlgos.patSequences_cff import *

from TopQuarkAnalysis.SingleTop.simpleEleIdSequence_cff import *


#from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import nTupleTopJetsPF
#from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import nTuplePatMETsPF
#from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import nTupleElectrons
#from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import nTupleMuons
#from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import nTuplesSkim

from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import nTupleTopJetsPF
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import nTuplePatMETsPF
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import nTuplePatType1METsPF
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import nTupleElectrons
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import nTupleMuons
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import nTuplesSkim

from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import nTupleAllElectrons
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import nTupleAllMuons


from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import nTupleQCDElectrons
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import nTupleQCDMuons

from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import nTupleAllJets

from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import nTupleVetoElectrons
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import nTupleVetoElectronsMVA
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import nTupleVetoMuons
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import nTupleVertices
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import nTupleZVetoElectrons


from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import singleTopMCLeptons
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import singleTopMCNeutrinos
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import singleTopMCQuarks
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import singleTopMCBQuarks
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import singleTopMCTops
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import singleTopMCTopsW
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import singleTopMCTopsBQuark
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import singleTopMCTopsQuark
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import singleTopMCTopsQuarkBar
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import singleTopMCTopsLepton
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import singleTopMCTopsNeutrino

from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_cff import nTuplesSkimMCTruth



# require scraping filter
scrapingVeto = cms.EDFilter("FilterOutScraping",
                                                                applyfilter=cms.untracked.bool(True),
                                                                debugOn=cms.untracked.bool(False),
                                                                numtrack=cms.untracked.uint32(10),
                                                                thresh=cms.untracked.double(0.2)
                                                                )
# HB + HE noise filtering
from CommonTools.RecoAlgos.HBHENoiseFilter_cfi import HBHENoiseFilter

HBHENoiseFilter.minIsolatedNoiseSumE = cms.double(999999.)
HBHENoiseFilter.minNumIsolatedNoiseChannels = cms.int32(999999)
HBHENoiseFilter.minIsolatedNoiseSumEt = cms.double(999999.)

from CommonTools.RecoAlgos.HBHENoiseFilterResultProducer_cfi import HBHENoiseFilterResultProducer
HBHENoiseFilterResultProducer.minRatio = cms.double(-999)
HBHENoiseFilterResultProducer.maxRatio = cms.double(999)
HBHENoiseFilterResultProducer.minHPDHits = cms.int32(17)
HBHENoiseFilterResultProducer.minRBXHits = cms.int32(999)
HBHENoiseFilterResultProducer.minHPDNoOtherHits = cms.int32(10)
HBHENoiseFilterResultProducer.minZeros = cms.int32(10)
HBHENoiseFilterResultProducer.minHighEHitTime = cms.double(-9999.0)
HBHENoiseFilterResultProducer.maxHighEHitTime = cms.double(9999.0)
HBHENoiseFilterResultProducer.maxRBXEMF = cms.double(-999.0)
HBHENoiseFilterResultProducer.minNumIsolatedNoiseChannels = cms.int32(999999)
HBHENoiseFilterResultProducer.minIsolatedNoiseSumE = cms.double(999999.)
HBHENoiseFilterResultProducer.minIsolatedNoiseSumEt = cms.double(999999.)
HBHENoiseFilterResultProducer.useTS4TS5 = cms.bool(True)


from RecoMET.METAnalyzers.CSCHaloFilter_cfi import CSCTightHaloFilter
from RecoMET.METFilters.hcalLaserEventFilter_cfi import hcalLaserEventFilter
from RecoMET.METFilters.trackingFailureFilter_cfi import trackingFailureFilter
from RecoMET.METFilters.eeBadScFilter_cfi import eeBadScFilter
from RecoMET.METFilters.ecalLaserCorrFilter_cfi import ecalLaserCorrFilter
from RecoMET.METFilters.EcalDeadCellBoundaryEnergyFilter_cfi import EcalDeadCellBoundaryEnergyFilter
from RecoMET.METFilters.EcalDeadCellTriggerPrimitiveFilter_cfi import EcalDeadCellTriggerPrimitiveFilter


EcalDeadCellTriggerPrimitiveFilter.tpDigiCollection = cms.InputTag("ecalTPSkimNA")
EcalDeadCellBoundaryEnergyFilter.taggingMode = cms.bool(False)
EcalDeadCellBoundaryEnergyFilter.cutBoundEnergyDeadCellsEB=cms.untracked.double(10)
EcalDeadCellBoundaryEnergyFilter.cutBoundEnergyDeadCellsEE=cms.untracked.double(10)
EcalDeadCellBoundaryEnergyFilter.cutBoundEnergyGapEB=cms.untracked.double(100)
EcalDeadCellBoundaryEnergyFilter.cutBoundEnergyGapEE=cms.untracked.double(100)
EcalDeadCellBoundaryEnergyFilter.enableGap=cms.untracked.bool(False)
EcalDeadCellBoundaryEnergyFilter.limitDeadCellToChannelStatusEB = cms.vint32(12,14)
EcalDeadCellBoundaryEnergyFilter.limitDeadCellToChannelStatusEE = cms.vint32(12,14)


goodVertices = cms.EDFilter( "VertexSelector" ,
                             filter = cms.bool(False),
                             src = cms.InputTag("offlinePrimaryVertices"),
                               cut = cms.string("!isFake && ndof > 4 && abs(z) <= 24 && position.rho < 2")
                             )

nTuplePatMETsPF.src = cms.InputTag('patMETs')


from RecoEgamma.ElectronIdentification.electronIdSequence_cff import *
from EGamma.EGammaAnalysisTools.electronIdMVAProducer_cfi import *

mvaID = cms.Sequence(  mvaTrigV0 + mvaNonTrigV0 )

patElectronIDs = cms.Sequence(simpleEleIdSequence +
                              eIdSequence +
                              mvaID
                              )


electronIDSources = cms.PSet(
    mvaTrigV0    = cms.InputTag("mvaTrigV0"),
    mvaNonTrigV0    = cms.InputTag("mvaNonTrigV0"),
    simpleEleId70cIso = cms.InputTag("simpleEleId70cIso"),
    simpleEleId80cIso = cms.InputTag("simpleEleId80cIso"),
    simpleEleId90cIso = cms.InputTag("simpleEleId90cIso"),
    simpleEleId95cIso = cms.InputTag("simpleEleId95cIso"),
    )

#cFlavorHistory

patElectrons.addElectronID = cms.bool(True)
patElectrons.electronIDSources = electronIDSources


#makeNewPatElectrons = cms.Sequence(patElectronIDs * patElectronIsolation * patElectrons)

patElectrons.usePV = cms.bool(False)
patMuons.usePV = cms.bool(False)


#In those paths the customized collections are produced

basePath = cms.Sequence(
    preselectedMETs +
          vetoMuons +
          PVFilterProducer +
          vetoElectrons +
          vetoElectronsMVA +
       #   zVetoElectrons +
          topJetsPF +
          UnclusteredMETPF +
       #   UnclusteredType1METPF +
          genJetsPF +
          NVertices +
          NGenParticles +
          tightMuonsZeroIso +
          tightElectronsZeroIso +
          tightMuons +
          tightElectrons +
          PDFInfo
          )

basePathData = cms.Sequence(
       preselectedMETs +
          vetoMuons +
          PVFilterProducer +
          vetoElectrons +
          vetoElectronsMVA +
          topJetsPF +
          UnclusteredMETPF +
          tightMuonsZeroIso +
          tightElectronsZeroIso +
          tightMuons +
          tightElectrons 
          #  SingleTopMCProducer +
         )


#PV Filter
pvfilters = cms.Sequence(
    PVFilter
    )

#Selection step: require 1 high pt muon/electron
preselection = cms.Sequence(
#    PVFilter +
    HBHENoiseFilter *
    scrapingVeto *
    CSCTightHaloFilter *
    hcalLaserEventFilter *
    EcalDeadCellTriggerPrimitiveFilter *
    EcalDeadCellBoundaryEnergyFilter *
    goodVertices *
    trackingFailureFilter *
    eeBadScFilter *
    ecalLaserCorrFilter *
    countLeptons
    )

#Selection step: require 1 high pt muon/electron
preselectionData = cms.Sequence(
    #    hltFilter +
#    PVFilter +
    HBHENoiseFilter *
    scrapingVeto *
    CSCTightHaloFilter *
    hcalLaserEventFilter *
    EcalDeadCellTriggerPrimitiveFilter *
    EcalDeadCellBoundaryEnergyFilter *
    goodVertices *
    trackingFailureFilter *
    eeBadScFilter *
    ecalLaserCorrFilter *
    countLeptons
    )

