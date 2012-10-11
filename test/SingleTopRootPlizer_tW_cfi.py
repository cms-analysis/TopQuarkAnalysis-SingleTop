import FWCore.ParameterSet.Config as cms

TreesDileptontW = cms.EDAnalyzer('SingleTopSystematicsTreesDumper_tW',
#General Info
#systematics = cms.untracked.vstring("BTagUp","BTagDown","MisTagUp","MisTagDown","JESUp","JESDown","UnclusteredMETUp","UnclusteredMETDown","PUUp","PUDown"),
systematics = cms.untracked.vstring("JESUp","JESDown","UnclusteredMETUp","UnclusteredMETDown","JERUp","JERDown"),
#systematics = cms.untracked.vstring("JESUp","JESDown","UnclusteredMETUp","UnclusteredMETDown"),
#systematics = cms.untracked.vstring(""),
#rateSystematics = cms.untracked.vstring("WLightRateUp",                                        "WLightRateDown",                                        "TTBarRateUp",                                        "Ttbarratedown ",                                        "WHFRateUp",                                        "WHFRateDown"),
rateSystematics = cms.untracked.vstring(),
doPU = cms.untracked.bool(True),
#doResol  = cms.untracked.bool(False),

#algo  = cms.untracked.string("TCHPT"),
algo  = cms.untracked.string("CSVT"),#doLooseBJetVeto= cms.untracked.bool(True),

doResol  = cms.untracked.bool(True),
takeBTagSFFromDB = cms.untracked.bool(False),
#dataPUFile = cms.untracked.string("pileUpDistr.root"),
#mcPUFile = cms.untracked.string("pileupdistr_TChannel.root"),
#puHistoName = cms.untracked.string("pileUpDumper/PileUpTChannel"),
#mode = cms.untracked.string("pt"),
#maxPtCut = cms.untracked.double("45"),

#x1/x2
x1 = cms.InputTag("PDFInfo","x1"),
x2 = cms.InputTag("PDFInfo","x2"),
id1 = cms.InputTag("PDFInfo","id1"),
id2 = cms.InputTag("PDFInfo","id2"),
scalePDF = cms.InputTag("PDFInfo","scalePDF"),
doPDF =cms.untracked.bool(True),

channelInfo = cms.PSet(
    crossSection = cms.untracked.double(20.93),
    channel = cms.untracked.string("TChannel"),
    originalEvents = cms.untracked.double(480000),
    finalLumi = cms.untracked.double(14.5),
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    loosePtCut = cms.untracked.double(30.0),#Default 30.0 GeV
    RelIsoCut = cms.untracked.double(0.1),
    mcPUFile = cms.untracked.string("pileupdistr_TChannel.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTChannel"),

    ),

#Electrons
electronsPt = cms.InputTag("nTupleElectrons","tightElectronsPt"),  
electronsEta = cms.InputTag("nTupleElectrons","tightElectronsEta"),  
electronsPhi = cms.InputTag("nTupleElectrons","tightElectronsPhi"),  
electronsEnergy = cms.InputTag("nTupleElectrons","tightElectronsE"),  
electronsCharge = cms.InputTag("nTupleElectrons","tightElectronsCharge"),  
electronsDB = cms.InputTag("nTupleElectrons","tightElectronsAbsoluteDB"),  
electronsDXY = cms.InputTag("nTupleElectrons","tightElectronsPVDxy"),  
electronsDZ = cms.InputTag("nTupleElectrons","tightElectronsPVDz"),  
electronsRelIso = cms.InputTag("nTupleElectrons","tightElectronsPFRelIso"),  
electronsDeltaCorrectedRelIso = cms.InputTag("nTupleElectrons","tightElectronsPFDeltaCorrectedRelIso"),  
electronsRhoCorrectedRelIso = cms.InputTag("nTupleElectrons","tightElectronsPFRhoCorrectedRelIso"),  

electronsEleId70cIso = cms.InputTag("nTupleElectrons","tightElectronsSimpleEleId70cIso"),  
electronsEleId80cIso = cms.InputTag("nTupleElectrons","tightElectronsSimpleEleId80cIso"),  
electronsEleId90cIso = cms.InputTag("nTupleElectrons","tightElectronsSimpleEleId90cIso"),  
electronsEleId95cIso = cms.InputTag("nTupleElectrons","tightElectronsSimpleEleId95cIso"),  
electronsMVAID = cms.InputTag("nTupleElectrons","tightElectronsMvaTrigV0"),  

#Muons
muonsPt = cms.InputTag("nTupleMuons","tightMuonsPt"),  
muonsEta = cms.InputTag("nTupleMuons","tightMuonsEta"),  
muonsPhi = cms.InputTag("nTupleMuons","tightMuonsPhi"),  
muonsEnergy = cms.InputTag("nTupleMuons","tightMuonsE"),  
muonsCharge = cms.InputTag("nTupleMuons","tightMuonsCharge"),  
muonsDB = cms.InputTag("nTupleMuons","tightMuonsAbsoluteDB"),  
muonsDXY = cms.InputTag("nTupleMuons","tightMuonsPVDxy"),  
muonsDZ = cms.InputTag("nTupleMuons","tightMuonsPVDz"),  
muonsRelIso = cms.InputTag("nTupleMuons","tightMuonsPFRelIso"),  
muonsDeltaCorrectedRelIso = cms.InputTag("nTupleMuons","tightMuonsPFDeltaCorrectedRelIso"),  
muonsRhoCorrectedRelIso = cms.InputTag("nTupleMuons","tightMuonsPFRhoCorrectedRelIso"),  


#Vertex
#Vertices
vertexZ = cms.InputTag("nTupleVertices","z"),  
vertexchi = cms.InputTag("nTupleVertices","rho"),  
vertexrho = cms.InputTag("nTupleVertices","chi"),  
vertexNDOF = cms.InputTag("nTupleVertices","ndof"),  

nVerticesPlus = cms.InputTag("NVertices","PileUpP1"),
nVerticesMinus = cms.InputTag("NVertices","PileUpM1"),
nVertices = cms.InputTag("NVertices","PileUpTrue"),

#Jets

genjetsPt =cms.InputTag("genJetsPF","genJetsPt"),  
genjetsEta =cms.InputTag("genJetsPF","genJetsEta"),  
#genjetsPhi =cms.InputTag("genJetsPF","genJetsPhi"),  
#genJetsPt =cms.InputTag("nTupleTopJetsPF","topJetsPFPt"),  
#genJetsEta =cms.InputTag("nTupleTopJetsPF","topJetsPFEta"),  

jetsPt = cms.InputTag("nTupleTopJetsPF","topJetsPFPt"),  
jetsPhi = cms.InputTag("nTupleTopJetsPF","topJetsPFPhi"),  
jetsEta = cms.InputTag("nTupleTopJetsPF","topJetsPFEta"),  
jetsEnergy = cms.InputTag("nTupleTopJetsPF","topJetsPFE"),  

jetsTCHP = cms.InputTag("nTupleTopJetsPF","topJetsPFTrackCountingHighPur"),  
jetsCSV =  cms.InputTag("nTupleTopJetsPF","topJetsPFCombinedSecondaryVertexBJetTags"),  
jetsRMS = cms.InputTag("nTupleTopJetsPF","topJetsPFRMS"),  
jetsCHEmEn = cms.InputTag("nTupleTopJetsPF","topJetsPFCHEmEn"),  
jetsCHHadEn = cms.InputTag("nTupleTopJetsPF","topJetsPFCHHadEn"),  
jetsCHMult = cms.InputTag("nTupleTopJetsPF","topJetsPFChargedMultiplicity"),  
jetsNeuEmEn = cms.InputTag("nTupleTopJetsPF","topJetsPFNeuEmEn"),  
jetsNeuHadEn = cms.InputTag("nTupleTopJetsPF","topJetsPFNeuHadEn"),  
jetsNeuMult = cms.InputTag("nTupleTopJetsPF","topJetsPFNeutralMultiplicity"),  
jetsBeta = cms.InputTag("nTupleTopJetsPF","topJetsPFBeta"),  
jetsBetaStar = cms.InputTag("nTupleTopJetsPF","topJetsPFBetaStar"),  
jetsFlavour = cms.InputTag("nTupleTopJetsPF","topJetsPFFlavour"),   
jetsDZ = cms.InputTag("nTupleTopJetsPF","topJetsPFdZ"),  

jetsPUChargedDiscr = cms.InputTag("nTupleTopJetsPF","topJetsPFPUChargedDiscriminant"),  
jetsPUChargedWP = cms.InputTag("nTupleTopJetsPF","topJetsPFPUChargedWorkingPoint"),  
jetsPUFullDiscr = cms.InputTag("nTupleTopJetsPF","topJetsPFPUFullDiscriminant"),  
jetsPUFullWP = cms.InputTag("nTupleTopJetsPF","topJetsPFPUFullWorkingPoint"),  



#REMOVED###jetsCorrTotal = cms.InputTag("nTupleTopJetsPF","topJetsPFJetCorrTotal"),   

#MET 

METPhi = cms.InputTag("nTuplePatMETsPF","patMETsPFPhi"),
METPt = cms.InputTag("nTuplePatMETsPF","patMETsPFPt"),

UnclusteredMETPx = cms.InputTag("UnclusteredMETPF","UnclusteredMETPx"),
UnclusteredMETPy = cms.InputTag("UnclusteredMETPF","UnclusteredMETPy"),


)

