#ifndef __CATO_CMS_LEPTON_H__
#define __CATO_CMS_LEPTON_H__


#include <map>
#include <vector>
#include <string>

#include "Vec.h"

namespace CatoCMS
{
  class Lepton 
  {
  public:
    Lepton();
    ~Lepton();
    
    void Reset();
    
    int GetId() { return id; };
    int GetIndex() { return index; };
    int GetMask() { return idmask; };
    std::string GetName() { return name; };
    
    int id;
    int index;
    int idmask;
    std::string name;
    
    LorentzVector v4;
    Point3        vertex;   // vertex position
    
    double P;
    double Et;
    double Charge;

    // variables for electron ID - only filled for electrons!:
    double caloEnergy;
    double eSuperClusterOverP;
    double deltaEtaSeedClusterTrackAtCalo;
    double deltaPhiSeedClusterTrackAtCalo;
    double hadronicOverEm;
    
    int    classification;
    size_t NumberOfTracks;
    
    // variables for lepton isolation:
    // globalMuon / Electron track variables:
    double TrkPt;  
    double TrkZ0;
    double TrkIso;
    int    TrkNhits;
    double TrkChi2;
    double Trkd0;
    double SigmaD0;
    
    // innerMuonTrack (silicon fit) variables:
    double innerTrkPt;  
    double innerTrkZ0;
    double innerTrkIso;
    int    innerTrkNhits;
    double innerTrkChi2;
    double innerTrkd0;
    double innerSigmaD0;

    // calorimeter info
    double HadEnergy;
    double EmEnergy;
    //    double CluPx;
    //    double CluPy;
    //    double CluPz;
    //    double CluEn;
    double CaloIso;
    double isoDepECal;  // only filled for muons!
    double isoDepHCal;  // only filled for muons!
    
    // ID flags
    bool isTightEle;
    bool isGlobalTightMu;
    
    //  double Clu_totEt_jetZ;
    //  double Clu_phi_jetZ;
    //  double PxCorr;
    //  double PyCorr;
    //  double PzCorr;
    //  double PCorr;
  };
}
#endif
