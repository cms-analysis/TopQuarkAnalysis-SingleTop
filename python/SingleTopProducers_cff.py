import FWCore.ParameterSet.Config as cms


#muon skim part

looseMuons = cms.EDProducer("SingleTopMuonProducer",
  src = cms.InputTag("selectedPatMuons"),
  cut = cms.string('pt >  20 & abs(eta) < 2.4'),
  rho = cms.InputTag("kt6PFJetsCentralNeutral:rho"),
                              
)

#electron skim part
#looseElectrons = cms.EDFilter("PATElectronSelector",
#  src = cms.InputTag("selectedPatElectrons"),
#  cut = cms.string('pt >  20 & abs(eta) < 2.4'),
#)

looseElectrons = cms.EDProducer("SingleTopElectronProducer",
  src = cms.InputTag("selectedPatElectrons"),
  cut = cms.string('pt >  20 & abs(eta) < 2.4'),
  rho = cms.InputTag("kt6PFJetsCentralNeutral:rho"),
  category = cms.untracked.string("veto"),
)

looseElectronsEle = cms.EDProducer("SingleTopElectronProducer",
  src = cms.InputTag("selectedPatElectrons"),
  cut = cms.string('pt >  20 & abs(eta) < 2.4'),
  rho = cms.InputTag("kt6PFJetsCentralNeutral:rho"),
  category = cms.untracked.string("veto"),
)



#electrons for z veto part
zVetoElectrons = cms.EDFilter("PATElectronSelector",
  src = cms.InputTag("selectedPatElectrons"),
  cut = cms.string('pt >  20 & abs(eta) < 2.4'),
)

preselectedJets = cms.EDFilter("PATJetSelector",
  src = cms.InputTag("selectedPatJets"),
  cut = cms.string('pt >  30 & abs(eta) < 5.0'),
  filter = cms.bool(False)                                
)

#UnclusteredMET
UnclusteredMETPF = cms.EDProducer("SingleTopUnclusteredMETProducer",
                                  metSource = cms.InputTag("patMETs"),
                                  jetsSource = cms.InputTag("selectedPatJets"),
                                  electronsSource = cms.InputTag("selectedPatElectrons"),
                                  muonsSource = cms.InputTag("selectedPatMuons"),
                                  )


UnclusteredType1METPF = cms.EDProducer("SingleTopUnclusteredMETProducer",
                                                                         metSource = cms.InputTag("patType1CorrectedPFMet"),
                                                                         jetsSource = cms.InputTag("selectedPatJets"),
                                                                         electronsSource = cms.InputTag("patElectrons"),
                                                                         muonsSource = cms.InputTag("patMuons"),
                                                                         )

#genJets:
genJetsPF = cms.EDProducer("SingleTopGenJetPtEtaProducer",
                                                    jetsSource = cms.InputTag("topJetsPF"),
                                                    )



#PDF Info
NVertices = cms.EDProducer("SingleTopPileUpProducer")

#PDF Info
PDFInfo = cms.EDProducer("PDFInfoDumper",
                         )

topJetsPF = cms.EDFilter("PATJetSelector",
                         preselection = cms.string(''),
                         src = cms.InputTag("selectedPatJets"),
                         cut = cms.string('pt >  20 & abs(eta) < 5.'),
                         checkOverlaps = cms.PSet(),
                           )



tightElectrons = cms.EDProducer("SingleTopElectronProducer",
  src = cms.InputTag("selectedPatElectrons"),
  cut = cms.string('pt >  20 & abs(eta) < 2.4'),
  rho = cms.InputTag("kt6PFJetsCentralNeutral:rho"),
  category = cms.untracked.string("tight"),
)

tightElectronsZeroIso = cms.EDProducer("SingleTopElectronProducer",
  src = cms.InputTag("patElectronsZeroIso"),
  cut = cms.string('pt >  20 & abs(eta) < 2.4'),
  rho = cms.InputTag("kt6PFJetsCentralNeutral:rho"),
  category = cms.untracked.string("tight"),
)



tightMuons = cms.EDProducer("SingleTopMuonProducer",
  src = cms.InputTag("selectedPatMuons"),
  cut = cms.string('pt >  20 & abs(eta) < 2.4'),
  rho = cms.InputTag("kt6PFJetsCentralNeutral:rho"),
)

tightMuonsTest = cms.EDFilter("PATMuonSelector",
  src = cms.InputTag("selectedPatMuons"),
  cut = cms.string('pt >  20 & abs(eta) < 2.4'),
)

tightMuonsZeroIso = cms.EDProducer("SingleTopMuonProducer",
  src = cms.InputTag("patMuonsZeroIso"),
  cut = cms.string('pt >  20 & abs(eta) < 2.4'),
  rho = cms.InputTag("kt6PFJetsCentralNeutral:rho"),
)

#Met skim part
preselectedMETs = cms.EDFilter("PATMETSelector",
  src = cms.InputTag("patMETs"),
  cut = cms.string('pt >   0'),
  filter = cms.bool(False)                                
)


#Part of MC Truth particles production
MCTruthParticles = cms.EDProducer("SingleTopTChannelMCProducer",
                                          genParticlesSource = cms.InputTag("genParticles")
                                          )

