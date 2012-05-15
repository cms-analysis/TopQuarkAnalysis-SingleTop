import FWCore.ParameterSet.Config as cms

#lumiMu = cms.untracked.double(869.129366562)
#lumiMu = cms.untracked.double(1078.75640263)
#lumiMu = cms.untracked.double(1496.275-368+179)
#lumiEle = cms.untracked.double(191.091)


lumiMu = cms.untracked.double(1)
lumiEle = cms.untracked.double(1)

#lumiEle = cms.untracked.double(1299.)
#lumiMu = cms.untracked.double(1496.275-368.88+179.35)


wToLNuBranchingRatio = 0.108+0.1075+0.1125



relIsoCutMuons = 0.15
relIsoCutElectrons = 0.125

PileUpSeason = "SummerFlatTail11"


TChannelMu = cms.PSet(
#    crossSection = cms.untracked.double(41.92*wToLNuBranchingRatio),
    crossSection = cms.untracked.double(43.),
    channel = cms.untracked.string("TChannel"),
    originalEvents = cms.untracked.double(3900171),
    finalLumi = lumiMu,
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(relIsoCutMuons),
    mcPUFile = cms.untracked.string("pileupdistr_TChannel.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTChannel"),
    Season = cms.untracked.string(PileUpSeason),
    )


TChannelEle = cms.PSet(
#    crossSection = cms.untracked.double(41.92*wToLNuBranchingRatio),
    crossSection = cms.untracked.double(43.),
    channel = cms.untracked.string("TChannel"),
    originalEvents = cms.untracked.double(3900171),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    mcPUFile = cms.untracked.string("pileupdistr_TChannel.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTChannel"),
    )

TbarChannelMu = cms.PSet(
#    crossSection = cms.untracked.double(22.65 *wToLNuBranchingRatio),
    crossSection = cms.untracked.double(22.9),
    channel = cms.untracked.string("TbarChannel"),
    originalEvents = cms.untracked.double(1944826),
    finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(relIsoCutMuons),

    mcPUFile = cms.untracked.string("pileupdistr_TChannel.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTChannel"),
    )


TbarChannelEle = cms.PSet(
#    crossSection = cms.untracked.double(22.65 *wToLNuBranchingRatio),
    crossSection = cms.untracked.double(22.9),
    channel = cms.untracked.string("TbarChannel"),
    originalEvents = cms.untracked.double(1944826),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    mcPUFile = cms.untracked.string("pileupdistr_TChannel.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTChannel"),
    )


TWChannelMu = cms.PSet(
        crossSection = cms.untracked.double(7.87),
            channel = cms.untracked.string("TWChannel"),
#            originalEvents = cms.untracked.double(494961),
            originalEvents = cms.untracked.double(814690),
            finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
            MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
                RelIsoCut = cms.untracked.double(relIsoCutMuons),

        mcPUFile = cms.untracked.string("pileupdistr_TWChannel.root"),
        puHistoName = cms.untracked.string("pileUpDumper/PileUpTWChannel"),
            )

TWChannelEle = cms.PSet(
        crossSection = cms.untracked.double(7.87),
            channel = cms.untracked.string("TWChannel"),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
            finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
            originalEvents = cms.untracked.double(814690),
#            originalEvents = cms.untracked.double(494961),
        mcPUFile = cms.untracked.string("pileupdistr_TWChannel.root"),
        puHistoName = cms.untracked.string("pileUpDumper/PileUpTWChannel"),

            )


TbarWChannelMu = cms.PSet(
        crossSection = cms.untracked.double(7.87),
            channel = cms.untracked.string("TbarWChannel"),
#            originalEvents = cms.untracked.double(494961),
            originalEvents = cms.untracked.double(809984),
            finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
            MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
                RelIsoCut = cms.untracked.double(relIsoCutMuons),

        mcPUFile = cms.untracked.string("pileupdistr_TWChannel.root"),
        puHistoName = cms.untracked.string("pileUpDumper/PileUpTWChannel"),
            )

