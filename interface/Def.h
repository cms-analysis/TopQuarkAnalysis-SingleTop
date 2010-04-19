#ifndef __CATO_CMS_DEF_H__
#define __CATO_CMS_DEF_H__

namespace CatoCMS
{
  class Def {
  public:
    static const int nDet = 6;
    enum LeptonCategories {
      BARREL_GOLDEN = 0,
      BARREL_BIGBREM = 10,
      BARREL_NARROW = 20,
      BARREL_SHOWERING_NBREM_0 = 30,
      BARREL_SHOWERING_NBREM_1 = 31,
      BARREL_SHOWERING_NBREM_2 = 32,
      BARREL_SHOWERING_NBREM_3 = 33,
      BARREL_SHOWERING_NBREM_MORE_THAN_4 = 34,
      BARREL_CRACK = 40,
      
      ENDCAP_GOLDEN = 100,
      ENDCAP_BIGBREM = 110,
      ENDCAP_NARROW = 120,
      ENDCAP_SHOWERING_NBREM_0 = 130,
      ENDCAP_SHOWERING_NBREM_1 = 131,
      ENDCAP_SHOWERING_NBREM_2 = 132,
      ENDCAP_SHOWERING_NBREM_3 = 133,
      ENDCAP_SHOWERING_NBREM_MORE_THAN_4 = 134,
      
      NONE = -1,
      ALL  = 1000,
      BARREL = 1001,
      ENDCAP = 1002
    };
    enum LeptonID{	
      ELECTRON,
      MUON,
      TAU
    };
  };
}
#endif



