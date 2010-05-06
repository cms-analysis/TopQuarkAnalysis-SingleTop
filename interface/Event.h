#ifndef __CATO_CMS_EVENT_H__
#define __CATO_CMS_EVENT_H__
//-------------------------------------------------------------------------------
// Header file for the CatoEvent class that provides a mini-event format
// for top analysis. It is filled after the preselection step.
//
// CVS revision record:
// $Author: weinelt $
// $Date: 2010/01/14 16:38:31 $
// $Revision: 1.1 $
// 
//-------------------------------------------------------------------------------

#include <string>
#include <vector>
#include <map>


#include "Vec.h"
#include "Jet.h"
#include "Lepton.h"
#include "Trigger.h"
#include "MET.h"
#include "PDFInfo.h"

namespace CatoCMS
{
  class Event
  {
  public:
    Event();
    ~Event();
    
    void Reset();
    void PrintHeader(std::ostream &os = std::cout);
    void Print(std::ostream &os = std::cout) const;
    void PrintTrailer(std::ostream &os = std::cout);
    Lepton* NewLepton();
    Jet* NewJet();
    Jet* NewLooseJet();
    
    // ---- General event information.
    unsigned int               runId;
    unsigned int               eventId;
    double                     eventWeight;
    
    int          nZvtx;
    Point3       primV;             // Primary vertex.

    // ---- Monte Carlo information
    int    procId;
    Point3 mcPrimV;           // Monte Carlo primary vertex.
      
    // ---- jets 
    std::vector<Jet>    jetVec;      // vector of selected jets
    std::vector<Jet>    looseJetVec; // vector of loose jets
    
    double sumEtJet;    // include also soft jets.
    double sumEtJetRaw; // use uncorrected JetEt for mistag matrix
    int    nJets;
    int    nLooseJets;
    
    // ---- MET
    MET met;                       // MET

    // ---- pdfinfo 
    PDFInfo pdfinfo;

    // ---- trigger
    Trigger trigger;       
    
    // ---- leptons
    //    Lepton primLep;
    std::vector<Lepton> lepVec;      // vector of selected leptons
    
    // ---- info filled in EventSelection: 
    int    nBtags;
    int    nTaggable;
    int    nLooseBtags;
    int    nHyp;

  }; 
}
#endif


// old stuff: --------------------------------------------------------------

//Double_t sumEtJet;  // Include also soft jets.
//Double_t sumEtJetRaw; //use uncorrected JetEt for mistag matrix
//Double_t Delta12;   // Delta 12 from Kt algorithm
//Double_t Delta23;   // Delta 23 from Kt algorithm
//Double_t Delta34;   // Delta 34 from Kt algorithm
//  TVector2 misEtraw;          // missing Et vector
//  TVector2 misEtl4;           // missing Et vector with L4 jet corrections
//  TVector2 misEtl6;           // missing Et vector with L6 jet corrections
//    float lepQ;
//    float lepIso;
//    float muonCalEnergy; 

// --------------------------------------------------------------------------
