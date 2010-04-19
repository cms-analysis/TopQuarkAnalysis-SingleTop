#ifndef __CATO_CMS_MET_H__
#define __CATO_CMS_MET_H__


#include <map>
#include <vector>
#include <string>

//#include "TVector2.h"

#include "Vec.h"

namespace CatoCMS
{
  class MET
  {
  public:
    MET();
    ~MET();
    
    void Reset();
    
    //    TVector2   misEt;
    LorentzVector v4;        // missing Et vector -->> 4D vector since no 2D object available in [root/5.14.00f-CMS3q] ...
    std::vector<double> dmEx;   // missing Et x corrections
    std::vector<double> dmEy;   // missing Et y corrections
    double sumEt;               // scalar sum of transverse energy over all objects
    
  };
}
#endif
