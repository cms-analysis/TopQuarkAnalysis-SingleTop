import FWCore.ParameterSet.Config as cms



#muon skim part
preselectedMuons = cms.EDFilter("PATMuonSelector",
  src = cms.InputTag("cleanPatMuons"),
  cut = cms.string('pt > 10 & abs(eta) < 2.1 & isGlobalMuon'),
  filter = cms.bool(False)                                
)

#electron skim part
preselectedElectrons = cms.EDProducer("SingleTopElectronProducer",
  src = cms.InputTag("cleanPatElectrons"),
  cut = cms.string('pt >  20 & abs(eta) < 2.4'),
  isData = cms.untracked.bool(False),                                   
  id = cms.string("none"), 
  useConversionVeto = cms.untracked.bool(False),
)

#loose second electron skim part
looseElectrons = cms.EDProducer("SingleTopElectronProducer",
  src = cms.InputTag("cleanPatElectrons"),
  cut = cms.string('pt >  20 & abs(eta) < 2.4'),
  id = cms.string("cIso95"), 
  useConversionVeto = cms.untracked.bool(False),
)

###Cleaning options for jets:

preselectedJets = cms.EDFilter("PATJetSelector",
  src = cms.InputTag("cleanPatJets"),
  cut = cms.string('pt >  30 & abs(eta) < 5.0'),
  filter = cms.bool(False)                                
)

topJets = cms.EDProducer("SingleTopJetsProducer",
                         src = cms.InputTag("preselectedJets"),
                         eleSrc = cms.InputTag("topElectrons"),
                         muSrc = cms.InputTag("topMuons"),
                         isJPT = cms.untracked.bool(True),
                         isPF = cms.untracked.bool(False),
)

topJetsPF = topJets.clone(
      src = cms.InputTag("selectedPatJetsPFlow"),
      isJPT = cms.untracked.bool(False),
      isPF = cms.untracked.bool(True),
      )


topMuons = cms.EDFilter("PATMuonSelector",
                        src = cms.InputTag("preselectedMuons"),
                        filter = cms.bool(False),
                        cut = cms.string("pt > 0")
                        )
#Met skim part
preselectedMETs = cms.EDFilter("PATMETSelector",
  src = cms.InputTag("patMETs"),
  cut = cms.string('pt >   0'),
  filter = cms.bool(False)                                
)

#Part of BJets tagging and Forward Jets production
allTopJets = cms.EDProducer("SingleTopJetsProducer",
                            jetsSource = cms.InputTag("preselectedJets"),
                            )

topMuonsPF =  topMuons.clone(jetSrc = cms.InputTag("topJetsPF")) 

topElectrons = cms.EDProducer("SingleTopElectronProducer",
                            src = cms.InputTag("preselectedElectrons"),
                            filter = cms.bool(False),
                            id = cms.string("cIso70"), 
                            cut = cms.string("pt > 0"),
                            useConversionVeto = cms.untracked.bool(True),
                            )


bJets = cms.EDFilter("PATJetSelector",
                     src = cms.InputTag("topJets"),
#                     src = cms.InputTag("preselectedJets"),
                     cut = cms.string('pt>0'),
                     filter = cms.bool(False)
                     )

bJetsPF = cms.EDFilter("PATJetSelector",
                     src = cms.InputTag("topJetsPF"),
#                     src = cms.InputTag("preselectedJets"),
                     cut = cms.string('pt>0'),
                     filter = cms.bool(False)
                     )


forwardJetsPF = cms.EDFilter("PATJetSelector",
                     src = cms.InputTag("topJetsPF"),
#                     src = cms.InputTag("preselectedJets"),
                     cut = cms.string('pt>0'),
                     filter = cms.bool(False)
                     )

patPFBJets = cms.EDFilter("PATJetSelector",
                          src = cms.InputTag("patJetsPFlow"),
                          cut = cms.string('pt>0'),
                          filter = cms.bool(False)
                          )

antiBJets = cms.EDFilter("PATJetSelector",
                     src = cms.InputTag("topJets"),
#                     src = cms.InputTag("preselectedJets"),
                     cut = cms.string('pt>0'),
                     filter = cms.bool(False)
                     )


forwardJets = cms.EDFilter("PATJetSelector",
                     src = cms.InputTag("topJets"),
#                     src = cms.InputTag("preselectedJets"),
                     cut = cms.string('pt>0'),
                     filter = cms.bool(False)
                     )

allTopLeptons = cms.EDProducer("SingleTopLeptonsProducer",
                                electronsSource = cms.InputTag("preselectedElectrons"),
                                muonsSource = cms.InputTag("preselectedMuons"),
                                jetsSource = cms.InputTag("preselectedJets"),
                                )

#Top Production : candidate made of a lepton, MET and a b-tagged Jet
recoTops = cms.EDProducer("TopProducer",
                                  electronsSource = cms.InputTag("topElectrons"),
                                  muonsSource = cms.InputTag("topMuons"),
                                  jetsSource = cms.InputTag("bJets"),
                          METsSource = cms.InputTag("preselectedMETs"),
#                                  METsSource = cms.InputTag("patMETsPFlow"),
                                )

boostedTops = cms.EDProducer(
    'NamedCompositeCandidateBooster',
    src = cms.InputTag('recoTops'),
    boostSrc = cms.InputTag('recoTops')
    )

boostedForwardJets = cms.EDProducer(
    'PATJetBooster',
    src = cms.InputTag('forwardJets'),
    boostSrc = cms.InputTag('recoTops')
    )

#Part of MC Truth particles production
MCTruthParticles = cms.EDProducer("SingleTopTChannelMCProducer",
                                          genParticlesSource = cms.InputTag("genParticles")
                                          )


#Part for control samples:

#AntiIso cut for QCD: 
topMuonsAntiIso = topMuons.clone(src = cms.InputTag("cleanPatMuons"))
topElectronsAntiIso = topElectrons.clone(src = cms.InputTag("cleanPatElectrons"))


preselectedMuonsAntiIso = topMuons.clone()
preselectedElectronsAntiIso = topElectrons.clone()

topJetsAntiIso = topJets.clone(muSrc = cms.InputTag("topMuonsAntiIso"),eleSrc= cms.InputTag("topElectronsAntiIso"))

bJetsAntiIso = bJets.clone(src=cms.InputTag('topJetsAntiIso'))
antiBJetsAntiIso = antiBJets.clone(src=cms.InputTag('topJetsAntiIso'))
forwardJetsAntiIso = forwardJets.clone(src=cms.InputTag('topJetsAntiIso'))

