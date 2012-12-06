import FWCore.ParameterSet.Config as cms


#muon skim part

looseMuons = cms.EDProducer("SingleTopMuonProducer",
  src = cms.InputTag("selectedPatMuons"),
  cut = cms.string('pt >  20 & abs(eta) < 2.4'),
 # rho = cms.InputTag("kt6PFJetsCentralNeutral:rho"),
 rho = cms.InputTag("kt6PFJetsForIsolation","rho"),
                              
)

#electron skim part
#looseElectrons = cms.EDFilter("PATElectronSelector",
#  src = cms.InputTag("selectedPatElectrons"),
#  cut = cms.string('pt >  20 & abs(eta) < 2.4'),
#)

looseElectrons = cms.EDProducer("SingleTopElectronProducer",
  src = cms.InputTag("selectedPatElectrons"),
  cut = cms.string('pt >  20 & abs(eta) < 2.4'),
# rho = cms.InputTag("kt6PFJetsCentralNeutral:rho"),
  rho = cms.InputTag("kt6PFJetsForIsolation","rho"),
  category = cms.untracked.string("veto"),
)

looseElectronsEle = cms.EDProducer("SingleTopElectronProducer",
  src = cms.InputTag("selectedPatElectrons"),
  cut = cms.string('pt >  20 & abs(eta) < 2.4'),
  rho = cms.InputTag("kt6PFJetsForIsolation","rho"),
#  rho = cms.InputTag("kt6PFJetsCentralNeutral:rho"),
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

#n gen particles Info
NGenParticles = cms.EDProducer("SingleTopNGenParticlesProducer")

#PDF Info
PDFInfo = cms.EDProducer("PDFInfoDumper",
                         )

#topJetsPF = cms.EDFilter("PATJetSelector",
##                         preselection = cms.string(''),
#                         src = cms.InputTag("selectedPatJets"),
#                         cut = cms.string('pt >  20 & abs(eta) < 5.'),
#                         checkOverlaps = cms.PSet(),
#                           )



topJetsPF = cms.EDProducer("SingleTopJetsProducer",
#                        preselection = cms.string(''),
                         electronsSrc = cms.InputTag("selectedPatElectrons"),
                         src = cms.InputTag("selectedPatJets"),
                         cut = cms.string('pt >  20 & abs(eta) < 5.'),
                         puFullDiscriminant = cms.InputTag("puJetMva","fullDiscriminant"),
                         puFullID  = cms.InputTag("puJetMva","fullId"),
                         puChargedDiscriminant = cms.InputTag("puJetMvaChs","fullDiscriminant"),
                         puChargedID  = cms.InputTag("puJetMvaChs","fullId"),
                           puIDVariables  = cms.InputTag("puJetId"),
                           removeOverlap = cms.untracked.bool(False),
                         #                         checkOverlaps  cms.PSet(),
                           )



tightElectrons = cms.EDProducer("SingleTopElectronProducer",
  src = cms.InputTag("selectedPatElectrons"),
  cut = cms.string('pt >  20 & abs(eta) < 2.4'),
#  rho = cms.InputTag("kt6PFJetsCentralNeutral:rho"),
  rho = cms.InputTag("kt6PFJetsForIsolation","rho"),
  category = cms.untracked.string("tight"),
)

tightElectronsZeroIso = cms.EDProducer("SingleTopElectronProducer",
  src = cms.InputTag("patElectronsZeroIso"),
  cut = cms.string('pt >  20 & abs(eta) < 2.4'),
#  rho = cms.InputTag("kt6PFJetsCentralNeutral:rho"),
  rho = cms.InputTag("kt6PFJetsForIsolation","rho"),
  category = cms.untracked.string("qcd"),
  isData = cms.untracked.bool(False),
 )



tightMuons = cms.EDProducer("SingleTopMuonProducer",
  src = cms.InputTag("selectedPatMuonsTriggerMatch"),
  cut = cms.string('pt >  20 & abs(eta) < 2.4'),
#  rho = cms.InputTag("kt6PFJetsCentralNeutral:rho"),
  rho = cms.InputTag("kt6PFJetsForIsolation","rho"),
)

tightMuonsTest = cms.EDFilter("PATMuonSelector",
  src = cms.InputTag("selectedPatMuons"),
  cut = cms.string('pt >  20 & abs(eta) < 2.4'),
)

tightMuonsZeroIso = cms.EDProducer("SingleTopMuonProducer",
  src = cms.InputTag("patMuonsZeroIso"),
  cut = cms.string('pt >  20 & abs(eta) < 2.4'),
#  rho = cms.InputTag("kt6PFJetsCentralNeutral:rho"),
  rho = cms.InputTag("kt6PFJetsForIsolation","rho"),
)

#Met skim part
preselectedMETs = cms.EDFilter("PATMETSelector",
  src = cms.InputTag("patMETs"),
  cut = cms.string('pt >   0'),
  filter = cms.bool(False)                                
)


#Part of MC Truth particles production
#MCTruthParticles = cms.EDProducer("SingleTopTChannelMCProducer",
#                                          genParticlesSource = cms.InputTag("genParticles")
#                                          )

MCTruthParticles = cms.EDProducer("SingleTopMCProducer",
                                  genParticlesSource = cms.InputTag("genParticles")
                                  )

##################Trigger matching part


PatMuonTriggerMatchHLTIsoMu24 = cms.EDProducer(
      "PATTriggerMatcherDRDPtLessByR"                 # match by DeltaR only, best match by DeltaR
      , src     = cms.InputTag( "selectedPatMuons" )
      , matched = cms.InputTag( "patTrigger" )          # default producer label as defined in PhysicsTools/PatAlgos/python/triggerLayer1/triggerProducer_cfi.py
#      , matchedCuts = cms.string( 'path( "HLT_IsoMu24_eta2p1_v*" )' )
      , matchedCuts = cms.string( 'path( "HLT_IsoMu24_eta2p1_v13" )' )
      , maxDPtRel = cms.double( 0.5 )
      , maxDeltaR = cms.double( 0.5 )
      , resolveAmbiguities    = cms.bool( True )        # only one match per trigger object
      , resolveByMatchQuality = cms.bool( True )        # take best match found per reco object: by DeltaR here (s. above)
      )

PatJetTriggerMatchHLTIsoMuBTagIP = cms.EDProducer(
      "PATTriggerMatcherDRDPtLessByR"                 # match by DeltaR only, best match by DeltaR
      , src     = cms.InputTag( "selectedPatJets" )
      , matched = cms.InputTag( "patTrigger" )          # default producer label as defined in PhysicsTools/PatAlgos/python/triggerLayer1/triggerProducer_cfi.py
#      , matchedCuts = cms.string( 'path( "HLT_IsoMu24_eta2p1_v*" )' )
      , matchedCuts = cms.string( 'path( "HLT_Mu17_eta2p1_CentralPFNoPUJet30_BTagIPIter_v*" )' )
      , maxDPtRel = cms.double( 0.5 )
      , maxDeltaR = cms.double( 0.5 )
      , resolveAmbiguities    = cms.bool( True )        # only one match per trigger object
      , resolveByMatchQuality = cms.bool( True )        # take best match found per reco object: by DeltaR here (s. above)
      )


PatElectronTriggerMatchHLTEle27WP80 = cms.EDProducer(
      "PATTriggerMatcherDRDPtLessByR"                 # match by DeltaR only, best match by DeltaR
      , src     = cms.InputTag( "selectedPatElectrons" )
      , matched = cms.InputTag( "patTrigger" )          # default producer label as defined in PhysicsTools/PatAlgos/python/triggerLayer1/triggerProducer_cfi.py
      , matchedCuts = cms.string( 'path( "HLT_Ele27_WP80_v*" )' )
      , maxDPtRel = cms.double( 0.5 )
      , maxDeltaR = cms.double( 0.5 )
      , resolveAmbiguities    = cms.bool( True )        # only one match per trigger object
      , resolveByMatchQuality = cms.bool( True )        # take best match found per reco object: by DeltaR here (s. above)
      )



triggerMatchingSequence = cms.Sequence(
    PatMuonTriggerMatchHLTIsoMu24 # +#    somePatMuonTriggerMatchHLTEle27WP80
    )

#triggerMatchingInputTags = cms.VInputTag(
#    cms.InputTag( 'somePatMuonTriggerMatchHLTIsoMu24' ),
#    cms.InputTag( 'somePatMuonTriggerMatchHLTEle27WP80' ),
#)

