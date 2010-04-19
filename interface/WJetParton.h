#ifndef __CATO_CMS_W_JET_PARTON_H__
#define __CATO_CMS_W_JET_PARTON_H__

//SW header
#include <DataFormats/HepMCCandidate/interface/GenParticle.h>
#include <DataFormats/Candidate/interface/Candidate.h>
//cato header
#include "TopQuarkAnalysis/SingleTop/interface/WJetsMC.h"


class WJetParton{
public:
  WJetParton();
  ~WJetParton();
	void GetWJetTruth(edm::Handle<std::vector<reco::GenParticle> > genParticles, double weight, CatoCMS::WJetsMC* mcWJ);
	void PrintList(edm::Handle<std::vector<reco::GenParticle> > genParticles, int pStatus);
private:
}; 
#endif //__CATO_CMS_W_JET_PARTON_H__
