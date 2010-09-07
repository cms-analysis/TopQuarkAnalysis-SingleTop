// Orso Iorio, INFN Napoli 
//
//

#include "TopQuarkAnalysis/SingleTop/interface/SingleTopElectronFilter.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Scalers/interface/DcsStatus.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include "RecoEgamma/EgammaTools/interface/ConversionFinder.h"

#include "PhysicsTools/SelectorUtils/interface/SimpleCutBasedElectronIDSelectionFunctor.h"

SingleTopElectronFilter::SingleTopElectronFilter(const edm::ParameterSet& iConfig){


  src_ = iConfig.getParameter<edm::InputTag>("src"); 
  isData_ = iConfig.getUntrackedParameter<bool>("isData",false); 
  //dcsTag_ = iConfig.getParameter<edm::InputTag>("dcsTag"); 
  //  min_ = iConfig.getUntrackedParameter<double>("min"); 
  // max_ = iConfig.getUntrackedParameter<double>("max"); 

}


bool SingleTopElectronFilter::filter( edm::Event& iEvent, const edm::EventSetup& iSetup){

  //  dcsTag_ = "scalersRawToDigi";

  edm::Handle<edm::View<pat::Electron> > src ;
  iEvent.getByLabel(src_, src);

  edm::Handle<reco::TrackCollection> ctfTracks;
  iEvent.getByLabel("generalTracks",ctfTracks);  

  double bfield = 3.8;

  if(isData_){
    edm::Handle<DcsStatusCollection> dcsHandle;
    //    iEvent.getByLabel(dcsTag_,dcsHandle);
    iEvent.getByLabel("scalersRawToDigi",dcsHandle);
    float currentScaleFactor =2.09237036221512717e-04;
    float current = (*dcsHandle)[0].magnetCurrent();
    bfield = current*currentScaleFactor;
  }
  else{
  edm::ESHandle<MagneticField> magneticField;
  iSetup.get<IdealMagneticFieldRecord>().get(magneticField);
  bfield = magneticField->inTesla(GlobalPoint(0.,0.,0.)).z();
  }
  SimpleCutBasedElectronIDSelectionFunctor patSeleC70(SimpleCutBasedElectronIDSelectionFunctor::cIso70,bfield,ctfTracks);
  
  
  for(edm::View<pat::Electron>::const_iterator it = src->begin();it != src->end();++it){
    //    int a = (int) it-> electronID("simpleEleId70cIso");
    //    bool hadId(a & 0x1);
    bool hadId = patSeleC70(*it);
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
