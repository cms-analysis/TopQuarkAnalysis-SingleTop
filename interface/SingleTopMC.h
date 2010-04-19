#ifndef __CATO_CMS_SINGLE_TOP_MC_H__
#define __CATO_CMS_SINGLE_TOP_MC_H__

//-------------------------------------------------------------------------------
// Header file for the MCCatoSingleTop class. 
//  
//
// CVS revision record:
// $Author: weinelt $
// $Date: 2010/01/14 16:38:31 $
// $Revision: 1.1 $
// 
//-------------------------------------------------------------------------------

#include "Vec.h"

namespace CatoCMS
{
  class SingleTopMC 
  {
  public:
    SingleTopMC();
    ~SingleTopMC();
    
    void Reset();
    
    // filled for all DecChans
    LorentzVector p4_q1_gen; 
    LorentzVector p4_q2_gen; 
    LorentzVector p4_2ndb_gen; 
    LorentzVector p4_top_gen;     
    LorentzVector p4_btop_gen;      
    LorentzVector p4_Wtop_gen;    
    LorentzVector p4_lep_gen;      
    LorentzVector p4_nu_gen;      
    
    double QLep_gen;             // charge of the lepton
    
    int procID;                  // = 22 for 2->2 process
                                 // = 23 for 2->3 process
    
    //Int_t ProdProc;            // =1 for q + qbar -> gluon
                                 // =2 for gluon + gluon -> gluon
    // ---->> not filled!

    int    DecChan;              // =0 for e/mu/nu
                                 // =1 for tau/nu
                                 // =2 for qqbar (not included in MG samples!!)
    
    int    mcLepID;              // set for decay channel = 0 and = 1

    double eventWeight;          // event weight sign for mc@nlo 
    


    // pdf reweighting stuff ---------
    double partx[2];             // momentum fraction of initial partons 
    int    ptype[2];             // parton type (u,d,s,...,g) of initial partons
    double Qscale;               // factorisation scale mu=Q (GeV)  
    double PDFval[60];           // PDF values: f_p(x_p)*f_pbar(x_pbar) 
                                 // for different PDF's
  }; 
}
#endif
