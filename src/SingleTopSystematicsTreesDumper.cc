/*
*\Author:  O.Iorio
*
*
*
*\version  $Id: SingleTopSystematicsTreesDumper.cc,v 1.12.2.10 2011/09/20 13:36:21 oiorio Exp $ 
*/
// This analyzer dumps the histograms for all systematics listed in the cfg file 
//
//
//

#define DEBUG    0 // 0=false
#define MC_DEBUG 0 // 0=false   else -> dont process preselection
#define C_DEBUG  0 // currently debuging

#include "TopQuarkAnalysis/SingleTop/interface/SingleTopSystematicsTreesDumper.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Common/interface/TriggerNames.h"
//#include "PhysicsTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
//#include "FWCore/Framework/interface/TriggerNames.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/Candidate/interface/NamedCompositeCandidate.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include <Math/VectorUtil.h>
//#include "CommonTools/CandUtils/interface/Booster.h"
#include <sstream> //libreria per usare stringstream
//#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "TopQuarkAnalysis/SingleTop/interface/EquationSolver.h"

#include "CondFormats/JetMETObjects/interface/JetResolution.h"

SingleTopSystematicsTreesDumper::SingleTopSystematicsTreesDumper(const edm::ParameterSet& iConfig)
{
  //MCLightQuarkProducer   = iConfig.getParameter<InputTag>("MCLightQuarkProducer");
  all_syst = iConfig.getUntrackedParameter<std::vector<std::string> >("systematics"); 
  // systematics = iConfig.getUntrackedParameter<std::vector<std::string> >("systematics"); 
  rate_systematics = iConfig.getUntrackedParameter<std::vector<std::string> >("rateSystematics"); 
  //Channel information
    
  channelInfo = iConfig.getParameter<edm::ParameterSet>("channelInfo"); 
  //Cross section, name and number of events 
  channel = channelInfo.getUntrackedParameter<string>("channel");
  crossSection = channelInfo.getUntrackedParameter<double>("crossSection");
  originalEvents = channelInfo.getUntrackedParameter<double>("originalEvents");
  finalLumi = channelInfo.getUntrackedParameter<double>("finalLumi");
  mcPUFile_ = channelInfo.getUntrackedParameter< std::string >("mcPUFile","pileupdistr_TChannel.root");
  puHistoName_ = channelInfo.getUntrackedParameter< std::string >("puHistoName","pileUpDumper/PileUp");

  RelIsoCut = channelInfo.getUntrackedParameter<double>("RelIsoCut",0.1);
  
  maxPtCut = iConfig.getUntrackedParameter<double>("maxPtCut",30);
  
  leptonsPt_ =  iConfig.getParameter< edm::InputTag >("leptonsPt");
  leptonsPhi_ =  iConfig.getParameter< edm::InputTag >("leptonsPhi");
  leptonsEta_ =  iConfig.getParameter< edm::InputTag >("leptonsEta");
  leptonsEnergy_ =  iConfig.getParameter< edm::InputTag >("leptonsEnergy");
  leptonsCharge_ =  iConfig.getParameter< edm::InputTag >("leptonsCharge");
  leptonsRelIso_ =  iConfig.getParameter< edm::InputTag >("leptonsRelIso");
  leptonsDB_ =  iConfig.getParameter< edm::InputTag >("leptonsDB");
  leptonsID_ =  iConfig.getParameter< edm::InputTag >("leptonsID");
  leptonsFlavour_ =  iConfig.getUntrackedParameter< std::string >("leptonsFlavour");

  genJetsPt_  = iConfig.getParameter< edm::InputTag >("genJetsPt");
  //  genJetsEta_  = iConfig.getParameter< edm::InputTag >("genJetsEta");

  looseMuonsRelIso_ =  iConfig.getParameter< edm::InputTag >("looseMuonsRelIso");
  looseElectronsRelIso_ =  iConfig.getParameter< edm::InputTag >("looseElectronsRelIso");

  jetsEta_ =  iConfig.getParameter< edm::InputTag >("jetsEta");
  jetsPt_ =  iConfig.getParameter< edm::InputTag >("jetsPt");
  jetsPhi_ =  iConfig.getParameter< edm::InputTag >("jetsPhi");
  jetsEnergy_ =  iConfig.getParameter< edm::InputTag >("jetsEnergy");
  jetsBTagAlgo_ =  iConfig.getParameter< edm::InputTag >("jetsBTagAlgo");
  jetsAntiBTagAlgo_ =  iConfig.getParameter< edm::InputTag >("jetsAntiBTagAlgo");
  jetsFlavour_ =  iConfig.getParameter< edm::InputTag >("jetsFlavour");

  METPhi_ =  iConfig.getParameter< edm::InputTag >("METPhi");
  METPt_ =  iConfig.getParameter< edm::InputTag >("METPt");
  
  //  UnclMETPx_ =  iConfig.getParameter< edm::InputTag >("UnclusteredMETPx");
  //  UnclMETPy_ =  iConfig.getParameter< edm::InputTag >("UnclusteredMETPy");
  UnclMETPx_ =  iConfig.getParameter< edm::InputTag >("UnclusteredMETPx");
  UnclMETPy_ =  iConfig.getParameter< edm::InputTag >("UnclusteredMETPy");
  
  jetsCorrTotal_ =  iConfig.getParameter< edm::InputTag >("jetsCorrTotal");

  doQCD_  =  iConfig.getUntrackedParameter< bool >("doQCD",true); 

  //Q2 part
  x1_ = iConfig.getParameter<edm::InputTag>("x1") ;
  x2_ = iConfig.getParameter<edm::InputTag>("x2") ;
  
  //Pile Up Part
  np1_ = iConfig.getParameter< edm::InputTag >("nVerticesPlus");//,"PileUpSync"); 
  nm1_ = iConfig.getParameter< edm::InputTag >("nVerticesMinus");//,"PileUpSync"); 
  n0_ = iConfig.getParameter< edm::InputTag >("nVertices");//,"PileUpSync"); 

  doPU_ = iConfig.getUntrackedParameter< bool >("doPU",false);
  doResol_ = iConfig.getUntrackedParameter< bool >("doResol",false);
  doTurnOn_ = iConfig.getUntrackedParameter< bool >("doTurnOn",true);

  doReCorrection_ = iConfig.getUntrackedParameter< bool >("doReCorrection",false);
  dataPUFile_ =  iConfig.getUntrackedParameter< std::string >("dataPUFile","pileUpDistr.root");
  
  if(doPU_){
    //    cout << " before lumiWeights "<<endl;
    LumiWeights_ = edm::LumiReWeighting(mcPUFile_,
					dataPUFile_,
					puHistoName_,
					std::string("pileup") );
    //    cout << " built lumiWeights "<<endl;
  }
  
  preWeights_ =  iConfig.getParameter< edm::InputTag >("preWeights");
  
  systematics.push_back("noSyst");
  
  Service<TFileService> fs;
  
  bScanSteps =1*doBScan_;
  bTagThreshold =3.41;
  
  TFileDirectory SingleTopSystematics = fs->mkdir( "systematics_histograms" );
  TFileDirectory SingleTopTrees = fs->mkdir( "systematics_trees" );
  
  resolScale =0.1;
   
  for(size_t i = 0; i < all_syst.size();++i){
    systematics.push_back(all_syst.at(i));  
  }

  for(size_t i = 0; i < rate_systematics.size();++i){
    all_syst.push_back(rate_systematics.at(i));  
  }

  all_syst.push_back("noSyst");

  for(size_t i = 0; i < all_syst.size();++i){
    
    string syst = all_syst[i];
    
    string treename = (channel+"_"+syst);
    string treenameQCD = (channel+"_"+syst+"QCD");
    //bWeightTree,PUWeightTree,turnOnWeightTree,limuWeightTree;
    
    trees[syst] = new TTree(treename.c_str(),treename.c_str()); 
    
    trees[syst]->Branch("eta",&etaTree);
    trees[syst]->Branch("costhetalj",&cosTree);
    trees[syst]->Branch("topMass",&topMassTree);
    trees[syst]->Branch("mtwMass",&mtwMassTree);
    
    trees[syst]->Branch("charge",&chargeTree);
    trees[syst]->Branch("runid",&runTree);
    trees[syst]->Branch("lumiid",&lumiTree);
    trees[syst]->Branch("eventid",&eventTree);
    trees[syst]->Branch("weight",&weightTree);

    trees[syst]->Branch("Q2",&Q2);
    trees[syst]->Branch("x1",&x1);
    trees[syst]->Branch("x2",&x2);

    trees[syst]->Branch("bWeight",&bWeightTree);
    trees[syst]->Branch("PUWeight",&PUWeightTree);
    trees[syst]->Branch("turnOnWeight",&turnOnWeightTree);


    //Extra info
    
    trees[syst]->Branch("leptonPt",&lepPt);
    trees[syst]->Branch("leptonEta",&lepEta);
    trees[syst]->Branch("leptonPhi",&lepPhi);
    trees[syst]->Branch("leptonRelIso",&lepRelIso);
    
    trees[syst]->Branch("fJetPt",&fJetPt);
    trees[syst]->Branch("fJetE",&fJetE);
    trees[syst]->Branch("fJetEta",&fJetEta);
    trees[syst]->Branch("fJetPhi",&fJetPhi);
    
    trees[syst]->Branch("bJetPt",&bJetPt);
    trees[syst]->Branch("bJetE",&bJetE);
    trees[syst]->Branch("bJetEta",&bJetEta);
    trees[syst]->Branch("bJetPhi",&bJetPhi);
    
    trees[syst]->Branch("metPt",&metPt);
    trees[syst]->Branch("metPhi",&metPhi);
    
    trees[syst]->Branch("topPt",&topPt);
    trees[syst]->Branch("topPhi",&topPhi);
    trees[syst]->Branch("topEta",&topEta);
    trees[syst]->Branch("topE",&topE);

    trees[syst]->Branch("ID",&electronID);

    trees[syst]->Branch("totalEnergy",&totalEnergy);
    trees[syst]->Branch("totalMomentum",&totalMomentum);

    trees[syst]->Branch("bJetFlavour",&bJetFlavourTree);
    
    trees[syst]->Branch("nVertices",&nVertices);

    trees[syst]->Branch("lowBTag",&lowBTagTree);
    trees[syst]->Branch("highBTag",&highBTagTree);

    
    treesWSample[syst] = new TTree((treename+"WSample").c_str(),(treename+"WSample").c_str()); 
    
    treesWSample[syst]->Branch("etaLowBTag",&etaTree);
    treesWSample[syst]->Branch("etaHighBTag",&etaTree2);
    treesWSample[syst]->Branch("costhetalj",&cosTree);
    treesWSample[syst]->Branch("topMass",&topMassTree);
    treesWSample[syst]->Branch("topMassLowBTag",&topMassLowBTagTree);
    treesWSample[syst]->Branch("topMassBestTop",&topMassBestTopTree);
    treesWSample[syst]->Branch("mtwMass",&mtwMassTree);
    
    treesWSample[syst]->Branch("charge",&chargeTree);
    treesWSample[syst]->Branch("runid",&runTree);
    treesWSample[syst]->Branch("lumiid",&lumiTree);
    treesWSample[syst]->Branch("eventid",&eventTree);
    treesWSample[syst]->Branch("weight",&weightTree);
    
    treesWSample[syst]->Branch("ID",&electronID);
    
    treesWSample[syst]->Branch("bWeight",&bWeightTree);
    treesWSample[syst]->Branch("PUWeight",&PUWeightTree);
    treesWSample[syst]->Branch("turnOnWeight",&turnOnWeightTree);

    treesWSample[syst]->Branch("Q2",&Q2);
    treesWSample[syst]->Branch("x1",&x1);
    treesWSample[syst]->Branch("x2",&x2);

    
    //Extra info
    
    treesWSample[syst]->Branch("leptonPt",&lepPt);
    treesWSample[syst]->Branch("leptonEta",&lepEta);
    treesWSample[syst]->Branch("leptonPhi",&lepPhi);
    treesWSample[syst]->Branch("leptonRelIso",&lepRelIso);
    
    treesWSample[syst]->Branch("fJetPt",&fJetPt);
    treesWSample[syst]->Branch("fJetE",&fJetE);
    treesWSample[syst]->Branch("fJetEta",&fJetEta);
    treesWSample[syst]->Branch("fJetPhi",&fJetPhi);
    treesWSample[syst]->Branch("bJetFlavour",&bJetFlavourTree);
    
    treesWSample[syst]->Branch("bJetPt",&bJetPt);
    treesWSample[syst]->Branch("bJetE",&bJetE);
    treesWSample[syst]->Branch("bJetEta",&bJetEta);
    treesWSample[syst]->Branch("bJetPhi",&bJetPhi);
    
    treesWSample[syst]->Branch("highBTag",&highBTagTree);
    treesWSample[syst]->Branch("lowBTag",&lowBTagTree);
    
    treesWSample[syst]->Branch("metPt",&metPt);
    treesWSample[syst]->Branch("metPhi",&metPhi);
    
    treesWSample[syst]->Branch("topPt",&topPt);
    treesWSample[syst]->Branch("topPhi",&topPhi);
    treesWSample[syst]->Branch("topEta",&topEta);
    treesWSample[syst]->Branch("topE",&topE);
    
    treesWSample[syst]->Branch("nVertices",&nVertices);
    
    
    //    treesWSample[syst]->Branch("totalEnergy",&totalEnergy);
    //treesWSample[syst]->Branch("totalMomentum",&totalMomentum);
    
    //QCD
    
    treesQCD[syst] = new TTree(treenameQCD.c_str(),treenameQCD.c_str()); 
    

    treesQCD[syst]->Branch("lowBTag",&lowBTagTree);

    treesQCD[syst]->Branch("eta",&etaTree);
    treesQCD[syst]->Branch("costhetalj",&cosTree);
    treesQCD[syst]->Branch("topMass",&topMassTree);
    treesQCD[syst]->Branch("mtwMass",&mtwMassTree);
    treesQCD[syst]->Branch("leptonRelIso",&lepRelIso);
    
    treesQCD[syst]->Branch("ID",&electronID);
    
    treesQCD[syst]->Branch("leptonPt",&lepPt);
    treesQCD[syst]->Branch("leptonEta",&lepEta);
    treesQCD[syst]->Branch("leptonPhi",&lepPhi);
    treesQCD[syst]->Branch("leptonRelIso",&lepRelIso);
    
    treesQCD[syst]->Branch("Q2",&Q2);
    treesQCD[syst]->Branch("x1",&x1);
    treesQCD[syst]->Branch("x2",&x2);

    treesQCD[syst]->Branch("fJetPt",&fJetPt);
    treesQCD[syst]->Branch("fJetE",&fJetE);
    treesQCD[syst]->Branch("fJetEta",&fJetEta);
    treesQCD[syst]->Branch("fJetPhi",&fJetPhi);
    
    treesQCD[syst]->Branch("bJetPt",&bJetPt);
    treesQCD[syst]->Branch("bJetE",&bJetE);
    treesQCD[syst]->Branch("bJetEta",&bJetEta);
    treesQCD[syst]->Branch("bJetPhi",&bJetPhi);
    
    treesQCD[syst]->Branch("metPt",&metPt);
    treesQCD[syst]->Branch("metPhi",&metPhi);
    
    treesQCD[syst]->Branch("topPt",&topPt);
    //    treesQCD[syst]->Branch("topPhi",&topPhi);
    //    treesQCD[syst]->Branch("topEta",&topEta);
    //    treesQCD[syst]->Branch("topE",&topE);

    treesQCD[syst]->Branch("charge",&chargeTree);
    treesQCD[syst]->Branch("runid",&runTree);
    treesQCD[syst]->Branch("lumiid",&lumiTree);
    treesQCD[syst]->Branch("eventid",&eventTree);
    treesQCD[syst]->Branch("weight",&weightTree);

    treesQCD[syst]->Branch("bWeight",&bWeightTree);
    treesQCD[syst]->Branch("PUWeight",&PUWeightTree);
    treesQCD[syst]->Branch("turnOnWeight",&turnOnWeightTree);

    treesQCD[syst]->Branch("nVertices",&nVertices);

    treesQCD[syst]->Branch("lowBTag",&lowBTagTree);
    treesQCD[syst]->Branch("highBTag",&highBTagTree);

    //W Sample QCD

    treesWSampleQCD[syst] = new TTree((treename+"WSampleQCD").c_str(),(treename+"WSampleQCD").c_str()); 
    
    treesWSampleQCD[syst]->Branch("etaLowBTag",&etaTree);
    treesWSampleQCD[syst]->Branch("etaHighBTag",&etaTree2);
    treesWSampleQCD[syst]->Branch("costhetalj",&cosTree);
    treesWSampleQCD[syst]->Branch("topMass",&topMassTree);
    treesWSampleQCD[syst]->Branch("topMassLowBTag",&topMassLowBTagTree);
    treesWSampleQCD[syst]->Branch("topMassBestTop",&topMassBestTopTree);
    treesWSampleQCD[syst]->Branch("mtwMass",&mtwMassTree);
    treesWSampleQCD[syst]->Branch("leptonRelIso",&lepRelIso);

    treesWSampleQCD[syst]->Branch("ID",&electronID);


    treesWSampleQCD[syst]->Branch("leptonPt",&lepPt);
    treesWSampleQCD[syst]->Branch("leptonEta",&lepEta);
    treesWSampleQCD[syst]->Branch("leptonPhi",&lepPhi);
    treesWSampleQCD[syst]->Branch("leptonRelIso",&lepRelIso);
    
    treesWSampleQCD[syst]->Branch("fJetPt",&fJetPt);
    treesWSampleQCD[syst]->Branch("fJetE",&fJetE);
    treesWSampleQCD[syst]->Branch("fJetEta",&fJetEta);
    treesWSampleQCD[syst]->Branch("fJetPhi",&fJetPhi);
    
    
    treesWSampleQCD[syst]->Branch("bJetPt",&bJetPt);
    treesWSampleQCD[syst]->Branch("bJetE",&bJetE);
    treesWSampleQCD[syst]->Branch("bJetEta",&bJetEta);
    treesWSampleQCD[syst]->Branch("bJetPhi",&bJetPhi);
    
    treesWSampleQCD[syst]->Branch("metPt",&metPt);
    treesWSampleQCD[syst]->Branch("metPhi",&metPhi);
    
    treesWSampleQCD[syst]->Branch("topPt",&topPt);
    treesWSampleQCD[syst]->Branch("topPhi",&topPhi);
    treesWSampleQCD[syst]->Branch("topEta",&topEta);
    treesWSampleQCD[syst]->Branch("topE",&topE);
    
    treesWSampleQCD[syst]->Branch("Q2",&Q2);
    treesWSampleQCD[syst]->Branch("x1",&x1);
    treesWSampleQCD[syst]->Branch("x2",&x2);

 
    treesWSampleQCD[syst]->Branch("charge",&chargeTree);
    treesWSampleQCD[syst]->Branch("runid",&runTree);
    treesWSampleQCD[syst]->Branch("lumiid",&lumiTree);
    treesWSampleQCD[syst]->Branch("eventid",&eventTree);
    treesWSampleQCD[syst]->Branch("weight",&weightTree);

    treesWSampleQCD[syst]->Branch("bWeight",&bWeightTree);
    treesWSampleQCD[syst]->Branch("PUWeight",&PUWeightTree);
    treesWSampleQCD[syst]->Branch("turnOnWeight",&turnOnWeightTree);

    treesWSampleQCD[syst]->Branch("nVertices",&nVertices);



    //W Sample    

  }
  
  for(size_t i = 0; i < systematics.size();++i){
    
    string syst = systematics[i];
    
    string treename = (channel+"_"+syst);
    
      
    //     stringstream ssstep;
    //      ssstep << step;
    string sstep = "0";//ssstep.str();
    treesScan[syst] = new TTree((treename+"_step_"+sstep).c_str(),(treename+"_step_"+sstep).c_str()); 
    
      treesScan[syst]->Branch("etaLowBTag",&etaTree);
      treesScan[syst]->Branch("etaHighBTag",&etaTree2);
      treesScan[syst]->Branch("costhetalj",&cosTree);
      treesScan[syst]->Branch("topMass",&topMassTree);
      treesScan[syst]->Branch("mtwMass",&mtwMassTree);
      
      treesScan[syst]->Branch("highBTag",&highBTagTree);
      treesScan[syst]->Branch("lowBTag",&lowBTagTree);

      treesScan[syst]->Branch("bJetPt",&bJetPt);
      treesScan[syst]->Branch("bJetFlavour",&bJetFlavourTree);
      treesScan[syst]->Branch("fJetPt",&fJetPt);
      
      treesScan[syst]->Branch("charge",&chargeTree);
      treesScan[syst]->Branch("runid",&runTree);
      treesScan[syst]->Branch("lumiid",&lumiTree);
      treesScan[syst]->Branch("eventid",&eventTree);
      treesScan[syst]->Branch("weight",&weightTree);


      treesScan[syst]->Branch("leptonPt",&lepPt);
      treesScan[syst]->Branch("leptonPhi",&lepPhi);
      treesScan[syst]->Branch("leptonRelIso",&lepRelIso);

      
      treesScan[syst]->Branch("fJetPt",&fJetPt);
      treesScan[syst]->Branch("fJetE",&fJetE);
      treesScan[syst]->Branch("fJetEta",&fJetEta);
      treesScan[syst]->Branch("fJetPhi",&fJetPhi);
      treesScan[syst]->Branch("bJetFlavour",&bJetFlavourTree);
      
      treesScan[syst]->Branch("bJetPt",&bJetPt);
      treesScan[syst]->Branch("bJetE",&bJetE);
      treesScan[syst]->Branch("bJetEta",&bJetEta);
      treesScan[syst]->Branch("bJetPhi",&bJetPhi);

      treesScan[syst]->Branch("metPt",&metPt);
      treesScan[syst]->Branch("metPhi",&metPhi);

      treesScan[syst]->Branch("bWeight",&bWeightTree);
      treesScan[syst]->Branch("PUWeight",&PUWeightTree);
      treesScan[syst]->Branch("turnOnWeight",&turnOnWeightTree);

      treesScan[syst]->Branch("Q2",&Q2);
      treesScan[syst]->Branch("x1",&x1);
      treesScan[syst]->Branch("x2",&x2);

      //Sample ESB
      treesESB[syst] = new TTree((treename+"ESB").c_str(),(treename+"ESB").c_str()); 
      
      treesESB[syst]->Branch("eta",&etaTree);
      treesESB[syst]->Branch("costhetalj",&cosTree);
      treesESB[syst]->Branch("topMass",&topMassTree);
      treesESB[syst]->Branch("mtwMass",&mtwMassTree);
    
      treesESB[syst]->Branch("charge",&chargeTree);
      treesESB[syst]->Branch("runid",&runTree);
      treesESB[syst]->Branch("lumiid",&lumiTree);
      treesESB[syst]->Branch("eventid",&eventTree);
      treesESB[syst]->Branch("weight",&weightTree);
      
      treesESB[syst]->Branch("Q2",&Q2);
      treesESB[syst]->Branch("x1",&x1);
      treesESB[syst]->Branch("x2",&x2);
      
      treesESB[syst]->Branch("bWeight",&bWeightTree);
      treesESB[syst]->Branch("PUWeight",&PUWeightTree);
      treesESB[syst]->Branch("turnOnWeight",&turnOnWeightTree);
      
      
      //Extra info
      
      treesESB[syst]->Branch("leptonPt",&lepPt);
      treesESB[syst]->Branch("leptonEta",&lepEta);
      treesESB[syst]->Branch("leptonPhi",&lepPhi);
      treesESB[syst]->Branch("leptonRelIso",&lepRelIso);
      
      treesESB[syst]->Branch("fJetPt",&fJetPt);
    treesESB[syst]->Branch("fJetE",&fJetE);
    treesESB[syst]->Branch("fJetEta",&fJetEta);
    treesESB[syst]->Branch("fJetPhi",&fJetPhi);
    
    treesESB[syst]->Branch("bJetPt",&bJetPt);
    treesESB[syst]->Branch("bJetE",&bJetE);
    treesESB[syst]->Branch("bJetEta",&bJetEta);
    treesESB[syst]->Branch("bJetPhi",&bJetPhi);
    
    treesESB[syst]->Branch("metPt",&metPt);
    treesESB[syst]->Branch("metPhi",&metPhi);
    
    treesESB[syst]->Branch("topPt",&topPt);
    treesESB[syst]->Branch("topPhi",&topPhi);
    treesESB[syst]->Branch("topEta",&topEta);
    treesESB[syst]->Branch("topE",&topE);

    treesESB[syst]->Branch("ID",&electronID);

    treesESB[syst]->Branch("totalEnergy",&totalEnergy);
    treesESB[syst]->Branch("totalMomentum",&totalMomentum);

    treesESB[syst]->Branch("bJetFlavour",&bJetFlavourTree);
    
    treesESB[syst]->Branch("nVertices",&nVertices);

    treesESB[syst]->Branch("lowBTag",&lowBTagTree);
    treesESB[syst]->Branch("highBTag",&highBTagTree);


//Sample ESBQCD
    treesESBQCD[syst] = new TTree((treename+"ESBQCD").c_str(),(treename+"ESBQCD").c_str()); 
      
      treesESBQCD[syst]->Branch("eta",&etaTree);
      treesESBQCD[syst]->Branch("costhetalj",&cosTree);
      treesESBQCD[syst]->Branch("topMass",&topMassTree);
      treesESBQCD[syst]->Branch("mtwMass",&mtwMassTree);
    
      treesESBQCD[syst]->Branch("charge",&chargeTree);
      treesESBQCD[syst]->Branch("runid",&runTree);
      treesESBQCD[syst]->Branch("lumiid",&lumiTree);
      treesESBQCD[syst]->Branch("eventid",&eventTree);
      treesESBQCD[syst]->Branch("weight",&weightTree);
      
      treesESBQCD[syst]->Branch("Q2",&Q2);
      treesESBQCD[syst]->Branch("x1",&x1);
      treesESBQCD[syst]->Branch("x2",&x2);
      
      treesESBQCD[syst]->Branch("bWeight",&bWeightTree);
      treesESBQCD[syst]->Branch("PUWeight",&PUWeightTree);
      treesESBQCD[syst]->Branch("turnOnWeight",&turnOnWeightTree);
      
      
      //Extra info
      
      treesESBQCD[syst]->Branch("leptonPt",&lepPt);
      treesESBQCD[syst]->Branch("leptonEta",&lepEta);
      treesESBQCD[syst]->Branch("leptonPhi",&lepPhi);
      treesESBQCD[syst]->Branch("leptonRelIso",&lepRelIso);
      
      treesESBQCD[syst]->Branch("fJetPt",&fJetPt);
      treesESBQCD[syst]->Branch("fJetE",&fJetE);
      treesESBQCD[syst]->Branch("fJetEta",&fJetEta);
      treesESBQCD[syst]->Branch("fJetPhi",&fJetPhi);
      
      treesESBQCD[syst]->Branch("bJetPt",&bJetPt);
      treesESBQCD[syst]->Branch("bJetE",&bJetE);
      treesESBQCD[syst]->Branch("bJetEta",&bJetEta);
      treesESBQCD[syst]->Branch("bJetPhi",&bJetPhi);
      
      treesESBQCD[syst]->Branch("metPt",&metPt);
      treesESBQCD[syst]->Branch("metPhi",&metPhi);
      
      treesESBQCD[syst]->Branch("topPt",&topPt);
      treesESBQCD[syst]->Branch("topPhi",&topPhi);
      treesESBQCD[syst]->Branch("topEta",&topEta);
      treesESBQCD[syst]->Branch("topE",&topE);
      
      treesESBQCD[syst]->Branch("ID",&electronID);
      
      treesESBQCD[syst]->Branch("totalEnergy",&totalEnergy);
      treesESBQCD[syst]->Branch("totalMomentum",&totalMomentum);
      
      treesESBQCD[syst]->Branch("bJetFlavour",&bJetFlavourTree);
      
      treesESBQCD[syst]->Branch("nVertices",&nVertices);
      
      treesESBQCD[syst]->Branch("lowBTag",&lowBTagTree);
      treesESBQCD[syst]->Branch("highBTag",&highBTagTree);

      
      //      treesScan[syst]->Branch("ID",&electronID);
      
      treesScan[syst]->Branch("ID",&electronID);

      treesScan[syst]->Branch("nVertices",&nVertices);


      treesScanQCD[syst] = new TTree((treename+"_stepQCD_"+sstep).c_str(),(treename+"_stepQCD_"+sstep).c_str()); 

      treesScanQCD[syst]->Branch("etaLowBTag",&etaTree);
      treesScanQCD[syst]->Branch("etaHighBTag",&etaTree2);
      treesScanQCD[syst]->Branch("costhetalj",&cosTree);
      treesScanQCD[syst]->Branch("topMass",&topMassTree);
      treesScanQCD[syst]->Branch("mtwMass",&mtwMassTree);

      treesScanQCD[syst]->Branch("metPt",&metPt);
      treesScanQCD[syst]->Branch("metPhi",&metPhi);
      
      treesScanQCD[syst]->Branch("highBTag",&highBTagTree);
      treesScanQCD[syst]->Branch("lowBTag",&lowBTagTree);
      
      treesScanQCD[syst]->Branch("charge",&chargeTree);
      treesScanQCD[syst]->Branch("runid",&runTree);
      treesScanQCD[syst]->Branch("lumiid",&lumiTree);
      treesScanQCD[syst]->Branch("eventid",&eventTree);
      treesScanQCD[syst]->Branch("weight",&weightTree);
      treesScanQCD[syst]->Branch("leptonRelIso",&lepRelIso);

      treesScanQCD[syst]->Branch("bWeight",&bWeightTree);
      treesScanQCD[syst]->Branch("PUWeight",&PUWeightTree);
      treesScanQCD[syst]->Branch("turnOnWeight",&turnOnWeightTree);

      treesScanQCD[syst]->Branch("nVertices",&nVertices);

      treesScanQCD[syst]->Branch("Q2",&Q2);
      treesScanQCD[syst]->Branch("x1",&x1);
      treesScanQCD[syst]->Branch("x2",&x2);
      
    
  }  

  b_tchpt_signal_region = BTagWeight(1,1);
  b_tchel_sample_A = BTagWeight(0,0);
  b_tchel_sample_B = BTagWeight(1,1);
  b_tchpt_sample_B = BTagWeight(0,0);

  b_tchpm_sample_ESB = BTagWeight(1,2);
  b_tchpt_sample_ESB = BTagWeight(0,0);

  //  JEC_PATH = "CondFormats/JetMETObjects/data/";
  //  JEC_PATH = "./JECs/";
  JEC_PATH = "./";
  //  fip = edm::FileInPath(JEC_PATH+"Spring10_Uncertainty_AK5PF.txt");
  //fip = edm::FileInPath(JEC_PATH+"GR_R_42_V19_AK5PF_Uncertainty.txt");
  //jecUnc = new JetCorrectionUncertainty(fip.fullPath());
  jecUnc  = new JetCorrectionUncertainty(JEC_PATH+"GR_R_42_V19_AK5PF_Uncertainty.txt");
  JES_SW = 0.015;
  JES_b_cut = 0.02;
  JES_b_overCut = 0.03;

  //JetResolution part
  string fileResolName = "Spring10_PtResolution_AK5PF.txt";
  bool  doGaussianResol = false;
  ptResol = new JetResolution(fileResolName, doGaussianResol);  
  
  leptonRelIsoQCDCutUpper = 0.5,leptonRelIsoQCDCutLower=0.3;  


  topMassMeas = 172.9;
  
  if(doReCorrection_){//FIXME CURRENTLY NOT WORKING!!!
  cout << "jec 1" << endl;
  JetCorrectorParameters *ResJetParData = new JetCorrectorParameters(JEC_PATH+"GR_R_42_V19_AK5PF_L2L3Residual.txt"); 
  cout << "jec 1A" << endl;
  JetCorrectorParameters *L3JetParData  = new JetCorrectorParameters(JEC_PATH+"GR_R_42_V19_AK5PF_L3Absolute.txt");
  JetCorrectorParameters *L2JetParData  = new JetCorrectorParameters(JEC_PATH+"GR_R_42_V19_AK5PF_L2Relative.txt");
  JetCorrectorParameters *L1JetParData  = new JetCorrectorParameters(JEC_PATH+"GR_R_42_V19_AK5PF_L1FastJet.txt");
  cout << "jec 1B" << endl;
  vParData->push_back(*L1JetParData);
  cout << "jec 1C" << endl;
  vParData->push_back(*L2JetParData);
  vParData->push_back(*L3JetParData);
  vParData->push_back(*ResJetParData);

  cout << "jec 2" << endl;
  JetCorrectorParameters *L3JetParMC = new JetCorrectorParameters(JEC_PATH+"START42_V13::All_AK5PF_L3Absolute.txt");
  JetCorrectorParameters *L2JetParMC  = new JetCorrectorParameters(JEC_PATH+"START42_V13::All_AK5PF_L2Relative.txt");
  JetCorrectorParameters *L1JetParMC  = new JetCorrectorParameters(JEC_PATH+"START42_V13::All_AK5PF_L1FastJet.txt");
   vParMC->push_back(*L1JetParMC);
   vParMC->push_back(*L2JetParMC);
   vParMC->push_back(*L3JetParMC);
   
  cout << "jec 3" << endl;
   JetCorrectorData = new FactorizedJetCorrector(*vParData);
   JetCorrectorMC = new FactorizedJetCorrector(*vParMC);
  }
   InitializeEventScaleFactorMap();
  //  cout<< "I work for now but I do nothing. But again, if you gotta do nothing, you better do it right. To prove my good will I will provide you with somse numbers later."<<endl;

  //iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHPT",perfHP);
  //iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHEL",perfHE);
  
  //iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHPT",perfHP);
  //iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHEL",perfHE);
  
  isFirstEvent = true;

}

