import FWCore.ParameterSet.Config as cms


from ElectroWeakAnalysis.WENu.simpleEleIdSequence_cff import *



electronIDSources = cms.PSet(
    simpleEleId60cIso = cms.InputTag("simpleEleId60cIso"),
    simpleEleId70cIso = cms.InputTag("simpleEleId70cIso"),
    simpleEleId80cIso = cms.InputTag("simpleEleId80cIso"),
    simpleEleId85cIso = cms.InputTag("simpleEleId85cIso"),
    simpleEleId90cIso = cms.InputTag("simpleEleId90cIso"),
    simpleEleId95cIso = cms.InputTag("simpleEleId95cIso"),

    simpleEleId60relIso = cms.InputTag("simpleEleId60relIso"),
    simpleEleId70relIso = cms.InputTag("simpleEleId70relIso"),
    simpleEleId80relIso = cms.InputTag("simpleEleId80relIso"),
    simpleEleId85relIso = cms.InputTag("simpleEleId85relIso"),
    simpleEleId90relIso = cms.InputTag("simpleEleId90relIso"),
    simpleEleId95relIso = cms.InputTag("simpleEleId95relIso"),
    )

