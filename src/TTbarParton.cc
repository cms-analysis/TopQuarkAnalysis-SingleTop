#define DEBUG 0 // 0=false

#include <iostream>
#include <iomanip>

#include "TopQuarkAnalysis/SingleTop/interface/TTbarParton.h"

using namespace std;
using namespace edm;
using namespace reco;

//math::XYZTLorentzVector

TTbarParton::TTbarParton(){
}


TTbarParton::~TTbarParton(){
}


void TTbarParton::GetTTbarTruth( edm::Handle<std::vector<reco::GenParticle> > genParticles, double weight,
				   CatoCMS::TTbarMC* mcTT){
#if DEBUG
  std::cout << "GetTTbarTruth" << std::endl;
#endif
 
   mcTT->Reset();

  double Qlep=0;
  double checksum=0;
  
  bool q1set=false;
  bool q2set=false;
  bool p2set=false;
  bool nu_set=false;
  bool W2bq=false;
  bool blep=false;
  bool bhad=false;

  const Candidate* lep=0;
  const Candidate* lepMo=0;

  const Candidate* W=0;
  const Candidate* WMo=0;
  const Candidate* Wq1=0;
  const Candidate* Wq1Mo=0;
  
  const Candidate* Top=0;
  const Candidate* Topq1=0;
  
  const Candidate* Q1=0;
  const Candidate* Q1Mo=0;
  const Candidate* Q2=0;
  const Candidate* Q2Mo=0;
  
  const Candidate* B=0;
  const Candidate* BMo=0;

  math::XYZTLorentzVector paV;

  
  //---------------------------------------------------------------------------
  //                 decay channel: (DecChan)
  //---------------------------------------------------------------------------
  int e=0,t=0,m=0;

#if DEBUG
  int num=0;
  
#endif

  //cout << " Ind    ID   Charge  NDa  Da1        E      Mass  NMo  Mo1         Px         Py         Pz   Stdhep" << endl;
  
  int indPa = 0;

  for(std::vector<reco::GenParticle> ::const_iterator paIt = genParticles->begin();
      paIt != genParticles->end(); paIt++){ //Loop over particles 1
    if(paIt->status() != 3) continue;
    int indMo = -999;
    if(paIt->numberOfMothers() > 0)  indMo=paIt->mother()->pdgId();

    int indDa = -999;
    if(paIt->numberOfDaughters() > 0)  indDa=paIt->daughter(0)->pdgId();
    //cout << setw(4)<< indPa << " " << setw(5) << paIt->pdgId() << " "<< setw(8) << paIt->charge() << " "<< setw(4) << paIt->numberOfDaughters() << " "<< setw(4) <<  indDa <<" "<< setw(8) <<  paIt->energy() << " " <<" "<< setw(8) << paIt->mass() << " "<< setw(4) << paIt->numberOfMothers() << " "<< setw(4) << indMo <<" "<< setw(10) << paIt->px() << " "<< setw(10) << paIt->py() << " "<< setw(10) << paIt->pz() << " "<< setw(8) << paIt->status() << endl;
	//cout << setw(4)<< indPa << endl;
    indPa++;
  }

  
  for(std::vector<reco::GenParticle>::const_iterator paIt = genParticles->begin();
      paIt != genParticles->end(); paIt++){ //Loop over particles 1
    if(paIt->numberOfMothers() == 0) continue;
    if(paIt->status() != 3) continue;
    //Candidate pa = *paIt;
    
    int paKF = abs(paIt->pdgId());

    const Candidate* paMo = 0;
    int MoKF =0;
    //if ( paIt->numberOfMothers()>0 && ( &(*paIt->mother()) <= &(*paIt)) ){
      paMo = paIt->mother();
      MoKF = abs(paMo->pdgId());
      //}

    
//#if DEBUG 
//    std::cout<< "pa "<< paIt->index()<<" "<<paIt->pdgId()<<" "<<paIt->mother()<<"\n";
//    if(paMo)
//      std::cout<< "paMo "<<paMo->index()<<" "<<paMo->pdgId()<<" " <<paMo->hasChildren()<<"\n";
//#endif


    // finding electron ( -> W -> t )
    //--------------------------------
    if ( (paKF == 11) && (MoKF == 24) ){
      WMo = paMo;
      do{
	W = WMo;
	WMo = W->mother();
      }
      while ( (abs(WMo->pdgId()) == 24) && WMo->numberOfMothers()>0 );
	
      if (abs(WMo->pdgId()) == 6){	
	lep   = &(*paIt);
	Qlep  = ( paIt->pdgId() == 11 ) ? -1 : 1;
	lepMo = paMo;
	Top   = WMo;
	e++;
#if DEBUG
	std::cout << "electron found\n"
		  << paIt->index() << "\t" << W->pdgId()   << "\t"
		  << W->mother()   << "\t" << Top->pdgId() << "\n";
#endif
      }
    }

    
    // finding muon ( -> W -> t )
    //----------------------------
    if ( (paKF == 13) && (MoKF == 24) ){
      WMo = paMo;
      do{
	W = WMo;
	WMo = W->mother();
      }
      while ( (abs(WMo->pdgId()) == 24) && WMo->numberOfMothers()>0 );
	
      if (abs(WMo->pdgId()) == 6){	
	lep   =  &(*paIt);
	Qlep  = ( paIt->pdgId() == 13 ) ? -1 : 1;
	lepMo = paMo;
	Top   = WMo;
	m++;
#if DEBUG
	std::cout << "muon found\n"
		  << paIt->index() << "\t" << W->pdgId()   << "\t"
		  << W->mother()   << "\t" << Top->pdgId() << "\n";
#endif
      }
    }

    
    // finding tau ( -> W -> t ) 
    //-----------------------------
    if ( (paKF == 15) && (MoKF == 24) ){
      WMo = paMo;
      do{
	W =WMo;
	WMo = W->mother();
      }
      while ( (abs(WMo->pdgId()) == 24) && WMo->numberOfMothers()>0 );
	
      if (abs(WMo->pdgId()) == 6){	
	lep   =  &(*paIt);
	Qlep  = ( paIt->pdgId() == 15 ) ? -1 : 1;
	lepMo = paMo;
	Top   = WMo;
	t++;
#if DEBUG
	std::cout << "tau found\t"
		  << paIt->index() << "\t" << W->pdgId()  << "\t"
		  << W->mother()   << "\t" << Top->pdgId() << "\n";
#endif
      }
    }

  
    //-------------------------------------------------------------------------
    //                  production process: (ProdProc)
    //-------------------------------------------------------------------------
    if(paKF == 6){
     std::vector<reco::GenParticle>::const_iterator paIt2 = paIt+1;
      const Candidate* top2 = &(*paIt2);
      int top2KF = abs(top2->pdgId());
	
      if(top2KF == 6){
	const Candidate* topMo1 = paIt->mother();
	int topMo1KF = abs(topMo1->pdgId());

	  if(topMo1KF==1 || topMo1KF==2 || topMo1KF==3 
	     || topMo1KF==4 || topMo1KF==5)
	    mcTT->ProdProc=1;
	    
	  if(topMo1KF==21)
	    mcTT->ProdProc=2;
	  
      }
    }

  
#if DEBUG
    std::cout
      <<std::setw(5)<< (*paIt)->index()  << " "
      <<std::setw(5)<< (*paIt)->pdgId()   << " "
      <<std::setw(3)<< (*paIt)->mother()   << " "
      <<std::setw(3)<< (*paIt)->mother(1) << " \n";

    num++;

    if(num==20)
      break;

#endif

    if( (e+m+t)>1 )
      break;
    
  } //Loop over particles 1
    
  

  if((e==1 && m==0 && t==0) || (e==0 && m==1 && t==0))
    mcTT->DecChan=0;

  if(e==0 && m==0 && t==1){
    mcTT->DecChan=1;
    mcTT->Tautag=1;
  }

  if(e==0 && m==0 && t==0)
    mcTT->DecChan=2;

  if((e>1 && m==0 && t==0) || (e==0 && m>1 && t==0) || (e==1 && m==1 && t==0))
    mcTT->DecChan=3;

  if((e==1 && m==0 && t==1) || (e==0 && m==1 && t==1))
    mcTT->DecChan=4;

  if(e==0 && m==0 && t>1)
    mcTT->DecChan=5;
  
#if DEBUG
  std::cout << "DecChan = " << mcTT->DecChan << "\n";
#endif
  //---------------------------------------------------------------------------
  //        filling 4vectors for all DecChan 
  //---------------------------------------------------------------------------

 for(std::vector<reco::GenParticle>::const_iterator paIt = genParticles->begin();
     paIt != genParticles->end(); paIt++){//Loop over particles 2
   if(paIt->numberOfMothers() == 0) continue;
   if(paIt->status() != 3) continue;
   
   
   int paKF = abs(paIt->pdgId());
   const Candidate* paMo = 0;
   int MoKF =0;
   //if ( paIt->numberOfMothers()>0 && ( &(*(paIt->mother())) <= &(*paIt)) ){
   paMo = paIt->mother();
   MoKF = abs(paMo->pdgId());
   //}
   
   
   // finding parton1 & parton2:
   //----------------------------
   
   
   //finding p1 and p2 for Z'(32) or ordinary ttbar
   if(paKF == 32 || ( paKF == 6 && paIt->numberOfMothers()==2 ) ){
     const Candidate* part1 = paIt->mother();
     int part1KF = abs(part1->pdgId());
     //   std::cout << "Hier ist das Z' !!!" << std::endl;
     //std::cout << "Nmother = " << paIt->numberOfMothers() << std::endl;
     const Candidate* part2 = paIt->mother(1);
     int part2KF =abs(part2->pdgId());
     
     if(part1KF==1 || part1KF==2 || part1KF==3
	|| part1KF==4 || part1KF==5 || part1KF==21){
       
       paV = part1->p4();
       mcTT->p4Parton1_gen.SetCoordinates(paV.px(), paV.py(), 
				      paV.pz(), paV.e());
#if DEBUG
       std::cout << "set parton1_vec\n"
		 << paIt->pdgId() << "\t" << part1->pdgId() << "\n";
#endif
     } 
     if(part2KF==1 || part2KF==2 || part2KF==3
	|| part2KF==4 || part2KF==5 || part2KF==21){
       
       paV = part2->p4();
       mcTT->p4Parton2_gen.SetCoordinates(paV.px(), paV.py(), 
				      paV.pz(), paV.e());
       p2set =true;
       
#if DEBUG
       std::cout << "set parton2_vec\n"
		 << paIt->pdgId() << "\t" << part2->pdgId() << "\n";
#endif
     }
     
   }
   
   
 }
 //---------------------------------------------------------------------------
 //        filling 4vectors for DecChan=0/1 (lepton (e,mu,tau) + jets)
 //---------------------------------------------------------------------------

 if(mcTT->DecChan==0 || mcTT->DecChan==1)
   {


    // lep, Qlep, W, Top set above
    //-----------------------------
    paV = lep->p4();
    mcTT->p4Lep_gen.SetCoordinates(paV.px(), paV.py(), paV.pz(), paV.e());
    mcTT->QLep_gen = Qlep;
    mcTT->mc_LepID  = lep->pdgId();

    paV = W->p4();
    mcTT->p4W_lep_gen.SetCoordinates(paV.px(), paV.py(), paV.pz(), paV.e());
    
    paV = Top->p4();
    mcTT->p4Top_lep_gen.SetCoordinates(paV.px(), paV.py(), paV.pz(), paV.e());

   }
 // filling top 4-vectors for other decay channels
 else{
    for(std::vector<reco::GenParticle>::const_iterator paIt = genParticles->begin();
	paIt != genParticles->end(); paIt++){//Loop over particles 2
      if(paIt->numberOfMothers() == 0) continue;
      if(paIt->status() != 3) continue;
     
      int paKF = paIt->pdgId();

      //put top to top_had and antitop to top_lep
      if ( paKF==6 ){
		    
	paV = paIt->p4();
	mcTT->p4Top_had_gen.SetCoordinates(paV.px(), paV.py(), paV.pz(), paV.e());
      
      }
      if ( paKF==-6 ){
		    
	paV = paIt->p4();
	mcTT->p4Top_lep_gen.SetCoordinates(paV.px(), paV.py(), paV.pz(), paV.e());
      
      }
    }
 }
#if DEBUG
            
    std::cout << "set lep_vec\n"
	      << lep->pdgId() << "\t" << lep->mother() << "\t"
	      << lepMo->pdgId() << "\n"

	      << "set Wlep_vec\n"
	      << W->pdgId() << "\t" << W->mother() << "\t"
	      << WMo->pdgId() << "\n"

	      << "set Toplep_vec\n"
	      << Top->pdgId() << "\t" << Top->mother() << "\n";
#endif
 if(mcTT->DecChan==0 || mcTT->DecChan==1)
   {
    //std::cout << "TT: Start of loop 2" << std::endl;
    for(std::vector<reco::GenParticle>::const_iterator paIt = genParticles->begin();
	paIt != genParticles->end(); paIt++){//Loop over particles 2
      if(paIt->numberOfMothers() == 0) continue;
      if(paIt->status() != 3) continue;

     
      int paKF = abs(paIt->pdgId());
      const Candidate* paMo = 0;
      int MoKF =0;
      //if ( paIt->numberOfMothers()>0 && ( &(*(paIt->mother())) <= &(*paIt)) ){
	paMo = paIt->mother();
	MoKF = abs(paMo->pdgId());
	//}
      
      

      // finding neutrino  
      //------------------
      if ( (paKF==12 || paKF==14 || paKF==16)
	   && (MoKF == 24) && (paIt->mother()==lep->mother()) ){
		    
	paV = paIt->p4();
	mcTT->p4Nu_gen.SetCoordinates(paV.px(), paV.py(), paV.pz(), paV.e());
	nu_set =true;
	
#if DEBUG
	std::cout << "set nu_vec\n"
		  << paIt->index() << "\t" << paIt->pdgId()   << "\t"
		  << paIt->mother()  << "\t" << paMo->pdgId() << "\n";
#endif
      }
      

      // finding q1 & q2:
      //------------------
      if( (paKF <= 5) && (MoKF == 24) ){
	if( paKF==5 )
	  W2bq=true;	
	
	Wq1Mo = paMo;
	do{
	  Wq1 = Wq1Mo;
	  Wq1Mo = Wq1->mother();
	}
	while ( (abs(Wq1Mo->pdgId()) == 24) && Wq1Mo->numberOfMothers()>0 );

	

	if (abs(Wq1Mo->pdgId()) == 6){
	  if(!q1set){
	    
	    Q1 =  &(*paIt);
	    Q1Mo = paMo;
	    paV = Q1->p4();
	    mcTT->p4Q1_had_gen.SetCoordinates(paV.px(), paV.py(), 
					  paV.pz(), paV.e());
	    
	    //W_had found -> set 4vector
	    paV = Wq1->p4();
	    mcTT->p4W_had_gen.SetCoordinates(paV.px(), paV.py(), 
					 paV.pz(), paV.e());
	    
	    Topq1 = Wq1->mother();
	    //Top_had found -> set 4vector
	    paV = Topq1->p4();
	    mcTT->p4Top_had_gen.SetCoordinates(paV.px(), paV.py(), 
					   paV.pz(), paV.e());
	    q1set=true;
#if DEBUG
	    std::cout << "set q1_vec\n"
		      << paIt->index() << "\t" << Q1->pdgId()   << "\t"
		      << Q1->mother()  << "\t" << Q1Mo->pdgId() << "\n"
		  

		      << "set had_vecs 1\n"
		      << Wq1->pdgId() << "\t"
		      << Wq1->mother() << "\t" << Wq1Mo->pdgId() << "\n"
	    
		      << "set topq1\n"
		      << Topq1->pdgId() << "\t" << Topq1->mother() << "\n";
#endif
	  }

	  
	  if(q1set && (paIt->mother()==Q1->mother()) && (&(*paIt) != (&(*Q1))) ){
	    //q2 found -> set 4vector
	    
	    Q2 =  &(*paIt);
	    Q2Mo = paMo;
	    paV = Q2->p4();
	    mcTT->p4Q2_had_gen.SetCoordinates(paV.px(), paV.py(), 
					  paV.pz(), paV.e());
	    q2set=true;
#if DEBUG
	    std::cout << "set q2_vec\n"
		      << paIt->index() << "\t" << Q2->pdgId()   << "\t"
		      << Q2->mother()  << "\t" << Q2Mo->pdgId() << "\n";
#endif
	  }
	  
	}
      }
      

     
     if(nu_set && q2set && p2set)
       break;
     
    }//Loop over particles 2
    
        
    // check Whad decay into q1, q2:
    //----------------------------
    
    

    checksum = (abs(Q1->pdgId())+abs(Q2->pdgId()));

    if(W2bq && checksum==9)
      mcTT->DecChan=(mcTT->DecChan)+20;            // decay: W->bc
    
    if(W2bq && checksum==7)
      mcTT->DecChan=(mcTT->DecChan)+200;           // decay: W->bu
    
    if(!W2bq && checksum==5)
      mcTT->DecChan=(mcTT->DecChan)+2000;          // decay: W->su
  
        
    if((mcTT->DecChan)>2){
#if DEBUG
      std::cout << "!! SPECIAL EVENT !! DecChan=" << mcTT->DecChan << "\n"
 		<< "no code" << "\n";
#endif
    }
  
    
    for(std::vector<reco::GenParticle>::const_iterator paIt = genParticles->begin();
      paIt != genParticles->end(); paIt++){//Loop over particles 3
      if(paIt->numberOfMothers() == 0) continue;
      if(paIt->status() != 3) continue;

      //Candidate* pa = *paIt;
      int paKF = abs(paIt->pdgId());

      const Candidate* paMo = 0;
      int MoKF =0;
      //if ( paIt->numberOfMothers()>0 && ( &(*paIt->mother()) <= &(*paIt)) ){
	paMo = paIt->mother();
	MoKF = abs(paMo->pdgId());
      //}

    
      // finding B_lep & B_had:
      //------------------------          
      if ( (paKF==5 || paKF==3 || paKF==1) && MoKF==6 ){
	if(!blep || !bhad){
	  if(paKF==3){                             // t->Ws
	    mcTT->DecChan=(mcTT->DecChan)+10;
	    // std::cout << "DecChan+10" << endl;
	  }
	  if(paKF==1){                             // t->Wd
	    mcTT->DecChan=(mcTT->DecChan)+100;
	    // std::cout << "DecChan+100" << endl;
	  }                                        // DecChan = 1: t->Wb
	  B = &(*paIt);
	  if (B->mother() == W->mother()){
	    BMo = paMo;
	    paV = B->p4();
	    mcTT->p4B_lep_gen.SetCoordinates(paV.px(), paV.py(), 
					 paV.pz(), paV.e());
	    blep=true;
#if DEBUG
	    std::cout << "set Blep_vec\n"
		      << paIt->index() << "\t" << B->pdgId()   << "\t"
		      << B->mother()   << "\t" << BMo->pdgId() << "\n";
#endif
	  }  
	  if (B->mother() == Wq1->mother()){
	    BMo = paMo;
	    paV = B->p4();
	    mcTT->p4B_had_gen.SetCoordinates(paV.px(), paV.py(), 
					 paV.pz(), paV.e());
	    bhad=true;
#if DEBUG
	    std::cout << "set Bhad_vec\n"
		      << paIt->index() << "\t" << B->pdgId()   << "\t"
		      << B->mother()   << "\t" << BMo->pdgId() << "\n";
#endif
	  }
	}
      }

      if(blep && bhad)
	break;
      
    }//Loop over particles 3
#if DEBUG
  std::cout << "TT: End of loop 3" << std::endl;
  std::cout << "DecChan=" << mcTT->DecChan << std::endl;
#endif
#if DEBUG
      
    std::cout << "\nP1   : " <<std::setw(15)<< mcTT->p4Parton1_gen.Px()
	      <<std::setw(15)<< mcTT->p4Parton1_gen.Py()
	      <<std::setw(15)<< mcTT->p4Parton1_gen.Pz()
	      <<std::setw(15)<< mcTT->p4Parton1_gen.E() <<"\n"
      
	      << "P2   : " <<std::setw(15)<< mcTT->p4Parton2_gen.Px()
	      <<std::setw(15)<< mcTT->p4Parton2_gen.Py()
	      <<std::setw(15)<< mcTT->p4Parton2_gen.Pz()
	      <<std::setw(15)<< mcTT->p4Parton2_gen.E() <<"\n\n"
	  
	      << "lep  : " <<std::setw(15)<< mcTT->p4Lep_gen.Px()
	      <<std::setw(15)<< mcTT->p4Lep_gen.Py()
	      <<std::setw(15)<< mcTT->p4Lep_gen.Pz()
	      <<std::setw(15)<< mcTT->p4Lep_gen.E() <<"\n"

	      << "nu   : " <<std::setw(15)<< mcTT->p4Nu_gen.Px()
	      <<std::setw(15)<< mcTT->p4Nu_gen.Py()
	      <<std::setw(15)<< mcTT->p4Nu_gen.Pz()
	      <<std::setw(15)<< mcTT->p4Nu_gen.E() <<"\n"
	  
	      << "W_lep: " <<std::setw(15)<< mcTT->p4W_lep_gen.Px()
	      <<std::setw(15)<< mcTT->p4W_lep_gen.Py()
	      <<std::setw(15)<< mcTT->p4W_lep_gen.Pz()
	      <<std::setw(15)<< mcTT->p4W_lep_gen.E() <<"\n"

	      << "B_lep: " <<std::setw(15)<< mcTT->p4B_lep_gen.Px()
	      <<std::setw(15)<< mcTT->p4B_lep_gen.Py()
	      <<std::setw(15)<< mcTT->p4B_lep_gen.Pz()
	      <<std::setw(15)<< mcTT->p4B_lep_gen.E() <<"\n"
	  
	      << "T_lep: " <<std::setw(15)<< mcTT->p4Top_lep_gen.Px()
	      <<std::setw(15)<< mcTT->p4Top_lep_gen.Py()
	      <<std::setw(15)<< mcTT->p4Top_lep_gen.Pz()
	      <<std::setw(15)<< mcTT->p4Top_lep_gen.E() <<"\n\n"

	      << "Q1   : " <<std::setw(15)<< mcTT->p4Q1_had_gen.Px()
	      <<std::setw(15)<< mcTT->p4Q1_had_gen.Py()
	      <<std::setw(15)<< mcTT->p4Q1_had_gen.Pz()
	      <<std::setw(15)<< mcTT->p4Q1_had_gen.E() <<"\n"

	      << "Q2   : " <<std::setw(15)<< mcTT->p4Q2_had_gen.Px()
	      <<std::setw(15)<< mcTT->p4Q2_had_gen.Py()
	      <<std::setw(15)<< mcTT->p4Q2_had_gen.Pz()
	      <<std::setw(15)<< mcTT->p4Q2_had_gen.E() <<"\n"
	  
	      << "W_had: " <<std::setw(15)<< mcTT->p4W_had_gen.Px()
	      <<std::setw(15)<< mcTT->p4W_had_gen.Py()
	      <<std::setw(15)<< mcTT->p4W_had_gen.Pz()
	      <<std::setw(15)<< mcTT->p4W_had_gen.E() <<"\n"

	      << "B_had: " <<std::setw(15)<< mcTT->p4B_had_gen.Px()
	      <<std::setw(15)<< mcTT->p4B_had_gen.Py()
	      <<std::setw(15)<< mcTT->p4B_had_gen.Pz()
	      <<std::setw(15)<< mcTT->p4B_had_gen.E() <<"\n"
	  
	      << "T_had: " <<std::setw(15)<< mcTT->p4Top_had_gen.Px()
	      <<std::setw(15)<< mcTT->p4Top_had_gen.Py()
	      <<std::setw(15)<< mcTT->p4Top_had_gen.Pz()
	      <<std::setw(15)<< mcTT->p4Top_had_gen.E() <<"\n\n";

	

    std::cout<<"\n"<<std::setw(4)<<"Id "<<std::setw(4)<<"KS "<<std::setw(6)<<"KF "<<std::setw(6)<<"Mo"<<std::setw(15)<<"Px "<<std::setw(15)<<"Py "<<std::setw(15)<<"Pz "<<std::setw(15)<<"Energy "<<"\n";
    
    int z=0;
    
      
    std::cout << "\n\n\n";

#endif

  
  }
  
 
}