TbarWChannelEle = cms.PSet(
        crossSection = cms.untracked.double(7.87),
            channel = cms.untracked.string("TbarWChannel"),
            finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
            originalEvents = cms.untracked.double(809984),
#            originalEvents = cms.untracked.double(494961),
        mcPUFile = cms.untracked.string("pileupdistr_TWChannel.root"),
        puHistoName = cms.untracked.string("pileUpDumper/PileUpTWChannel"),

            )

SChannelMu = cms.PSet(
#            crossSection = cms.untracked.double(4.63*wToLNuBranchingRatio),
            crossSection = cms.untracked.double(3.14),
                        channel = cms.untracked.string("SChannel"),
                        originalEvents = cms.untracked.double(494967),
            #                        originalEvents = cms.untracked.double(259971),
                        finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
                        MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
                            RelIsoCut = cms.untracked.double(relIsoCutMuons),

            mcPUFile = cms.untracked.string("pileupdistr_SChannel.root"),
#            mcPUFile = cms.untracked.string("pileupdistr_TChannel.root"),
        puHistoName = cms.untracked.string("pileUpDumper/PileUpSChannel"),
                        )

SChannelEle = cms.PSet(
#            crossSection = cms.untracked.double(4.63*wToLNuBranchingRatio),
#            crossSection = cms.untracked.double(3.19*wToLNuBranchingRatio),
            crossSection = cms.untracked.double(3.14),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
                        channel = cms.untracked.string("SChannel"),
                        finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
                       originalEvents = cms.untracked.double(494967),
#                        originalEvents = cms.untracked.double(259971),
            mcPUFile = cms.untracked.string("pileupdistr_SChannel.root"),
#            mcPUFile = cms.untracked.string("pileupdistr_TChannel.root"),
        puHistoName = cms.untracked.string("pileUpDumper/PileUpSChannel"),

                        )


SbarChannelMu = cms.PSet(
            crossSection = cms.untracked.double(1.42),
                        channel = cms.untracked.string("SbarChannel"),
                        originalEvents = cms.untracked.double(137980),
                        finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
                        MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
                            RelIsoCut = cms.untracked.double(relIsoCutMuons),

            mcPUFile = cms.untracked.string("pileupdistr_SChannel.root"),
        puHistoName = cms.untracked.string("pileUpDumper/PileUpSChannel"),
                        )

SbarChannelEle = cms.PSet(
            crossSection = cms.untracked.double(1.42),
            RelIsoCut = cms.untracked.double(relIsoCutElectrons),
            channel = cms.untracked.string("SbarChannel"),
            finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
            originalEvents = cms.untracked.double(137980),
            mcPUFile = cms.untracked.string("pileupdistr_SChannel.root"),
        puHistoName = cms.untracked.string("pileUpDumper/PileUpSChannel"),

                        )


ZJetsMu = cms.PSet(
    crossSection = cms.untracked.double(3048),
    channel = cms.untracked.string("ZJets"),
    finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(36277961),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
        RelIsoCut = cms.untracked.double(relIsoCutMuons),

    mcPUFile = cms.untracked.string("pileupdistr_ZJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpZJets"),
)


ZJetsEle = cms.PSet(
    crossSection = cms.untracked.double(3048),
    channel = cms.untracked.string("ZJets"),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(36277961),#3 6 277 961
    mcPUFile = cms.untracked.string("pileupdistr_ZJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpZJets"),
    )

WJetsMu = cms.PSet(
    crossSection = cms.untracked.double(31314),
    channel = cms.untracked.string("WJets"),
    finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
#    originalEvents = cms.untracked.double(81352581),
    originalEvents = cms.untracked.double(74396066),
#    originalEvents = cms.untracked.double(76106157),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
        RelIsoCut = cms.untracked.double(relIsoCutMuons),

    mcPUFile = cms.untracked.string("pileupdistr_WJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWJets"),
)


WJetsEle = cms.PSet(
    crossSection = cms.untracked.double(31314),
    channel = cms.untracked.string("WJets"),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
#    originalEvents = cms.untracked.double(81352581),
    originalEvents = cms.untracked.double(74396066),
#    originalEvents = cms.untracked.double(76106157),
    mcPUFile = cms.untracked.string("pileupdistr_WJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWJets"),
    )
  


