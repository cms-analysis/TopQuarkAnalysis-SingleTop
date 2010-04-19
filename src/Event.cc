//-------------------------------------------------------------------------------
//
// CVS revision record:
// $Author: weinelt $
// $Date: 2010/01/14 16:39:11 $
// $Revision: 1.1 $
// 
//-------------------------------------------------------------------------------


#include "TopQuarkAnalysis/SingleTop/interface/Event.h"

using namespace CatoCMS;

Event::Event() :
  runId(1), eventId(0), eventWeight(-1), nZvtx(-1),
  procId(-1), 
  nJets(-1), nLooseJets(-1), nBtags(-1), nTaggable(-1), 
  nLooseBtags(-1), nHyp(-1)

  
  /*sphericity(-1.0), aplanarity(-1.0), sumEtJet(-10.0), sumEtJetRaw(-10.0),
    Delta12(-10.0), Delta23(-10.0), Delta34(-10.0)*/
{

}

Event::~Event()
{

}

void Event::Reset()
{
  runId = 0;  
  eventId = 0;
  eventWeight = -1;
  nZvtx = -1;
  primV.SetCoordinates(0.0, 0.0, 0.0);
  
  procId = -1;
  mcPrimV.SetXYZ(0.0, 0.0, 0.0);
  
  //  primLep.Reset();
  lepVec.clear();
  jetVec.clear();
  looseJetVec.clear();
  
  sumEtJet = -10.0;
  sumEtJetRaw = -10.0;
  nJets = -1;
  nLooseJets = -1;
  nBtags = -1;
  nTaggable = -1;
  nLooseBtags = -1;
  nHyp =- 1;

  // ---------------------------
  // old stuff:
  //   misEtraw.Set(0.0, 0.0);
  //   misEtl4.Set(0.0, 0.0);
  //   misEtl6.Set(0.0, 0.0);
  //   Delta12 = -10.0;
  //   Delta23 = -10.0;
  //   Delta34 = -10.0;
  // ---------------------------

}

Lepton* Event::NewLepton(){
  Lepton lepton;
  lepVec.push_back(lepton);
  return &(lepVec.back());
  
}

Jet* Event::NewJet(){
  Jet jet;
  jetVec.push_back(jet);
  return &(jetVec.back());
}

Jet* Event::NewLooseJet(){
  Jet jet;
  looseJetVec.push_back(jet);
  return &(looseJetVec.back());
}

void Event::Print(std::ostream &os) const
{

  os.setf(std::ios::fixed); // Benutze Festkommadarstellung
  os << runId << " & " << eventId;
  os << " & ";
//   if (lepType == CatoDef::CEM) os << "CEM";
//   if (lepType == CatoDef::PHX) os << "PHX";
//   if (lepType == CatoDef::CMUP) os << "CMUP";
//   if (lepType == CatoDef::CMX) os << "CMX";
  os << " & " << std::flush;
  os.precision(1);
//   os << lep4.Pt();
//   os << " & " << jet[1].v4.Pt() << " & " << jet[2].v4.Pt() << std::flush;
//   os.precision(2);
//   os << " & " << jet[1].v4.Eta() << " & " << jet[2].v4.Eta() << std::flush;
  os.precision(1);
  //os << " & " << nBtag;
  os << " \\\\ \\hline" << std::endl;

}

void Event::PrintHeader(std::ostream &os)
{
  os << "\\begin{table}\n\\begin{center}" << std::endl;
  os << "\\begin{tabular}{|c|r|c|r|r|r|r|r|r|}" << std::endl;
  os << "\\hline" << std::endl;
  os << "Run & Event & Det. & $E_T(\\ell)$ & $E_T(j1)$ & ";
  os << "$E_T(j2)$ & $\\eta(1)$ & $\\eta(2)$ & $N_B$ & ";
  os << "\\\\ \\hline" << std::endl;
}

void Event::PrintTrailer(std::ostream &os)
{
  os << "\\end{tabular}\n\\end{center}" << std::endl;
  os << "\\caption{\\label{tab:eventListing} Selected candidate events";
  os << "\n of single top analysis. The table contains the";
  os << "\n run number, the event number, the detector name where the ";
  os << "\n trigger lepton was measured, the $E_T$ of the lepton, the ";
  os << "\n $E_T$ and $\\eta$ of the first and second jet, the number ";
  os << "\n of the b-tagged jets in the event.";
  os << std::endl;
  os << "\\end{table}" << std::endl;

  os << "\n\n\n\n" << std::endl;
}

