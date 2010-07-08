#include "FWCore/Utilities/interface/EDMException.h"
#include "FWCore/FWLite/interface/AutoLibraryLoader.h"
#include "DataFormats/FWLite/interface/Event.h"
#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include <iostream>
#include <string.h>
#include <sstream> //libreria per usare stringstream
#include <stdio.h>
#include <fstream>
#include "TCanvas.h"
#include "TTree.h"
#include "TH1.h"
#include "TFile.h"
#include "TStyle.h"
#include "RooDataHist.h"
#include "RooPolynomial.h"
#include "RooExponential.h"
#include "RooProdPdf.h"
#include <RooDataSet.h>
#include <RooHistPdf.h>
#include <RooAddPdf.h>
#include <RooRealVar.h>
#include <RooChi2Var.h>
#include <RooMinuit.h>
#include <RooFitResult.h>
#include <RooGlobalFunc.h>
#include <RooPlot.h>
#include <RooCBShape.h>
#include <RooNLLVar.h>
#include "TMath.h"
#include <algorithm>


using namespace RooFit;
using namespace std;

int main(int argc,  char* argv[]){


  gStyle->SetPalette(1);
  gStyle->SetOptStat(0);
  gStyle->SetFrameBorderMode(0);
  gStyle->SetCanvasBorderMode(0);
  gStyle->SetPadBorderMode(0);
  gStyle->SetPadColor(0);
  gStyle->SetCanvasColor(0);
  gStyle->SetTitleColor(1);
  gStyle->SetStatColor(0);
  gStyle->SetFillColor(0);

  AutoLibraryLoader::enable();

  stringstream WTM_minimum, WTM_maximum, title_str, DirStr, out_figureFitIso, out_resultsFitIso, out_figureFitAntiIso, out_resultsFitAntiIso;
  stringstream  binwidthstr,txtInputFile, nJetsStr ;
  

  txtInputFile         << argv[1];
  WTM_minimum          << argv[2];
  WTM_maximum          << argv[3];
  binwidthstr          << argv[4];
  DirStr               << argv[5];
  nJetsStr             << argv[6];
  
  double WTM_min, WTM_max, bin_width;
  unsigned int nJets;

  WTM_minimum    >> WTM_min;
  WTM_maximum    >> WTM_max;
  binwidthstr    >> bin_width;
  nJetsStr       >> nJets; 
  
  title_str << "W transverse mass fit in (" << WTM_min << "," << WTM_max << ") " ; 
  
  int Nbins =  int( (WTM_max - WTM_min + 0.00001)/bin_width);

  RooRealVar WTM("WTM","W Transverse Mass", 0.1, WTM_min, WTM_max);
  RooRealVar yield_sig("yield_sig","yield_sig", 30., 10., 80.);
  RooRealVar yield_bkg("yield_bkg","yield_bkg", 10., 1., 50.);

  //  yield_sig.setConstant(true);
  //  yield_bkg.setConstant(true);
  
  
  //  RooRealVar a("a","a",  0.749,   -4, 4.);
  //  RooRealVar b("b","b", -0.109,   -3, 3.);
  //  RooRealVar c("c","c",  0.007,   -2, 2.);
  //  RooRealVar expo ("expo", "expo", -0.174, -4.5, 0.0);
  
  RooRealVar a("a","a", 3.61,   -4, 4.);
  RooRealVar b("b","b",-0.61,   -3, 3.);
  RooRealVar c("c","c", 0.028,   -2, 2.);
  RooRealVar expo ("expo", "expo", -0.17, -4.5, 0.0);
  
  RooRealVar mean ("mean", "mean",  65., 40., 90.);
  RooRealVar sigma("sigma","sigma", 15., 0. , 40.);
  RooRealVar alpha("alpha","alpha", 0.44, -2. , 2.);
  RooRealVar n("n","n", 120., 0. , 500.);
  
  
  int count_Iso   = 0;
  
  
  ifstream cfgfile(argv[1]);
  string filename;
  
  
  RooDataSet datasetIso("dataIso","dataIso", WTM);
  vector<double> dataIso_vec;
  
  
  
  while(!cfgfile.eof()){
    
    cfgfile >> filename;
    
    TFile file_sig (filename.c_str());
    fwlite::Event ev_sig(&file_sig);
    
    for( ev_sig.toBegin(); ! ev_sig.atEnd(); ++ev_sig) {
      
      fwlite::Handle<std::vector<pat::Jet> > topJetsIso;
      fwlite::Handle<std::vector<pat::Muon> > topMuonsIso;
      fwlite::Handle<std::vector<pat::MET> >  MET;
   
      topJetsIso.getByLabel(ev_sig, "topJets" );
      topMuonsIso.getByLabel(ev_sig, "topMuons" );
      MET.getByLabel(ev_sig, "patMETsPFlow" );
      //      MET.getByLabel(ev_sig, "preselectedMETs" );
      
      if (topJetsIso.failedToGet()) continue;
      
      //      cout << "Jet Iso size: " << topJetsIso -> size() << endl;
      
      bool cond = (topJetsIso -> size() == nJets);
      
      
      if (nJets == 999)
	cond = true;
      
      if(cond){
	
	if(!MET.failedToGet()){
	  
	  for(unsigned int i = 0; i < MET->size(); ++i){
	    
	    double preselectedMETsPt  = (*MET)[i].pt();
	    double preselectedMETsPx  = (*MET)[i].px();
	    double preselectedMETsPy  = (*MET)[i].py();
	    
	    double WTMass;
	    
	    if (!topMuonsIso.failedToGet()&& topMuonsIso->size() !=0 ){
	      
	      double topMuonsPt  = (*topMuonsIso)[i].pt();
	      double topMuonsPx  = (*topMuonsIso)[i].px();
	      double topMuonsPy  = (*topMuonsIso)[i].py();
	      
	      WTMass = sqrt((preselectedMETsPt+topMuonsPt)*(preselectedMETsPt+topMuonsPt) -
			    (preselectedMETsPy+topMuonsPy)*(preselectedMETsPy+topMuonsPy) -
			    (preselectedMETsPx+topMuonsPx)*(preselectedMETsPx+topMuonsPx)) ;
	      
	      
	      if ((WTMass > WTM_min) && (WTMass < WTM_max)){
		WTM.setVal(WTMass);
		
		datasetIso.add(WTM);
		dataIso_vec.push_back(datasetIso.get(count_Iso)->getRealValue("WTM"));
		//	      cout << " datasetIso counting WTMass " << WTMass  << endl;
		
		count_Iso++;
	      }
	    }
	  }
	} 
      }
    }
    //    cout << "total number is: " << count_Iso << endl;
    
  }
  
  cfgfile.close();
  
  
  
  //******** BUILD PDFs
  
  RooPolynomial *poly = new RooPolynomial("poly","poly",WTM, RooArgList(a,b,c));
  a.setConstant(true);
  b.setConstant(true);
  c.setConstant(true);
  
  RooExponential *exponential = new RooExponential( "exponential", "exponential", WTM, expo);
  expo.setConstant(true);
  
  
  RooProdPdf ProdPdf("ProdPdf", "ProdPdf", *poly, *exponential);
  
  
  RooCBShape CBall("CBall", "CBall", WTM, mean, sigma, alpha, n);
  //  mean.setConstant(true);
  //  sigma.setConstant(true);
  alpha.setConstant(true);
  n.setConstant(true);
  
  
  
  //******** BUILD ROOADDPDF
  
  RooAddPdf * Model = new RooAddPdf ("Model", "Model", RooArgList(ProdPdf, CBall), RooArgList(yield_bkg, yield_sig));
  
  
  
  //******** FIT
  
  Model -> fitTo(datasetIso, Hesse(true), Minos(false), Extended(kTRUE));
  
  
  
  out_resultsFitIso       << DirStr.str().c_str() << "FitIsoWTM"      << nJets << "_" << WTM_min << "_" << WTM_max << ".txt";
  out_figureFitIso        << DirStr.str().c_str() << "FitIsoWTM"      << nJets << "_" << WTM_min << "_" << WTM_max << ".eps";
  
  
  TCanvas *CanvasIso = new TCanvas("CanvasIso","");
  RooPlot* pl_WTM = WTM.frame();
  
  datasetIso.plotOn(pl_WTM, Binning(Nbins), DataError(RooAbsData::SumW2) );
  Model -> plotOn(pl_WTM, Components("ProdPdf"),LineWidth(2),LineColor(kBlue));
  //  Model -> plotOn(pl_WTM, Components("CBall"),LineWidth(2),LineColor(kRed));
  Model -> plotOn(pl_WTM, LineWidth(2),LineColor(kRed));
  
  pl_WTM -> GetXaxis() -> SetTitle("M_{W}^{T} (GeV) ");
  pl_WTM -> Draw(); 
  CanvasIso -> SaveAs(out_figureFitIso.str().c_str());
  
  
  cout << "Iso events "     << count_Iso <<endl;
   
  
  ofstream outIso;
  outIso.open(out_resultsFitIso.str().c_str(),ios::trunc);
  outIso <<"yield_sig        "<< yield_sig.getVal()     << endl;
  outIso <<"yield_sig_err    "<< yield_sig.getError()   << endl;
  outIso <<"yield_bkg        "<< yield_bkg.getVal()     << endl;
  outIso <<"yield_bkg_err    "<< yield_bkg.getError()   << endl;
  outIso <<"mean             "<< mean.getVal()          << endl;
  outIso <<"mean_err         "<< mean.getError()        << endl;
  outIso <<"sigma            "<< sigma.getVal()         << endl;
  outIso <<"sigma_err        "<< sigma.getError()       << endl;
  outIso <<"alpha            "<< alpha.getVal()         << endl;
  outIso <<"alpha_err        "<< alpha.getError()       << endl;
  outIso <<"n                "<< n.getVal()             << endl;
  outIso <<"n_err            "<< n.getError()           << endl;
  outIso.close();


  TH1  * Hist_Prod;
  Hist_Prod = ProdPdf.createHistogram("Hist_Prod", WTM, Binning(120., 0., 120. ));
  double integral = Hist_Prod->Integral(50,120);
  cout << "Integral:  "  << integral << endl;

  
  return 0;
}