WJets_wlightMu = cms.PSet(
    crossSection = cms.untracked.double(31314),
    channel = cms.untracked.string("WJets_wlight"),
    finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
#    originalEvents = cms.untracked.double(81352581),
    originalEvents = cms.untracked.double(81352581),#originalEvents = cms.untracked.double(74396066),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
        RelIsoCut = cms.untracked.double(relIsoCutMuons),

    mcPUFile = cms.untracked.string("pileupdistr_WJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWJets"),
    )


WJets_wlightEle = cms.PSet(
    crossSection = cms.untracked.double(31314),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    channel = cms.untracked.string("WJets_wlight"),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(81352581),#originalEvents = cms.untracked.double(74396066),#originalEvents = cms.untracked.double(81352581),
    mcPUFile = cms.untracked.string("pileupdistr_WJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWJets"),
    )
  


WJets_wccMu = cms.PSet(
    crossSection = cms.untracked.double(31314),
    channel = cms.untracked.string("WJets_wcc"),
    finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(81352581),#originalEvents = cms.untracked.double(74396066),#originalEvents = cms.untracked.double(81352581),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
        RelIsoCut = cms.untracked.double(relIsoCutMuons),

    mcPUFile = cms.untracked.string("pileupdistr_WJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWJets"),
    )


WJets_wccEle = cms.PSet(
    crossSection = cms.untracked.double(31314),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    channel = cms.untracked.string("WJets_wcc"),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(81352581),#originalEvents = cms.untracked.double(74396066),#originalEvents = cms.untracked.double(81352581),
    mcPUFile = cms.untracked.string("pileupdistr_WJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWJets"),
    )

WJets_wbbMu = cms.PSet(
    crossSection = cms.untracked.double(31314),
    channel = cms.untracked.string("WJets_wbb"),
    finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(81352581),#originalEvents = cms.untracked.double(74396066),#originalEvents = cms.untracked.double(81352581),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
        RelIsoCut = cms.untracked.double(relIsoCutMuons),

    mcPUFile = cms.untracked.string("pileupdistr_WJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWJets"),
    )


WJets_wbbEle = cms.PSet(
    crossSection = cms.untracked.double(31314),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    channel = cms.untracked.string("WJets_wbb"),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(81352581),#originalEvents = cms.untracked.double(74396066),y#originalEvents = cms.untracked.double(81352581),
    mcPUFile = cms.untracked.string("pileupdistr_WJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWJets"),
    )
  


#Z


ZJets_wlightMu = cms.PSet(
    crossSection = cms.untracked.double(3048),
    channel = cms.untracked.string("ZJets_wlight"),
    finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(36277961),#originalEvents = cms.untracked.double(4425520),#originalEvents = cms.untracked.double(36277961),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
        RelIsoCut = cms.untracked.double(relIsoCutMuons),

    mcPUFile = cms.untracked.string("pileupdistr_ZJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpZJets"),
    )


ZJets_wlightEle = cms.PSet(
    crossSection = cms.untracked.double(3048),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    channel = cms.untracked.string("ZJets_wlight"),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(36277961),#originalEvents = cms.untracked.double(4425520),#originalEvents = cms.untracked.double(36277961),
    mcPUFile = cms.untracked.string("pileupdistr_ZJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpZJets"),
    )
  


ZJets_wccMu = cms.PSet(
    crossSection = cms.untracked.double(3048),
    channel = cms.untracked.string("ZJets_wcc"),
    finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(36277961),#originalEvents = cms.untracked.double(4425520),#originalEvents = cms.untracked.double(36277961),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
        RelIsoCut = cms.untracked.double(relIsoCutMuons),

    mcPUFile = cms.untracked.string("pileupdistr_ZJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpZJets"),
    )