void SingleTopSystematicsTreesDumper::analyze(const Event& iEvent, const EventSetup& iSetup)
{
  
  //Very first check: if there are < 2 jets skip the event


  //  eventTree = iEvent.eventAuxiliary().event();
  //  if( eventTree != 124107024 )return;
  //  
  
  iEvent.getByLabel(jetsPt_,jetsPt);
  if(jetsPt->size() < 2)return; 
  if(jetsPt->size() > 25 && channel != "Data")return;  //Crazy events with huge jet multiplicity in mc
  
  if(isFirstEvent){
    cout <<  "isfirst " << endl;
   iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHPT",perfMHP);
   iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHPM",perfMHPM);
   iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHEL",perfMHE);

   iSetup.get<BTagPerformanceRecord>().get("BTAGTCHPM",perfBHPM);
   iSetup.get<BTagPerformanceRecord>().get("BTAGTCHPT",perfBHP);
   iSetup.get<BTagPerformanceRecord>().get("BTAGTCHEL",perfBHE);
   isFirstEvent = false;
  }
  //  iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHPT",perfHP);
  // iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHEL",perfHE);

  //  cout << "test 0 "<<endl;

  gotLeptons=0;
  gotLooseLeptons=0;
  gotJets=0;
  gotMets=0;
  gotPU=0;


  bool passesSignal=false,passesQCDSignal=false,
    passesSampleA=false,passesSampleB=false,
    passesQCDSampleA=false,passesQCDSampleB= false,
    passesESBQCD = false, passesESB = false;    

  //bool isControlSample_ = false; 

  //  iEvent.getByLabel(leptonsQCDRelIso_,leptonsQCDRelIso);
  iEvent.getByLabel(leptonsRelIso_,leptonsRelIso);

  
 
  double PUWeight =1;
  
  BinningPointByMap measurePoint;
  
  float metPx = 0; 
  float metPy = 0;

  double puZero=1;
  

  size_t nLeptons = 0;//leptonsPt->size();
  size_t nJets = 0;
  
  
  double WeightLumi = finalLumi*crossSection/originalEvents;
  double bTagWeight = 1;
  double bTagWeightWSample = 1;
  double bTagWeightTTSample = 1;
  double Weight = 1;
  double MTWValue =0;
  double MTWValueQCD =0;
  double RelIsoQCDCut = 0.1;
  
  float ptCut = 30;  
  //  float maxPtCut = maxPtCut_;

  

  //edm::EventBase* const iEventB = dynamic_cast<edm::EventBase*>(&iEvent);
  //double MyWeight = LumiWeights_.weight( (*iEventB) );
  
  //double w = LumiWeights_.weight(iEvent);

  float metPxTmp = 0;
  float metPyTmp = 0;

  if(channel=="Data")WeightLumi=1;


  //  cout << "test 01 "<<endl;


  double b_weight_signal_region_noSyst =1, b_weight_sample_A_noSyst=1, b_weight_sample_B_noSyst=1, b_weight_sample_ESB_noSyst =1; 
  
  for(size_t s = 0; s < systematics.size();++s){
    string syst_name =  systematics.at(s);
    string syst = syst_name;

    //Here the weight of the event is the weight
    //to normalize the sample to the luminosity 
    //required in the cfg
    Weight = WeightLumi;
    //    Weight *= PUWeight;
    bTagWeight = 1;
    bTagWeightWSample = 1;
    bTagWeightTTSample = 1;
    

    bool is_btag_relevant = ((syst_name=="noSyst" || syst_name == "BTagUp" || syst_name == "BTagDown" 
			     || syst_name == "MisTagUp" || syst_name == "MisTagDown"
			      || syst_name == "JESUp" || syst_name == "JESDown" ) && channel != "Data"
			     );


    //    cout << "test 02 systs "<< syst_name <<endl;
    //Setup for systematics

    //This is done according to old b-tagging prescriptions
    //Where the b(c) jet Scale Factors were taken 0.9 +-15%(30%)
    //Will have to be updated
    

    //Here we have vectors of weights 
    //to be associated with the 
    //b-jets selection in the sample according to algorythm X: 
    //a b-tag requirement implies a b_weight_tag_algoX,
    //a b-veto requirement implies a b_weight_antitag_algoX
 
    
    b_weight_signal_region =1; b_weight_sample_A=1; b_weight_sample_B=1; 
   
    nb =0;
    nc =0;
    nudsg =0;

    //Clear the vector of objects to be used in the selection
    leptons.clear();
    leptonsQCD.clear();
    
    //Define - initialize some variables
    MTWValue =0;
    
    
    //position of lowest and highest b-tag used to chose the top candidate 
    int lowBTagTreePosition=-1;
    lowBTagTree = 99999;
    
    int highBTagTreePosition=-1;
    highBTagTree = -9999;

    int maxPtTreePosition=-1;
    maxPtTree = -99999;
    int minPtTreePosition=-1;
    minPtTree = 99999;

    //Taking the unclustered met previously evaluated 
    //and already present in the n-tuples
    //This is used for syst up and down

    
    //Define - initialize some variables
    float eta;
    float ptCorr;
    int flavour;
    double unc =0;
    
    //Loops to apply systematics on jets-leptons
    


    //Lepton loop
    nLeptons = leptonsRelIso->size();
    for(size_t i = 0;i<nLeptons;++i){

      //      cout << "test 03 systs "<< syst_name <<" leps "<< nLeptons << " loop pos" <<  i<<endl;

      
      float leptonRelIso = leptonsRelIso->at(i);
      //      float leptonQCDRelIso = leptonsQCDRelIso->at(i);
      float leptonQCDRelIso = leptonRelIso;
      
     //Apply isolation cut
      if(leptonRelIso>RelIsoCut)continue;
      if(!gotLeptons){
	iEvent.getByLabel(leptonsEta_,leptonsEta);
	iEvent.getByLabel(leptonsPt_,leptonsPt);
	iEvent.getByLabel(leptonsPhi_,leptonsPhi);
	iEvent.getByLabel(leptonsEnergy_,leptonsEnergy);
	iEvent.getByLabel(leptonsCharge_,leptonsCharge);
	iEvent.getByLabel(leptonsID_,leptonsID);
	iEvent.getByLabel(leptonsDB_,leptonsDB);

	gotLeptons=true;
      }
      //if electron apply ID cuts
      if(leptonsFlavour_ == "electron"  ) {
	if(leptonsID->size()==0)cout<< "warning requiring ele id of collection which has no entries! Check the leptonsFlavour parameter "<<endl;
	float leptonID = leptonsID->at(i);
	//Legenda for eleId : 0 fail, 1 ID only, 2 iso Only, 3 ID iso only, 4 conv rej, 5 conv rej and ID, 6 conv rej and iso, 7 all 
	//Require Full ID selection
	if ((leptonID !=7)&&leptonID !=5)continue;
	electronID = leptonID;
	//This is to require conv rejection and ID but do not make requests on iso from id
	//	if (!(leptonID==5 || leptonID ==7))continue;
      }
      float leptonDB = leptonsDB->at(i);
      if ( fabs(leptonDB) >0.02) continue;

      lepRelIso = leptonRelIso;
      
      float leptonPt = leptonsPt->at(i);
      float leptonPhi = leptonsPhi->at(i);
      float leptonEta = leptonsEta->at(i);
      float leptonE = leptonsEnergy->at(i);
      //Build the lepton 4-momentum
      leptons.push_back(math::PtEtaPhiELorentzVector(leptonPt,leptonEta,leptonPhi,leptonE));
  
     }


    //  cout << "test 03 "<<endl;
    //Loop for the qcd leptons
    if(doQCD_){
      for(size_t i = 0;i<nLeptons;++i){
	
	//	cout << "test 04 systs "<< syst_name <<" leps qcd "<< nLeptons << " loop pos" <<  i<<endl;


	float leptonRelIso = leptonsRelIso->at(i);
	float leptonQCDRelIso = leptonRelIso;
	
		
		//Use an anti-isolation requirement

	if(leptonsFlavour_ == "muon"){
	  if( leptonQCDRelIso > leptonRelIsoQCDCutUpper )continue;
	  if( leptonQCDRelIso < leptonRelIsoQCDCutLower )continue;
	  
	  if(!gotLeptons){
	    iEvent.getByLabel(leptonsEta_,leptonsEta);
	    iEvent.getByLabel(leptonsPt_,leptonsPt);
	    iEvent.getByLabel(leptonsPhi_,leptonsPhi);
	    iEvent.getByLabel(leptonsEnergy_,leptonsEnergy);
	    iEvent.getByLabel(leptonsCharge_,leptonsCharge);
	    iEvent.getByLabel(leptonsID_,leptonsID);
	    

iEvent.getByLabel(leptonsDB_,leptonsDB);
	    gotLeptons=true;
	  }
	 
	}
	
	if(leptonsFlavour_ == "electron"  ) {
	  bool QCDCondition = false;
	  iEvent.getByLabel(leptonsID_,leptonsID);
	  iEvent.getByLabel(leptonsDB_,leptonsDB);
	  float leptonID = leptonsID->at(i);
	  float beamspot  = abs(leptonsDB->at(i));
	  bool isid =	(leptonID ==  1 || leptonID == 3 || leptonID == 5 || leptonID == 7);
	  //Legenda for eleId : 0 fail, 1 ID only, 2 iso Only, 3 ID iso only, 4 conv rej, 5 conv rej and ID, 6 conv rej and iso, 7 all 
	  QCDCondition = (!(leptonRelIso < 0.1) && !(beamspot<0.02))  || (!(leptonRelIso<0.1) && !isid) ||(!isid && !(beamspot<0.02));
	  electronID = leptonID;
	  
	  if(!QCDCondition) continue;
	  if(!gotLeptons){
	    iEvent.getByLabel(leptonsEta_,leptonsEta);
	    iEvent.getByLabel(leptonsPt_,leptonsPt);
	    iEvent.getByLabel(leptonsPhi_,leptonsPhi);
	    iEvent.getByLabel(leptonsEnergy_,leptonsEnergy);
	    iEvent.getByLabel(leptonsCharge_,leptonsCharge);
	    gotLeptons=true;
	  }
	} 


	lepRelIso = leptonRelIso;
	
	 float leptonPt = leptonsPt->at(i);
	 float leptonPhi = leptonsPhi->at(i);
	 float leptonEta = leptonsEta->at(i);
	 float leptonE = leptonsEnergy->at(i);
	 //Create the lepton
	
	 leptonsQCD.push_back(math::PtEtaPhiELorentzVector(leptonPt,leptonEta,leptonPhi,leptonE));
      }
     }
    
    if(leptons.size()!=1 && leptonsQCD.size()!=1) continue;

    //Clear the vector of btags //NOT USED NOW
    //    b_weight_tag_algo1.clear();
    //    b_weight_tag_algo2.clear();
    //    b_weight_antitag_algo1.clear();
    //    b_weight_antitag_algo2.clear();
    
    //        b_discriminator_value_tag_algo1.clear();
    //    b_discriminator_value_antitag_algo2.clear();
    
    ntchpt_tags=0;
    ntchpm_tags=0;
    ntche_tags=0;
    ntchpt_antitags=0;
    ntche_antitags=0;


    //Clear the vectors of non-leptons
    jets.clear();
    bjets.clear();
    antibjets.clear();


    
  if(doPU_){
    if(!gotPU ){
      //    cout << " before npv "<<endl;
    iEvent.getByLabel(npv_,npv);
    nVertices = *npv;
    //    cout << "after npv val"<< *npv << endl;
    //int temppv= *npv; 
    puZero =    LumiWeights_.weight( *npv);
    //    cout << "got weight val "<<PUWeight << endl;
      //    PUWeight = *preWeights;
    gotPU = true;
    }
  
    if(syst_name=="PUUp"){
      if(*npv<=49){
	int temppv= *npv +1 ;
	//	PUWeight =1;
	PUWeight =  LumiWeights_.weight( temppv);
      }
    }
    if(syst_name=="PUDown"){
      if(*npv>=1){
	//	PUWeight =1;
	int temppv= *npv -1 ;
	PUWeight =  LumiWeights_.weight( temppv);
      }
      //    PUWeight = *preWeights;
    }
    if((syst_name != "PUUp" && syst_name!= "PUDown")){
      PUWeight =  puZero;
    }
  }
  else(nVertices = -1);
  //  cout << " test 1 "<<endl;

  jsfshpt.clear();//  bjs.clear();cjs.clear();ljs.clear(); 
  jsfshpm.clear();//  bjs.clear();cjs.clear();ljs.clear(); 
  jsfshel.clear();//  bjs.clear();cjs.clear();ljs.clear(); 
  jetprobs.clear();

  bool hasTurnOnWeight = false;
  double turnOnWeightValue =1;


    if(!gotMets){
      iEvent.getByLabel(METPhi_,METPhi);
      iEvent.getByLabel(METPt_,METPt);
      
      metPx = METPt->at(0)*cos(METPhi->at(0));
      metPy = METPt->at(0)*sin(METPhi->at(0));
      
      metPxTmp = metPx; 
      metPyTmp = metPy;

      metPhi = METPhi->at(0);

      
      gotMets = true;
    }

    metPx = metPxTmp; 
    metPy = metPyTmp;

     
    if(syst_name == "UnclusteredMETUp"){
      iEvent.getByLabel(UnclMETPx_,UnclMETPx);
      iEvent.getByLabel(UnclMETPy_,UnclMETPy);
      metPx+= (*UnclMETPx) *0.1;
      metPy+= (*UnclMETPy) *0.1;
    }
    if(syst_name == "UnclusteredMETDown"){
      iEvent.getByLabel(UnclMETPx_,UnclMETPx);
      iEvent.getByLabel(UnclMETPy_,UnclMETPy);
      metPx-= (*UnclMETPx) *0.1;
      metPy-= (*UnclMETPy) *0.1;
    }
    

    
    if(!gotJets){
      iEvent.getByLabel(jetsEta_,jetsEta);
      iEvent.getByLabel(jetsPhi_,jetsPhi);
      
      iEvent.getByLabel(jetsEnergy_,jetsEnergy);
      iEvent.getByLabel(jetsBTagAlgo_,jetsBTagAlgo);
      iEvent.getByLabel(jetsAntiBTagAlgo_,jetsAntiBTagAlgo);
      iEvent.getByLabel(jetsFlavour_,jetsFlavour);
      iEvent.getByLabel(jetsCorrTotal_,jetsCorrTotal);
      if(doResol_)iEvent.getByLabel(genJetsPt_,genJetsPt);
      

      nJets = jetsPt->size();

      if(channel != "Data"){
      iEvent.getByLabel(x1_,x1h);
      iEvent.getByLabel(x2_,x2h);
      
      x1 = *x1h;
      x2 = *x2h;
      }
      Q2 = x1 * x2 * 7000*7000;

      gotJets= true;
   }
    
    if(leptonsFlavour_ == "electron" && doTurnOn_){
      if (!hasTurnOnWeight){
	for(size_t i = 0;i<nJets;++i){
	 
	  // 	  cout << "test 05 systs "<< syst_name <<" jets qcd "<< nJets << " loop pos" <<  i<<endl;


	  if (fabs(jetsEta->at(i))>2.6) jetprobs.push_back(0.);
	  else jetprobs.push_back(jetprob(jetsPt->at(i),jetsBTagAlgo->at(i)));
	}
	turnOnWeightValue = turnOnWeight(jetprobs,1);
	hasTurnOnWeight=true;
      }
    }

    turnOnWeightTree = turnOnWeightValue;
    PUWeightTree = PUWeight;
    
    //    Weight * turnOnWeightValue;
    Weight *= PUWeight;
    //Jets loop
    for(size_t i = 0;i<nJets;++i){
      
      //      cout << "test 06 systs "<< syst_name <<" jets qcd "<< nJets << " loop pos" <<  i<<endl;


      eta = jetsEta->at(i);
      if (fabs(eta )>4.5)continue;
      ptCorr = jetsPt->at(i);
      flavour = jetsFlavour->at(i);
      double energyCorr = jetsEnergy->at(i); 

      if(doReCorrection_){
	ptCorr = ptCorr/jetsCorrTotal->at(i);
	
      }
      
      //      float geneta =genJetsEta->at(i);
      float genpt = -1.;
      if(doResol_)genpt = genJetsPt->at(i);
      float rndm = 0.1;
      
      
      //If systematics JES up/down we need to change the pt of the jet
      //consider if it passes the threshold or not
      if(syst_name == "JESUp"){
	unc = jetUncertainty( eta,  ptCorr, flavour);
	ptCorr = ptCorr * (1+unc);
	energyCorr = energyCorr *(1+unc);
      }
      if(syst_name == "JESDown"){
	unc = jetUncertainty( eta,  ptCorr, flavour);
	ptCorr = ptCorr * (1-unc);
	energyCorr = energyCorr *(1-unc);
      }
      
      if(doResol_ && genpt > 0.0){
	//	TF1* fPtResol = ptResol->resolutionEtaPt(eta,ptCorr);
	//cout<< " function parameters ";
	//	  fPtResol -> Print();
	//cout<<endl;
	//double sigmaFunc = fPtResol->GetParameter("\\sigma");
	//fPtResol->SetParameter("\\sigma",sigmaFunc*1.1);
	//rndm = fPtResol->GetRandom();
	double smear = std::max((double)(0.0),(double)(ptCorr+(ptCorr-genpt)*resolScale)/ptCorr);
	energyCorr = energyCorr * smear;
	ptCorr = ptCorr*smear;
      }
      
	//Pt cut
	bool passesPtCut = ptCorr>ptCut;
	if(passesPtCut) jets.push_back(math::PtEtaPhiELorentzVector(ptCorr,jetsEta->at(i), jetsPhi->at(i), energyCorr) ); 
      
	

	//      if(passesPtCut) cout <<" jet "<< i <<" passes pt cut, flavour "<< abs(flavour)<< " syst " << syst_name << " pt "<< ptCorr<< " pt with unc "<< jets.back().pt() <<" unc "<< unc << endl;
      
      //Require the lepton jet DR > 0.3 veto
	/*if(passesPtCut && !leptons.empty()){
	  for(size_t l =0;l<leptons.size();++l){
	    if( deltaR<math::PtEtaPhiELorentzVector,math::PtEtaPhiELorentzVector>(jets.back(),leptons.at(l))<0.3){
	      jets.pop_back();
	      continue;
	    }
	  }
	  }*/
	
      if(!passesPtCut) continue;

      //b tag thresholds 
      
      
      double valueAlgo1 = jetsBTagAlgo->at(i);
      double valueAlgo2 = jetsAntiBTagAlgo->at(i);
      
      bool passesMediumBTag = valueAlgo1  > 1.93;

      bool passesBTag = valueAlgo1  >bTagThreshold;
      bool passesAntiBTag = valueAlgo2 <1.7;

      //      if(leptonsFlavour_ == "electron" && !isControlSample_) 
      //	{
      //	  valueAlgo2 = jetsBTagAlgo->at(i);
      //	  passesAntiBTag = valueAlgo2 <1.93;
      //	}
      
      
      //max pt position:
      int pos =jets.size()-1;
      if(ptCorr > maxPtTree){ 
	maxPtTreePosition = pos;
	maxPtTree = ptCorr;
      }
      //min pt position:
      if(ptCorr < minPtTree){ 
	minPtTreePosition = pos;
	minPtTree = ptCorr;
      }
      
      //Passes firs algorythm (b tag requirement in the case of t-channel standard selection)
      //      cout << " test 2 "<<endl;
  
  double etaMin =  min(fabs(eta),(float)2.3999);
  double ptMin =  min(ptCorr,(float)239.9);//min(jets.back().pt(),998.0);
  //  if(is_btag_relevant ){
    measurePoint.insert(BinningVariables::JetAbsEta,etaMin);
    measurePoint.insert(BinningVariables::JetEt,ptMin);
    //  }
  //Apply different SFs if it is b,c or light jet
  if(abs(flavour)==4){ 
    ++nc;
    if(is_btag_relevant ){
      //double hpteff =(perfBHP->getResult(PerformanceResult::BTAGBEFF,measurePoint));
      double hpteff = EFFMap("TCHPT_C");
      double hptSF = (perfBHP->getResult(PerformanceResult::BTAGBEFFCORR,measurePoint));
      double hptSFErr =0.;
      //double hpteff =(perfBHP->getResult(PerformanceResult::BTAGBEFF,measurePoint));
      double hptmeff = EFFMap("TCHPM_C");
      double hptmSF = (perfBHPM->getResult(PerformanceResult::BTAGBEFFCORR,measurePoint));
      double hptmSFErr =0.;
      //double heleff =(perfBHE->getResult(PerformanceResult::BTAGBEFF,measurePoint));
      double heleff = EFFMap("TCHEL_C");
      double helSF = (perfBHE->getResult(PerformanceResult::BTAGBEFFCORR,measurePoint));
      double helSFErr =0.;
      if(syst_name == "BTagUp"){                             
	hptSFErr = fabs(perfBHP->getResult(PerformanceResult::BTAGBERRCORR,measurePoint));
	hptmSFErr = fabs(perfBHPM->getResult(PerformanceResult::BTAGBERRCORR,measurePoint));
	helSFErr = fabs(perfBHE->getResult(PerformanceResult::BTAGBERRCORR,measurePoint));
      }
      if(syst_name == "BTagDown"){
	hptSFErr = -fabs(perfBHP->getResult(PerformanceResult::BTAGBERRCORR,measurePoint));
	hptmSFErr = -fabs(perfBHPM->getResult(PerformanceResult::BTAGBERRCORR,measurePoint));
	helSFErr = -fabs(perfBHE->getResult(PerformanceResult::BTAGBERRCORR,measurePoint));
      }
      //      cout <<"cjet hpt "<<hpteff<< " hpt sf "<< hptSF <<endl;
      
      jsfshpm.push_back(BTagWeight::JetInfo(hptmeff,hptmSF+hptmSFErr));
      jsfshpt.push_back(BTagWeight::JetInfo(hpteff,hptSF+hptSFErr));
      jsfshel.push_back(BTagWeight::JetInfo(heleff,helSF+helSFErr));
    }
    //  jsfshpt.push_back(BTagWeight::JetInfo(1.,1.));
    //    jsfshel.push_back(BTagWeight::JetInfo(1.,1.));
  }
  else if(abs(flavour)==5){
    ++nb;
    if(is_btag_relevant ){
      //double hpteff =(perfBHP->getResult(PerformanceResult::BTAGBEFF,measurePoint));
      double hpteff = EFFMap("TCHPT_B");
      double hptSF = (perfBHP->getResult(PerformanceResult::BTAGBEFFCORR,measurePoint));
      double hptSFErr =0.;
      //double hpteff =(perfBHP->getResult(PerformanceResult::BTAGBEFF,measurePoint));
      double hptmeff = EFFMap("TCHPM_B");
      double hptmSF = (perfBHP->getResult(PerformanceResult::BTAGBEFFCORR,measurePoint));
      double hptmSFErr =0.;
      //    double heleff =(perfBHE->getResult(PerformanceResult::BTAGBEFF,measurePoint));
      double heleff = EFFMap("TCHEL_B");
      double helSF = (perfBHE->getResult(PerformanceResult::BTAGBEFFCORR,measurePoint));
      double helSFErr =0.;
      if(syst_name == "BTagUp"){
      hptSFErr = fabs(perfBHP->getResult(PerformanceResult::BTAGBERRCORR,measurePoint));
      hptmSFErr = fabs(perfBHPM->getResult(PerformanceResult::BTAGBERRCORR,measurePoint));
      helSFErr = fabs(perfBHE->getResult(PerformanceResult::BTAGBERRCORR,measurePoint));
    }
    if(syst_name == "BTagDown"){
      hptSFErr = -fabs(perfBHP->getResult(PerformanceResult::BTAGBERRCORR,measurePoint));
      hptmSFErr = -fabs(perfBHPM->getResult(PerformanceResult::BTAGBERRCORR,measurePoint));
      helSFErr = -fabs(perfBHE->getResult(PerformanceResult::BTAGBERRCORR,measurePoint));
    }
    //    cout <<"bjet hpt "<<hpteff<< " hpt sf "<< hptSF << " jet pt "<< ptCorr<<"eta"<<etaMin <<endl;
    jsfshpm.push_back(BTagWeight::JetInfo(hptmeff,hptmSF+hptmSFErr));
    jsfshpt.push_back(BTagWeight::JetInfo(hpteff,hptSF+hptSFErr));
    jsfshel.push_back(BTagWeight::JetInfo(heleff,helSF+helSFErr));
    }

    //	  jsfshpt.push_back(BTagWeight::JetInfo(1.,1.));
    //	  jsfshel.push_back(BTagWeight::JetInfo(1.,1.));
  }
  //	else if(abs(flavour) != 6 ){
  else{
    if(is_btag_relevant ){
    double hpteff =(perfMHP->getResult(PerformanceResult::BTAGLEFF,measurePoint));
    double hptSF = (perfMHP->getResult(PerformanceResult::BTAGLEFFCORR,measurePoint));
    double hptSFErr =0.;
    double hptmeff =(perfMHPM->getResult(PerformanceResult::BTAGLEFF,measurePoint));
    double hptmSF = (perfMHPM->getResult(PerformanceResult::BTAGLEFFCORR,measurePoint));
    double hptmSFErr =0.;
    double heleff =(perfMHE->getResult(PerformanceResult::BTAGLEFF,measurePoint));
    double helSF = (perfMHE->getResult(PerformanceResult::BTAGLEFFCORR,measurePoint));
    double helSFErr =0.;
    if(syst_name == "MisTagUp"){
      hptSFErr = fabs(perfMHP->getResult(PerformanceResult::BTAGLERRCORR,measurePoint));
      hptmSFErr = fabs(perfMHPM->getResult(PerformanceResult::BTAGBERRCORR,measurePoint));
      helSFErr = fabs(perfMHE->getResult(PerformanceResult::BTAGLERRCORR,measurePoint));
    }
    if(syst_name == "MisTagDown"){
      hptSFErr = -fabs(perfMHP->getResult(PerformanceResult::BTAGLERRCORR,measurePoint));
      hptmSFErr = -fabs(perfMHPM->getResult(PerformanceResult::BTAGBERRCORR,measurePoint));
      helSFErr = -fabs(perfMHE->getResult(PerformanceResult::BTAGLERRCORR,measurePoint));
    }
    //    cout <<"light jet hpt "<<hpteff<< " hpt sf "<< hptSF <<endl;
    jsfshpm.push_back(BTagWeight::JetInfo(hptmeff,hptmSF+hptmSFErr));
    jsfshpt.push_back(BTagWeight::JetInfo(hpteff,hptSF+hptSFErr));
    jsfshel.push_back(BTagWeight::JetInfo(heleff,helSF+helSFErr));
    }
    ++nudsg;
  
  }
  if(is_btag_relevant ) measurePoint.reset();
  //	cout << " test 3 "<<endl;
    
  if(passesMediumBTag){
    ++ntchpm_tags;
  }
  if(passesBTag) {
    //Add to b-jet collection
    bjets.push_back(jets.back()); 
    ++ntchpt_tags;
  }
  else ++ntchpt_antitags;
  
  if(passesAntiBTag){
    antibjets.push_back(jets.back());
    ++ntche_antitags;
  }else ++ntche_tags;
  
  
  //Condition to find the highest/lowest b-tag 
  //according to algo 1 (tchp) 
  //      cout << " test highLow " << endl;
  //cout << " i "<< i <<" jets size "<< jets.size()<< " btag  "<< 
  if(jetsBTagAlgo->at(i) > highBTagTree){
    highBTagTree=jetsBTagAlgo->at(i);
    highBTagTreePosition=jets.size()-1;
    bJetFlavourTree = jetsFlavour->at(i);
  } 
  if(jetsBTagAlgo->at(i) < lowBTagTree){
    lowBTagTree=jetsBTagAlgo->at(i);
    lowBTagTreePosition=jets.size()-1;
  }
    }
    
    
    //cout << " test 3 "<<endl;
    //    cout <<" test "<<channel<<"nb" << nb << "nc"  << nc << " nudsg " <<nudsg<< " passes ? "<<  flavourFilter(channel,nb,nc,nudsg)<<endl;
    if( !flavourFilter(channel,nb,nc,nudsg) ) continue;
    
    /////////
    ///End of the standard lepton-jet loop 
    /////////
    
    if( jets.size()<2 )continue;
    if( maxPtTree< maxPtCut )continue;
    
    //Definition of the bjets:
    
    
    //    cout << "test syst "<< syst << " leptons " << leptons.size()<< " jets " << jets.size()<< " btags " << ntchpt_tags<< " medium tags "<< ntchpm_tags << endl;
  	
    //b_weight_signal_region = 1.;
    //b_weight_sample_A = 1.;
    //b_weight_sample_B = 1.;
    //b_weight_sample_B*= 1.;

     //Part of the effective selection and filling
  
     //QCD Samples
     if (doQCD_){
       //      cout << " qcd lep size " <<leptonsQCD.size()<< " non qcd lep size" <<looseMuonsRelIso->size()+ looseElectronsRelIso->size()<< endl;
       if(leptonsQCD.size()==1 && jets.size()==2){
	 //MTW definition
	 metPt = sqrt(metPx*metPx+metPy*metPy);
	 MTWValueQCD =  sqrt((leptonsQCD.at(0).pt()+metPt)*(leptonsQCD.at(0).pt()+metPt)  -(leptonsQCD.at(0).px()+metPx)*(leptonsQCD.at(0).px()+metPx) -(leptonsQCD.at(0).py()+metPy)*(leptonsQCD.at(0).py()+metPy));

	 //Sample ESB QCD
	 
       	 
       	 //Signal QCD sample
	 if( bjets.size()==1){
	   
	   if(syst=="noSyst") passesQCDSignal = true;
	   //cout << " Signal Sample QCD; antib  algo 2 weight size "<< b_weight_antitag_algo2.size()<< " b algo 1 weight size "<< b_weight_tag_algo1.size()<< endl;

	 
	   if(is_btag_relevant || !passesQCDSignal){
	     b_weight_signal_region = b_tchpt_signal_region.weight(jsfshpt,ntchpt_tags);
	     if(syst_name == "noSyst"){
	       b_weight_signal_region_noSyst = b_weight_signal_region;
	       
	     }
	   }
	   if(!is_btag_relevant && passesQCDSignal){
	     b_weight_signal_region = b_weight_signal_region_noSyst;
	     //	     b_weight_sample_A  = b_weight_sample_A_noSyst; 
	     // b_weight_sample_B = b_weight_sample_B_noSyst;  
	   }	   
	   
	   cout <<" t sample qcd" <<endl;

	   
 	   math::PtEtaPhiELorentzVector top = top4Momentum(leptonsQCD.at(0),bjets.at(0),metPx,metPy);
	   float fCosThetaLJ =  cosThetaLJ(leptonsQCD.at(0), jets.at(lowBTagTreePosition), top);
	   
	   runTree = iEvent.eventAuxiliary().run();
	   lumiTree = iEvent.eventAuxiliary().luminosityBlock();	
	   eventTree = iEvent.eventAuxiliary().event();   

	   bWeightTree= b_weight_signal_region;
	   weightTree = Weight*bWeightTree*turnOnWeightValue ;
	   
	   etaTree = fabs(jets.at(lowBTagTreePosition).eta());
	   cosTree = fCosThetaLJ;
	   topMassTree = top.mass();
	   mtwMassTree = MTWValueQCD;
	   chargeTree = leptonsCharge->at(0) ; 

	   
	   lepPt = leptonsQCD.at(0).pt();
	   lepEta = leptonsQCD.at(0).eta();
	   lepPhi = leptonsQCD.at(0).phi();
	   

	   bJetPt = bjets.at(0).pt();
	   bJetE = bjets.at(0).energy();
	   bJetEta = bjets.at(0).eta();
	   bJetPhi = bjets.at(0).phi();
	   
	   fJetPt = jets.at(lowBTagTreePosition).pt();
	   fJetE = jets.at(lowBTagTreePosition).energy();
	   fJetEta = jets.at(lowBTagTreePosition).eta();
	   fJetPhi = jets.at(lowBTagTreePosition).phi();


	   
	   //	   lowBTagTree = lowest
	   
	   //topPt = top.pt();
	   //topE = top.energy();
	   //topEta = top.eta();
	   //topPhi = top.phi();
	   
	   //	   totalEnergy = (top+jets.at(lowBTagTreePosition)).energy();
	   //	   totalMomentum = (top+jets.at(lowBTagTreePosition)).P();
	   
	   //	   metPt = mePPt->at(0);
	   //	   metPhi = METPhi->at(0);
	   
	   //	   metPhi = METPhi->at(0);

	   treesQCD[syst_name]->Fill();

   
	   cout << " passes cuts pre-mtw qcd sample, syst " << syst_name << " top mass "<< top.mass() << " cosTheta* "<< fCosThetaLJ << " fjetEta " << fabs(jets.at(lowBTagTreePosition).eta()) << " Weight "  << Weight << " B Weight "<<bTagWeight << " b weight 2 test"<< b_weight_signal_region << endl;
	   
	 }
	 
	 if( ntchpm_tags >=1 && ntchpt_tags ==0 ){
	   
	   if(syst=="noSyst") passesESBQCD = true;
	   //cout << " Signal Sample QCD; antib  algo 2 weight size "<< b_weight_antitag_algo2.size()<< " b algo 1 weight size "<< b_weight_tag_algo1.size()<< endl;
	   if(is_btag_relevant || !passesESBQCD){	
	     b_weight_sample_ESB = b_tchpm_sample_ESB.weight(jsfshpm,ntchpm_tags);
	     b_weight_sample_ESB *= b_tchpt_sample_ESB.weight(jsfshpt,ntchpt_tags);
	     if(syst_name == "noSyst"){
	       b_weight_sample_ESB_noSyst = b_weight_sample_ESB;
	       
	     }
	   }
	   
	   if(!is_btag_relevant && passesESBQCD){
	     b_weight_sample_ESB = b_weight_sample_ESB_noSyst;
	     //	     b_weight_sample_A  = b_weight_sample_A_noSyst; 
	       // b_weight_sample_B = b_weight_sample_B_noSyst;  
	     }	   
	     
	     cout <<" esb sample qcd" <<endl;

	     

	     if(ntchpt_tags != 1){

	       
	       cout << " lepton size " << leptonsQCD.size()<< " bhets suze "<< bjets.size()
		    << " jets size "<< jets.size() << " lowbtagtree pos" <<lowBTagTreePosition<<endl; 

	       math::PtEtaPhiELorentzVector top = top4Momentum(leptonsQCD.at(0),jets.at(highBTagTreePosition),metPx,metPy);
	       float fCosThetaLJ =  cosThetaLJ(leptonsQCD.at(0), jets.at(lowBTagTreePosition), top);
	       
	       runTree = iEvent.eventAuxiliary().run();
	       lumiTree = iEvent.eventAuxiliary().luminosityBlock();
	       eventTree = iEvent.eventAuxiliary().event();

	       cout <<" esb sample qcd 1" <<endl;
		   
	       
	       etaTree = fabs(jets.at(lowBTagTreePosition).eta());
	       cosTree = fCosThetaLJ;
	       topMassTree = top.mass();
	       mtwMassTree = MTWValueQCD;
	       chargeTree = leptonsCharge->at(0) ; 
	       

	       cout <<" esb sample qcd 2" <<endl;


	       lepPt = leptonsQCD.at(0).pt();
	       lepEta = leptonsQCD.at(0).eta();
	       lepPhi = leptonsQCD.at(0).phi();


	       cout <<" esb sample qcd 3" <<endl;
	       
	       bJetPt = jets.at(highBTagTreePosition).pt();
	       bJetE = jets.at(highBTagTreePosition).energy();
	       bJetEta = jets.at(highBTagTreePosition).eta();
	       bJetPhi = jets.at(highBTagTreePosition).phi();
	       
	       cout <<" esb sample qcd 4" <<endl;


	       fJetPt = jets.at(lowBTagTreePosition).pt();
	       fJetE = jets.at(lowBTagTreePosition).energy();
	       fJetEta = jets.at(lowBTagTreePosition).eta();
	       fJetPhi = jets.at(lowBTagTreePosition).phi();
	     }

	     cout <<" esb sample qcd 5" <<endl;

	     bWeightTree= b_weight_sample_ESB;
	     weightTree = Weight*bWeightTree*turnOnWeightValue ;
	     
	     //	   lowBTagTree = lowest
	     //topPt = top.pt();
	     //topE = top.energy();
	     //topEta = top.eta();
	     //topPhi = top.phi();
	     
	     //	   totalEnergy = (top+jets.at(lowBTagTreePosition)).energy();
	     //	   totalMomentum = (top+jets.at(lowBTagTreePosition)).P();
	     
	     //	   metPt = mePPt->at(0);
	     //	   metPhi = METPhi->at(0);
	     
	     //	   metPhi = METPhi->at(0);
	     
	     treesESBQCD[syst_name]->Fill();
	     
	     
	   
	 }
       
     
	 
	 if( lowBTagTreePosition > -1 && highBTagTreePosition > -1) {
	   if(highBTagTreePosition != lowBTagTreePosition){
	     
	     	     
	   
	     //Sample B QCD:
	     if(doBScan_ && antibjets.size()==1 && bjets.size()==0){
		
	       if(syst=="noSyst") passesQCDSampleB = true;

	    
	       if(is_btag_relevant || !passesQCDSampleB){
		 b_weight_sample_B = b_tchpt_sample_B.weight(jsfshpt,ntchpt_tags);
		 b_weight_sample_B*= b_tchel_sample_B.weight(jsfshel,ntche_tags);
		 if(syst_name == "noSyst"){
		   b_weight_sample_B_noSyst = b_weight_sample_B;  
		 }
	       }
	       if(!is_btag_relevant && passesQCDSampleB){
		 //  b_weight_signal_region = b_weight_signal_region_noSyst;
		 // b_weight_sample_A  = b_weight_sample_A_noSyst; 
		 b_weight_sample_B = b_weight_sample_B_noSyst;  
	       }	   
	       
	       cout <<" b sample qcd " <<endl;


		 math::PtEtaPhiELorentzVector top = top4Momentum(leptonsQCD.at(0),jets.at(highBTagTreePosition),metPx,metPy);
		 float fCosThetaLJ =  cosThetaLJ(leptonsQCD.at(0),jets.at(lowBTagTreePosition),top);
		 
		 runTree = iEvent.eventAuxiliary().run();
		 lumiTree = iEvent.eventAuxiliary().luminosityBlock();
		 eventTree = iEvent.eventAuxiliary().event();
		 bWeightTree= b_weight_sample_B;

		 weightTree = bWeightTree*turnOnWeightValue*Weight;
		 //		 weightTree = bWeightTree*Weight;

		 lepPt = leptonsQCD.at(0).pt();
		 lepEta = leptonsQCD.at(0).eta();
		 lepPhi = leptonsQCD.at(0).phi();
		 
		 bJetPt = jets.at(highBTagTreePosition).pt();
		 bJetE = jets.at(highBTagTreePosition).energy();
		 bJetEta = jets.at(highBTagTreePosition).eta();
		 bJetPhi = jets.at(highBTagTreePosition).phi();
		 
		 fJetPt = jets.at(lowBTagTreePosition).pt();
		 fJetE = jets.at(lowBTagTreePosition).energy();
		 fJetEta = jets.at(lowBTagTreePosition).eta();
		 fJetPhi = jets.at(lowBTagTreePosition).phi();
		 

		 etaTree = fabs(jets.at(lowBTagTreePosition).eta());
		 etaTree2 = fabs(jets.at(highBTagTreePosition).eta());
		 cosTree = fCosThetaLJ;
		 topMassTree = top.mass();
		 mtwMassTree = MTWValueQCD;
		 chargeTree = leptonsCharge->at(0);
		 treesScanQCD[syst_name]->Fill();            
	     }
	     
	     //WSample QCD
	     if (antibjets.size()==2 ){ 
	       
	       if(syst=="noSyst") passesQCDSampleA = true;


	       if(is_btag_relevant || !passesQCDSampleA){
		 b_weight_sample_A = b_tchel_sample_A.weight(jsfshel,ntche_tags);
		 if(syst_name == "noSyst"){
		   b_weight_sample_A_noSyst  =     b_weight_sample_A; 
		 }
	       }
	       if(!is_btag_relevant && passesQCDSampleA){
		 //		 b_weight_signal_region = b_weight_signal_region_noSyst;
		 b_weight_sample_A  = b_weight_sample_A_noSyst; 
		 //		 b_weight_sample_B = b_weight_sample_B_noSyst;  
	       }

	       int positionHigh = highBTagTreePosition;
	       int positionLow = lowBTagTreePosition;
	       
	       if(mode_=="pt"){
		 positionHigh = maxPtTreePosition;
		 positionLow = minPtTreePosition;
	       }
	       
	       cout <<" w sample qcd" <<endl;


	       math::PtEtaPhiELorentzVector top = top4Momentum(leptonsQCD.at(0),jets.at(positionHigh),metPx,metPy);
	       float fCosThetaLJ =  cosThetaLJ(leptonsQCD.at(0),jets.at(positionLow),top);
	       
	       runTree = iEvent.eventAuxiliary().run();
	       lumiTree = iEvent.eventAuxiliary().luminosityBlock();
	       eventTree = iEvent.eventAuxiliary().event();

	       bWeightTree= b_weight_sample_A;
	       
	       weightTree = bWeightTree*turnOnWeightValue*Weight;
	       //weightTree = Weight * bWeightTree;
	       //      bWeightTree = b_weight_antitag_algo2.at(0) * b_weight_antitag_algo2.at(1);
	       //      weightTree = Weight * b_weight_antitag_algo2.at(0) * b_weight_antitag_algo2.at(1);

	       cosTree = fCosThetaLJ;
	       topMassTree = top.mass();
	       mtwMassTree = MTWValue;
	       chargeTree = leptonsCharge->at(0);
	       
	       lepPt = leptonsQCD.at(0).pt();
	       lepEta = leptonsQCD.at(0).eta();
	       lepPhi = leptonsQCD.at(0).phi();
	       
	       topPt = top.pt();
	       topE = top.energy();
	       topEta = top.eta();
	       topPhi = top.phi();
	       
	       //       metPt = METPt->at(0);
	       //metPhi = METPhi->at(0);
	       
	       topMassTree = top.mass();

	       //math::PtEtaPhiELorentzVector top2 = top4Momentum(leptonsQCD.at(0),jets.at(positionLow),metPx,metPy);
	       //topMassLowBTagTree = top2.mass();

	       //if(fabs(topMassLowBTagTree - topMassMeas) > fabs(topMassTree - topMassMeas) ) topMassBestTopTree = topMassTree;
	       //else topMassBestTopTree = topMassLowBTagTree;
	       topMassLowBTagTree = topMassTree;
	       topMassBestTopTree = topMassTree;
	       
	       
	       mtwMassTree = MTWValueQCD;
	       
	       //Mode - dependent part


	       etaTree = fabs(jets.at(positionLow).eta());
	       etaTree2 = fabs(jets.at(positionHigh).eta());
	       
	       bJetPt = jets.at(positionHigh).pt();
	       bJetE = jets.at(positionHigh).energy();
	       bJetEta = jets.at(positionHigh).eta();
	       bJetPhi = jets.at(positionHigh).phi();
	       fJetPt = jets.at(positionLow).pt();
	       fJetE = jets.at(positionLow).energy();
	       fJetEta = jets.at(positionLow).eta();
	       fJetPhi = jets.at(positionLow).phi();
	       
		       //	       totalEnergy = (top+jets.at(positionLow)).energy();
	       //	       totalMomentum = (top+jets.at(positionLow)).P();
		 
	       //
	       
	       
	       
	       treesWSampleQCD[syst_name]->Fill();
	     }
	   }
	   }
       }
     }
     
     
     //Non-qcd lepton requirement:
     if(leptons.size()!=1)continue;
     
     //MTW Definition
     metPt = sqrt(metPx*metPx+metPy*metPy);
     MTWValue =  sqrt((leptons.at(0).pt()+metPt)*(leptons.at(0).pt()+metPt)  -(leptons.at(0).px()+metPx)*(leptons.at(0).px()+metPx) -(leptons.at(0).py()+metPy)*(leptons.at(0).py()+metPy));
     
     if(!gotLooseLeptons){
       iEvent.getByLabel(looseElectronsRelIso_,looseElectronsRelIso);
       iEvent.getByLabel(looseMuonsRelIso_,looseMuonsRelIso);     
       gotLooseLeptons = true;
     }
     if( (leptons.size() == 1 && (looseMuonsRelIso->size( )+ looseElectronsRelIso->size())>1))   continue;//Loose muons size always >=1 due to presence of tight muon 
     
     //Signal sample
     if( jets.size()!=2)continue;
     
     if( bjets.size()==1 ){
       
       if(syst=="noSyst") passesSignal = true;
       
       if(is_btag_relevant || !passesSignal){
	 b_weight_signal_region = b_tchpt_signal_region.weight(jsfshpt,ntchpt_tags);
	 if(syst_name == "noSyst"){
	   b_weight_signal_region_noSyst = b_weight_signal_region;
	 }
       }
       if(!is_btag_relevant && passesSignal  ){
	 b_weight_signal_region = b_weight_signal_region_noSyst;
	 // b_weight_sample_A  = b_weight_sample_A_noSyst; 
	 //b_weight_sample_B = b_weight_sample_B_noSyst;  
       }

       cout <<" s sample " <<endl;


       math::PtEtaPhiELorentzVector top = top4Momentum(leptons.at(0),bjets.at(0),metPx,metPy);
       //float fCosThetaLJ =  cosThetaLJ(leptons.at(0), antibjets.at(0), top);
       
       float fCosThetaLJ =  cosThetaLJ(leptons.at(0), jets.at(lowBTagTreePosition), top);
       
       //       lowBTagTreePosition
       //       cout << " Signal Sample ; antib  algo 2 weight size "<< b_weight_antitag_algo2.size()<< " b algo 1 weight size "<< b_weight_tag_algo1.size()<< endl;



       runTree = iEvent.eventAuxiliary().run();
       lumiTree = iEvent.eventAuxiliary().luminosityBlock();
       eventTree = iEvent.eventAuxiliary().event();

       bWeightTree = b_weight_signal_region ;
       weightTree = Weight*bWeightTree* turnOnWeightValue;
       
       etaTree = fabs(jets.at(lowBTagTreePosition).eta());
       cosTree = fCosThetaLJ;
       topMassTree = top.mass();
       mtwMassTree = MTWValue;
       chargeTree = leptonsCharge->at(0) ; 
       
       lepPt = leptons.at(0).pt();
       lepEta = leptons.at(0).eta();
       lepPhi = leptons.at(0).phi();
       
      bJetPt = bjets.at(0).pt();
      bJetE = bjets.at(0).energy();
      bJetEta = bjets.at(0).eta();
      bJetPhi = bjets.at(0).phi();

      //fJetPt = antibjets.at(0).pt();
      //fJetE = antibjets.at(0).energy();
      //fJetEta = antibjets.at(0).eta();
      //fJetPhi = antibjets.at(0).phi();

      
      fJetPt = jets.at(lowBTagTreePosition).pt();
      fJetE = jets.at(lowBTagTreePosition).energy();
      fJetEta = jets.at(lowBTagTreePosition).eta();
      fJetPhi = jets.at(lowBTagTreePosition).phi();

      
      
      topPt = top.pt();
      topE = top.energy();
      topEta = top.eta();
      topPhi = top.phi();
      
      totalEnergy = (top+jets.at(lowBTagTreePosition)).energy();
      totalMomentum = (top+jets.at(lowBTagTreePosition)).P();
      
      //      metPt = METPt->at(0);
      //      metPhi = METPhi->at(0);
      
      trees[syst_name]->Fill();

      //      cout << " b weight size " << b_weight_tag_algo1.size()<< " anti b weight size " <<  b_weight_antitag_algo2.size()<< endl;
      
      cout << " passes cuts pre-mtw, syst " << syst_name << " top mass "<< top.mass() << " cosTheta* "<< fCosThetaLJ << " fjetEta " << fabs(jets.at(lowBTagTreePosition).eta()) << " Weight "  << Weight << " B Weight "<<bTagWeight << " b weight 2 test"<< bWeightTree  <<endl;
      
     }
     
     if( ntchpm_tags>=1 && ntchpt_tags ==0){
       
       if(syst=="noSyst") passesESB = true;
       //cout << " Signal Sample QCD; antib  algo 2 weight size "<< b_weight_antitag_algo2.size()<< " b algo 1 weight size "<< b_weight_tag_algo1.size()<< endl;
       if(is_btag_relevant || !passesESB){
	 b_weight_sample_ESB = b_tchpm_sample_ESB.weight(jsfshpm,ntchpm_tags);
	 b_weight_sample_ESB *= b_tchpt_sample_ESB.weight(jsfshpt,ntchpt_tags);
	 if(syst_name == "noSyst"){
	   b_weight_sample_ESB_noSyst = b_weight_sample_ESB;
	 }
       }
       
       if(!is_btag_relevant && passesESB){
	 b_weight_sample_ESB = b_weight_sample_ESB_noSyst;
	 //	     b_weight_sample_A  = b_weight_sample_A_noSyst; 
	 // b_weight_sample_B = b_weight_sample_B_noSyst;  
       }	   
       
       cout <<" esb sample" <<endl;
       
       if(ntchpt_tags != 1){
	 math::PtEtaPhiELorentzVector top = top4Momentum(leptons.at(0),jets.at(highBTagTreePosition),metPx,metPy);
	 float fCosThetaLJ =  cosThetaLJ(leptons.at(0), jets.at(lowBTagTreePosition), top);
	 
	 runTree = iEvent.eventAuxiliary().run();
	 lumiTree = iEvent.eventAuxiliary().luminosityBlock();
	 eventTree = iEvent.eventAuxiliary().event();
	 
	 etaTree = fabs(jets.at(lowBTagTreePosition).eta());
	 cosTree = fCosThetaLJ;
	 topMassTree = top.mass();
	 mtwMassTree = MTWValue;
	 chargeTree = leptonsCharge->at(0) ; 
	 
	 lepPt = leptons.at(0).pt();
	 lepEta = leptons.at(0).eta();
	 lepPhi = leptons.at(0).phi();
	 
	 bJetPt = jets.at(highBTagTreePosition).pt();
	 bJetE = jets.at(highBTagTreePosition).energy();
	 bJetEta = jets.at(highBTagTreePosition).eta();
	 bJetPhi = jets.at(highBTagTreePosition).phi();
	 
	 fJetPt = jets.at(lowBTagTreePosition).pt();
	 fJetE = jets.at(lowBTagTreePosition).energy();
	 fJetEta = jets.at(lowBTagTreePosition).eta();
	 fJetPhi = jets.at(lowBTagTreePosition).phi();
       }
       
       bWeightTree= b_weight_sample_ESB;
       weightTree = Weight*bWeightTree*turnOnWeightValue ;
       
	     
       //	   lowBTagTree = lowest
       
       //topPt = top.pt();
       //topE = top.energy();
       //topEta = top.eta();
       //topPhi = top.phi();
       
       //	   totalEnergy = (top+jets.at(lowBTagTreePosition)).energy();
       //	   totalMomentum = (top+jets.at(lowBTagTreePosition)).P();
       
       //	   metPt = mePPt->at(0);
       //	   metPhi = METPhi->at(0);
       
       //	   metPhi = METPhi->at(0);
       
       treesESB[syst_name]->Fill();
       
       
       
     }
 
     if( lowBTagTreePosition > -1 && highBTagTreePosition > -1 ){
      if(highBTagTreePosition != lowBTagTreePosition){
	
	//Sample B
	if(doBScan_ && antibjets.size()==1 && bjets.size()==0){
	  

	  if(syst=="noSyst") passesSampleB = true;

	  if(is_btag_relevant || !passesSampleB){
	    b_weight_sample_B = b_tchpt_sample_B.weight(jsfshpt,ntchpt_tags);
	    b_weight_sample_B*= b_tchel_sample_B.weight(jsfshel,ntche_tags);
	    if(syst_name == "noSyst"){
	      b_weight_sample_B_noSyst =     b_weight_sample_B;  
	    }
	  }
	    if(!is_btag_relevant){
	      //	      b_weight_signal_region = b_weight_signal_region_noSyst;
	      //	      b_weight_sample_A  = b_weight_sample_A_noSyst; 
	      b_weight_sample_B = b_weight_sample_B_noSyst;  
	    }	   

	    cout <<" b sample " <<endl;

	    math::PtEtaPhiELorentzVector top = top4Momentum(leptons.at(0),jets.at(highBTagTreePosition),metPx,metPy);
	    float fCosThetaLJ =  cosThetaLJ(leptons.at(0),jets.at(lowBTagTreePosition),top);
	
	    
	    //cout << " Sample B Iso; antib weight size algo 2 "<< b_weight_antitag_algo2.size()<< " b weight size algo 2 "<< b_weight_tag_algo2.size()<<  " antib weight size algo 1" << b_weight_antitag_algo1.size()<<endl;	

	    runTree = iEvent.eventAuxiliary().run();
	    lumiTree = iEvent.eventAuxiliary().luminosityBlock();
	    eventTree = iEvent.eventAuxiliary().event();

	    
	    weightTree = bWeightTree*turnOnWeightValue*Weight;
	    bWeightTree = b_weight_sample_B;
	    //	    weightTree = bWeightTree*Weight;
	    
	    etaTree = fabs(jets.at(lowBTagTreePosition).eta());
	    etaTree2 = fabs(jets.at(highBTagTreePosition).eta());
		 cosTree = fCosThetaLJ;
		 topMassTree = top.mass();
		 mtwMassTree = MTWValue;
		 
		 //	    metPt = METPt->at(0);
		 
		 fJetPt = jets.at(lowBTagTreePosition).pt();
		 bJetPt = jets.at(highBTagTreePosition).pt();
		 
		 chargeTree = leptonsCharge->at(0);
		 treesScan[syst_name]->Fill();            
		 
	}
	//W Sample

	if (antibjets.size()==2 ){ 

	  if(syst=="noSyst") passesSampleA = true;


	  if(is_btag_relevant || !passesSampleA){
	    b_weight_sample_A = b_tchel_sample_A.weight(jsfshel,ntche_tags);
	    if(syst_name == "noSyst"){
	      b_weight_sample_A_noSyst  =     b_weight_sample_A; 
	    }
	  }
	  if(!is_btag_relevant && passesSampleA){
	    // b_weight_signal_region = b_weight_signal_region_noSyst;
	    b_weight_sample_A  = b_weight_sample_A_noSyst; 
	    // b_weight_sample_B = b_weight_sample_B_noSyst;  
	  }	   

	  //if(bjets.size()==0 ){
	  
	  //	  cout << "W Sample Iso; antib weight size algo 1 "<< b_weight_antitag_algo1.size() <<" number 0 "<< b_weight_antitag_algo1.at(0) <<" number 1 "<< b_weight_antitag_algo1.at(1) <<endl;
	  
	  cout <<" w sample " <<endl;

	  int positionHigh = highBTagTreePosition;
	  int positionLow = lowBTagTreePosition;
	  
	  if(mode_=="pt"){
	    positionHigh = maxPtTreePosition;
	    positionLow = minPtTreePosition;
	  }
	  
	  math::PtEtaPhiELorentzVector top = top4Momentum(leptons.at(0),jets.at(positionHigh),metPx,metPy);
	  float fCosThetaLJ =  cosThetaLJ(leptons.at(0),jets.at(positionLow),top);
	  
	  runTree = iEvent.eventAuxiliary().run();
	  lumiTree = iEvent.eventAuxiliary().luminosityBlock();
	  eventTree = iEvent.eventAuxiliary().event();
	  
	  bWeightTree = b_weight_sample_A;
	  //	  weightTree = Weight*b_weight_sample_A;
	  weightTree = bWeightTree*turnOnWeightValue*Weight;

	  cosTree = fCosThetaLJ;
	  topMassTree = top.mass();
	  
	  //	  math::PtEtaPhiELorentzVector top2 = top4Momentum(leptons.at(0),jets.at(positionLow),metPx,metPy);
	  //	  topMassLowBTagTree = top2.mass();
	  
	  //	  if(fabs(topMassLowBTagTree - topMassMeas) > fabs(topMassTree - topMassMeas) ) topMassBestTopTree = topMassTree;
	  //	  else topMassBestTopTree = topMassLowBTagTree;
	  
	  topMassLowBTagTree = topMassTree;
	  topMassBestTopTree = topMassTree;
	  
	  
	  mtwMassTree = MTWValue;
	  chargeTree = leptonsCharge->at(0);
	  
	  lepPt = leptons.at(0).pt();
	  lepEta = leptons.at(0).eta();
	  lepPhi = leptons.at(0).phi();


	  //Mode - dependent part

	  etaTree = fabs(jets.at(positionLow).eta());
	  etaTree2 = fabs(jets.at(positionHigh).eta());
	  
	  bJetPt = jets.at(positionHigh).pt();
	  bJetE = jets.at(positionHigh).energy();
	  bJetEta = jets.at(positionHigh).eta();
	  bJetPhi = jets.at(positionHigh).phi();
	  
	  fJetPt = jets.at(positionLow).pt();
	  fJetE = jets.at(positionLow).energy();
	  fJetEta = jets.at(positionLow).eta();
	  fJetPhi = jets.at(positionLow).phi();
	  
	  //totalEnergy = (top+jets.at(positionLow)).energy();
	  //totalMomentum = (top+jets.at(positionLow)).P();
	  //
	  
	  topPt = top.pt();
	  topE = top.energy();
	  topEta = top.eta();
	  topPhi = top.phi();
	  
	  
	  //	  metPt = METPt->at(0);
	  //metPhi = METPhi->at(0);
	  

	  treesWSample[syst_name]->Fill();
	}
      }
    }
  }
}
																					
