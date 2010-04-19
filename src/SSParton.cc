#include <iostream>
#include <iomanip>

#include "TopQuarkAnalysis/SingleTop/interface/SSParton.h"


SSParton::SSParton(){
}


SSParton::~SSParton(){
}


//void SSParton::GetSchannelTruth(edm::Handle<reco::CandidateCollection> genParticles, edm::Handle<double>genEventWeight, CatoCMS::SchannelMC* mcSS)
void SSParton::GetSchannelTruth(edm::Handle<std::vector<reco::GenParticle> > genParticles, double weight, CatoCMS::SchannelMC* mcSS)
{
  bool debug = false;

  using namespace std;
  using namespace edm;
  using namespace reco;

  if (debug) cout << "I'm inside SSParton::GetSchannelTruth" << endl;

  mcSS->Reset();

  if (debug) cout << "I just did a Reset()" << endl;

  bool error              = false;
  //bool isGluonSplitLQLine = false;
  //bool noVtb              = false;
  
  bool top_found  = false;
  bool btop_found = false;
  bool W_found    = false;
  bool lep_found  = false;
  bool nu_found   = false;
  //  bool lq_found   = false;
  bool secb_found = false;
  
  int idx       =  0;
  int top_id    =  0;
  int secb_id   =  0;

  //const Candidate *topMo=NULL, *top=NULL ,*W=NULL, *btop=NULL,*lep=NULL, *nu=NULL;
  const Candidate *top=NULL ,*W=NULL, *btop=NULL,*lep=NULL, *nu=NULL;
  
  // get event weight 
  double wgt = 0;
  //  double weight = *genEventWeight; 
  wgt = (weight > 0) ? 1. : -1.; // take only sign of event weigth!
  
  mcSS->eventWeight = wgt;

  //   h["eventWeightSign"]->Fill(wgt);
  //   h["eventWeight"]->Fill(weight);
  
  for(std::vector<reco::GenParticle> ::const_iterator p=genParticles->begin(); p != genParticles->end(); ++p){
    
    // top quark:
    bool endTop = false;
    if(abs(p->pdgId()) == 6 && !top_found){
      int nDau = 0;
      if (debug) cout << "I found a top" << endl;
      nDau = p->numberOfDaughters();
      if(nDau > 1){
	if (debug) cout << "This top has " << nDau << " daughters" << endl;
	for (unsigned int j=0; j<p->numberOfDaughters(); j++){
	  if (debug) cout << "pdgId = " << p->daughter(j)->pdgId() << endl;
	  if(abs(p->daughter(j)->pdgId() == 6) ){
	    if (debug) cout << "top->top" << endl;
	    top = p->daughter(j);
	    endTop = true;
	  }
	  if(abs(p->daughter(j)->pdgId()) == 24 ){
	    if (debug) cout << "top->W" << endl;
	    top = &(*p);
	    endTop = true;
	    W = p->daughter(j);
	    W_found = true;
	  }
	  if(abs(p->daughter(j)->pdgId()) == 5 ){
	    if (debug) cout << "top->b" << endl;
	    top = &(*p);
	    endTop = true;
	    btop = p->daughter(j);
	    btop_found = true;
	  }
	  if(abs(p->daughter(j)->pdgId()) == 11 || abs(p->daughter(j)->pdgId()) == 13 || abs(p->daughter(j)->pdgId()) == 15 ){
	    if (debug) cout << "top->l" << endl;
	    lep = p->daughter(j);
	    lep_found = true;
	  }
	  if(abs(p->daughter(j)->pdgId()) == 12 || abs(p->daughter(j)->pdgId()) == 14 || abs(p->daughter(j)->pdgId()) == 16 ){
	    if (debug) cout << "top->nu" << endl;
	    nu = p->daughter(j);
	    nu_found = true;
	  }
	}
      }
      else {
	if (debug) cout << "This top has " << p->numberOfDaughters() << "daughter" << endl;
	top = &(*p);      
      }
      
      //      bool endTop = false;

	/*
      while(!endTop){
	if (debug) cout << "I'm in the !endTop case" << endl;
	if (debug) cout << "(2) top->numberOfDaughters() = " << top->numberOfDaughters() << endl;
	if(top->numberOfDaughters() > 1){
	  if (debug) cout << "(2) This top has more than one daughter" << endl;
	  for (unsigned int j=0; j<top->numberOfDaughters(); j++){
	    if (debug) cout << "(2) I'm in the loop of daughters" << endl;
	    if (debug) cout << "(2) pdgId = " << p->daughter(j)->pdgId() << endl;
	    if(abs(top->daughter(j)->pdgId()) == 6 ){
	      if (debug) cout << "top->top" << endl;
	      top = top->daughter(j);
	    }
	  }
	}
	else top = top->daughter(0);
	
	if(abs(top->daughter(0)->pdgId()) == 24 || abs(top->daughter(0)->pdgId()) == 5)
	  endTop=true;

      }
	*/
      
      if(debug) cout << "this is my new top: " << top->pdgId() << "\t" << top->status() << "\t" << top->px() << endl;
      
      mcSS->p4_top_gen.SetCoordinates(top->px(), top->py(), top->pz(), top->energy());
      top_id = top->pdgId();
      if(top_id == 6){
	secb_id = -5;
	mcSS->QLep_gen = 1;
      }
      else{
	secb_id = 5;
	mcSS->QLep_gen = -1;
      }
      top_found = true;
      
      // W boson / btop:
      if (W_found) {
	if(abs( top->daughter(0)->pdgId() ) == 24){
	  W = top->daughter(0);
	  btop = top->daughter(1);
	  btop_found = true;
	}
	else{
	  W = top->daughter(1);
	  btop = top->daughter(0);
	  if(debug) cout << "INFO: top daughters switched!" << endl;
	  btop_found = true;
	}
      }

      mcSS->p4_btop_gen.SetCoordinates(btop->px(), btop->py(), btop->pz(), btop->energy());
      
      if (W_found) {
      // for W boson: go down until "ready-for-decay" W boson is reached in list
	while(abs(W->daughter(0)->pdgId()) == 24) 
	  W = W->daughter(0);
	mcSS->p4_Wtop_gen.SetCoordinates(W->px(), W->py(), W->pz(), W->energy());
	if(debug) cout << "this is my new W boson: " << W->pdgId() << "\t" << W->status() << "\t" << W->px() << endl;
	W_found = true;

      // lep and neutrino:
	if( abs( W->daughter(0)->pdgId() ) == 11 || 
	    abs( W->daughter(0)->pdgId() ) == 13 || 
	    abs( W->daughter(0)->pdgId() ) == 15 ){
	  lep = W->daughter(0);
	  nu  = W->daughter(1);
	  mcSS->mcLepID = W->daughter(0)->pdgId();
	  lep_found = true;
	  nu_found  = true;
	}
	else{
	  lep = W->daughter(1);
	  nu  = W->daughter(0);
	  mcSS->mcLepID = W->daughter(1)->pdgId();
	  lep_found = true;
	  nu_found  = true;
	  if(debug) cout << "INFO: W boson daughters switched!" << endl;
	  printList(genParticles,3);
	}
      }


      mcSS->p4_nu_gen.SetCoordinates(nu->px(), nu->py(), nu->pz(), nu->energy());
      mcSS->p4_lep_gen.SetCoordinates(lep->px(), lep->py(), lep->pz(), lep->energy());
      //      mcSS->mcLepID = lep->pdgId();
	    
      if(abs(lep->pdgId()) == 11 || abs(lep->pdgId()) == 13)
	mcSS->DecChan = 0;
      if(abs(lep->pdgId()) == 15)
	mcSS->DecChan = 1;
            
    }
    
    // second b quark:
    if(!secb_found && p->pdgId() == secb_id){
      if (debug) cout << "I've found a second b quark" << endl;
      const Candidate * mom = p->mother(0);
      if (debug) cout << "It has code " << secb_id << " while its mother has code " << mom->pdgId() << endl;
      if (mom->pdgId() == secb_id) mom = mom->mother(0);
      if (debug) cout << "The top's mother has code " << top->mother(0)->pdgId() << endl;
      if(mom->pdgId() == top->mother(0)->pdgId()){ 
	secb_found = true;
	mcSS->p4_2ndb_gen.SetCoordinates(p->px(), p->py(), p->pz(), p->energy());
	if(debug) cout << "secb found in line " << idx << endl;
      }
    }

    idx++;
  } // END: particle loop  

  // ----------------------
  //    error messages:
  // ----------------------

  if(!secb_found){
    //    if(!noVtb && !isGluonSplitLQLine){
      cout << "ERROR: no secb found!" << endl;
      error = true;
      //}
  }
  if(!top_found){
    cout << "ERROR: no top found!" << endl;
    error = true;
  }
  if(!btop_found){
    cout << "ERROR: no btop found!" << endl;
    error = true;
  }
  if(!W_found){
    cout << "ERROR: no W found!" << endl;
    error = true;
  }
  if(!lep_found){
    cout << "ERROR: no lep found!" << endl;
    error = true;
  }
  if(!nu_found){
    cout << "ERROR: no nu found!" << endl;
    error = true;
  }
  /*
  if(!lq_found){
    if(noVtb)
      cout << "no Vtb vertex - no event acceptance ..." << endl;
    else {
      if(isGluonSplitLQLine)
	cout << "gluon splitting in lq line - no event acceptance ..." << endl;
      else{
	error = true;
	cout << "ERROR: no lq found!" << endl;
      }
    }
  }
  */
  
  if(error){
    printList(genParticles,3);
    //    ErrCount++;
  }
  
  

}

void SSParton::printList(edm::Handle<std::vector<reco::GenParticle> > genParticles, int pStatus)
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