ZJets_wccEle = cms.PSet(
    crossSection = cms.untracked.double(3048),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    channel = cms.untracked.string("ZJets_wcc"),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(36277961),#originalEvents = cms.untracked.double(4425520),#originalEvents = cms.untracked.double(36277961),
    mcPUFile = cms.untracked.string("pileupdistr_ZJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpZJets"),
    )

ZJets_wbbMu = cms.PSet(
    crossSection = cms.untracked.double(3048),
    channel = cms.untracked.string("ZJets_wbb"),
    finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(36277961),#originalEvents = cms.untracked.double(4425520),#originalEvents = cms.untracked.double(36277961),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
        RelIsoCut = cms.untracked.double(relIsoCutMuons),

    mcPUFile = cms.untracked.string("pileupdistr_ZJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpZJets"),
    )
ZJets_wbbEle = cms.PSet(
    crossSection = cms.untracked.double(3048),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    channel = cms.untracked.string("ZJets_wbb"),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(36277961),#originalEvents = cms.untracked.double(4425520),#originalEvents = cms.untracked.double(36277961),
    mcPUFile = cms.untracked.string("pileupdistr_ZJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpZJets"),
    )
  




Vqq_wbbMu = cms.PSet(
    crossSection = cms.untracked.double(36),
    channel = cms.untracked.string("Vqq_wbb"),
    finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(740488),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
        RelIsoCut = cms.untracked.double(relIsoCutMuons),
    mcPUFile = cms.untracked.string("pileupdistr_Vqq.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpVqq"),
    )


Vqq_wbbEle = cms.PSet(
    crossSection = cms.untracked.double(36),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    channel = cms.untracked.string("Vqq_wbb"),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(740488),
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
      mcPUFile = cms.untracked.string("pileupdistr_Vqq.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpVqq"),
    )
  

Vqq_wccMu = cms.PSet(
    crossSection = cms.untracked.double(36),
    channel = cms.untracked.string("Vqq_wcc"),
    finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(740488),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(relIsoCutMuons),
    mcPUFile = cms.untracked.string("pileupdistr_Vqq.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpVqq"),
    )


Vqq_wccEle = cms.PSet(
    crossSection = cms.untracked.double(36),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    channel = cms.untracked.string("Vqq_wcc"),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(740488),
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    mcPUFile = cms.untracked.string("pileupdistr_Vqq.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpVqq"),
    )
  


Wc_wcMu = cms.PSet(
    crossSection = cms.untracked.double(606),
    channel = cms.untracked.string("Wc_wc"),
    finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(2792637),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(relIsoCutMuons),
    mcPUFile = cms.untracked.string("pileupdistr_Wc.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWc"),
    )

Wc_wcEle = cms.PSet(
    crossSection = cms.untracked.double(606),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    channel = cms.untracked.string("Wc_wc"),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(2792637),
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    mcPUFile = cms.untracked.string("pileupdistr_Wc.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWc"),
    )
WWMu = cms.PSet(
    crossSection = cms.untracked.double(43),
    channel = cms.untracked.string("WW"),
    finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(4225916),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(relIsoCutMuons),
    mcPUFile = cms.untracked.string("pileupdistr_WW.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWW"),
    )

WWEle = cms.PSet(
    crossSection = cms.untracked.double(43),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    channel = cms.untracked.string("WW"),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(4225916),
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    mcPUFile = cms.untracked.string("pileupdistr_WW.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWW"),
    )

ZZMu = cms.PSet(
    crossSection = cms.untracked.double(5.9),
    channel = cms.untracked.string("ZZ"),
    finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(4187885),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(relIsoCutMuons),
    mcPUFile = cms.untracked.string("pileupdistr_ZZ.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpZZ"),
    )

ZZEle = cms.PSet(
    crossSection = cms.untracked.double(5.9),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    channel = cms.untracked.string("ZZ"),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(4187885),
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    mcPUFile = cms.untracked.string("pileupdistr_ZZ.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpZZ"),
    )

WZMu = cms.PSet(
    crossSection = cms.untracked.double(18.2),
    channel = cms.untracked.string("WZ"),
    finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(4265243),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(relIsoCutMuons),
    mcPUFile = cms.untracked.string("pileupdistr_WZ.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWZ"),
    )
