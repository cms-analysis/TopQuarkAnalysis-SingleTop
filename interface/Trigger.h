#ifndef __CATO_CMS_Trigger_H__
#define __CATO_CMS_Trigger_H__


#include <map>
#include <vector>
#include <string>

//#include "TVector2.h"

#include "Vec.h"

namespace CatoCMS
{
  class Trigger
  {
  public:
    Trigger();
    ~Trigger();
    
    void Reset();
    
    int mu;
    int el;
  };
}
#endif
