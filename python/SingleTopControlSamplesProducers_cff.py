import FWCore.ParameterSet.Config as cms

###CosThetaStar
from TopQuarkAnalysis.SingleTop.SingleTopProducers_cff import *
from TopQuarkAnalysis.SingleTop.SingleTopSelectors_cff import *

#Part of single top t-Channel sample
singleTopObservablesTSample = cms.EDProducer(
    'TopCosThetaStarDumper',
    jetsSource = cms.InputTag('boostedForwardJets'), 
    topsSource = cms.InputTag('boostedTops'), 
    )


###Part of W enriched sample
recoTopsWSamplePseudoBTags = recoTops.clone(jetsSource = cms.InputTag('pseudoBJets'))

boostedTopsWSamplePseudoBTagsTops = boostedTops.clone(
    src = cms.InputTag('recoTopsWSamplePseudoBTags'),
    boostSrc = cms.InputTag('recoTopsWSamplePseudoBTags'),
)

boostedForwardJetsWSamplePseudoBTagsTops = boostedForwardJets.clone(
    boostSrc = cms.InputTag('recoTopsWSamplePseudoBTags'),
    )




###Part of QCD enriched samples
recoTopsAntiIso = recoTops.clone(
    jetsSource = cms.InputTag('bJetsAntiIso'),
    electronsSource = cms.InputTag('topElectronsAntiIso'),
    muonsSource = cms.InputTag('topMuonsAntiIso'),
    )


boostedTopsAntiIsoTops = boostedTops.clone(
    src = cms.InputTag('recoTopsAntiIso'),
    boostSrc = cms.InputTag('recoTopsAntiIso'),
    )

boostedForwardJetsAntiIsoTops = boostedForwardJets.clone(
    src = cms.InputTag('forwardJetsAntiIso'),
    boostSrc = cms.InputTag('recoTopsAntiIso'),
    )



#### W-Like samples
recoTopsWSamplePseudoBTagsAntiIso = recoTopsAntiIso.clone(jetsSource = cms.InputTag('pseudoBJetsAntiIso'))

boostedTopsWSamplePseudoBTagsAntiIsoTops = boostedTops.clone(
    src = cms.InputTag('recoTopsWSamplePseudoBTagsAntiIso'),
    boostSrc = cms.InputTag('recoTopsWSamplePseudoBTagsAntiIso'),
    )

boostedForwardJetsWSamplePseudoBTagsAntiIsoTops = boostedForwardJets.clone(
    src = cms.InputTag('forwardJetsAntiIso'),
    boostSrc = cms.InputTag('recoTopsWSamplePseudoBTagsAntiIso'),
    )



###Produce the observables

singleTopObservablesWSample = singleTopObservablesTSample.clone(
    jetsSource = cms.InputTag('boostedForwardJetsWSamplePseudoBTagsTops'),
    topsSource = cms.InputTag('boostedTopsWSamplePseudoBTagsTops'),
)

singleTopObservablesTTBarSample = singleTopObservablesTSample.clone()

singleTopObservablesAntiIso = singleTopObservablesTSample.clone(
    jetsSource = cms.InputTag('boostedForwardJetsAntiIsoTops'),
    topsSource = cms.InputTag('boostedTopsAntiIsoTops'),
    )

###Produce the observables

singleTopObservablesWSampleAntiIso = singleTopObservablesTSample.clone(
    jetsSource = cms.InputTag('boostedForwardJetsWSamplePseudoBTagsAntiIsoTops'),
    topsSource = cms.InputTag('boostedTopsWSamplePseudoBTagsAntiIsoTops'),
)


###Cuts on W transverse mass
SingleTopWtransverseMassFilter = cms.EDFilter(
    'SingleTopDoubleFilter',
    src = cms.InputTag("singleTopObservablesTSample","topWTransverseMass"),
    min = cms.untracked.double(50.),
    max = cms.untracked.double(14000.),
    )

SingleTopWtransverseMassFilterWSample = SingleTopWtransverseMassFilter.clone(
    src = cms.InputTag("singleTopObservablesWSample","topWTransverseMass"),
    )

SingleTopWtransverseMassFilterTTBarSample = SingleTopWtransverseMassFilter.clone(
    src = cms.InputTag("singleTopObservablesTTBarSample","topWTransverseMass"),
    ) 



pseudoBJets = preselectedJets.clone(
    src= cms.InputTag("topJets"),
    checkOverlaps = cms.PSet(
    myForwardJets = cms.PSet(
    src = cms.InputTag('forwardJets'),
    preselection = cms.string(""),
    algorithm = cms.string('byDeltaR'),
    deltaR = cms .double(0.05),
    checkRecoComponents = cms.bool(False),
    pairCut =cms.string(""),
    requireNoOverlaps = cms.bool(False),
    ),
    
    ),
    finalCut = cms.string('pt > 30 & abs(eta) < 2.5 & !hasOverlaps("myForwardJets") && bDiscriminator("trackCountingHighPurBJetTags") < 5.36'),
)

countWSamplePseudoBTags = countBTags.clone(src = cms.InputTag('pseudoBJets')) 


###QCD AntiIso W-Like sample 

pseudoBJetsAntiIso = topJetsAntiIso.clone(
    checkOverlaps = cms.PSet(
    myForwardJetsAntiIso = cms.PSet(
    src = cms.InputTag('forwardJetsAntiIso'),
    preselection = cms.string(""),
    algorithm = cms.string('byDeltaR'),
    deltaR = cms .double(0.05),
    checkRecoComponents = cms.bool(False),
    pairCut =cms.string(""),
    requireNoOverlaps = cms.bool(False),
    ),
    
    ),
    finalCut = cms.string('pt > 30 & abs(eta) < 2.5 & !hasOverlaps("myForwardJetsAntiIso") && bDiscriminator("trackCountingHighPurBJetTags") < 5.36'),
)

countWSamplePseudoBTagsAntiIso = countBTags.clone(src = cms.InputTag('pseudoBJetsAntiIso')) 