WZEle = cms.PSet(
    crossSection = cms.untracked.double(18.2),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    channel = cms.untracked.string("WZ"),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(4265243),
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    mcPUFile = cms.untracked.string("pileupdistr_WZ.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWZ"),
    )

TTBarMu = cms.PSet(
    crossSection = cms.untracked.double(165.),
    channel = cms.untracked.string("TTBar"),
    originalEvents = cms.untracked.double(3701947),#1089625
    finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
   RelIsoCut = cms.untracked.double(relIsoCutMuons),
    mcPUFile = cms.untracked.string("pileupdistr_TTBar.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTTBar"),
    )

TTBarEle = cms.PSet(
    crossSection = cms.untracked.double(165.),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    channel = cms.untracked.string("TTBar"),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(3701947),#1089625
    mcPUFile = cms.untracked.string("pileupdistr_TTBar.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTTBar"),
    )
    
DataMu = cms.PSet(
    crossSection = cms.untracked.double(-1),
    channel = cms.untracked.string("Data"),
    originalEvents = cms.untracked.double(-1),
    finalLumi = cms.untracked.double(-1),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
   RelIsoCut = cms.untracked.double(relIsoCutMuons),
    mcPUFile = cms.untracked.string("pileupdistr_VV.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpVV"),
    )

DataEle = cms.PSet(
    crossSection = cms.untracked.double(-1),
    channel = cms.untracked.string("Data"),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    originalEvents = cms.untracked.double(-1),
    finalLumi = cms.untracked.double(-1),
    mcPUFile = cms.untracked.string("pileupdistr_VV.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpVV"),
    )


QCD_Pt_20to30_EMEnrichedEle = cms.PSet(
    crossSection = cms.untracked.double(2454400.),
    channel = cms.untracked.string("QCD_Pt_20to30_EMEnriched"),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
   RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    originalEvents = cms.untracked.double(35729669),
    mcPUFile = cms.untracked.string("pileupdistr_QCD_Pt_20to30_EMEnriched.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_Pt_20to30_EMEnriched"),
    )

QCD_Pt_20to30_EMEnrichedMu = cms.PSet(
    crossSection = cms.untracked.double(2454400.),
    channel = cms.untracked.string("QCD_Pt_20to30_EMEnriched"),
   RelIsoCut = cms.untracked.double(relIsoCutMuons),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(35729669),
    mcPUFile = cms.untracked.string("pileupdistr_QCD_Pt_20to30_EMEnriched.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_Pt_20to30_EMEnriched"),
    )

QCD_Pt_30to80_EMEnrichedEle = cms.PSet(
    crossSection = cms.untracked.double(3866200.),#
    channel = cms.untracked.string("QCD_Pt_30to80_EMEnriched"),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(70392060),
    mcPUFile = cms.untracked.string("pileupdistr_QCD_Pt_30to80_EMEnriched.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_Pt_30to80_EMEnriched"),
    )

QCD_Pt_30to80_EMEnrichedMu = cms.PSet(
        crossSection = cms.untracked.double(3866200.),
        channel = cms.untracked.string("QCD_Pt_30to80_EMEnriched"),
        RelIsoCut = cms.untracked.double(relIsoCutMuons),
            finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
            originalEvents = cms.untracked.double(70392060),
        mcPUFile = cms.untracked.string("pileupdistr_QCD_Pt_30to80_EMEnriched.root"),
        puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_Pt_30to80_EMEnriched"),
            )


QCD_Pt_80to170_EMEnrichedEle = cms.PSet(
    crossSection = cms.untracked.double(139500.),
    channel = cms.untracked.string("QCD_Pt_80to170_EMEnriched"),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(8150672),
    mcPUFile = cms.untracked.string("pileupdistr_QCD_Pt_80to170_EMEnriched.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_Pt_80to170_EMEnriched"),
    )