//CosThetalj given top quark, lepton and light jet
float SingleTopSystematicsTreesDumper::cosThetaLJ(math::PtEtaPhiELorentzVector lepton, math::PtEtaPhiELorentzVector jet, math::PtEtaPhiELorentzVector top){
  
  math::PtEtaPhiELorentzVector boostedLepton = ROOT::Math::VectorUtil::boost(lepton,top.BoostToCM());
  math::PtEtaPhiELorentzVector boostedJet = ROOT::Math::VectorUtil::boost(jet,top.BoostToCM());

  return  ROOT::Math::VectorUtil::CosTheta(boostedJet.Vect(),boostedLepton.Vect());
  
}

//top quark 4-momentum given lepton, met and b-jet
math::PtEtaPhiELorentzVector SingleTopSystematicsTreesDumper::top4Momentum(math::PtEtaPhiELorentzVector lepton, math::PtEtaPhiELorentzVector jet, float metPx, float metPy){
  return top4Momentum(lepton.px(),lepton.py(),lepton.pz(),lepton.energy(),jet.px(),jet.py(),jet.pz(),jet.energy(),metPx,metPy);
}

//top quark 4-momentum original function given the necessary parameters 
math::PtEtaPhiELorentzVector SingleTopSystematicsTreesDumper::top4Momentum(float leptonPx, float leptonPy, float leptonPz, float leptonE, float jetPx, float jetPy, float jetPz,float jetE, float metPx, float metPy){
  float lepton_Pt = sqrt( (leptonPx*leptonPx)+  (leptonPy*leptonPy) );
  
  math::XYZTLorentzVector neutrino = NuMomentum(leptonPx,leptonPy,leptonPz,lepton_Pt,leptonE,metPx,metPy);//.at(0);;
    
  math::XYZTLorentzVector lep(leptonPx,leptonPy,leptonPz,leptonE);
  math::XYZTLorentzVector jet(jetPx,jetPy,jetPz,jetE);
  
  math::XYZTLorentzVector top = lep + jet + neutrino;
  return math::PtEtaPhiELorentzVector(top.pt(),top.eta(),top.phi(),top.E());  
}

