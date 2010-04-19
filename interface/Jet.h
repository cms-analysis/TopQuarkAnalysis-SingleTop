#ifndef __CATO_CMS_JET_H__
#define __CATO_CMS_JET_H__

#include <map>
#include <vector>
#include <string>

#include "Vec.h"

namespace CatoCMS
{
  class Jet 
  {
  public:
    Jet();
    ~Jet();
    
    void   Reset();
    double GetTag(std::string label="default");
    void   PrintTags();
    
    LorentzVector v4;         // 4 vector of jet.
    double        scale;      // Jet correction factor
    
    std::map<std::string, double> tags; 
    
    double emEnergyFraction;
    int    nTracks;
    int    partonFlavour;
    Point3 vertex;

    int    isTagged;        // flag for a tagged jet: is 1 for jets that fulfill the b tagging requirement,
                            //                        is 0 else
                            // ... filled in EventSelection.cc
    
  }; 
}
#endif