QCD_Pt_80to170_EMEnrichedMu = cms.PSet(
        crossSection = cms.untracked.double(139500.),
            channel = cms.untracked.string("QCD_Pt_80to170_EMEnriched"),
            finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
 RelIsoCut = cms.untracked.double(relIsoCutMuons),
            originalEvents = cms.untracked.double(8150672),
    mcPUFile = cms.untracked.string("pileupdistr_QCD_Pt_80to170_EMEnriched.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_Pt_80to170_EMEnriched"),
            )



QCD_Pt_20to30_BCtoEEle = cms.PSet(
    crossSection = cms.untracked.double(132160.),
    channel = cms.untracked.string("QCD_Pt_20to30_BCtoE"),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(2081560),
    mcPUFile = cms.untracked.string("pileupdistr_QCD_Pt_20to30_BCtoE.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_Pt_20to30_BCtoE"),
    )

QCD_Pt_20to30_BCtoEMu = cms.PSet(
        crossSection = cms.untracked.double(132160.),
            channel = cms.untracked.string("QCD_Pt_20to30_BCtoE"),
 RelIsoCut = cms.untracked.double(relIsoCutMuons),
            finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
            originalEvents = cms.untracked.double(2081560),
        mcPUFile = cms.untracked.string("pileupdistr_QCD_Pt_20to30_BCtoE.root"),
        puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_Pt_20to30_BCtoE"),
            )


QCD_Pt_30to80_BCtoEEle = cms.PSet(
    crossSection = cms.untracked.double(136804.),
    channel = cms.untracked.string("QCD_Pt_30to80_BCtoE"),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(2030033),
    mcPUFile = cms.untracked.string("pileupdistr_QCD_Pt_30to80_BCtoE.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_Pt_30to80_BCtoE"),
    )

QCD_Pt_30to80_BCtoEMu = cms.PSet(
        crossSection = cms.untracked.double(136804.),
            channel = cms.untracked.string("QCD_Pt_30to80_BCtoE"),
 RelIsoCut = cms.untracked.double(relIsoCutMuons),
            finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
            originalEvents = cms.untracked.double(2030033),
        mcPUFile = cms.untracked.string("pileupdistr_QCD_Pt_30to80_BCtoE.root"),
        puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_Pt_30to80_BCtoE"),
            )


QCD_Pt_80to170_BCtoEEle = cms.PSet(
    crossSection = cms.untracked.double(9360.),
    channel = cms.untracked.string("QCD_Pt_80to170_BCtoE"),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(1082691),
    mcPUFile = cms.untracked.string("pileupdistr_QCD_Pt_80to170_BCtoE.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_Pt_80to170_BCtoE"),
    )

QCD_Pt_80to170_BCtoEMu = cms.PSet(
        crossSection = cms.untracked.double(9360.),
            channel = cms.untracked.string("QCD_Pt_80to170_BCtoE"),
 RelIsoCut = cms.untracked.double(relIsoCutMuons),
            finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
            originalEvents = cms.untracked.double(1082691),
    mcPUFile = cms.untracked.string("pileupdistr_QCD_Pt_80to170_BCtoE.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_Pt_80to170_BCtoE"),
            )


QCD_HT_40_100_GJetsEle = cms.PSet(
    crossSection = cms.untracked.double(23620.),
    channel = cms.untracked.string("QCD_HT_40_100_GJets"),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(2217101),
    mcPUFile = cms.untracked.string("pileupdistr_QCD_HT_40_100_GJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_HT_40_100_GJets"),
    )

QCD_HT_40_100_GJetsMu = cms.PSet(
        crossSection = cms.untracked.double(23620.),
        channel = cms.untracked.string("QCD_HT_40_100_GJets"),
 RelIsoCut = cms.untracked.double(relIsoCutMuons),
        finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
        originalEvents = cms.untracked.double(2217101),
    mcPUFile = cms.untracked.string("pileupdistr_QCD_HT_40_100_GJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_HT_40_100_GJets"),
        )



QCD_HT_100_200_GJetsEle = cms.PSet(
    crossSection = cms.untracked.double(3476.),
    channel = cms.untracked.string("QCD_HT_100_200_GJets"),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(1065691),
    mcPUFile = cms.untracked.string("pileupdistr_QCD_HT_100_200_GJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_HT_100_200_GJets"),
    )

