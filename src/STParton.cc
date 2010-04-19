// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
//
//   new filling method since 22x ... only valid for MG tchannel samples!! 
//   (no guaratee for other MC generators ... )
//   JW - 26. Jan. 2009 
//
// +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#include <iostream>
#include <iomanip>

#include "TopQuarkAnalysis/SingleTop/interface/STParton.h"


STParton::STParton(){
}


STParton::~STParton(){
}


void STParton::GetSingleTopTruth(edm::Handle<std::vector<reco::GenParticle> > genParticles, double weight, CatoCMS::SingleTopMC* mcST)
{
  bool debug = false;

  using namespace std;
  using namespace edm;
  using namespace reco;

  mcST->Reset();

  bool error              = false;
  bool isGluonSplitLQLine = false;
  bool noVtb              = false;
  
  bool top_found  = false;
  bool btop_found = false;
  bool W_found    = false;
  bool lep_found  = false;
  bool nu_found   = false;
  bool lq_found   = false;
  bool secb_found = false;

  bool noW        = true; // MG samples 22x: sometimes no W from top decay listed, build it as sum of lep and nu!
  bool noTop      = true; // MG samples 22x: sometimes no top listed, build it as sum of lep, nu, and btop!

  int idx       = 0;
  int top_id    = 0;
  int secb_id   = 0;
  int btop_id   = 0;

  const Candidate *topMo=NULL, *top=NULL ,*W=NULL, *btop=NULL,*lep=NULL, *nu=NULL;
  
  // get event weight 
  double wgt = 0;
  wgt = (weight > 0) ? 1. : -1.; // take only sign of event weigth!
  
  mcST->eventWeight = wgt;
  
  //   h["eventWeightSign"]->Fill(wgt);
  //   h["eventWeight"]->Fill(weight);
  
  for(std::vector<reco::GenParticle> ::const_iterator p=genParticles->begin(); p != genParticles->end(); ++p){
    
    

    if((abs(p->pdgId()) == 11 
	|| abs(p->pdgId()) == 13 
	|| abs(p->pdgId()) == 15) && !lep_found){  // charged lepton found ...first one in list
      lep = &(*p);
      lep_found = true;
      
      mcST->mcLepID = p->pdgId();

      // lep info  -------------------------------------------------------------
      if(lep->pdgId() == -11 || lep->pdgId() == -13 || lep->pdgId() == -15){
	top_id = 6;
	secb_id = -5;
	btop_id = 5;
	mcST->QLep_gen = 1;
      }
      else 
	if(lep->pdgId() == 11 || lep->pdgId() == 13 || lep->pdgId() == 15){
	  top_id = -6;
	  secb_id = 5;
	  btop_id = -5;
	  mcST->QLep_gen = -1;
	}
      
      if(p->numberOfMothers()>= 1){
	for (unsigned int ilepM=0; ilepM<p->numberOfMothers(); ilepM++){       // check lep mothers ...
	  if(abs(p->mother(ilepM)->pdgId()) == 24){                            // yes, we found the W!!
	    W=p->mother(ilepM);
	    W_found = true;
	    noW = false;
	    // set neutrino ...
	    for (unsigned int iWD=0; iWD<W->numberOfDaughters(); iWD++){
	      if(abs(W->daughter(iWD)->pdgId()) == 12 
		 || abs(W->daughter(iWD)->pdgId()) == 14 
		 || abs(W->daughter(iWD)->pdgId()) == 16){
		nu=W->daughter(iWD);
		nu_found = true;
	      }
	    }
	    for (unsigned int iWM=0; iWM<W->numberOfMothers(); iWM++){   //check W mothers ...
	      if(abs(W->mother(iWM)->pdgId()) == 6){                     // yes, we found the top via the W!!
		top=W->mother(iWM);
		top_found = true;
		noTop = false;
	      }
	    }
	    if(!top_found){                                                                    // no top found in list -> need to get btop as daughter of W mother
	      for (unsigned int iWM=0; iWM<W->numberOfMothers(); iWM++){                       // check W mothers
		for (unsigned int iWMD=0; iWMD<(W->mother(iWM))->numberOfDaughters(); iWMD++){ // check daughters of W mothers
		  if((W->mother(iWM))->daughter(iWMD)->pdgId() == btop_id){                    // btop found
		    btop_found = true;
		    btop = (W->mother(iWM))->daughter(iWMD);
		  }
		}
	      }
	    }
	    else{                                                                 // top was found, we are able to check directly the top daughters to find btop
	      for (unsigned int itop=0; itop<top->numberOfDaughters(); itop++){   //check top daughters ...
		if(abs(top->daughter(itop)->pdgId()) == 5){                       // btop found
		  btop = top->daughter(itop);
		  btop_found = true;
		}
	      }
	    }
	  }
	  else{                                                      // no W found ... 
	    noW = true;
	    W_found = true;
	    if(abs(p->mother(ilepM)->pdgId()) == 6){                 //  ... but we found top directly as mother of lep ...-> no W in list!
	      top=p->mother(ilepM);
	      top_found = true;
	      noTop=false;
	      for (unsigned int itopD=0; itopD<top->numberOfDaughters(); itopD++){   // loop daughters of top to get neutrino:
		if(abs(top->daughter(itopD)->pdgId()) == 12 
		   || abs(top->daughter(itopD)->pdgId()) == 14 
		   || abs(top->daughter(itopD)->pdgId()) == 16){                     // neutrino found ...
		  nu = top->daughter(itopD);
		  nu_found = true;
		}
		if(abs(top->daughter(itopD)->pdgId()) == 5){                         // btop found
		  btop = top->daughter(itopD);
		  btop_found = true;
		}
	      }
	    }
	  }
	}
	
	// special case: neither top nor W are in the list!
	if(noW)
	  if(noTop){
	    for (unsigned int ilepM=0; ilepM<lep->numberOfMothers(); ilepM++){                           // check mothers of lepton
	      for (unsigned int ilepMD=0; ilepMD<(lep->mother(ilepM))->numberOfDaughters(); ilepMD++){   // check daughters of lepton mothers
		if((lep->mother(ilepM))->daughter(ilepMD)->pdgId() == btop_id){                          // found btop
		  btop_found = true;
		  btop = (lep->mother(ilepM))->daughter(ilepMD);
		}
		if(abs((lep->mother(ilepM))->daughter(ilepMD)->pdgId()) == 12 
		   || abs((lep->mother(ilepM))->daughter(ilepMD)->pdgId()) == 14 
		   || abs((lep->mother(ilepM))->daughter(ilepMD)->pdgId()) == 16){
		  nu_found = true;                                                                       // found neutrino 
		  nu = (lep->mother(ilepM))->daughter(ilepMD);
		}
	      }
	    }
	  }
      }
      
      // decay channel:
      if(abs(lep->pdgId()) == 11 || abs(lep->pdgId()) == 13)
	mcST->DecChan = 0;
      if(abs(lep->pdgId()) == 15)
	mcST->DecChan = 1;
      
      
      // --------------------- DEBUG INFO ----------------------------------------
      if(debug)cout << "after first finding stuff .. let's summarize:" << endl;
      
      if(noW && !noTop)
	if(debug) cout << "there is no W from top decay!" << endl;
      if(noTop && !noW)
	if(debug) cout << "there is no top!" << endl;
      if(noW && noTop)
	if(debug) cout << "there is neither top nor W in list!" << endl;
      
      if(!noTop) if(debug) cout << "this is my new top: " << top->pdgId() << "\t" << top->status() << "\t" << top->px() << endl;
      if(!noTop && !noW) if(debug) cout << "this is my new btop: " << btop->pdgId() << "\t" << btop->status() << "\t" << btop->px() << endl;		      
      if(!noW) if(debug) cout << "this is my new W boson: " << W->pdgId() << "\t" << W->status() << "\t" << W->px() << endl;
      if(debug) cout << "this is my new neutrino: " << nu->pdgId() << "\t" << nu->status() << "\t" << nu->px() << endl;		
      if(debug) cout << "this is my new lepton: " << lep->pdgId() << "\t" << lep->status() << "\t" << lep->px() << endl;		
      // --------------------- DEBUG INFO END ----------------------------------------
      
     
      // --- light quark ----------------------
      
      const Candidate *p_=NULL; // pointer to "earliest" parton in process chain after the hard scattering 
                                //             (which has initial state partons as mothers)
                                // ideal: top is in list
                                // if not: set it on W
                                // if no W: set it on lepton
      
      if(!noTop){                              // top was found!
	p_ = &(*top);      
      }
      else{
	if(noTop && !noW)                      // not top, but we have a W
	  p_ = &(*W);
	else if(noTop && noW) p_ = &(*lep);    // we have neither top nor W in the list ... 
      }
      
      // ---------------------------------- OLD MCatNLO STUFF ------------------------------------------
      // check if we have gluon splitting in the light quark line:
      if( ( p_->mother(0)->pdgId() == 21 && abs( p_->mother(1)->pdgId() ) == 5 ) 
	  || ( p_->mother(1)->pdgId() == 21 && abs( p_->mother(0)->pdgId() ) == 5 )){
	isGluonSplitLQLine = true;
      }
      // check if we have a Vtb vertex (for events w/o gluon splitting!):
      if(abs(p_->mother(0)->pdgId()) < 5 && abs(p_->mother(1)->pdgId()) < 5){
	noVtb = true;
      }
      // --------------------------------- END OLD MCatNLO STUFF ----------------------------------------
      
      
      // choose light quark as topMother:               // "top mother" is now (more general) 
      if( abs( p_->mother(0)->pdgId() ) < 5 )           //  the mother of the starting paticle (top, W, or lep) 
	topMo = p_->mother(0);
      else
	topMo = p_->mother(1);
      
      // if the incoming light quark comes directly from the proton:
      if(!noVtb && !isGluonSplitLQLine){
	// top mother:
	int nd = topMo->numberOfDaughters();
	for (int j = 0; j<nd; j++){
	  if(abs( topMo->daughter(j)->pdgId() ) < 5 
	     && topMo->daughter(j)->pdgId() != topMo->pdgId()){
	    const Candidate *lq = topMo->daughter(j);
	    mcST->p4_q2_gen.SetCoordinates(lq->px(), lq->py(), lq->pz(), lq->energy());
	    lq_found = true;
	    if(debug) cout << "this is my new light quark: " << lq->pdgId() 
			   << "\t" << lq->status() << "\t" << lq->px() << endl;
	  }
	}
      }
    }
    
   
  } // END: particle loop  
  
  // second particle loop for second b quark, since charge is not determined before lep was found, 
  // but 2ndb is often listed above the lepton (23 process)!  
  for(std::vector<reco::GenParticle> ::const_iterator p=genParticles->begin(); p != genParticles->end(); ++p){
    // second b quark:
    if(!secb_found && p->pdgId() == secb_id){
      const Candidate * mom = p->mother(0);
      if(abs(mom->pdgId()) < 6 || mom->pdgId() == 21){
	secb_found = true;
	mcST->p4_2ndb_gen.SetCoordinates(p->px(), p->py(), p->pz(), p->energy());
	if(p->status() == 2)
	  mcST->procID = 22;
	else{
	  if(p->status() == 3)
	    mcST->procID = 23;
	}
	if(debug) cout << "secb found in line " << idx << endl;
      }
    }
    idx++;
    if(secb_found)
      break;
  } // END: particle loop
  
  
  // set four vectors of SingleTopT Truth ----------------------------------------------:

  mcST->p4_nu_gen.SetCoordinates(nu->px(), nu->py(), nu->pz(), nu->energy());
  mcST->p4_lep_gen.SetCoordinates(lep->px(), lep->py(), lep->pz(), lep->energy());
  mcST->p4_btop_gen.SetCoordinates(btop->px(), btop->py(), btop->pz(), btop->energy());
  
  if(!noTop){  // top found
    mcST->p4_top_gen.SetCoordinates(top->px(), top->py(), top->pz(), top->energy());
    if(!noW) mcST->p4_Wtop_gen.SetCoordinates(W->px(), W->py(), W->pz(), W->energy()); // and W found
    else mcST->p4_Wtop_gen.SetCoordinates((lep->px()+nu->px()), (lep->py()+nu->py()), (lep->pz()+nu->pz()), (lep->energy()+nu->energy())); // no W found
  }
  else{      // no top found 
    if(!noW){ // but W found
      mcST->p4_top_gen.SetCoordinates((W->px()+btop->px()),(W->py()+btop->py()),(W->pz()+btop->pz()),(W->energy()+btop->energy()));
      mcST->p4_Wtop_gen.SetCoordinates(W->px(), W->py(), W->pz(), W->energy());
    }
    else{     // neither top nor W
      mcST->p4_Wtop_gen.SetCoordinates((lep->px()+nu->px()), (lep->py()+nu->py()), (lep->pz()+nu->pz()), (lep->energy()+nu->energy()));
      mcST->p4_top_gen.SetCoordinates((lep->px()+nu->px()+btop->px()), (lep->py()+nu->py()+btop->py()), 
				      (lep->pz()+nu->pz()+btop->pz()), (lep->energy()+nu->energy()+btop->energy()));
    }
  }
  
  // ----------------------
  //    error messages:
  // ----------------------

  if(!secb_found){
    if(!noVtb && !isGluonSplitLQLine){
      cout << "ERROR: no secb found!" << endl;
      error = true;
    }
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
  
  if(error){
    printList(genParticles,3);
    //    ErrCount++;
  }
}




void STParton::printList(edm::Handle<std::vector<reco::GenParticle> > genParticles, int pStatus)
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
    if (!(p->status() >= pStatus)) continue;   //print only particles with status larger or equal than pStatus
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
