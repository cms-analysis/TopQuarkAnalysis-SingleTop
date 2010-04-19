#ifndef __PRESELECTION_H__
#define __PRESELECTION_H__

//----------------- system include files
#include <memory>
#include <iostream>
#include <list>
#include <string>
#include <sstream>
#include <map>
#include <vector>
#include <algorithm>

//----------------- cmssw includes

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include <FWCore/Framework/interface/Run.h>

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Framework/interface/TriggerNamesService.h"
#include "FWCore/ServiceRegistry/interface/Service.h" 

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "JetMETCorrections/JetVertexAssociation/interface/JetVertexMain.h"
#include "DataFormats/HepMCCandidate/interface/PdfInfo.h"

//--------------------PAT includes
#include "DataFormats/PatCandidates/interface/Particle.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Jet.h"


//--------------------ROOT includes
#include "TFile.h"
#include "TTree.h"
#include "TChain.h"
#include "TLorentzVector.h"
#include "TH1.h"

//--------------------CATO includes
#include "TopQuarkAnalysis/SingleTop/interface/Jet.h"
#include "TopQuarkAnalysis/SingleTop/interface/MET.h"
#include "TopQuarkAnalysis/SingleTop/interface/Event.h"
#include "TopQuarkAnalysis/SingleTop/interface/Lepton.h"
#include "TopQuarkAnalysis/SingleTop/interface/Trigger.h"
#include "TopQuarkAnalysis/SingleTop/interface/PDFInfo.h"
#include "TopQuarkAnalysis/SingleTop/interface/Def.h"
#include "TopQuarkAnalysis/SingleTop/interface/SingleTopMC.h"
#include "TopQuarkAnalysis/SingleTop/interface/SchannelMC.h"
#include "TopQuarkAnalysis/SingleTop/interface/CutFlowTable.h"
#include "TopQuarkAnalysis/SingleTop/interface/SampleInfo.h"
#include "TopQuarkAnalysis/SingleTop/interface/STParton.h"
#include "TopQuarkAnalysis/SingleTop/interface/SSParton.h"
#include "TopQuarkAnalysis/SingleTop/interface/WJetParton.h"
#include "TopQuarkAnalysis/SingleTop/interface/TTbarParton.h"
#include "TopQuarkAnalysis/SingleTop/interface/QCDParton.h"


using namespace std;
using namespace edm;
using namespace reco;

typedef CatoCMS::Event 	        CatoCMSEvent;
typedef CatoCMS::Jet 	        CatoCMSJet;
typedef CatoCMS::MET 	        CatoCMSMET;
typedef CatoCMS::Lepton         CatoCMSLepton;
typedef CatoCMS::Trigger        CatoCMSTrigger;
typedef CatoCMS::PDFInfo        CatoCMSPDFInfo;

typedef CatoCMS::Def 	        CatoCMSDef;

typedef CatoCMS::SingleTopMC    CatoCMSSingleTopMC;
typedef CatoCMS::SchannelMC     CatoCMSSchannelMC;
typedef CatoCMS::WJetsMC        CatoCMSWJetsMC;
typedef CatoCMS::TTbarMC        CatoCMSTTbarMC;
typedef CatoCMS::QCDMC          CatoCMSQCDMC;

typedef CatoCMS::CutFlowTable   CatoCMSCutFlowTable;
typedef CatoCMS::SampleInfo     CatoCMSSampleInfo;



class Preselection : public edm::EDAnalyzer {
 public:
  explicit Preselection(const edm::ParameterSet&);
  ~Preselection();
  
  
 private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  void         MCStatOut(ostream& os);
  void         EventInfo();
  
  // ----------member data ---------------------------

  edm::Event*   iEvent;

  bool          triggerInfo;
  bool          doPresel;
  bool          no0jets;
  
  unsigned int           MuTrigIdx;
  unsigned int           EleTrigIdx;
  
  InputTag      electronProducer;
  double	electron_cut_pt;
  double	electron_cut_eta;
  
  InputTag      muonProducer;
  double        muon_cut_pt;
  double 	muon_cut_eta;
  
  InputTag      jetProducer;
  string        jetAlgo;
  double        jet_loosecut_pt; //loose_jet_cut
  double 	jet_tightcut_pt; // tight jet cut
  double 	jet_cut_eta;     // eta cut

  InputTag      metProducer;
  
  std::vector<std::string> triggernames;
  
  InputTag      vertexProducer;
  InputTag      trackProducer;
  
  TTree*        miniTree;
  CatoCMSEvent* cev;
  
  double 	bTag_cut_discriminator;
  int           bTags_cut_min;
  
  InputTag      EventType;
  InputTag      AnaType;
  
  CatoCMSCutFlowTable* cft;
  std::map<std::string, CatoCMSCutFlowTable*>  cftMap;
  std::map<std::string, TTree*> minitrees;
  std::map<std::string, CatoCMSSampleInfo*> infos;
  string        MiniTreeName;
  string 	ResultDir;

  STParton*           stp;
  SSParton*           ssp;
  WJetParton*	      wjp;
  TTbarParton*        ttp;
  QCDParton*          qcdp;
  CatoCMSSingleTopMC* mcST;
  CatoCMSSchannelMC*  mcSS;
  CatoCMSWJetsMC*     mcWJ;
  CatoCMSTTbarMC*     mcTT;
  CatoCMSQCDMC*       mcQCD;
  
  JetVertexMain* vertexAlgo;
  
  string             cftbjetstring;
  CatoCMSSampleInfo* info;
  
  int lepJetEv;
  int tauJetEv;
  int diLepEv;
  int hadEv;
  int remainingLepJetsEv;
  int remainingTauJetsEv;
  int remainingDiLepEv;
  int remainingHadEv;
  int DecChan;
  
  // for testing ...
  std::map<std::string, TH1*> h;

};

#endif
