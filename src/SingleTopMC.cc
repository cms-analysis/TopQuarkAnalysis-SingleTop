#include "TopQuarkAnalysis/SingleTop/interface/SingleTopMC.h"

using namespace CatoCMS;

SingleTopMC::SingleTopMC() :
  QLep_gen(0), DecChan(-1), mcLepID(-1), eventWeight(0), Qscale(-1)

{
  

}

SingleTopMC::~SingleTopMC() 
{
}

void SingleTopMC::Reset()
{
  QLep_gen = 0;
  DecChan = -1;
  mcLepID = -1;
  eventWeight = 0.;
  procID = 0;
  for (int i=0; i<2; i++){
    partx[i] = -99.;                        
    ptype[i] = -99;                       
  }                       
  Qscale = -1; 
  for (int i=0; i<60; i++){
    PDFval[i] = 0.;    
  }
  p4_q1_gen.SetCoordinates(0.0, 0.0, 0.0, 0.0);
  p4_q2_gen.SetCoordinates(0.0, 0.0, 0.0, 0.0);
  p4_2ndb_gen.SetCoordinates(0.0, 0.0, 0.0, 0.0);
  p4_top_gen.SetCoordinates(0.0, 0.0, 0.0, 0.0); 
  p4_btop_gen.SetCoordinates(0.0, 0.0, 0.0, 0.0);
  p4_Wtop_gen.SetCoordinates(0.0, 0.0, 0.0, 0.0); 
  p4_lep_gen.SetCoordinates(0.0, 0.0, 0.0, 0.0);
  p4_nu_gen.SetCoordinates(0.0, 0.0, 0.0, 0.0);
}
