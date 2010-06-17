#ifndef SingleTopElectronFilter_h
#define SingleTopElectronFilter_h

// Orso Iorio, INFN Napoli 



#include <FWCore/Framework/interface/Frameworkfwd.h>
#include <FWCore/Framework/interface/EDFilter.h>
#include <FWCore/Framework/interface/Event.h>
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

#include "FWCore/ParameterSet/interface/InputTag.h"

class SingleTopElectronFilter : public edm::EDFilter{

public:

  explicit SingleTopElectronFilter(const edm::ParameterSet&);
  ~SingleTopElectronFilter();
  

private:

  virtual bool filter(edm::Event&, const edm::EventSetup&);

  edm::InputTag src_; 

};
#endif
