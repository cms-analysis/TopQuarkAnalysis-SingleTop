#ifndef __CATO_CMS_TTbar_MC_H__
#define __CATO_CMS_TTbar_MC_H__

//-------------------------------------------------------------------------------
// Header file for the MCCatoTTbar class. 
//  
//
// CVS revision record:
// $Author: weinelt $
// $Date: 2010/01/14 16:38:31 $
// $Revision: 1.1 $
// 
//-------------------------------------------------------------------------------

//#include "TLorentzVector.h"
#include "Vec.h"

namespace CatoCMS
{
	class TTbarMC 
	{
		public:
		 TTbarMC();
		 ~TTbarMC();

		 void Reset();

		 //for qqbar + e/mu/nu
		 LorentzVector p4Parton1_gen; 
		 LorentzVector p4Parton2_gen; 
		 LorentzVector p4Top_lep_gen; 
		 LorentzVector p4Top_had_gen; 
		 LorentzVector p4Lep_gen;     
		 LorentzVector p4Nu_gen;      
		 LorentzVector p4W_lep_gen;    
		 LorentzVector p4B_lep_gen;      
		 LorentzVector p4Q1_had_gen;      
		 LorentzVector p4Q2_had_gen;      
		 LorentzVector p4W_had_gen;     
		 LorentzVector p4B_had_gen;
		 double QLep_gen;                        // charge of the lepton

		 int Tautag;                           // =1 if charged lepton is Tau
                                          // =0 else
  	 int ProdProc;                         // =1 for q + qbar -> gluon
                                          // =2 for gluon + gluon -> gluon

  	 int DecChan;                          // =0 for qqbar + e/mu/nu
                                          // =1 for qqbar + tau/nu
                                          // =2 for qqbar + qqbar
                                          // =3 for e/mu/nu + e/mu/nu
                                          // =4 for e/mu/nu + tau/nu
                                          // =5 for tau/nu + tau/nu

  	int mc_LepID;                          // set for decay channel = 0 and = 1

		int weight;                           // = -1 if (Ep-Epbar)>0 
                                          // =  1  else

		double partx[2];                        // momentum fraction of initial partons 
		int    ptype[2];                        // parton type (u,d,s,...,g) of initial
                                          // partons
		double Qscale;                          // factorisation scale mu=Q (GeV)  
		double PDFval[60];                      // PDF values: f_p(x_p)*f_pbar(x_pbar) 
                                          // for different PDF's
	}; 
}
#endif
