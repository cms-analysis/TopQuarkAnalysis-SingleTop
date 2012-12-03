import FWCore.ParameterSet.Config as cms


lumi = cms.untracked.double(15000.)
lumiMu = cms.untracked.double(1)
lumiEle = cms.untracked.double(1)


PileUpSeason = "Summer12"
PileUpSeasonV6 = "Summer12V6"
PileUpSeason53X = "Summer12_53X"

tW_XSec = cms.untracked.double(11.1)
tbarW_XSec = cms.untracked.double(11.1)
ttbar_XSec = cms.untracked.double(234.)



TWChannel = cms.PSet(
    crossSection = tW_XSec,
    channel = cms.untracked.string("TWChannel"),
    originalEvents = cms.untracked.double(497658),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )


TbarWChannel = cms.PSet(
    crossSection = tbarW_XSec,
    channel = cms.untracked.string("TWChannel"),
    originalEvents = cms.untracked.double(493460),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBar = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar"),
    originalEvents = cms.untracked.double(6923750),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )

    
Data = cms.PSet(
    crossSection = cms.untracked.double(-1),
    channel = cms.untracked.string("Data"),
    originalEvents = cms.untracked.double(-1),
    finalLumi = cms.untracked.double(-1),
    )



TChannel = cms.PSet(
    crossSection = cms.untracked.double(56.4),
    channel = cms.untracked.string("TChannel"),
    originalEvents = cms.untracked.double(3758227),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )
    
    
TbarChannel = cms.PSet(
    crossSection = cms.untracked.double(30.7),
    channel = cms.untracked.string("TChannel"),
    originalEvents = cms.untracked.double(1935072),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )

SChannel = cms.PSet(
    crossSection = cms.untracked.double(3.79),
    channel = cms.untracked.string("SChannel"),
    originalEvents = cms.untracked.double(259961),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )

SbarChannel = cms.PSet(
    crossSection = cms.untracked.double(1.76),
    channel = cms.untracked.string("SChannel"),
    originalEvents = cms.untracked.double(139974),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )

ZJets = cms.PSet(
    crossSection = cms.untracked.double(3503.71),
    channel = cms.untracked.string("ZJets"),
    originalEvents = cms.untracked.double(30459503),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )

ZJetsLowMass = cms.PSet(
    crossSection = cms.untracked.double(3503.71),
    channel = cms.untracked.string("ZJets"),
    originalEvents = cms.untracked.double(7132223),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )


WJets = cms.PSet(
    crossSection = cms.untracked.double(36257.2),
    channel = cms.untracked.string("WJets"),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    originalEvents = cms.untracked.double(57709905),
    )

  
WW = cms.PSet(
    crossSection = cms.untracked.double(57.1097),
    channel = cms.untracked.string("WW"),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    originalEvents = cms.untracked.double(10000431),
    )


ZZ = cms.PSet(
    crossSection = cms.untracked.double(8.25561),
    channel = cms.untracked.string("ZZ"),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    originalEvents = cms.untracked.double(9799908),
    )


WZ = cms.PSet(
    crossSection = cms.untracked.double(32.3161),
    channel = cms.untracked.string("WZ"),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    originalEvents = cms.untracked.double(10000283),
    )



#Special Training samples

TWChannelDilepton = cms.PSet(
    crossSection = tW_XSec,
    channel = cms.untracked.string("TWChannelDilepton"),
    originalEvents = cms.untracked.double(2976510),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )


TbarWChannelDilepton = cms.PSet(
    crossSection = tbarW_XSec,
    channel = cms.untracked.string("TWChannelDilepton"),
    originalEvents = cms.untracked.double(2971482),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBarDilepton = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBarDilepton"),
    originalEvents = cms.untracked.double(10783509),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TestSample = cms.PSet(
    crossSection = cms.untracked.double(1.),
    channel = cms.untracked.string("TestSample"),
    originalEvents = cms.untracked.double(1.),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )



#Systs

TWChannel_DS = cms.PSet(
    crossSection = tW_XSec,
    channel = cms.untracked.string("TWChannel"),
    originalEvents = cms.untracked.double(2970011),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TbarWChannel_DS = cms.PSet(
    crossSection = tbarW_XSec,
    channel = cms.untracked.string("TWChannel"),
    originalEvents = cms.untracked.double(2940594),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )


TWChannel_Q2Up = cms.PSet(
    crossSection = tW_XSec,
    channel = cms.untracked.string("TWChannel_Q2Up"),
    originalEvents = cms.untracked.double(1492816),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TWChannel_Q2Down = cms.PSet(
    crossSection = tW_XSec,
    channel = cms.untracked.string("TWChannel_Q2Down"),
    originalEvents = cms.untracked.double(1493130),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TbarWChannel_Q2Up = cms.PSet(
    crossSection = tbarW_XSec,
    channel = cms.untracked.string("TWChannel_Q2Up"),
    originalEvents = cms.untracked.double(1492534),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TbarWChannel_Q2Down = cms.PSet(
    crossSection = tbarW_XSec,
    channel = cms.untracked.string("TWChannel_Q2Down"),
    originalEvents = cms.untracked.double(1493101),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBar_Q2Up = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar_Q2Up"),
    originalEvents = cms.untracked.double(5009488),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBar_Q2Down = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar_Q2Down"),
    originalEvents = cms.untracked.double(5009488),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBar_MatchingUp = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar_MatchingUp"),
    originalEvents = cms.untracked.double(5415010),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBar_MatchingDown = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar_MatchingDown"),
    originalEvents = cms.untracked.double(5476728),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBar_Mass166_5 = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar_Mass166_5"),
    originalEvents = cms.untracked.double(4469095),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBar_Mass178_5 = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar_Mass178_5"),
    originalEvents = cms.untracked.double(4733483),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TW_Mass166_5 = cms.PSet(
    crossSection = tW_XSec,
    channel = cms.untracked.string("TW_Mass166_5"),
    originalEvents = cms.untracked.double(1489880),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TbarW_Mass166_5 = cms.PSet(
    crossSection = tbarW_XSec,
    channel = cms.untracked.string("TW_Mass166_5"),
    originalEvents = cms.untracked.double(1478200),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TW_Mass178_5 = cms.PSet(
    crossSection = tW_XSec,
    channel = cms.untracked.string("TW_Mass178_5"),
    originalEvents = cms.untracked.double(1493428),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TbarW_Mass178_5 = cms.PSet(
    crossSection = tbarW_XSec,
    channel = cms.untracked.string("TW_Mass178_5"),
    originalEvents = cms.untracked.double(1493389),
    finalLumi = lumi,
    Season = cms.untracked.string(PileUpSeason53X),
    )


