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
  
  
  RooRealVar a("a","a", 0.,         -20, 20.);
  RooRealVar b("b","b", 0.0,        -8, 8.);
  RooRealVar c("c","c", 0.0,        -6, 6.);
  RooRealVar d("d","d", 0.0,        -2., 2.);
  RooRealVar e("e","e", 0.0,        -1., 1.);
  
  RooRealVar expo ("expo", "expo", -0.178, -4.5, 0.0);
  //  RooRealVar expo ("expo", "expo", -0.01, -4.5, 0.0);

  
  int count_AntiIso  = 0;
  
  ifstream cfgfile(argv[1]);
  string filename;
  
  
  RooDataSet datasetAntiIso("dataAntiIso","dataAntiIso", WTM);
  vector<double> dataAntiIso_vec;
  
  
  while(!cfgfile.eof()){
    
    cfgfile >> filename;
    
    TFile file_sig (filename.c_str());
    fwlite::Event ev_sig(&file_sig);
    
    for( ev_sig.toBegin(); ! ev_sig.atEnd(); ++ev_sig) {

      fwlite::Handle<std::vector<pat::Jet> >  topJetsAntiIso; 
      fwlite::Handle<std::vector<pat::Muon> > topMuonsAntiIso;
      fwlite::Handle<std::vector<pat::MET> >  MET;
      
      topJetsAntiIso.getByLabel(ev_sig, "topJetsAntiIso" );
      topMuonsAntiIso.getByLabel(ev_sig, "topMuonsAntiIso" );
      //      MET.getByLabel(ev_sig, "patMETsPFlow" );
      MET.getByLabel(ev_sig, "preselectedMETs" );

      if (topJetsAntiIso.failedToGet()) continue;

      //      cout << "Jet AntiIso size: " << topJetsAntiIso -> size() << endl;
      
      
      bool cond = (topJetsAntiIso -> size() == nJets);
      
      if (nJets == 999)
	cond = true;

      if(cond){
	
	if(!MET.failedToGet()){
	  
	  for(unsigned int i = 0; i < MET->size(); ++i){
	    
	    double preselectedMETsPt  = (*MET)[i].pt();
	    double preselectedMETsPx  = (*MET)[i].px();
	    double preselectedMETsPy  = (*MET)[i].py();
	    
	    double  WTMassAntiIso;
	  
	    
	    if (!topMuonsAntiIso.failedToGet() && topMuonsAntiIso->size()!=0){
	      
	      double Impact  = (*topMuonsAntiIso)[i].dB()/(*topMuonsAntiIso)[i].edB();
	      //	      if(Impact > 3.) continue;
	      
	      double topMuonsAntiIsoPt  = (*topMuonsAntiIso)[i].pt();
	      double topMuonsAntiIsoPx  = (*topMuonsAntiIso)[i].px();
	      double topMuonsAntiIsoPy  = (*topMuonsAntiIso)[i].py();
	      
	      WTMassAntiIso = sqrt((preselectedMETsPt+topMuonsAntiIsoPt)*(preselectedMETsPt+topMuonsAntiIsoPt) -
				   (preselectedMETsPy+topMuonsAntiIsoPy)*(preselectedMETsPy+topMuonsAntiIsoPy) -
				   (preselectedMETsPx+topMuonsAntiIsoPx)*(preselectedMETsPx+topMuonsAntiIsoPx)) ;
	      
	      
	      if ((WTMassAntiIso > WTM_min) && (WTMassAntiIso < WTM_max)){
		WTM.setVal(WTMassAntiIso);
		datasetAntiIso.add(WTM);
		dataAntiIso_vec.push_back(datasetAntiIso.get(count_AntiIso)->getRealValue("WTM"));
		count_AntiIso++;
	      }
	    }
	  }    
	}  
      }
    }
    //    cout << "total number is: " <<  count_AntiIso << endl;
    
  }
  
  cfgfile.close();
  
  
  
  //******** BUILD PDFs
  
  RooPolynomial *poly = new RooPolynomial("poly","poly",WTM, RooArgList(a,b,c,d,e));
  //  a.setConstant(true);
  //  b.setConstant(true);
  //  c.setConstant(true);
  d.setConstant(true);
  e.setConstant(true);
  
  RooExponential *exponential = new RooExponential( "exponential", "exponential", WTM, expo);
  //  expo.setConstant(true);
  
  
  RooProdPdf ProdPdf("ProdPdf", "ProdPdf", *poly, *exponential);
  
  
  
  //******** FIT
  
  ProdPdf . fitTo(datasetAntiIso, Hesse(true), Minos(false));
  
  
  out_figureFitAntiIso    << DirStr.str().c_str() << "FitAntiIsoWTM"  << nJets << "_" << WTM_min << "_" << WTM_max << ".eps";
  out_resultsFitAntiIso   << DirStr.str().c_str() << "FitAntiIsoWTM"  << nJets << "_" << WTM_min << "_" << WTM_max << ".txt";
  
  
  TCanvas *CanvasAntiIso = new TCanvas("CanvasAntiIso","");
  RooPlot* pl_ProdPdfWTM = WTM.frame();
  datasetAntiIso.plotOn(pl_ProdPdfWTM, Binning(Nbins), DataError(RooAbsData::SumW2) );
  ProdPdf . plotOn(pl_ProdPdfWTM, LineWidth(2), LineColor(kBlue));
  pl_ProdPdfWTM -> GetXaxis() -> SetTitle("M_{W}^{T} (GeV) ");
  pl_ProdPdfWTM -> Draw();
  CanvasAntiIso -> SaveAs(out_figureFitAntiIso.str().c_str());
  
  cout << "AntiIso events " << count_AntiIso <<endl;
  
  
  ofstream  outAntiIso;
  outAntiIso.open(out_resultsFitAntiIso.str().c_str(),ios::trunc);
  outAntiIso <<"a          "<< a.getVal()     << endl;
  outAntiIso <<"a_err      "<< a.getError()   << endl;
  outAntiIso <<"b          "<< b.getVal()     << endl;
  outAntiIso <<"b_err      "<< b.getError()   << endl;
  outAntiIso <<"c          "<< c.getVal()     << endl;
  outAntiIso <<"c_err      "<< c.getError()   << endl;
  outAntiIso <<"d          "<< d.getVal()     << endl;
  outAntiIso <<"d_err      "<< d.getError()   << endl;
  outAntiIso <<"e          "<< e.getVal()     << endl;
  outAntiIso <<"e_err      "<< e.getError()   << endl;
  outAntiIso <<"expo       "<< expo.getVal()     << endl;
  outAntiIso <<"expo_err   "<< expo.getError()   << endl;
  outAntiIso.close();


  TH1  * Hist_Prod;
  Hist_Prod = ProdPdf.createHistogram("Hist_Prod", WTM, Binning(120., 0., 120. ));
  double integral = Hist_Prod->Integral(50,120);
  cout << "Integral:  "  << integral << endl;

  
  return 0;
}
