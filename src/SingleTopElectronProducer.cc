/*
 *\Author: A. Orso M. Iorio 
 *
 *
 *\version  $Id: SingleTopElectronProducer.cc,v 1.7 2011/03/24 15:58:06 oiorio Exp $ 
 */

// Single Top producer: produces a top candidate made out of a Lepton, a B jet and a MET

#include "PhysicsTools/PatAlgos/plugins/PATJetProducer.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"

#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/Association.h"
#include "DataFormats/Candidate/interface/CandAssociation.h"

#include "DataFormats/JetReco/interface/JetTracksAssociation.h"
#include "DataFormats/BTauReco/interface/JetTag.h"
#include "DataFormats/BTauReco/interface/TrackProbabilityTagInfo.h"
#include "DataFormats/BTauReco/interface/TrackIPTagInfo.h"
#include "DataFormats/BTauReco/interface/TrackCountingTagInfo.h"
#include "DataFormats/BTauReco/interface/SecondaryVertexTagInfo.h"
#include "DataFormats/BTauReco/interface/SoftLeptonTagInfo.h"

#include "DataFormats/Candidate/interface/CandMatchMap.h"
#include "SimDataFormats/JetMatching/interface/JetFlavourMatching.h"

#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "DataFormats/Math/interface/deltaR.h"

#include "DataFormats/PatCandidates/interface/JetCorrFactors.h"

#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"


#include "FWCore/Framework/interface/Selector.h"

#include "TopQuarkAnalysis/SingleTop/interface/SingleTopElectronProducer.h"


#include "DataFormats/Scalers/interface/DcsStatus.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "RecoEgamma/EgammaTools/interface/ConversionFinder.h"
#include "PhysicsTools/SelectorUtils/interface/SimpleCutBasedElectronIDSelectionFunctor.h"


#include <vector>
#include <memory>

#include "DataFormats/Math/interface/LorentzVector.h"


//using namespace pat;


SingleTopElectronProducer::SingleTopElectronProducer(const edm::ParameterSet& iConfig)
{
  src_                 = iConfig.getParameter<edm::InputTag>( "src" );
  cut_ = iConfig.getParameter< std::string >("cut"); 
  rho_ = iConfig.getParameter<edm::InputTag> ("rho");
  deltaR_ = iConfig.getUntrackedParameter<double>         ( "deltaR",0.3 );

  produces<std::vector<pat::Electron> >();
}

void SingleTopElectronProducer::produce(edm::Event & iEvent, const edm::EventSetup & iEventSetup){


  ////std::cout << " mark 0 " << std::endl;

  ////std::cout << " mark 1 " << std::endl;
  //  edm::Handle<edm::View<pat::Electron> > electrons;
  edm::Handle<std::vector<pat::Electron> > electrons;
  iEvent.getByLabel(src_,electrons);
  iEvent.getByLabel(rho_,rho);
  double energy_ = TMath::Pi()*deltaR_*deltaR_* (*rho);
  
  Selector cut(cut_);
  std::auto_ptr< std::vector< pat::Electron > > finalElectrons (new std::vector<pat::Electron>(*electrons));

  ////std::cout << " mark 2 " << std::endl;
    
  
  for(size_t i = 0; i < finalElectrons->size(); ++i){
    
    pat::Electron & el = (*finalElectrons)[i];
    el.addUserFloat("DeltaCorrectedIso",(el.chargedHadronIso() + std::max(0., el.neutralHadronIso() + el.photonIso() -0.5*el.puChargedHadronIso()))/el.et());
    el.addUserFloat("RhoCorrectedIso",(el.chargedHadronIso() + std::max(0., el.neutralHadronIso() + el.photonIso() -energy_))/el.et());
    
    if(!cut(el)) finalElectrons->erase(finalElectrons->begin()+i) ; 
    
    //std::cout << " passes cut " << cut_ <<  std::endl;
    
    //    finalElectrons->push_back(electrons->at(i));
  } 
 
  ////std::cout << " mark 7 " << std::endl;

  //std::auto_ptr< std::vector< pat::Electron > > finalElectronsPtr(finalElectrons);
 

iEvent.put(finalElectrons);

}

SingleTopElectronProducer::~SingleTopElectronProducer(){;}
DEFINE_FWK_MODULE(SingleTopElectronProducer);