//top neutrino 4-momentum function given the parameters
//In brief: 
//Works for top->1l+1neutrino+1bjet
//Assuming all met comes from neutrino
/////What it does:
//w boson mass put to pdg value
//obtained neutrino pz from kinematics
//We get a second order equation 
/////In case of two positive Delta solutions:
//we choose solution with minimum |pz|
/////In case of two negative Delta solutions:
//in such case: mtw > mw
//To solve this: put mtw = mw 
//Solve the equations
//In this way we must
//drop the constraints px_Nu = MET_x and py_Nu = MET_y
//Solve this by chosing the px_Nu and py_Nu that 
//minimize the distance from the MET in the px-py plane
//Such minimization can be done analytically with derivatives
//and much patience. Here we exploit such analytical minimization
/////
//More detailed inline description: work in progress! 
math::XYZTLorentzVector SingleTopSystematicsTreesDumper::NuMomentum(float leptonPx, float leptonPy, float leptonPz, float leptonPt, float leptonE, float metPx, float metPy ){

  double  mW = 80.399;
  
  math::XYZTLorentzVector result;
  
  //  double Wmt = sqrt(pow(Lepton.et()+MET.pt(),2) - pow(Lepton.px()+metPx,2) - pow(leptonPy+metPy,2) );
    
  double MisET2 = (metPx*metPx + metPy*metPy);
  double mu = (mW*mW)/2 + metPx*leptonPx + metPy*leptonPy;
  double a  = (mu*leptonPz)/(leptonE*leptonE - leptonPz*leptonPz);
  double a2 = TMath::Power(a,2);
  double b  = (TMath::Power(leptonE,2.)*(MisET2) - TMath::Power(mu,2.))/(TMath::Power(leptonE,2) - TMath::Power(leptonPz,2));
  double pz1(0),pz2(0),pznu(0);
  int nNuSol(0);

  math::XYZTLorentzVector p4nu_rec;
  math::XYZTLorentzVector p4W_rec;
  math::XYZTLorentzVector p4b_rec;
  math::XYZTLorentzVector p4Top_rec;
  math::XYZTLorentzVector p4lep_rec;    
  
  p4lep_rec.SetPxPyPzE(leptonPx,leptonPy,leptonPz,leptonE);
  
  math::XYZTLorentzVector p40_rec(0,0,0,0);
  
  if(a2-b > 0 ){
    //if(!usePositiveDeltaSolutions_)
    //  {
    //	result.push_back(p40_rec);
    //	return result;
    //	}
    double root = sqrt(a2-b);
    pz1 = a + root;
    pz2 = a - root;
    nNuSol = 2;     
    
    //    if(usePzPlusSolutions_)pznu = pz1;    
    //    if(usePzMinusSolutions_)pznu = pz2;
    //if(usePzAbsValMinimumSolutions_){
    pznu = pz1;
    if(fabs(pz1)>fabs(pz2)) pznu = pz2;
    //}
    
    
    double Enu = sqrt(MisET2 + pznu*pznu);
    
    p4nu_rec.SetPxPyPzE(metPx, metPy, pznu, Enu);
    
    //    result =.push_back(p4nu_rec);
    result = p4nu_rec;
    
  }
  else{
    
    // if(!useNegativeDeltaSolutions_){
    //result.push_back(p40_rec);
    //  return result;
    //    }
    //    double xprime = sqrt(mW;
    

      double ptlep = leptonPt,pxlep=leptonPx,pylep=leptonPy,metpx=metPx,metpy=metPy;
      
      double EquationA = 1;
      double EquationB = -3*pylep*mW/(ptlep);
      double EquationC = mW*mW*(2*pylep*pylep)/(ptlep*ptlep)+mW*mW-4*pxlep*pxlep*pxlep*metpx/(ptlep*ptlep)-4*pxlep*pxlep*pylep*metpy/(ptlep*ptlep);
      double EquationD = 4*pxlep*pxlep*mW*metpy/(ptlep)-pylep*mW*mW*mW/ptlep;
      
      std::vector<long double> solutions = EquationSolve<long double>((long double)EquationA,(long double)EquationB,(long double)EquationC,(long double)EquationD);
      
      std::vector<long double> solutions2 = EquationSolve<long double>((long double)EquationA,-(long double)EquationB,(long double)EquationC,-(long double)EquationD);
      
      
      double deltaMin = 14000*14000;
      double zeroValue = -mW*mW/(4*pxlep); 
      double minPx=0;
      double minPy=0;
      
      //    std::cout<<"a "<<EquationA << " b " << EquationB  <<" c "<< EquationC <<" d "<< EquationD << std::endl; 
      
   //  if(usePxMinusSolutions_){
	for( int i =0; i< (int)solutions.size();++i){
	  if(solutions[i]<0 ) continue;
	  double p_x = (solutions[i]*solutions[i]-mW*mW)/(4*pxlep); 
	  double p_y = ( mW*mW*pylep + 2*pxlep*pylep*p_x -mW*ptlep*solutions[i])/(2*pxlep*pxlep);
	  double Delta2 = (p_x-metpx)*(p_x-metpx)+(p_y-metpy)*(p_y-metpy); 
	  
      //      std::cout<<"intermediate solution1 met x "<<metpx << " min px " << p_x  <<" met y "<<metpy <<" min py "<< p_y << std::endl; 

      if(Delta2< deltaMin && Delta2 > 0){deltaMin = Delta2;
      minPx=p_x;
      minPy=p_y;}
      //     std::cout<<"solution1 met x "<<metpx << " min px " << minPx  <<" met y "<<metpy <<" min py "<< minPy << std::endl; 
      }
	
	//    } 
	
	//if(usePxPlusSolutions_){
      for( int i =0; i< (int)solutions2.size();++i){
	if(solutions2[i]<0 ) continue;
	double p_x = (solutions2[i]*solutions2[i]-mW*mW)/(4*pxlep); 
	double p_y = ( mW*mW*pylep + 2*pxlep*pylep*p_x +mW*ptlep*solutions2[i])/(2*pxlep*pxlep);
	double Delta2 = (p_x-metpx)*(p_x-metpx)+(p_y-metpy)*(p_y-metpy); 
	//  std::cout<<"intermediate solution2 met x "<<metpx << " min px " << minPx  <<" met y "<<metpy <<" min py "<< minPy << std::endl; 
	if(Delta2< deltaMin && Delta2 > 0){deltaMin = Delta2;
	  minPx=p_x;
	  minPy=p_y;}
	//	std::cout<<"solution2 met x "<<metpx << " min px " << minPx  <<" met y "<<metpy <<" min py "<< minPy << std::endl; 
      }
      //}
  
    double pyZeroValue= ( mW*mW*pxlep + 2*pxlep*pylep*zeroValue);
    double delta2ZeroValue= (zeroValue-metpx)*(zeroValue-metpx) + (pyZeroValue-metpy)*(pyZeroValue-metpy);
    
    if(deltaMin==14000*14000)return result;    
    //    else std::cout << " test " << std::endl;

    if(delta2ZeroValue < deltaMin){
      deltaMin = delta2ZeroValue;
      minPx=zeroValue;
      minPy=pyZeroValue;}
  
    //    std::cout<<" MtW2 from min py and min px "<< sqrt((minPy*minPy+minPx*minPx))*ptlep*2 -2*(pxlep*minPx + pylep*minPy)  <<std::endl;
    ///    ////Y part   

    double mu_Minimum = (mW*mW)/2 + minPx*pxlep + minPy*pylep;
    double a_Minimum  = (mu_Minimum*leptonPz)/(leptonE*leptonE - leptonPz*leptonPz);
    pznu = a_Minimum;
  
    //if(!useMetForNegativeSolutions_){
      double Enu = sqrt(minPx*minPx+minPy*minPy + pznu*pznu);
      p4nu_rec.SetPxPyPzE(minPx, minPy, pznu , Enu);
  
      //    }
      //    else{
      //      pznu = a;
      //      double Enu = sqrt(metpx*metpx+metpy*metpy + pznu*pznu);
      //      p4nu_rec.SetPxPyPzE(metpx, metpy, pznu , Enu);
      //    }
    
      //      result.push_back(p4nu_rec);
      result = p4nu_rec;
  }
  return result;    
}

