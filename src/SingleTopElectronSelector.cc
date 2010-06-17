// Orso Iorio, INFN Napoli 
//
//

#include "TopQuarkAnalysis/SingleTop/interface/SingleTopElectronFilter.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Common/interface/Handle.h"

SingleTopElectronFilter::SingleTopElectronFilter(const edm::ParameterSet& iConfig){

  src_ = iConfig.getParameter<edm::InputTag>("src"); 
  //  min_ = iConfig.getUntrackedParameter<double>("min"); 
  // max_ = iConfig.getUntrackedParameter<double>("max"); 

}


bool SingleTopElectronFilter::filter( edm::Event& iEvent, const edm::EventSetup& iSetup){

  edm::Handle<edm::View<pat::Electron> > src ;
  iEvent.getByLabel(src_, src);
  
  
  for(edm::View<pat::Electron>::const_iterator it = src->begin();it != src->end();++it){
    int a = (int) it-> electronID("simpleEleId70cIso");
    bool hadId(a & 0x1);
    /*    std::cout << " value of eleid 95c "
	      <<a<<" hadId? " << hadId << std::endl 
	      <<" 80c? " << (int) it-> electronID("simpleEleId80cIso") << std::endl
	      <<" 90c? " << (int) it-> electronID("simpleEleId90cIso") << std::endl
	      <<" 95c? " << (int) it-> electronID("simpleEleId95cIso") << std::endl
	      <<" 95relIso? " << (int) it-> electronID("simpleEleId95relIso") << std::endl
	      ;*/
      	      

    if (hadId) return true;
  }
  return false;

}

SingleTopElectronFilter::~SingleTopElectronFilter(){}

DEFINE_FWK_MODULE(SingleTopElectronFilter);
