#ifndef __CATO_CMS_TTBAR_PARTON_H__
#define __CATO_CMS_TTBAR_PARTON_H__

#include "SimDataFormats/GeneratorProducts/interface/HepMCProduct.h"

#include "TopQuarkAnalysis/SingleTop/interface/TTbarMC.h"
#include <DataFormats/HepMCCandidate/interface/GenParticle.h>
#include <DataFormats/Candidate/interface/Candidate.h>


class TTbarParton{

 public:

  TTbarParton();
  ~TTbarParton();

  void GetTTbarTruth( edm::Handle<std::vector<reco::GenParticle> > genParticles,double weight, CatoCMS::TTbarMC* mcTT);


 private:



}; 
#endif

