import FWCore.ParameterSet.Config as cms

lumiMu = cms.untracked.double(869.129366562)
lumiEle = cms.untracked.double(191.091)

TChannelMu = cms.PSet(
    crossSection = cms.untracked.double(20.93),
    channel = cms.untracked.string("TChannel"),
    originalEvents = cms.untracked.double(480000),
    finalLumi = lumiMu,
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.05),
    )


TChannelEle = cms.PSet(
    crossSection = cms.untracked.double(20.93),
    channel = cms.untracked.string("TChannel"),
    originalEvents = cms.untracked.double(480000),
    finalLumi = lumiEle,
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    )

TWChannelMu = cms.PSet(
        crossSection = cms.untracked.double(10.6),
            channel = cms.untracked.string("TWChannel"),
            originalEvents = cms.untracked.double(494961),
            finalLumi = lumiMu,
            MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
            RelIsoCut = cms.untracked.double(0.05),
            )

TWChannelEle = cms.PSet(
        crossSection = cms.untracked.double(10.6),
            channel = cms.untracked.string("TWChannel"),
            finalLumi = lumiEle,
            originalEvents = cms.untracked.double(494961),
            )

sChanMu = cms.PSet(
            crossSection = cms.untracked.double(1.533),
                        channel = cms.untracked.string("sChan"),
                        originalEvents = cms.untracked.double(494967),
                        finalLumi = lumiMu,
                        MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
                        RelIsoCut = cms.untracked.double(0.05),
                        )

sChanEle = cms.PSet(
            crossSection = cms.untracked.double(1.533),
                        channel = cms.untracked.string("sChan"),
                        finalLumi = lumiEle,
                        originalEvents = cms.untracked.double(494967),
                        )
  

ZJetsMu = cms.PSet(
    crossSection = cms.untracked.double(2321),
    channel = cms.untracked.string("ZJets"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(2595097),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.05),
)