//JES uncertainty as a function of pt, eta and jet flavour 
double SingleTopSystematicsTreesDumper::jetUncertainty(double eta, double ptCorr, int flavour){
  jecUnc->setJetEta(eta); 
  jecUnc->setJetPt(ptCorr);
  double JetCorrection = jecUnc->getUncertainty(true); // In principle, boolean controls if uncertainty on +ve or -ve side is returned (asymmetric errors) but not yet implemented.
  bool cut = ptCorr> 50 && ptCorr < 200 && fabs(eta) < 2.0;
  JES_SW = 0.015;                                                                                                                                 
  double JES_PU=0.75*0.8*2.2/ptCorr;
  //  double JES_PU=0.; //We are using pfNoPU must understand what value to put there
  double JES_b=0;
  if(abs(flavour)==5){
    if(cut) JES_b = JES_b_cut;
    else JES_b = JES_b_overCut;
  }
  //    float JESUncertaintyTmp = sqrt(JESUncertainty*JESUncertainty + JetCorrection*JetCorrection);                                                 
  //  return sqrt(JES_b*JES_b + JES_PU*JES_PU +JES_SW*JES_SW + JetCorrection*JetCorrection);
  return JetCorrection;
}

//EndJob filling rate systematics trees
void SingleTopSystematicsTreesDumper::endJob(){
  
  //part for rate systematics

  for(size_t i = 0; i < rate_systematics.size();++i){
    string syst = rate_systematics[i];
    string treename = (channel+"_"+syst);

    cout<< " endjob"  << syst<< " 0 "<<endl;
    
    trees[syst]->CopyAddresses(trees["noSyst"]);
    treesWSample[syst]->CopyAddresses(treesWSample["noSyst"]);

    trees[syst]->CopyEntries(trees["noSyst"]); 
    treesWSample[syst]->CopyEntries(trees["noSyst"]); 
    

        cout<< " endjob"  << syst<< " 1 "<<endl;

    /*  for(size_t step = 0; step < bScanSteps;++step){
      treesScan[syst]->CopyAddresses(treesScan["noSyst"]); 
      treesScan[syst]->CopyEntries(treesScan["noSyst"]); 
    }
    */
    
    //modify the weight by a constant factor    
    double tmpWeight = 0;
    double weightSF = 1.;
    
    TBranch * b = trees["noSyst"]->GetBranch("weight");
    int entries = b->GetEntries();
    b->SetAddress(&tmpWeight);    


    cout<< " endjob"  << syst<< " 2 "<<endl;
    
    trees[syst]->GetBranch("weight")->Reset();
    trees[syst]->GetBranch("weight")->SetAddress(&tmpWeight);
    

    cout<< " endjob"  << syst<< " 3 "<<endl;
    
    for(int t =0; t < entries ; ++t){
      b->GetEntry(t);
      tmpWeight*=weightSF;
      trees[syst]->GetBranch("weight")->Fill();
      
    }
    

    
    b->SetAddress(&weightTree);
    trees[syst]->GetBranch("weight")->SetAddress(&weightTree);
    

    
    //    cout<< " syst "<< syst<< " weights entries "<<  entries <<endl;

  }
}
  
