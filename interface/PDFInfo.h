#ifndef __CATO_CMS_PDFINFO_H__
#define __CATO_CMS_PDFINFO_H__


#include <map>
#include <vector>
#include <string>

//#include "TVector2.h"

#include "Vec.h"

namespace CatoCMS
{
  class PDFInfo
  {
  public:
    PDFInfo();
    ~PDFInfo();
    
    void Reset();

    double x1,x2;
    int id1,id2;
    double scalePDF;
    
  };
}
#endif
