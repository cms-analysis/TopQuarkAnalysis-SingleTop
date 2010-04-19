#include "TopQuarkAnalysis/SingleTop/interface/Event.h"
#include "TopQuarkAnalysis/SingleTop/interface/SingleTopMC.h"
#include "TopQuarkAnalysis/SingleTop/interface/SchannelMC.h"
#include "TopQuarkAnalysis/SingleTop/interface/SampleInfo.h"

#include "TopQuarkAnalysis/SingleTop/interface/CutMap.h"
#include "TopQuarkAnalysis/SingleTop/interface/CutFlowTable.h"
#include "TopQuarkAnalysis/SingleTop/interface/WJetsMC.h"
#include "TopQuarkAnalysis/SingleTop/interface/TTbarMC.h"
#include "TopQuarkAnalysis/SingleTop/interface/QCDMC.h"
#include "TopQuarkAnalysis/SingleTop/interface/PDFInfo.h"

#include <vector>
namespace{
  namespace{
    CatoCMS::Event        ev;
    CatoCMS::Jet          j;
    //    CatoCMS::Lepton       l;
    CatoCMS::MET          met;
    CatoCMS::Trigger      trigger;
    CatoCMS::SampleInfo   si;
    CatoCMS::SingleTopMC  stmc;
    CatoCMS::SchannelMC   ssmc;
    CatoCMS::WJetsMC      wjetmc;
    CatoCMS::TTbarMC      ttbarmc;
    CatoCMS::QCDMC        qcdmc;
    CatoCMS::CutMap       cm;
    CatoCMS::PDFInfo      pdfinfo;	
    CatoCMS::CutFlowTable cft(std::ifstream&);
    std::vector<CatoCMS::Jet>      jet;
    std::vector<CatoCMS::Lepton>   lep;
    
    std::map<std::string, double> tg;
    std::vector< std::pair<int,int> > LE;
    std::vector<ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double> > > lvec;
    LorentzVector         vec;
    //Point3                point;  

  }
}