QCD_HT_100_200_GJetsMu = cms.PSet(
        crossSection = cms.untracked.double(3476.),
            channel = cms.untracked.string("QCD_HT_100_200_GJets"),
 RelIsoCut = cms.untracked.double(relIsoCutMuons),
            finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
            originalEvents = cms.untracked.double(1065691),
    mcPUFile = cms.untracked.string("pileupdistr_QCD_HT_100_200_GJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_HT_100_200_GJets"),
            )


QCD_HT_200_inf_GJetsEle = cms.PSet(
    crossSection = cms.untracked.double(485.),
    channel = cms.untracked.string("QCD_HT_200_inf_GJets"),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(942171), 
    mcPUFile = cms.untracked.string("pileupdistr_QCD_HT_200_inf_GJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_HT_200_inf_GJets"),
   )

QCD_HT_200_inf_GJetsMu = cms.PSet(
        crossSection = cms.untracked.double(485.),
            channel = cms.untracked.string("QCD_HT_200_inf_GJets"),
 RelIsoCut = cms.untracked.double(relIsoCutMuons),
            finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
            originalEvents = cms.untracked.double(942171),
    mcPUFile = cms.untracked.string("pileupdistr_QCD_HT_200_inf_GJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_HT_200_inf_GJets"),
            )


QCDMuMu = cms.PSet(
    crossSection = cms.untracked.double(84679.),
    channel = cms.untracked.string("QCDMu"),
    finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
 RelIsoCut = cms.untracked.double(relIsoCutMuons),
    originalEvents = cms.untracked.double(29434562),
    mcPUFile = cms.untracked.string("pileupdistr_QCDMu.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCDMu"),
    )


QCDMuEle = cms.PSet(
    crossSection = cms.untracked.double(84679.),
    channel = cms.untracked.string("QCDMu"),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(29434562),
    mcPUFile = cms.untracked.string("pileupdistr_QCDMu.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCDMu"),
    )



#Systs

TbarChannel_Q2UpMu = cms.PSet(
#    crossSection = cms.untracked.double(22.65 *wToLNuBranchingRatio),
    crossSection = cms.untracked.double(22.9),
    channel = cms.untracked.string("TbarChannel_Q2Up"),
    originalEvents = cms.untracked.double(565520),
    finalLumi = lumiMu,
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(relIsoCutMuons),

    mcPUFile = cms.untracked.string("pileupdistr_TChannel.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTChannel"),
    Season = cms.untracked.string(PileUpSeason),
    )


TbarChannel_Q2UpEle = cms.PSet(
#    crossSection = cms.untracked.double(22.65 *wToLNuBranchingRatio),
    crossSection = cms.untracked.double(22.9),
    channel = cms.untracked.string("TbarChannel_Q2Up"),
    originalEvents = cms.untracked.double(565520),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    finalLumi = lumiEle,
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    mcPUFile = cms.untracked.string("pileupdistr_TChannel.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTChannel"),
    Season = cms.untracked.string(PileUpSeason),
    )




TbarChannel_Q2DownMu = cms.PSet(
#    crossSection = cms.untracked.double(22.65 *wToLNuBranchingRatio),
    crossSection = cms.untracked.double(22.9),
    channel = cms.untracked.string("TbarChannel_Q2Down"),
    originalEvents = cms.untracked.double(565454),
    finalLumi = lumiMu,
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(relIsoCutMuons),

    mcPUFile = cms.untracked.string("pileupdistr_TChannel.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTChannel"),
    Season = cms.untracked.string(PileUpSeason),
    )


TbarChannel_Q2DownEle = cms.PSet(
#    crossSection = cms.untracked.double(22.65 *wToLNuBranchingRatio),
    crossSection = cms.untracked.double(22.9),
    channel = cms.untracked.string("TbarChannel_Q2Down"),
    originalEvents = cms.untracked.double(565454),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    finalLumi = lumiEle,
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    mcPUFile = cms.untracked.string("pileupdistr_TChannel.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTChannel"),
    Season = cms.untracked.string(PileUpSeason),
    )



