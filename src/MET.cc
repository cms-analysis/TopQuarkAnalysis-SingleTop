#include "TopQuarkAnalysis/SingleTop/interface/MET.h"


using namespace CatoCMS;

MET::MET():
  sumEt(-999.)
{
}

MET::~MET()
{
}

void MET::Reset()
{
  v4.SetCoordinates(0.0,0.0,0.0,0.0);
  dmEx.clear();
  dmEy.clear();
  sumEt = -999.0;
}
