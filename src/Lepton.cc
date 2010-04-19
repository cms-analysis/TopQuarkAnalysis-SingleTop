#include "TopQuarkAnalysis/SingleTop/interface/Lepton.h"

using namespace CatoCMS;

Lepton::Lepton():
  id(0),
  index(-1),
  idmask(-1),
  name(""),
  P(-999.),
  Et(-999),
  Charge(-999.),
  caloEnergy(-999.),
  eSuperClusterOverP(-999.),
  deltaEtaSeedClusterTrackAtCalo(-999.),
  deltaPhiSeedClusterTrackAtCalo(-999.),
  hadronicOverEm(-999.),
  classification(-1),
  TrkPt(-999.),
  TrkZ0(-999.),
  TrkIso(-999.),
  TrkNhits(-999),
  TrkChi2(-999.),
  Trkd0(-999.),
  SigmaD0(-999),
  innerTrkPt(-999.),
  innerTrkZ0(-999.),
  innerTrkIso(-999.),
  innerTrkNhits(-999),
  innerTrkChi2(-999.),
  innerTrkd0(-999.),
  innerSigmaD0(-999),
  HadEnergy(-999.),
  EmEnergy(-999.),
  //  CluPx(-999.),
  //  CluPy(-999.),
  //  CluPz(-999.),
  //  CluEn(-999.),
  CaloIso(-999.),
  isoDepECal(-999.),
  isoDepHCal(-999.),
  isTightEle(0),
  isGlobalTightMu(0)  
{
}

Lepton::~Lepton()
{
}

void Lepton::Reset()
{
  id = 0;
  index = -1;
  idmask = -1;
  name = "";

  caloEnergy = -999.;
  eSuperClusterOverP = -999.;
  deltaEtaSeedClusterTrackAtCalo = -999.;
  deltaPhiSeedClusterTrackAtCalo = -999.;
  hadronicOverEm = -999.;
  classification = -1;
  NumberOfTracks = 0;

  v4.SetCoordinates(0.0,0.0,0.0,0.0);
  vertex.SetCoordinates(0.0,0.0,0.0);
  
  P      = -999.;
  Et     = -999;
  Charge = -999.;

  TrkPt  = -999.;
  TrkNhits = -999;
  TrkChi2 = -999.;
  Trkd0 = -999.;
  SigmaD0 = -999.;
  TrkZ0 = -999.;
  TrkIso = -999.;
  
  innerTrkPt  = -999.;
  innerTrkNhits = -999;
  innerTrkChi2 = -999.;
  innerTrkd0 = -999.;
  innerSigmaD0 = -999.;
  innerTrkZ0 = -999.;
  innerTrkIso = -999.;

  HadEnergy = -999.;
  EmEnergy  = -999.;
  //  CluPx = -999.;
  //  CluPy = -999.;
  //  CluPz = -999.;
  //  CluEn = -999.;
  CaloIso= -999.;
  isoDepECal = -999.;
  isoDepHCal = -999.;
  
  isTightEle = false;
  isGlobalTightMu  = false;

  //   Clu_totEt_jetZ = -999.;
  //   Clu_phi_jetZ = -999.;
  //   PxCorr = -999.;
  //   PyCorr = -999.;
  //   PzCorr = -999.;
  //   PCorr = -999.;
  
  //  Phi = -999.;
  //  Eta = -999.;
  //  Z0 = -999.;
  //  D0 = -999.;
  //  AxSeg = -999.;
  //  StSeg = -999.;

  
}