//B-C weight as function of jet flavour, systematics and scale factors: 
//WILL BE CHANGED VERY SOON ACCORDING TO NEW PRESCRIPTIONS 
double SingleTopSystematicsTreesDumper::BScaleFactor(string algo,string syst_name){
  
  double bcentral =0.9;  
  double berr = 0.15*bcentral;
  double cerr =0.3*bcentral;
  double tcheeff =0.7;
  
  if(syst_name == "BTagUp"){
    if(algo == "TCHP_B"){
      return bcentral+berr;
    }
    if(algo == "TCHP_C"){
      return bcentral+cerr;
    }
    
    if(algo == "TCHEL_B"){
      return bcentral+berr;
    }
    
    if(algo == "TCHEL_C"){
      return bcentral+cerr;
    }
    
  }
  
  if(syst_name == "BTagDown"){
    if(algo == "TCHP_B"){
      return bcentral-berr;
    }
    if(algo == "TCHP_C"){
      return bcentral-cerr;
    }
  
    if(algo == "TCHEL_B"){
      return bcentral-berr;
    }
    if(algo == "TCHEL_C"){
      return bcentral-berr;
    }
  }

  if(algo == "TCHP_B"){
    return bcentral;
  }
  if(algo == "TCHP_C"){
    return bcentral;
  }
  if(algo == "TCHEL_B"){
    return bcentral;
  }
  if(algo == "TCHEL_C"){
    return bcentral;
  }
    
  return 0.9;
}

