#ifndef __CATO_CMS_STParton_H__
#define __CATO_CMS_STParton_H__

#include <DataFormats/HepMCCandidate/interface/GenParticle.h>
#include "TopQuarkAnalysis/SingleTop/interface/SingleTopMC.h"
#include <DataFormats/Candidate/interface/Candidate.h>


class STParton{

 public:

  STParton();
  ~STParton();

  //  void GetSingleTopTruth(HepMC::GenEvent* mcEv, CatoCMS::SingleTopMC* mcST);
  //  void GetSingleTopTruth (edm::Handle<reco::CandidateCollection> genParticles, edm::Handle<double>genEventWeight, CatoCMS::SingleTopMC* mcST);
  void GetSingleTopTruth (edm::Handle<std::vector<reco::GenParticle> > genParticles, double weight, CatoCMS::SingleTopMC* mcST);
  void printList(edm::Handle<std::vector<reco::GenParticle> > genParticles, int pStatus);

 private:



}; 
#endif
