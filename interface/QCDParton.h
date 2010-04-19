#ifndef __CATO_CMS_QCD_PARTON_H__
#define __CATO_CMS_QCD_PARTON_H__

//SW header
#include <DataFormats/HepMCCandidate/interface/GenParticle.h>
#include <DataFormats/Candidate/interface/Candidate.h>
//cato header
#include "TopQuarkAnalysis/SingleTop/interface/QCDMC.h"


class QCDParton{
public:
  QCDParton();
  ~QCDParton();
	void GetQCDTruth(edm::Handle<std::vector<reco::GenParticle> > genParticles, double weight, CatoCMS::QCDMC* mcQCD);
	void PrintList(edm::Handle<std::vector<reco::GenParticle> > genParticles, int pStatus);
private:
}; 
#endif //__CATO_CMS_QCD_PARTON_H__