//EventScaleFactor Scale


double SingleTopSystematicsTreesDumper::EventScaleFactor(string algo,string syst_name){//,double sf, double eff, double sferr){

  //  double mistagcentral = sf;  
  //double mistagerr = sferr;
  //double tcheeff = eff;

  double mistagcentral = SFMap(algo);  
  double mistagerr = SFErrMap(algo);
  double tcheeff = EFFMap(algo);

  
  if(syst_name == "MisTagUp" || syst_name == "BTagUp"){
    return mistagcentral+mistagerr;
  }

  if(syst_name == "MisTagDown" || syst_name == "BTagDown"){
    return mistagcentral-mistagerr;
  }

  return mistagcentral;
}

//EventAntiScaleFactor

double SingleTopSystematicsTreesDumper::EventAntiScaleFactor(string algo,string syst_name ){
  //,double sf, double eff, double sferr){

  
  //double mistagcentral = sf;  
  //double mistagerr = sferr;
  //double tcheeff = eff;

  double mistagcentral = SFMap(algo);  
  double mistagerr = SFErrMap(algo);
  double tcheeff = EFFMap(algo);

  
  if(syst_name == "MisTagUp" || syst_name == "BTagUp"){
    return (1-tcheeff)/(1-tcheeff/(mistagcentral+mistagerr));
  }
  
  if(syst_name == "MisTagDown" || syst_name == "BTagDown"){
    return (1-tcheeff)/(1-tcheeff/(mistagcentral-mistagerr));
    
  }

  return (1-tcheeff)/(1-tcheeff/(mistagcentral));
  
}


//Mistag weight as function of jet flavour, systematics and scale factors: 
//WILL BE CHANGED VERY SOON ACCORDING TO NEW PRESCRIPTIONS 
double SingleTopSystematicsTreesDumper::MisTagScaleFactor(string algo,string syst_name,double sf, double eff, double sferr){
  double mistagcentral = sf;  
  double mistagerr = sferr;
  double tcheeff = eff;

  
  if(syst_name == "MisTagUp"){
    if(algo == "TCHP_L"){
      return mistagcentral+mistagerr;
    }
    if(algo == "TCHEL_L"){
      return mistagcentral+mistagerr;
    }
    
  }
  
  if(syst_name == "MisTagDown"){
    if(algo == "TCHP_L"){
      return mistagcentral-mistagerr;
    }
    if(algo == "TCHEL_L"){
      return mistagcentral-mistagerr;
    }
  }

  if(algo == "TCHP_L"){
    return mistagcentral;
  }
  if(algo == "TCHEL_L"){
    return mistagcentral;
  }
  
  return 0.9;


}

double SingleTopSystematicsTreesDumper::SFMap(string algo ){
  if(algo == "TCHPT_B")return 0.89;
  if(algo == "TCHPT_C")return 0.89;
  if(algo == "TCHPT_L")return 1.17;

  if(algo == "TCHPM_B")return 0.91;
  if(algo == "TCHPM_C")return 0.91;
  if(algo == "TCHPM_L")return 0.91;

  if(algo == "TCHEL_B")return 0.95;
  if(algo == "TCHEL_C")return 0.95;
  if(algo == "TCHEL_L")return 1.11;


  return 0.9;
}

double SingleTopSystematicsTreesDumper::SFErrMap(string algo ){
  if(algo == "TCHPT_B")return 0.092;
  if(algo == "TCHPT_C")return 0.092;
  if(algo == "TCHPT_L")return 0.18;

  if(algo == "TCHPM_B")return 0.10;
  if(algo == "TCHPM_C")return 0.10;
  if(algo == "TCHPM_L")return 0.11;

  if(algo == "TCHEL_B")return 0.10;
  if(algo == "TCHEL_C")return 0.10;
  if(algo == "TCHEL_L")return 0.11;

  return 0.1;
}

double SingleTopSystematicsTreesDumper::EFFMap(string algo ){
  if(algo == "TCHPT_B")return 0.365;
  if(algo == "TCHPT_C")return 0.365;
  if(algo == "TCHPT_L")return 0.0017;

  if(algo == "TCHEL_B")return 0.765;
  if(algo == "TCHEL_C")return 0.765;
  if(algo == "TCHEL_L")return 0.13;

  if(algo == "TCHPM_B")return 0.48;
  if(algo == "TCHPM_C")return 0.48;
  if(algo == "TCHPM_L")return 0.0177;

  return 0.36;
}



double SingleTopSystematicsTreesDumper::EFFErrMap(string algo ){
  if(algo == "TCHPT_B")return 0.05;
  if(algo == "TCHPT_C")return 0.05;
  if(algo == "TCHPT_L")return 0.0004;

  if(algo == "TCHEL_B")return 0.05;
  if(algo == "TCHEL_C")return 0.05;
  if(algo == "TCHEL_L")return 0.03;

  if(algo == "TCHEL_B")return 0.05;
  if(algo == "TCHEL_C")return 0.05;
  if(algo == "TCHEL_L")return 0.004;

  return 0.05;
}


