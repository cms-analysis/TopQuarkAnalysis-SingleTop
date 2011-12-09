/*
 *\Author: A. Orso M. Iorio 
 *
 *
 *\version  $Id: SingleTopLeptonCounter.cc,v 1.1 2011/04/28 08:47:55 oiorio Exp $ 
 */


#include "DataFormats/Candidate/interface/Candidate.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "TopQuarkAnalysis/SingleTop/interface/SingleTopLeptonCounter.h"
#include "DataFormats/Math/interface/deltaR.h"


SingleTopLeptonCounter::SingleTopLeptonCounter(const edm::ParameterSet& iConfig){

  looseMuons_ = iConfig.getParameter<edm::InputTag>("looseMuons");
  looseElectrons_ = iConfig.getParameter<edm::InputTag>("looseElectrons");

  tightMuons_ = iConfig.getParameter<edm::InputTag>("tightMuons");
  tightElectrons_ = iConfig.getParameter<edm::InputTag>("tightElectrons");

  qcdMuons_ = iConfig.getParameter<edm::InputTag>("qcdMuons");
  qcdElectrons_ = iConfig.getParameter<edm::InputTag>("qcdElectrons");

  minTight_ =  iConfig.getUntrackedParameter<int>("nTightLeptons",0);
  maxTight_ =  iConfig.getUntrackedParameter<int>("nTightLeptons",99);

  minLoose_ =  iConfig.getUntrackedParameter<int>("nTightLeptons",0);
  maxLoose_ =  iConfig.getUntrackedParameter<int>("nTightLeptons",99);

  minQCD_ =  iConfig.getUntrackedParameter<int>("nTightLeptons",0);
  maxQCD_ =  iConfig.getUntrackedParameter<int>("nTightLeptons",99);

  doOverlap_ = iConfig.getUntrackedParameter<bool>("rejectOverlap",true);
  doQCD_ = iConfig.getUntrackedParameter<bool>("doQCD",true);
}

bool SingleTopLeptonCounter::filter(edm::Event & iEvent, const edm::EventSetup & iSetup){


  iEvent.getByLabel(looseMuons_,looseMuons);
  iEvent.getByLabel(looseElectrons_,looseElectrons);

  iEvent.getByLabel(tightMuons_,tightMuons);
  iEvent.getByLabel(tightElectrons_,tightElectrons);

  iEvent.getByLabel(qcdMuons_,qcdMuons);
  iEvent.getByLabel(qcdElectrons_,qcdElectrons);

  /*  int tMuSize = tightMuons->size(), 
    lMuSize = looseMuons->size(), 
    tEleSize = tightElectrons->size(),
    lEleSize = looseElectrons->size(),
    qMuSize = qcdMuons->size(), 
    qMuSize =qcd ;

  */

  bool TightLeptonAccept = false;
  bool LooseLeptonAccept = false;
  bool LeptonAccept = false;
  bool QCDAccept = false;
    
  int nLoose =0, nTight=0, nQCD=0 ;
  
  //Counting loose leptons overlapping with each other 
  if(doOverlap_){
    for (size_t i = 0; i<looseMuons->size();++i){
      for (size_t j = 0; j<tightMuons->size();++j){
	if (!(deltaR(looseMuons->at(i),tightMuons->at(j))<0.01)) ++nLoose;
      }
    }
    
    for (size_t i = 0; i<looseElectrons->size();++i){
      for (size_t j = 0; j<tightElectrons->size();++j){
	if (!(deltaR(looseElectrons->at(i),tightElectrons->at(j))<0.01)) ++nLoose;
      }
    } 
  }
  else nLoose = looseMuons->size() +looseElectrons->size();
  nTight = tightMuons->size()+tightElectrons->size();
  
  LooseLeptonAccept =  ( nLoose >= minLoose_ && nLoose <= maxLoose_);
  TightLeptonAccept =  ( nTight >= minTight_ && nTight <= maxTight_);
  LeptonAccept  = LooseLeptonAccept && TightLeptonAccept;
  
  if(!doQCD_) return LeptonAccept;
  else {
    
    nQCD = qcdMuons->size()+qcdElectrons->size();
    QCDAccept = (nQCD>=minQCD_ && nQCD<= maxQCD_) ;
    return LeptonAccept || QCDAccept;
  }
  return true;

}

SingleTopLeptonCounter::~SingleTopLeptonCounter(){;}

DEFINE_FWK_MODULE( SingleTopLeptonCounter );