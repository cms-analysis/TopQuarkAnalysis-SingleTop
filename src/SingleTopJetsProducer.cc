/*
 *\Author: A. Orso M. Iorio 
 *
 *
 *\version  $Id: SingleTopJetsProducer.cc,v 1.5.12.1 2012/06/22 16:32:07 oiorio Exp $ 
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
#include "DataFormats/JetReco/interface/JPTJet.h"
#include "DataFormats/JetReco/interface/CaloJet.h"

#include "DataFormats/PatCandidates/interface/JetCorrFactors.h"

#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "CMGTools/External/interface/PileupJetIdentifier.h"

#include "CMGTools/External/interface/PileupJetIdentifier.h"

#include "FWCore/Framework/interface/Selector.h"



#include "TopQuarkAnalysis/SingleTop/interface/SingleTopJetsProducer.h"

#include <vector>
#include <memory>

#include "DataFormats/Math/interface/LorentzVector.h"


//using namespace pat;


SingleTopJetsProducer::SingleTopJetsProducer(const edm::ParameterSet& iConfig) 
{
  src_                 = iConfig.getParameter<edm::InputTag>	      ( "src" );

  PUFullDiscriminant_  = iConfig.getParameter<edm::InputTag>	      ( "puFullDiscriminant" );
  PUFullID_                 = iConfig.getParameter<edm::InputTag>	      ( "puFullID" );

  PUChargedDiscriminant_  = iConfig.getParameter<edm::InputTag>	      ( "puChargedDiscriminant" );
  PUChargedID_                 = iConfig.getParameter<edm::InputTag>	      ( "puChargedID" );

  PUIDVariables_                 = iConfig.getParameter<edm::InputTag>	      ( "puIDVariables" );

  cut_ = iConfig.getParameter< std::string >("cut"); 
  

produces<std::vector<pat::Jet> >();
//produces<std::vector<pat::Jet> >();

//edm::ParameterSet overlapPSet = iConfig.getParameter<edm::ParameterSet>("leptonsSrc");
  //  std::vector<edm::InputTag> names = overlapPSet.getParameterNamesForType< edm::InputTag >

}

void SingleTopJetsProducer::produce(edm::Event & iEvent, const edm::EventSetup & iEventSetup){
  
  
  
  //  for(std::vector<edm::InputTag>::const_iterator it=names.begin();it != names.end;++it){}

  iEvent.getByLabel(src_,jets);
  iEvent.getByLabel(src_,vjets);

  std::auto_ptr< std::vector< pat::Jet > > initialJets(new std::vector< pat::Jet >(*jets));
  std::auto_ptr< std::vector< pat::Jet > > finalJets(new std::vector< pat::Jet >);


  
  iEvent.getByLabel(PUFullDiscriminant_,puFullJetIdMVA);
  iEvent.getByLabel(PUFullID_,puFullJetIdFlag);  
  iEvent.getByLabel(PUChargedDiscriminant_,puChargedJetIdMVA);
  iEvent.getByLabel(PUChargedID_,puChargedJetIdFlag);  

  iEvent.getByLabel(PUIDVariables_, puIDVariables);  

  
  for(size_t i = 0; i < jets->size(); ++i){
    //    pat::Jet & jet = (*initialJets)[i];
    pat::Jet & jet = (*initialJets)[i];

    Selector cut(cut_);
    if(!cut(jet))continue; 

    

    jet.addUserFloat("PUFullDiscriminant", (*puFullJetIdMVA)[(vjets->refAt(i))]);
    jet.addUserFloat("PUChargedDiscriminant", (*puChargedJetIdMVA)[(vjets->refAt(i))]);


    jet.addUserFloat("beta", ((*puIDVariables)[(vjets->refAt(i))]).beta());
    jet.addUserFloat("betaStar", ((*puIDVariables)[(vjets->refAt(i))]).betaStar());
    jet.addUserFloat("RMS", ((*puIDVariables)[(vjets->refAt(i))]).RMS());
    jet.addUserFloat("dZ", ((*puIDVariables)[(vjets->refAt(i))]).dZ());
    
    int wp = 0;
    
    int idflag = (*puFullJetIdFlag)[ (vjets->refAt(i))];
    if( PileupJetIdentifier::passJetId( idflag, PileupJetIdentifier::kLoose ) ) {
	  wp =1;
	}
    if( PileupJetIdentifier::passJetId( idflag, PileupJetIdentifier::kMedium )) {
	  wp =2;
	 }
    if( PileupJetIdentifier::passJetId( idflag, PileupJetIdentifier::kTight )) {
	   wp =3;
	 }
	
    
    jet.addUserFloat("PUFullWorkingPoint",wp);

    int wpchs =0; 
    
    int idflagchs = (*puChargedJetIdFlag)[ (vjets->refAt(i))];
    if( PileupJetIdentifier::passJetId( idflag, PileupJetIdentifier::kLoose ) ) {
	  wpchs =1;
	}
    if( PileupJetIdentifier::passJetId( idflag, PileupJetIdentifier::kMedium )) {
	  wpchs =2;
	 }
    if( PileupJetIdentifier::passJetId( idflag, PileupJetIdentifier::kTight )) {
	   wpchs =3;
	 }

    jet.addUserFloat("PUChargedWorkingPoint",wpchs);
    
    


    finalJets->push_back(jet);

  }

  //std::cout << "mark 5"<< std::endl;  
  
  iEvent.put(finalJets);
  
  //std::cout << "mark 6"<< std::endl;  

}

SingleTopJetsProducer::~SingleTopJetsProducer(){;}
DEFINE_FWK_MODULE(SingleTopJetsProducer);