double SingleTopSystematicsTreesDumper::EventScaleFactorMap(string algo, string syst ){

  
  if( algo== "TCHPT_B" && syst == "BTagUp" )return
    TCHPT_BBTagUp;
  if( algo== "TCHPT_B" && syst == "BTagDown" )return
    TCHPT_BBTagDown;
  if( algo== "TCHPT_C" && syst == "BTagUp" )return
    TCHPT_CBTagUp;
  if( algo== "TCHPT_C" && syst == "BTagDown" )return
    TCHPT_CBTagDown;
  if( algo== "TCHPT_L" && syst == "MisTagUp" )return
    TCHPT_LMisTagUp;
  if( algo== "TCHPT_L" && syst == "MisTagDown" )return
    TCHPT_LMisTagDown;
    
  if( algo== "TCHPT_BAnti" && syst == "BTagUp" )return
    TCHPT_BAntiBTagUp;
  if( algo== "TCHPT_BAnti" && syst == "BTagDown" )return
    TCHPT_BAntiBTagDown;
  if( algo== "TCHPT_BAnti" && syst == "BTagUp" )return
    TCHPT_CAntiBTagUp;
  if( algo== "TCHPT_BAnti" && syst == "BTagDown" )return
    TCHPT_CAntiBTagDown;
  if( algo== "TCHPT_BAnti" && syst == "BTagUp" )return
    TCHPT_LAntiMisTagUp;
  if( algo== "TCHPT_BAnti" && syst == "BTagDown" )return
    TCHPT_LAntiMisTagDown;
  
  if( algo== "TCHPT_B" )return TCHPT_B;
  if( algo== "TCHPT_C" )return TCHPT_C;
  if( algo== "TCHPT_L" )return TCHPT_L;
  
  if( algo== "TCHPT_BAnti" )return   TCHPT_BAnti;
  if( algo== "TCHPT_CAnti" )return   TCHPT_CAnti;
  if( algo== "TCHPT_LAnti" )return   TCHPT_LAnti;


  /////m

  if( algo== "TCHPM_B" && syst == "BTagUp" )return
    TCHPM_BBTagUp;
  if( algo== "TCHPM_B" && syst == "BTagDown" )return
    TCHPM_BBTagDown;
  if( algo== "TCHPM_C" && syst == "BTagUp" )return
    TCHPM_CBTagUp;
  if( algo== "TCHPM_C" && syst == "BTagDown" )return
    TCHPM_CBTagDown;
  if( algo== "TCHPM_L" && syst == "MisTagUp" )return
    TCHPM_LMisTagUp;
  if( algo== "TCHPM_L" && syst == "MisTagDown" )return
    TCHPM_LMisTagDown;
    
  if( algo== "TCHPM_BAnti" && syst == "BTagUp" )return
    TCHPM_BAntiBTagUp;
  if( algo== "TCHPM_BAnti" && syst == "BTagDown" )return
    TCHPM_BAntiBTagDown;
  if( algo== "TCHPM_CAnti" && syst == "BTagUp" )return
    TCHPM_CAntiBTagUp;
  if( algo== "TCHPM_CAnti" && syst == "BTagDown" )return
    TCHPM_CAntiBTagDown;
  if( algo== "TCHPM_LAnti" && syst == "BTagUp" )return
    TCHPM_LAntiMisTagUp;
  if( algo== "TCHPM_LAnti" && syst == "BTagDown" )return
    TCHPM_LAntiMisTagDown;
  
  if( algo== "TCHPM_B" )return TCHPM_B;
  if( algo== "TCHPM_C" )return TCHPM_C;
  if( algo== "TCHPM_L" )return TCHPM_L;
  
  if( algo== "TCHPM_BAnti" )return   TCHPM_BAnti;
  if( algo== "TCHPM_CAnti" )return   TCHPM_CAnti;
  if( algo== "TCHPM_LAnti" )return   TCHPM_LAnti;


  /////m

  if( algo== "TCHEL_B" && syst == "BTagUp" )return
    TCHEL_BBTagUp;
  if( algo== "TCHEL_B" && syst == "BTagDown" )return
    TCHEL_BBTagDown;
  if( algo== "TCHEL_C" && syst == "BTagUp" )return
    TCHEL_CBTagUp;
  if( algo== "TCHEL_C" && syst == "BTagDown" )return
    TCHEL_CBTagDown;
  if( algo== "TCHEL_L" && syst == "MisTagUp" )return
  TCHEL_LMisTagUp;
  if( algo== "TCHEL_L" && syst == "MisTagDown" )return
  TCHEL_LMisTagDown;
    
  if( algo== "TCHEL_BAnti" && syst == "BTagUp" )return
  TCHEL_BAntiBTagUp;
  if( algo== "TCHEL_BAnti" && syst == "BTagDown" )return
  TCHEL_BAntiBTagDown;
  if( algo== "TCHEL_CAnti" && syst == "BTagUp" )return
  TCHEL_CAntiBTagUp;
  if( algo== "TCHEL_CAnti" && syst == "BTagDown" )return
  TCHEL_CAntiBTagDown;
  if( algo== "TCHEL_LAnti" && syst == "BTagUp" )return
  TCHEL_LAntiMisTagUp;
  if( algo== "TCHEL_LAnti" && syst == "BTagDown" )return
  TCHEL_LAntiMisTagDown;

 

  if( algo== "TCHEL_B" )return TCHEL_B;
  if( algo== "TCHEL_C" )return TCHEL_C;
  if( algo== "TCHEL_L" )return TCHEL_L;
    
  if( algo== "TCHEL_BAnti" )return   TCHEL_BAnti;
  if( algo== "TCHEL_CAnti" )return   TCHEL_CAnti;
  if( algo== "TCHEL_LAnti" )return   TCHEL_LAnti;
  
  return 1.;
  
  }


void SingleTopSystematicsTreesDumper::InitializeEventScaleFactorMap(){

    TCHPT_B = EventScaleFactor("TCHPT_B","noSyst");
    TCHPT_C = EventScaleFactor("TCHPT_C","noSyst");
    TCHPT_L = EventScaleFactor("TCHPT_L","noSyst");
    
  
    TCHPT_BBTagUp = EventScaleFactor("TCHPT_B","BTagUp");
    TCHPT_BBTagDown = EventScaleFactor("TCHPT_B","BTagDown");
    TCHPT_CBTagUp = EventScaleFactor("TCHPT_C","BTagUp");
    TCHPT_CBTagDown = EventScaleFactor("TCHPT_C","BTagDown");
    TCHPT_LMisTagUp = EventScaleFactor("TCHPT_L","MisTagUp");
    TCHPT_LMisTagDown = EventScaleFactor("TCHPT_L","MisTagDown");
    

    TCHPT_BAnti = EventAntiScaleFactor("TCHPT_B","noSyst");
    TCHPT_CAnti = EventAntiScaleFactor("TCHPT_C","noSyst");
    TCHPT_LAnti = EventAntiScaleFactor("TCHPT_L","noSyst");

    TCHPT_BAntiBTagUp = EventAntiScaleFactor("TCHPT_B","BTagUp");
    TCHPT_BAntiBTagDown = EventAntiScaleFactor("TCHPT_B","BTagDown");
    TCHPT_CAntiBTagUp = EventAntiScaleFactor("TCHPT_C","BTagUp");
    TCHPT_CAntiBTagDown = EventAntiScaleFactor("TCHPT_C","BTagDown");
    TCHPT_LAntiMisTagUp = EventAntiScaleFactor("TCHPT_L","MisTagUp");
    TCHPT_LAntiMisTagDown = EventAntiScaleFactor("TCHPT_L","MisTagDown");


  //  TCHP_LAntiMisTagDown = EventAntiScaleFactor("TCHP_L","MisTagDown");

    TCHPM_B = EventScaleFactor("TCHPM_B","noSyst");
    TCHPM_C = EventScaleFactor("TCHPM_C","noSyst");
    TCHPM_L = EventScaleFactor("TCHPM_L","noSyst");
    
  
    TCHPM_BBTagUp = EventScaleFactor("TCHPM_B","BTagUp");
    TCHPM_BBTagDown = EventScaleFactor("TCHPM_B","BTagDown");
    TCHPM_CBTagUp = EventScaleFactor("TCHPM_C","BTagUp");
    TCHPM_CBTagDown = EventScaleFactor("TCHPM_C","BTagDown");
    TCHPM_LMisTagUp = EventScaleFactor("TCHPM_L","MisTagUp");
    TCHPM_LMisTagDown = EventScaleFactor("TCHPM_L","MisTagDown");
    

    TCHPM_BAnti = EventAntiScaleFactor("TCHPM_B","noSyst");
    TCHPM_CAnti = EventAntiScaleFactor("TCHPM_C","noSyst");
    TCHPM_LAnti = EventAntiScaleFactor("TCHPM_L","noSyst");

    TCHPM_BAntiBTagUp = EventAntiScaleFactor("TCHPM_B","BTagUp");
    TCHPM_BAntiBTagDown = EventAntiScaleFactor("TCHPM_B","BTagDown");
    TCHPM_CAntiBTagUp = EventAntiScaleFactor("TCHPM_C","BTagUp");
    TCHPM_CAntiBTagDown = EventAntiScaleFactor("TCHPM_C","BTagDown");
    TCHPM_LAntiMisTagUp = EventAntiScaleFactor("TCHPM_L","MisTagUp");
    TCHPM_LAntiMisTagDown = EventAntiScaleFactor("TCHPM_L","MisTagDown");

    /////

    TCHEL_B = EventScaleFactor("TCHEL_B","noSyst");
    TCHEL_C = EventScaleFactor("TCHEL_C","noSyst");
    TCHEL_L = EventScaleFactor("TCHEL_L","noSyst");
    
    TCHEL_BBTagUp = EventScaleFactor("TCHEL_B","BTagUp");
    TCHEL_BBTagDown = EventScaleFactor("TCHEL_B","BTagDown");
    TCHEL_CBTagUp = EventScaleFactor("TCHEL_C","BTagUp");
    TCHEL_CBTagDown = EventScaleFactor("TCHEL_C","BTagDown");
    TCHEL_LMisTagUp = EventScaleFactor("TCHEL_L","MisTagUp");
    TCHEL_LMisTagDown = EventScaleFactor("TCHEL_L","MisTagDown");

    TCHEL_BAnti = EventAntiScaleFactor("TCHEL_B","noSyst");
    TCHEL_CAnti = EventAntiScaleFactor("TCHEL_C","noSyst");
    TCHEL_LAnti = EventAntiScaleFactor("TCHEL_L","noSyst");
   
    TCHEL_BAntiBTagUp = EventAntiScaleFactor("TCHEL_B","BTagUp");
    TCHEL_BAntiBTagDown = EventAntiScaleFactor("TCHEL_B","BTagDown");
    TCHEL_CAntiBTagUp = EventAntiScaleFactor("TCHEL_C","BTagUp");
    TCHEL_CAntiBTagDown = EventAntiScaleFactor("TCHEL_C","BTagDown");
    TCHEL_LAntiMisTagUp = EventAntiScaleFactor("TCHEL_L","MisTagUp");
    TCHEL_LAntiMisTagDown = EventAntiScaleFactor("TCHEL_L","MisTagDown");
  }


//B-C veto weight as function of jet flavour, systematics and scale factors: 
//WILL BE CHANGED VERY SOON ACCORDING TO NEW PRESCRIPTIONS 
double SingleTopSystematicsTreesDumper::AntiBScaleFactor(string algo,string syst_name){
  
  double bcentral =0.9;  
  double berr = 0.15*bcentral;
  double cerr =0.3*bcentral;
  double tcheeff =0.7;
  double tchpeff =0.26;


  //  double bcentralTCHPT =0.89;  
  //double berrTCHPT = 0.11*bcentralTCHPT;
  //double cerrTCHPT =0.22*bcentralTCHPT;
  //double tchpeff =0.365;
  
  //  double bcentralTCHEL =0.95;  
  //double berrTCHEL = 0.11*bcentralTCHEL;
  //double cerrTCHEL =0.22*bcentralTCHEL;
  //double tcheeff =0.76;

  
  if(syst_name == "BTagUp"){
    if(algo == "TCHP_B"){
      return (1-tchpeff*(bcentral+berr))/(1-tchpeff);
    }
    if(algo == "TCHP_C"){
      return (1-tchpeff*(bcentral+cerr))/(1-tchpeff);
    }
    
    if(algo == "TCHEL_B"){
      return (1-tcheeff*(bcentral+berr))/(1-tcheeff);
    }
    
    if(algo == "TCHEL_C"){
      return (1-tcheeff*(bcentral+cerr))/(1-tcheeff);
    }
  }
  
  if(syst_name == "BTagDown"){
    if(algo == "TCHP_B"){
      return (1-tchpeff*(bcentral-berr))/(1-tchpeff);
    }
    if(algo == "TCHP_C"){
      return (1-tchpeff*(bcentral-cerr))/(1-tchpeff);
    }
  
    if(algo == "TCHEL_B"){
      return (1-tcheeff*(bcentral-berr))/(1-tcheeff);
    }
    if(algo == "TCHEL_C"){
      return (1-tcheeff*(bcentral-cerr))/(1-tcheeff);
    }
  }

  if(algo == "TCHP_B"){
    return (1-tchpeff*(bcentral))/(1-tchpeff);
  }
  if(algo == "TCHP_C"){
    return (1-tchpeff*(bcentral))/(1-tchpeff);
  }
  if(algo == "TCHEL_B"){
    return (1-tcheeff*(bcentral))/(1-tcheeff);
  }
  if(algo == "TCHEL_C"){
    return (1-tcheeff*(bcentral))/(1-tcheeff);
  }
    
  return 0.9;
}

//MisTag veto weight as function of jet flavour, systematics and scale factors: 
//WILL BE CHANGED VERY SOON ACCORDING TO NEW PRESCRIPTIONS 
double SingleTopSystematicsTreesDumper::AntiMisTagScaleFactor(string algo,string syst_name,double sf, double eff, double sferr){
  double mistagcentral = sf;  
  double mistagerr = sferr;
  double tcheeff = eff;
  double tchpeff =eff;
  
  if(syst_name == "MisTagUp"){
    if(algo == "TCHP_L"){
      return (1-tchpeff)/(1-tchpeff/(mistagcentral+mistagerr));
      }
    if(algo == "TCHEL_L"){
      return (1-tcheeff)/(1-tcheeff/(mistagcentral+mistagerr));
    }
    
  }
  
  if(syst_name == "MisTagDown"){
    if(algo == "TCHP_L"){
      return (1-tchpeff)/(1-tchpeff/(mistagcentral-mistagerr));
    }
    if(algo == "TCHEL_L"){
      return (1-tcheeff)/(1-tcheeff/(mistagcentral-mistagerr));
    }
  }

  if(algo == "TCHP_L"){
    return (1-tchpeff)/(1-tchpeff/(mistagcentral));
  }
  if(algo == "TCHEL_L"){
    return (1-tcheeff)/(1-tcheeff/(mistagcentral));
  }
  
  return 0.9;


}


double SingleTopSystematicsTreesDumper::turnOnWeight (std::vector<double> probabilities, int njets_req =1){
  double prob =0;
  for(unsigned int i=0; i<pow(2,probabilities.size());++i){
    //at least njets_req objects for trigger required
    int ntrigobj=0;
    for(unsigned int j=0; j<probabilities.size();++j){
      if((int)(i/pow(2,j))%2) ntrigobj++;
    }
    if(ntrigobj<njets_req) continue;  
    double newprob=1;
    for(unsigned int j=0; j<probabilities.size();++j){
      if((int)(i/pow(2,j))%2) newprob*=probabilities[j];
      else newprob*=1-probabilities[j];
    }
    prob+=newprob;
  }
  return prob;
}


bool SingleTopSystematicsTreesDumper::flavourFilter(string ch, int nb, int nc, int nl){
  
  if(ch == "WJets_wbb" || ch == "ZJets_wbb") return (nb>0 );
  if(ch == "WJets_wcc" || ch == "ZJets_wcc") return (nb==0 && nc>0);
  if(ch == "WJets_wlight" || ch == "ZJets_wlight") return (nb==0 && nc==0);
   
  return true;
}

/*double SingleTopSystematicsTreesDumper::jetprob(double pt, double btag){
  double prob=0.993*(exp(-51.0*exp(-0.160*pt)));
  prob*=0.902*exp((-5.995*exp(-0.604*btag)));
  return prob;
  }*/

double SingleTopSystematicsTreesDumper::jetprob(double pt, double btag){
  double prob=0.982*exp(-30.6*exp(-0.151*pt));//PT turnOn
  prob*=0.844*exp((-6.72*exp(-0.720*btag)));//BTag turnOn
  return prob;
}


//BTag weighter
bool SingleTopSystematicsTreesDumper::BTagWeight::filter(int t)
{
  return (t >= minTags && t <= maxTags);
}

float SingleTopSystematicsTreesDumper::BTagWeight::weight(vector<JetInfo> jets, int tags)
{
  if(!filter(tags))
    {
      //   std::cout << "This event should not pass the selection, what is it doing here?" << std::endl;
      return 0;
    }
  int njets=jets.size();
  int comb= 1 << njets;
  float pMC=0;
  float pData=0;
  for(int i=0;i < comb; i++)
    {
      float mc=1.;
      float data=1.;
      int ntagged=0;
      for(int j=0;j<njets;j++)
	{
	  bool tagged = ((i >> j) & 0x1) == 1;
	  if(tagged) 
	    {
	      ntagged++;
	      mc*=jets[j].eff;
	      data*=jets[j].eff*jets[j].sf;
	    }
	  else
	    {
	      mc*=(1.-jets[j].eff);
	      data*=(1.-jets[j].eff*jets[j].sf);
	    }
	}       
   
      if(filter(ntagged))
	{
	  //	  std::cout << mc << " " << data << endl;
	  pMC+=mc;
	  pData+=data;
	}
    }

  if(pMC==0) return 0; 
  return pData/pMC;
}


//define this as a plug-in
DEFINE_FWK_MODULE(SingleTopSystematicsTreesDumper);


