//cato header
#include "TopQuarkAnalysis/SingleTop/interface/WJetParton.h"
//c++ header
#include <iostream>
#include <vector>

using namespace std;
using namespace CatoCMS;
using namespace reco;
using namespace edm;
WJetParton::WJetParton()
{
}

WJetParton::~WJetParton()
{
}

void WJetParton::PrintList(edm::Handle<std::vector<reco::GenParticle> > genParticles, int pStatus)
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

void WJetParton::GetWJetTruth(edm::Handle<std::vector<reco::GenParticle> > genParticles, double weight, CatoCMS::WJetsMC* mcWJ)
{
  mcWJ->Reset();
  int partons=0;
  LorentzVector v;
  PrintList(genParticles,3);
	//HepMC::GenParticle* pa;
  //std::vector<HepMC::GenParticle*> children;
  //std::vector<HepMC::GenParticle*> childrenQQ;
  //std::vector<HepMC::GenParticle*> parents;
  //std::vector<HepMC::GenParticle*> TauChildren;
  //std::vector<HepMC::GenParticle*> TauDesc;
  const Candidate *WDaughter;
	const Candidate *TauDaughter;
  const Candidate *Tau;
  const Candidate *QQDaughter;
  for(std::vector<reco::GenParticle>::const_iterator p=genParticles->begin(); 
			p != genParticles->end(); ++p){

//HepMC::GenEvent::particle_const_iterator paIt = mcEv->particles_begin();
//     paIt != mcEv->particles_end(); paIt++){ //Loop over particles
    if(abs(p->pdgId())==24){
 // find W
      /*  cout << pa->barcode()  << "\t" 
	  << pa->status() << "\t" 
	  << pa->pdg_id() << "\t" 
	  << pa->Mass() << "\t" 
	  << pa->Momentum() << endl;*/
    cout << "W "   
	 << "\t" << p->pdgId() 
	 << "\t" << p->status()  
	 << "\t" << p->px()
	 << "\t" << p->py()
	 << "\t" << p->pz()
 	 << "\t" << p->mass()	
   << "\t" << p->energy()
   << endl;
    

		
  //    children = pa->listChildren();
      for(unsigned int d=0;d<p->numberOfDaughters();d++){
		
//std::vector<HepMC::GenParticle*>::const_iterator cIt=children.begin();
//	  cIt!=children.end();cIt++){ //loop children of W
			WDaughter=p->daughter(d);
			if(WDaughter->status()==3){//only hard prozess particles	
				//look for leptons e->11 mu->13 tau->15
	  		if(abs(WDaughter->pdgId())==11 || abs(WDaughter->pdgId())==13 
	      															 || abs(WDaughter->pdgId())==15){
	    		    cout << "daughter of W "   
	 << "\t" << p->pdgId() 
	 << "\t" << p->status()  
	 << "\t" << p->px()
	 << "\t" << p->py()
	 << "\t" << p->pz()
 	 << "\t" << p->mass()	
   << "\t" << p->energy()
   << endl;


					mcWJ->p4Lep.SetCoordinates(WDaughter->p4().px(),WDaughter->p4().py(),
				  WDaughter->p4().pz(),WDaughter->p4().e());
	    		mcWJ->QLep = (WDaughter->pdgId() > 0 ) ? -1 : 1;
	   			mcWJ->mcLepId =WDaughter->pdgId();
	    		//Fill the W here
	    		mcWJ->p4W.SetCoordinates(p->p4().px(),p->p4().py(),
				 	p->p4().pz(),p->p4().e());
	    		mcWJ->mcWId =p->pdgId();
	    		mcWJ->QW = (p->pdgId() > 0 ) ? -1 : 1;
					
	    	//check if Lepton was a tau and fill decay Products of the tau
	    	if(abs(WDaughter->pdgId())==15){ //lepton is a tau
	     	  mcWJ->Tautag = 1;
	     	  mcWJ->DecChan = 1;
	     	  //get the taus children:
	     	  Tau = WDaughter;
					TauDaughter = Tau->daughter(0);

	     	  //check if tau children is still the tau
	     	  while(abs(TauDaughter->pdgId())==15){
						Tau = TauDaughter;
					  TauDaughter = TauDaughter->daughter(0);
	        }
	        for(unsigned int td=0;td<TauDaughter->numberOfDaughters();td++){ //loop over taus children..
						TauDaughter =Tau->daughter(td); 
						    cout << "daughter of Tau "   
	 << "\t" << p->pdgId() 
	 << "\t" << p->status()  
	 << "\t" << p->px()
	 << "\t" << p->py()
	 << "\t" << p->pz()
 	 << "\t" << p->mass()	
   << "\t" << p->energy()<< endl;


					/*	cout << TauDaughter->barcode()  << "\t" 
	 						 	 << TauDaughter->status()   << "\t" 
	  						 << TauDaughter->pdgId()   << "\t" 
	               << TauDaughter->mass()     << "\t" 
	               << TauDaughter->momentum() << endl;*/

						if(abs(TauDaughter->pdgId())==11){//e
		  				mcWJ->p4TLep.SetCoordinates(TauDaughter->p4().px(),
					  													TauDaughter->p4().py(),TauDaughter->p4().pz(),
					  													TauDaughter->p4().e());
		  			mcWJ->Muontag = 0;
					}//e
	   	    else if(abs(TauDaughter->pdgId())==12){//e neutrino
		        mcWJ->p4TLNu.SetCoordinates(TauDaughter->p4().px(),
					  TauDaughter->p4().py(), TauDaughter->p4().pz(),
					  TauDaughter->p4().e());
     		  }//e neutrino
		      else if(abs(TauDaughter->pdgId())==13){//mu
		        mcWJ->p4TLep.SetCoordinates(TauDaughter->p4().px(),
					  TauDaughter->p4().py(),TauDaughter->p4().pz(),
					  TauDaughter->p4().e());
		        mcWJ->Muontag = 1;
		      }//mu
		      else if(abs(TauDaughter->pdgId())==14){ //mu neutrino
		        mcWJ->p4TLNu.SetCoordinates(TauDaughter->p4().px(),
					  TauDaughter->p4().py(), TauDaughter->p4().pz(),
					  TauDaughter->p4().e());
		      }// mu neutrino
		      else if(abs(TauDaughter->pdgId())==16){ //get the 2nd tau neutrino
		        mcWJ->p4TTNu.SetCoordinates(TauDaughter->p4().px(),
					  TauDaughter->p4().py(), TauDaughter->p4().pz(),
					  TauDaughter->p4().e());
		      }//get the 2nd tau neutrino
	      }//loop over taus children
	    }// lepton is a tau
	    else{
	      mcWJ->Tautag = 0;
	      mcWJ->DecChan = 0;
	      if(abs(WDaughter->pdgId())==11 ) 
					mcWJ->Muontag = 0;
	      else if(abs(WDaughter->pdgId())==13)	
					mcWJ->Muontag = 1;
	    }

	    //Get the Partons from the hard blubb
	    //childrenQQ=pa->mother()->listChildren();
	    partons=0;
	    //for(vector<HepMC::GenParticle*>::const_iterator pcIt=childrenQQ.begin();
		//pcIt!=childrenQQ.end();pcIt++){ //loop over hard partons
		  for(unsigned int qq=0; qq < p->mother(0)->numberOfDaughters();qq++){
				QQDaughter =  p->mother(0)->daughter(qq);
   
        if(abs(QQDaughter->pdgId())!=24){
 cout << "hard partons "   
	 << "\t" << QQDaughter->pdgId() 
	 << "\t" << QQDaughter->status()  
	 << "\t" << QQDaughter->px()
	 << "\t" << QQDaughter->py()
	 << "\t" << QQDaughter->pz()
 	 << "\t" << QQDaughter->mass()	
   << "\t" << QQDaughter->energy()<< endl;

		      mcWJ->mcPId.push_back(QQDaughter->pdgId());
		      v.SetCoordinates(QQDaughter->p4().px(),QQDaughter->p4().py(),
			     QQDaughter->p4().pz(),QQDaughter->p4().e());
		      mcWJ->p4P.push_back(v);
		      partons++;
	      }
	    }//loop over hard partons
	    mcWJ->NumberOfHardPartons = partons;
	  }//Leptons
	  else if(abs(WDaughter->pdgId())==12 || abs(WDaughter->pdgId())==14 
		  || abs(WDaughter->pdgId())==16){//Neutrino
	    mcWJ->p4Nu.SetCoordinates(WDaughter->p4().px(),WDaughter->p4().py(),
				  WDaughter->p4().pz(),WDaughter->p4().e());
	    mcWJ->mcNuId =WDaughter->pdgId();
	  }//Neutrino*/
	}//only hard prozess particles
      }//loop children of W
      break;

    }// find W
  }//Loop over particles
  cout << mcWJ->DecChan << " " << mcWJ->Tautag << " " << mcWJ->Muontag << endl;
}
