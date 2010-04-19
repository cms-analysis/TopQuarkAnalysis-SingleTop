#ifndef __CATO_CMS_SSParton_H__
#define __CATO_CMS_SSParton_H__

#include <DataFormats/HepMCCandidate/interface/GenParticle.h>
#include "TopQuarkAnalysis/SingleTop/interface/SchannelMC.h"
#include <DataFormats/Candidate/interface/Candidate.h>


class SSParton{

 public:

  SSParton();
  ~SSParton();

  //  void GetSingleTopTruth(HepMC::GenEvent* mcEv, CatoCMS::SingleTopMC* mcSS);
  //  void GetSingleTopTruth (edm::Handle<reco::CandidateCollection> genParticles, edm::Handle<double>genEventWeight, CatoCMS::SingleTopMC* mcSS);
  void GetSchannelTruth (edm::Handle<std::vector<reco::GenParticle> > genParticles, double weight, CatoCMS::SchannelMC* mcSS);
  void printList(edm::Handle<std::vector<reco::GenParticle> > genParticles, int pStatus);

 private:



}; 
#endif
