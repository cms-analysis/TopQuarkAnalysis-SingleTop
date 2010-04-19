//cato header
#include "TopQuarkAnalysis/SingleTop/interface/QCDParton.h"
//c++ header
#include <iostream>
#include <vector>

using namespace std;
using namespace CatoCMS;
using namespace reco;
using namespace edm;
QCDParton::QCDParton()
{
}

QCDParton::~QCDParton()
{
}

void QCDParton::PrintList(edm::Handle<std::vector<reco::GenParticle> > genParticles, int pStatus)
{
  using namespace edm;
  using namespace reco;
  using namespace std;
  
  cout << "Gen Particle Listing" << endl
       << "====================" << endl
       << " idx  |   ID  |Stat|  Mo1  Mo2  Da1  Da2 |nMo nDa|    pt       eta     phi   |     px         py         pz        m     |" << endl;
  int idx  = -1;
  int iMo1 = -1;
  int iMo2 = -1;
  int iDa1 = -1;
  int iDa2 = -1;
  vector<const reco::Candidate *> cands;
  vector<const Candidate *>::const_iterator found = cands.begin();
  for(std::vector<reco::GenParticle>::const_iterator p = genParticles->begin();
     p != genParticles->end(); ++ p) {
     cands.push_back(&*p);
  }
  
  for(std::vector<reco::GenParticle>::const_iterator p  = genParticles->begin(); p != genParticles->end(); p ++) {
    if (!(p->status() >= pStatus)) continue;   //print only particles with status larger than pStatus
       // Particle Name
       //int id = p->pdgId();
       //const ParticleData * pd = pdt_->particle(id);
       //string particleName = pd == 0 ? "???" : pd->name();
       
       // Particle Index
       idx =  p - genParticles->begin();   //really dirty hack?? what are they smokin???

       // Particles Mothers and Daighters
       iMo1 = -1;
       iMo2 = -1;
       iDa1 = -1;
       iDa2 = -1;
       int nMo = p->numberOfMothers();
       int nDa = p->numberOfDaughters();
 
       found = find(cands.begin(), cands.end(), p->mother(0));
       if(found != cands.end()) iMo1 = found - cands.begin() ;
 
       found = find(cands.begin(), cands.end(), p->mother(nMo-1));
       if(found != cands.end()) iMo2 = found - cands.begin() ;
      
       found = find(cands.begin(), cands.end(), p->daughter(0));
       if(found != cands.end()) iDa1 = found - cands.begin() ;
 
       found = find(cands.begin(), cands.end(), p->daughter(nDa-1));
       if(found != cands.end()) iDa2 = found - cands.begin() ;
 
       char buf[256];
       sprintf(buf,
              " %4d | %5d | %2d | %4d %4d %4d %4d | %2d %2d | %7.3f %10.3f %6.3f | %10.3f %10.3f %10.3f %8.3f |\n",
              idx,
              p->pdgId(),
              p->status(),
              iMo1,iMo2,iDa1,iDa2,nMo,nDa,
              p->pt(),
              p->eta(),
              p->phi(),
              p->px(),
              p->py(),
              p->pz(),
              p->mass()
             );
       cout << buf;
    }
}

void QCDParton::GetQCDTruth(edm::Handle<std::vector<reco::GenParticle> > genParticles, double weight, CatoCMS::QCDMC* mcQCD)
{
  mcQCD->Reset();
  //int partons=0;
  LorentzVector v;
  PrintList(genParticles,3);

  const Candidate *ElMother;
  const Candidate *MuMother;

  // find leading generated muon and electron
  double highest_pt_el = 0.;
  double highest_pt_mu = 0.;
  for(std::vector<reco::GenParticle>::const_iterator p=genParticles->begin(); 
			p != genParticles->end(); ++p){
    double eta = p->eta();
    double pt = p->pt();
    if(pt > 5. && fabs(eta)<2.5 && abs(p->pdgId())==11){ // find Electron
      cout << "Electron "   
	   << "\t" << p->pdgId() 
	   << "\t" << p->status()  
	   << "\t" << p->px()
	   << "\t" << p->py()
	   << "\t" << p->pz()
	   << "\t" << p->mass()	
	   << "\t" << p->energy()
	   << endl;
      if (pt > highest_pt_el) {
	highest_pt_el=pt;
	mcQCD->p4El.SetCoordinates(p->px(),p->py(),p->pz(),p->energy());
	mcQCD->QEl = (p->pdgId() > 0 ) ? -1 : 1;
	mcQCD->mcElId = p->pdgId();
	for(unsigned int m=0;m<p->numberOfMothers();m++){
	  ElMother = p->mother(m);
	  cout << "ElMother "   
	       << "\t" << ElMother->pdgId() 
	       << "\t" << ElMother->status()  
	       << "\t" << ElMother->px()
	       << "\t" << ElMother->py()
	       << "\t" << ElMother->pz()
	       << "\t" << ElMother->mass()	
	       << "\t" << ElMother->energy()
	       << endl;
	  mcQCD->p4ElMother.SetCoordinates(ElMother->px(),ElMother->py(),ElMother->pz(),ElMother->energy());
	  mcQCD->QElMother = (ElMother->pdgId() > 0 ) ? -1 : 1;
	  mcQCD->mcElMotherId = ElMother->pdgId();
	}
      }

    } else if (pt > 5. && fabs(eta)<2.2 && abs(p->pdgId())==13){ // find Muon
      cout << "Muon "   
	   << "\t" << p->pdgId() 
	   << "\t" << p->status()  
	   << "\t" << p->px()
	   << "\t" << p->py()
	   << "\t" << p->pz()
	   << "\t" << p->mass()	
	   << "\t" << p->energy()
	   << endl;
      if (pt > highest_pt_mu) {
	highest_pt_mu=pt;
	mcQCD->p4Mu.SetCoordinates(p->px(),p->py(),p->pz(),p->energy());
	mcQCD->QMu = (p->pdgId() > 0 ) ? -1 : 1;
	mcQCD->mcMuId = p->pdgId();
	for(unsigned int m=0;m<p->numberOfMothers();m++){
	  MuMother = p->mother(m);
	  cout << "MuMother "   
	       << "\t" << MuMother->pdgId() 
	       << "\t" << MuMother->status()  
	       << "\t" << MuMother->px()
	       << "\t" << MuMother->py()
	       << "\t" << MuMother->pz()
	       << "\t" << MuMother->mass()	
	       << "\t" << MuMother->energy()
	       << endl;
	  mcQCD->p4MuMother.SetCoordinates(MuMother->px(),MuMother->py(),MuMother->pz(),MuMother->energy());
	  mcQCD->QMuMother = (MuMother->pdgId() > 0 ) ? -1 : 1;
	  mcQCD->mcMuMotherId = MuMother->pdgId();
	}
      }

    }
    

  }//Loop over particles

}
