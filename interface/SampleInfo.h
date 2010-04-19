#ifndef __CATO_CMS_SAMPLE_INFO__
#define __CATO_CMS_SAMPLE_INFO__

#include <string>
#include <vector>

namespace CatoCMS
{
  class SampleInfo
  {
  public:
    SampleInfo();
    ~SampleInfo();
    
    double  cross_section;
    int	TotalEvents;
    std::string	Name;
    std::vector<std::pair<int, int> > LostEvts;  // pair<ProcID,NLostEvts>
  };
}
#endif 