ZJetsEle = cms.PSet(
    crossSection = cms.untracked.double(2321),
    channel = cms.untracked.string("ZJets"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(2595097),
    )

WJetsMu = cms.PSet(
    crossSection = cms.untracked.double(31314),
    channel = cms.untracked.string("WJets"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(14800000),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.05),
)


WJetsEle = cms.PSet(
    crossSection = cms.untracked.double(31314),
    channel = cms.untracked.string("WJets"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(14800000),
    )
  


WJets_wlightMu = cms.PSet(
    crossSection = cms.untracked.double(24170),
    channel = cms.untracked.string("WJets_wlight"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(14800000),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.05),
    )


WJets_wlightEle = cms.PSet(
    crossSection = cms.untracked.double(24170),
    channel = cms.untracked.string("WJets_wlight"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(14800000),
    )
  


WJets_wccMu = cms.PSet(
    crossSection = cms.untracked.double(24170),
    channel = cms.untracked.string("WJets_wcc"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(14800000),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.05),
    )


WJets_wccEle = cms.PSet(
    crossSection = cms.untracked.double(24170),
    channel = cms.untracked.string("WJets_wcc"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(14800000),
    )

WJets_wbbMu = cms.PSet(
    crossSection = cms.untracked.double(24170),
    channel = cms.untracked.string("WJets_wbb"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(14800000),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.05),
    )
WJets_wbbEle = cms.PSet(
    crossSection = cms.untracked.double(24170),
    channel = cms.untracked.string("WJets_wbb"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(14800000),
    )
  


#Z


ZJets_wlightMu = cms.PSet(
    crossSection = cms.untracked.double(2321),
    channel = cms.untracked.string("ZJets_wlight"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(2543706),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.05),
    )


ZJets_wlightEle = cms.PSet(
    crossSection = cms.untracked.double(2321),
    channel = cms.untracked.string("ZJets_wlight"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(2543706),
    )
  


ZJets_wccMu = cms.PSet(
    crossSection = cms.untracked.double(2321),
    channel = cms.untracked.string("ZJets_wcc"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(2543706),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.05),
    )


ZJets_wccEle = cms.PSet(
    crossSection = cms.untracked.double(2321),
    channel = cms.untracked.string("ZJets_wcc"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(2543706),
    )

ZJets_wbbMu = cms.PSet(
    crossSection = cms.untracked.double(2321),
    channel = cms.untracked.string("ZJets_wbb"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(2543706),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.05),
    )
ZJets_wbbEle = cms.PSet(
    crossSection = cms.untracked.double(2321),
    channel = cms.untracked.string("ZJets_wbb"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(2543706),
    )
  





Vqq_wbbMu = cms.PSet(
    crossSection = cms.untracked.double(36),
    channel = cms.untracked.string("Vqq_wbb"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(740488),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.05),
    )


Vqq_wbbEle = cms.PSet(
    crossSection = cms.untracked.double(36),
    channel = cms.untracked.string("Vqq_wbb"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(740488),
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1)
    )
  

Vqq_wccMu = cms.PSet(
    crossSection = cms.untracked.double(36),
    channel = cms.untracked.string("Vqq_wcc"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(740488),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.05),
    )


Vqq_wccEle = cms.PSet(
    crossSection = cms.untracked.double(36),
    channel = cms.untracked.string("Vqq_wcc"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(740488),
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1)
    )
  


Wc_wcMu = cms.PSet(
    crossSection = cms.untracked.double(606),
    channel = cms.untracked.string("Wc_wc"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(2792637),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.05),
    )

Wc_wcEle = cms.PSet(
    crossSection = cms.untracked.double(606),
    channel = cms.untracked.string("Wc_wc"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(2792637),
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1)
    )
  

VVMu = cms.PSet(
    crossSection = cms.untracked.double(4.8),
    channel = cms.untracked.string("VV"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(963356),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.05),
    )

VVEle = cms.PSet(
    crossSection = cms.untracked.double(4.8),
    channel = cms.untracked.string("VV"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(963356),
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1)
    )
  

TTBarMu = cms.PSet(
    crossSection = cms.untracked.double(150.),
    channel = cms.untracked.string("TTBar"),
#    originalEvents = cms.untracked.double(1100000),
    originalEvents = cms.untracked.double(1014208),
    finalLumi = lumiMu,
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.05),
    )

TTBarEle = cms.PSet(
    crossSection = cms.untracked.double(150.),
    channel = cms.untracked.string("TTBar"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(1014208),
#    originalEvents = cms.untracked.double(1100000),
    )
    

DataMu = cms.PSet(
    crossSection = cms.untracked.double(-1),
    channel = cms.untracked.string("Data"),
    originalEvents = cms.untracked.double(-1),
    finalLumi = cms.untracked.double(-1),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.05),
    )

DataEle = cms.PSet(
    crossSection = cms.untracked.double(-1),
    channel = cms.untracked.string("Data"),
    originalEvents = cms.untracked.double(-1),
    finalLumi = cms.untracked.double(-1),
    )


#QCDQCD_Pt_20to30EMEnriched = cms.PSet(
#    crossSection = cms.untracked.double(2454400.),
#    channel = cms.untracked.string("QCD"),
#    finalLumi = lumiEle,
#    originalEvents = cms.untracked.double(1100000),
#    )

QCD_Pt_30to80EMEnrichedEle = cms.PSet(
    crossSection = cms.untracked.double(3866200.),
    channel = cms.untracked.string("QCD_Pt_30to80EMEnriched"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(70708892),
    )

QCD_Pt_30to80EMEnrichedMu = cms.PSet(
        crossSection = cms.untracked.double(3866200.),
            channel = cms.untracked.string("QCD_Pt_30to80EMEnriched"),
            finalLumi = lumiMu,
            originalEvents = cms.untracked.double(70708892),
            )


QCD_Pt_80to170EMEnrichedEle = cms.PSet(
    crossSection = cms.untracked.double(139500.),
    channel = cms.untracked.string("QCD_Pt_80to170EMEnriched"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(8069591),
    )

QCD_Pt_80to170EMEnrichedMu = cms.PSet(
        crossSection = cms.untracked.double(139500.),
            channel = cms.untracked.string("QCD_Pt_80to170EMEnriched"),
            finalLumi = lumiMu,
            originalEvents = cms.untracked.double(8069591),
            )



QCD_Pt_20to30BCtoEEle = cms.PSet(
    crossSection = cms.untracked.double(132160.),
    channel = cms.untracked.string("QCD_Pt_20to30BCtoE"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(1993439),
    )

QCD_Pt_20to30BCtoEMu = cms.PSet(
        crossSection = cms.untracked.double(132160.),
            channel = cms.untracked.string("QCD_Pt_20to30BCtoE"),
            finalLumi = lumiMu,
            originalEvents = cms.untracked.double(1993439),
            )


QCD_Pt_30to80BCtoEEle = cms.PSet(
    crossSection = cms.untracked.double(136804.),
    channel = cms.untracked.string("QCD_Pt_30to80BCtoE"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(1795502),
    )

QCD_Pt_30to80BCtoEMu = cms.PSet(
        crossSection = cms.untracked.double(136804.),
            channel = cms.untracked.string("QCD_Pt_30to80BCtoE"),
            finalLumi = lumiMu,
            originalEvents = cms.untracked.double(1795502),
            )


QCD_Pt_80to170BCtoEEle = cms.PSet(
    crossSection = cms.untracked.double(9360.),
    channel = cms.untracked.string("QCD_Pt_80to170BCtoE"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(1043390),
    )

QCD_Pt_80to170BCtoEMu = cms.PSet(
        crossSection = cms.untracked.double(9360.),
            channel = cms.untracked.string("QCD_Pt_80to170BCtoE"),
            finalLumi = lumiMu,
            originalEvents = cms.untracked.double(1043390),
            )


GJets_HT_40To100Ele = cms.PSet(
    crossSection = cms.untracked.double(23620.),
    channel = cms.untracked.string("GJets_HT_40To100"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(2217101),
    )

GJets_HT_40To100Mu = cms.PSet(
        crossSection = cms.untracked.double(23620.),
        channel = cms.untracked.string("GJets_HT_40To100"),
        finalLumi = lumiMu,
        originalEvents = cms.untracked.double(2217101),
        )



GJets_HT_100To200Ele = cms.PSet(
    crossSection = cms.untracked.double(3476.),
    channel = cms.untracked.string("GJets_HT_100To200"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(1065691),
    )

GJets_HT_100To200Mu = cms.PSet(
        crossSection = cms.untracked.double(3476.),
            channel = cms.untracked.string("GJets_HT_100To200"),
            finalLumi = lumiMu,
            originalEvents = cms.untracked.double(1065691),
            )


GJets_HT_200Ele = cms.PSet(
    crossSection = cms.untracked.double(485.),
    channel = cms.untracked.string("GJets_HT_200"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(942171),
    )

GJets_HT_200Mu = cms.PSet(
        crossSection = cms.untracked.double(485.),
            channel = cms.untracked.string("GJets_HT_200"),
            finalLumi = lumiMu,
            originalEvents = cms.untracked.double(942171),
            )


QCDMuMu = cms.PSet(
    crossSection = cms.untracked.double(84679.),
    channel = cms.untracked.string("QCDMu"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(29434562),
    )


QCDMuEle = cms.PSet(
    crossSection = cms.untracked.double(84679.),
    channel = cms.untracked.string("QCDMu"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(29434562),
    )

