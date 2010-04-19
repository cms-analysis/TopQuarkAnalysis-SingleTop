//-------------------------------------------------------------------------------
//
// CVS revision record:
// $Author: weinelt $
// $Date: 2010/01/14 16:39:11 $
// $Revision: 1.1 $
// 
//-------------------------------------------------------------------------------

#include "TLorentzVector.h"
#include "TopQuarkAnalysis/SingleTop/interface/TTbarMC.h"

using namespace CatoCMS;

CatoCMS::TTbarMC::TTbarMC() :
  QLep_gen(0), Tautag(-1), ProdProc(-1), DecChan(-1), mc_LepID(-1), weight(1), Qscale(-1)
{
}

CatoCMS::TTbarMC::~TTbarMC() 
{
}

void CatoCMS::TTbarMC::Reset()
{
  QLep_gen = 0;
  Tautag = -1;
  ProdProc = -1;
  DecChan = -1;
  mc_LepID = -1;
  weight = 1;
  for (int i=0; i<2; i++){
    partx[i] = -99.;                        
    ptype[i] = -99;                       
  }                       
  Qscale = -1; 
  for (int i=0; i<60; i++){
    PDFval[i] = 0.;    
  }
  p4Parton1_gen.SetCoordinates(0.0, 0.0, 0.0, 0.0);
  p4Parton2_gen.SetCoordinates(0.0, 0.0, 0.0, 0.0);
  p4Top_lep_gen.SetCoordinates(0.0, 0.0, 0.0, 0.0); 
  p4Top_had_gen.SetCoordinates(0.0, 0.0, 0.0, 0.0);
  p4Lep_gen.SetCoordinates(0.0, 0.0, 0.0, 0.0); 
  p4Nu_gen.SetCoordinates(0.0, 0.0, 0.0, 0.0);
  p4W_lep_gen.SetCoordinates(0.0, 0.0, 0.0, 0.0); 
  p4B_lep_gen.SetCoordinates(0.0, 0.0, 0.0, 0.0);
  p4Q1_had_gen.SetCoordinates(0.0, 0.0, 0.0, 0.0);
  p4Q2_had_gen.SetCoordinates(0.0, 0.0, 0.0, 0.0);
  p4W_had_gen.SetCoordinates(0.0, 0.0, 0.0, 0.0);
  p4B_had_gen.SetCoordinates(0.0, 0.0, 0.0, 0.0);
}