###
TChannel_Q2UpMu = cms.PSet(
#    crossSection = cms.untracked.double(22.65 *wToLNuBranchingRatio),
    crossSection = cms.untracked.double(43.0),
    channel = cms.untracked.string("TChannel_Q2Up"),
    originalEvents = cms.untracked.double(1032197),
    finalLumi = lumiMu,
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(relIsoCutMuons),

    mcPUFile = cms.untracked.string("pileupdistr_TChannel.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTChannel"),
    Season = cms.untracked.string(PileUpSeason),
    )


TChannel_Q2UpEle = cms.PSet(
#    crossSection = cms.untracked.double(22.65 *wToLNuBranchingRatio),
    crossSection = cms.untracked.double(43.0),
    channel = cms.untracked.string("TChannel_Q2Up"),
    originalEvents = cms.untracked.double(1032197),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    finalLumi = lumiEle,
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    mcPUFile = cms.untracked.string("pileupdistr_TChannel.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTChannel"),
    Season = cms.untracked.string(PileUpSeason),
    )




TChannel_Q2DownMu = cms.PSet(
#    crossSection = cms.untracked.double(22.65 *wToLNuBranchingRatio),
    crossSection = cms.untracked.double(43.0),
    channel = cms.untracked.string("TChannel_Q2Down"),
    originalEvents = cms.untracked.double(1041924),
    finalLumi = lumiMu,
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(relIsoCutMuons),

    mcPUFile = cms.untracked.string("pileupdistr_TChannel.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTChannel"),
    Season = cms.untracked.string(PileUpSeason),
    )


TChannel_Q2DownEle = cms.PSet(
#    crossSection = cms.untracked.double(22.65 *wToLNuBranchingRatio),
    crossSection = cms.untracked.double(43.0),
    channel = cms.untracked.string("TChannel_Q2Down"),
    originalEvents = cms.untracked.double(1041924),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    finalLumi = lumiEle,
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    mcPUFile = cms.untracked.string("pileupdistr_TChannel.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTChannel"),
    Season = cms.untracked.string(PileUpSeason),
    )



TTBar_Q2DownMu = cms.PSet(
    crossSection = cms.untracked.double(165.),
    channel = cms.untracked.string("TTBar_Q2Down"),
    originalEvents = cms.untracked.double(967055),#3701947),#1089625
    finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
   RelIsoCut = cms.untracked.double(relIsoCutMuons),
    mcPUFile = cms.untracked.string("pileupdistr_TTBar_Q2Down.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTTBar_Q2Down"),
    )

TTBar_Q2DownEle = cms.PSet(
    crossSection = cms.untracked.double(165.),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    channel = cms.untracked.string("TTBar_Q2Down"),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(967055),#3701947),#1089625
    mcPUFile = cms.untracked.string("pileupdistr_TTBar_Q2Down.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTTBar_Q2Down"),
    )



TTBar_Q2UpMu = cms.PSet(
    crossSection = cms.untracked.double(165.),
    channel = cms.untracked.string("TTBar_Q2Up"),
    originalEvents = cms.untracked.double(930483),#3701947),#1089625
    finalLumi = lumiMu,Season = cms.untracked.string(PileUpSeason),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
   RelIsoCut = cms.untracked.double(relIsoCutMuons),
    mcPUFile = cms.untracked.string("pileupdistr_TTBar_Q2Up.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTTBar_Q2Up"),
    )

TTBar_Q2UpEle = cms.PSet(
    crossSection = cms.untracked.double(165.),
RelIsoCut = cms.untracked.double(relIsoCutElectrons),
    channel = cms.untracked.string("TTBar_Q2Up"),
    finalLumi = lumiEle,Season = cms.untracked.string(PileUpSeason),
    originalEvents = cms.untracked.double(930483),#3701947),#1089625
    mcPUFile = cms.untracked.string("pileupdistr_TTBar_Q2Up.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTTBar_Q2Up"),
    )
