/*
*\Author:  O.Iorio
*
*
*
*\version  $Id: SingleTopSystematicsTreesDumper.cc,v 1.12.2.9 2011/07/22 14:08:53 oiorio Exp $ 
*/
// This analyzer dumps the histograms for all systematics listed in the cfg file 
//
//
//

#define DEBUG    0 // 0=false
#define MC_DEBUG 0 // 0=false   else -> dont process preselection
#define C_DEBUG  0 // currently debuging

#include "TopQuarkAnalysis/SingleTop/interface/SingleTopSystematicsJetsDumper.h"
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

SingleTopSystematicsJetsDumper::SingleTopSystematicsJetsDumper(const edm::ParameterSet& iConfig)
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
  MTWCut = channelInfo.getUntrackedParameter<double>("MTWCut",50);
  mcPUFile_ = channelInfo.getUntrackedParameter< std::string >("mcPUFile","pileupdistr_TChannel.root");
  puHistoName_ = channelInfo.getUntrackedParameter< std::string >("puHistoName","pileUpDumper/PileUp");

  isControlSample_ = iConfig.getUntrackedParameter<bool>("isControlSample",false);

  RelIsoCut = channelInfo.getUntrackedParameter<double>("RelIsoCut",0.1);
  loosePtCut = channelInfo.getUntrackedParameter<double>("loosePtCut",30); 

  maxPtCut = iConfig.getUntrackedParameter<double>("maxPtCut",30);

  leptonsPt_ =  iConfig.getParameter< edm::InputTag >("leptonsPt");
  leptonsPhi_ =  iConfig.getParameter< edm::InputTag >("leptonsPhi");
  leptonsEta_ =  iConfig.getParameter< edm::InputTag >("leptonsEta");
  leptonsEnergy_ =  iConfig.getParameter< edm::InputTag >("leptonsEnergy");
  leptonsCharge_ =  iConfig.getParameter< edm::InputTag >("leptonsCharge");
  leptonsRelIso_ =  iConfig.getParameter< edm::InputTag >("leptonsRelIso");
  leptonsQCDRelIso_ =  iConfig.getParameter< edm::InputTag >("leptonsQCDRelIso");


  leptonsDB_ =  iConfig.getParameter< edm::InputTag >("leptonsDB");

  genJetsPt_  = iConfig.getParameter< edm::InputTag >("genJetsPt");
  //  genJetsEta_  = iConfig.getParameter< edm::InputTag >("genJetsEta");

  leptonsID_ =  iConfig.getParameter< edm::InputTag >("leptonsID");

  leptonsFlavour_ =  iConfig.getUntrackedParameter< std::string >("leptonsFlavour");
  
  looseMuonsRelIso_ =  iConfig.getParameter< edm::InputTag >("looseMuonsRelIso");
  looseElectronsRelIso_ =  iConfig.getParameter< edm::InputTag >("looseElectronsRelIso");

  jetsEta_ =  iConfig.getParameter< edm::InputTag >("jetsEta");
  jetsPt_ =  iConfig.getParameter< edm::InputTag >("jetsPt");
  jetsPhi_ =  iConfig.getParameter< edm::InputTag >("jetsPhi");
  jetsEnergy_ =  iConfig.getParameter< edm::InputTag >("jetsEnergy");
  
  jetsBTagAlgo_ =  iConfig.getParameter< edm::InputTag >("jetsBTagAlgo");
  //  jetsAntiBTagAlgo_ =  iConfig.getParameter< edm::InputTag >("jetsAntiBTagAlgo");
  jetsAntiBTagAlgo_ =  iConfig.getParameter< edm::InputTag >("jetsAntiBTagAlgo");
  jetsFlavour_ =  iConfig.getParameter< edm::InputTag >("jetsFlavour");

  METPhi_ =  iConfig.getParameter< edm::InputTag >("METPhi");
  METPt_ =  iConfig.getParameter< edm::InputTag >("METPt");
  
  //  UnclMETPx_ =  iConfig.getParameter< edm::InputTag >("UnclusteredMETPx");
  //  UnclMETPy_ =  iConfig.getParameter< edm::InputTag >("UnclusteredMETPy");
  UnclMETPx_ =  iConfig.getParameter< edm::InputTag >("UnclusteredMETPx");
  UnclMETPy_ =  iConfig.getParameter< edm::InputTag >("UnclusteredMETPy");
  
  jetsCorrTotal_ =  iConfig.getParameter< edm::InputTag >("jetsCorrTotal");

  doBScan_  =  iConfig.getUntrackedParameter< bool >("doBScan",false); 
  doQCD_  =  iConfig.getUntrackedParameter< bool >("doQCD",true); 
  //  jetsPF_ =  iConfig.getParameter< edm::InputTag >("patJets");

  mode_ =  iConfig.getUntrackedParameter<std::string >("mode",""); 


  //Pile Up Part

  npv_ = iConfig.getParameter< edm::InputTag >("nvertices");//,"PileUpSync"); 

  doPU_ = iConfig.getUntrackedParameter< bool >("doPU",false);
  doResol_ = iConfig.getUntrackedParameter< bool >("doResol",false);
  doTurnOn_ = iConfig.getUntrackedParameter< bool >("doTurnOn",true);

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
    
    trees[syst]->Branch("nJ",&njets_pass);
    trees[syst]->Branch("nT",&ntchp_tags);
    trees[syst]->Branch("W1T",&b_weight_tchpt_1);
    trees[syst]->Branch("W2T",&b_weight_tchpt_2);
    trees[syst]->Branch("WG1T",&b_weight_tchpt_geq_1);
    trees[syst]->Branch("WG2T",&b_weight_tchpt_geq_2);
    
    trees[syst]->Branch("charge",&chargeTree);
    trees[syst]->Branch("runid",&runTree);
    trees[syst]->Branch("lumiid",&lumiTree);
    trees[syst]->Branch("eventid",&eventTree);
    trees[syst]->Branch("weight",&weightTree);

    trees[syst]->Branch("weightLumi",&weightLumi);
    trees[syst]->Branch("PUWeight",&PUWeightTree);
    trees[syst]->Branch("turnOnWeight",&turnOnWeightTree);

    
    //Extra info
    
    trees[syst]->Branch("leptonPt",&lepPt);
    trees[syst]->Branch("leptonEta",&lepEta);
    trees[syst]->Branch("leptonPhi",&lepPhi);
    trees[syst]->Branch("leptonRelIso",&lepRelIso);

    trees[syst]->Branch("metPt",&metPt);
    trees[syst]->Branch("mtwMass",&mtwMassTree);
    
    trees[syst]->Branch("ID",&electronID);

    trees[syst]->Branch("nVertices",&nVertices);
    
    

  }
  
  b_tchpt_geq_1 = BTagWeight(1,999);  
  b_tchpt_geq_2 = BTagWeight(2,999);  
  b_tchpt_1 = BTagWeight(1,1);  
  b_tchpt_2 = BTagWeight(2,2);  
    
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
  



  InitializeEventScaleFactorMap();
  //  cout<< "I work for now but I do nothing. But again, if you gotta do nothing, you better do it right. To prove my good will I will provide you with somse numbers later."<<endl;

  //iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHPT",perfHP);
  //iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHEL",perfHE);
  
  //iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHPT",perfHP);
  //iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHEL",perfHE);
  
  isFirstEvent = true;

}

void SingleTopSystematicsJetsDumper::analyze(const Event& iEvent, const EventSetup& iSetup)
{
  
  //Very first check: if there are < 2 jets skip the event
  
  iEvent.getByLabel(jetsPt_,jetsPt);
  if(jetsPt->size() > 20)return; 
  
  if(isFirstEvent){
    cout <<  "isfirst " << endl;
   iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHPT",perfMHP);
   iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHEL",perfMHE);

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


  bool passesSignal=false,passesQCDSignal=false,passesSampleA=false,passesSampleB=false,passesQCDSampleA=false,passesQCDSampleB= false;    

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
  weightLumi = WeightLumi;
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


  double b_weight_signal_region_noSyst =1, b_weight_sample_A_noSyst=1, b_weight_sample_B_noSyst=1; 
  


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
    
    weightTree = Weight;

    b_weight_tchpt_geq_1=0; b_weight_tchpt_geq_2=0;
    b_weight_tchpt_1=0; b_weight_tchpt_2=0;
  

    njets_pass=0;
    
    bool is_btag_relevant = ((syst_name=="noSyst" || syst_name == "BTagUp" || syst_name == "BTagDown" 
			     || syst_name == "MisTagUp" || syst_name == "MisTagDown"
			      || syst_name == "JESUp" || syst_name == "JESDown" ) && channel != "Data"
			     );


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
      
      float leptonRelIso = leptonsRelIso->at(i);
      //      float leptonQCDRelIso = leptonsQCDRelIso->at(i);
      float leptonQCDRelIso = leptonRelIso;
      lepRelIso = leptonRelIso;
      
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
      if ( abs(leptonDB) >0.02) continue;
      
      float leptonPt = leptonsPt->at(i);
      float leptonPhi = leptonsPhi->at(i);
      float leptonEta = leptonsEta->at(i);
      float leptonE = leptonsEnergy->at(i);
      //Build the lepton 4-momentum
      leptons.push_back(math::PtEtaPhiELorentzVector(leptonPt,leptonEta,leptonPhi,leptonE));
  
     }


    //  cout << "test 03 "<<endl;
    //Loop for the qcd leptons
     
    if(leptons.size()!=1) continue;
    
    //Clear the vector of btags //NOT USED NOW
    //    b_weight_tag_algo1.clear();
    //    b_weight_tag_algo2.clear();
    //    b_weight_antitag_algo1.clear();
    //    b_weight_antitag_algo2.clear();
    
    //        b_discriminator_value_tag_algo1.clear();
    //    b_discriminator_value_antitag_algo2.clear();

    ntchp_tags=0;
    ntche_tags=0;
    ntchp_antitags=0;
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

      gotJets= true;
    }
    
    if(leptonsFlavour_ == "electron" && doTurnOn_){
      if (!hasTurnOnWeight){
	for(size_t i = 0;i<nJets;++i){
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
      eta = jetsEta->at(i);
      if (fabs(eta )>4.5)continue;
      ptCorr = jetsPt->at(i);
      flavour = jetsFlavour->at(i);
      double energyCorr = jetsEnergy->at(i); 
      
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
      if(passesPtCut && !leptons.empty()){
	for(size_t l =0;l<leptons.size();++l){
	  if( deltaR<math::PtEtaPhiELorentzVector,math::PtEtaPhiELorentzVector>(jets.back(),leptons.at(l))<0.3){
	    jets.pop_back();
	    continue;
	  }
	}
      }

      if(!passesPtCut) continue;

      //b tag thresholds 

      
      double valueAlgo1 = jetsBTagAlgo->at(i);
      double valueAlgo2 = jetsAntiBTagAlgo->at(i);
      
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
      //  cout << " test 2 "<<endl;
  
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
      //double heleff =(perfBHE->getResult(PerformanceResult::BTAGBEFF,measurePoint));
      double heleff = EFFMap("TCHEL_C");
      double helSF = (perfBHE->getResult(PerformanceResult::BTAGBEFFCORR,measurePoint));
      double helSFErr =0.;
    if(syst_name == "BTagUp"){                             
      hptSFErr = fabs(perfBHP->getResult(PerformanceResult::BTAGBERRCORR,measurePoint));
      helSFErr = fabs(perfBHE->getResult(PerformanceResult::BTAGBERRCORR,measurePoint));
    }
    if(syst_name == "BTagDown"){
      hptSFErr = -fabs(perfBHP->getResult(PerformanceResult::BTAGBERRCORR,measurePoint));
      helSFErr = -fabs(perfBHE->getResult(PerformanceResult::BTAGBERRCORR,measurePoint));
    }
    //    cout <<"cjet hpt "<<hpteff<< " hpt sf "<< hptSF <<endl;
    
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
    //    double heleff =(perfBHE->getResult(PerformanceResult::BTAGBEFF,measurePoint));
    double heleff = EFFMap("TCHEL_B");
    double helSF = (perfBHE->getResult(PerformanceResult::BTAGBEFFCORR,measurePoint));
    double helSFErr =0.;
    if(syst_name == "BTagUp"){
      hptSFErr = fabs(perfBHP->getResult(PerformanceResult::BTAGBERRCORR,measurePoint));
      helSFErr = fabs(perfBHE->getResult(PerformanceResult::BTAGBERRCORR,measurePoint));
    }
    if(syst_name == "BTagDown"){
      hptSFErr = -fabs(perfBHP->getResult(PerformanceResult::BTAGBERRCORR,measurePoint));
      helSFErr = -fabs(perfBHE->getResult(PerformanceResult::BTAGBERRCORR,measurePoint));
    }
    //    cout <<"bjet hpt "<<hpteff<< " hpt sf "<< hptSF << " jet pt "<< ptCorr<<"eta"<<etaMin <<endl;
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
    double heleff =(perfMHE->getResult(PerformanceResult::BTAGLEFF,measurePoint));
    double helSF = (perfMHE->getResult(PerformanceResult::BTAGLEFFCORR,measurePoint));
    double helSFErr =0.;
    if(syst_name == "MisTagUp"){
      hptSFErr = fabs(perfMHP->getResult(PerformanceResult::BTAGLERRCORR,measurePoint));
      helSFErr = fabs(perfMHE->getResult(PerformanceResult::BTAGLERRCORR,measurePoint));
    }
    if(syst_name == "MisTagDown"){
      hptSFErr = -fabs(perfMHP->getResult(PerformanceResult::BTAGLERRCORR,measurePoint));
      helSFErr = -fabs(perfMHE->getResult(PerformanceResult::BTAGLERRCORR,measurePoint));
    }
    //    cout <<"light jet hpt "<<hpteff<< " hpt sf "<< hptSF <<endl;
    jsfshpt.push_back(BTagWeight::JetInfo(hpteff,hptSF+hptSFErr));
    jsfshel.push_back(BTagWeight::JetInfo(heleff,helSF+helSFErr));
    }
    ++nudsg;
  
  }
  if(is_btag_relevant ) measurePoint.reset();
  //	cout << " test 3 "<<endl;
    
  if(passesBTag) {
    //Add to b-jet collection
    bjets.push_back(jets.back()); 
    ++ntchp_tags;
  }
  else ++ntchp_antitags;
  
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
    
    njets_pass = jets.size();

    //MTW Definition
    metPt = sqrt(metPx*metPx+metPy*metPy);
    MTWValue =  sqrt((leptons.at(0).pt()+metPt)*(leptons.at(0).pt()+metPt)  -(leptons.at(0).px()+metPx)*(leptons.at(0).px()+metPx) -(leptons.at(0).py()+metPy)*(leptons.at(0).py()+metPy));
    mtwMassTree = MTWValue;
    
    /////////
    ///End of the standard lepton-jet loop 
    /////////
    //if( maxPtTree< maxPtCut )continue;
    
    // b_tchpt_geq_1, b_tchpt_geq_2;
    
    b_weight_tchpt_geq_1 = b_tchpt_geq_1.weight(jsfshpt,ntchp_tags);
    b_weight_tchpt_geq_2 = b_tchpt_geq_2.weight(jsfshpt,ntchp_tags);

    b_weight_tchpt_1 = b_tchpt_1.weight(jsfshpt,ntchp_tags);
    b_weight_tchpt_2 = b_tchpt_2.weight(jsfshpt,ntchp_tags);
    
    trees[syst]->Fill();

  }
}
																					
//CosThetalj given top quark, lepton and light jet
float SingleTopSystematicsJetsDumper::cosThetaLJ(math::PtEtaPhiELorentzVector lepton, math::PtEtaPhiELorentzVector jet, math::PtEtaPhiELorentzVector top){
  
  math::PtEtaPhiELorentzVector boostedLepton = ROOT::Math::VectorUtil::boost(lepton,top.BoostToCM());
  math::PtEtaPhiELorentzVector boostedJet = ROOT::Math::VectorUtil::boost(jet,top.BoostToCM());

  return  ROOT::Math::VectorUtil::CosTheta(boostedJet.Vect(),boostedLepton.Vect());
  
}

//top quark 4-momentum given lepton, met and b-jet
math::PtEtaPhiELorentzVector SingleTopSystematicsJetsDumper::top4Momentum(math::PtEtaPhiELorentzVector lepton, math::PtEtaPhiELorentzVector jet, float metPx, float metPy){
  return top4Momentum(lepton.px(),lepton.py(),lepton.pz(),lepton.energy(),jet.px(),jet.py(),jet.pz(),jet.energy(),metPx,metPy);
}

//top quark 4-momentum original function given the necessary parameters 
math::PtEtaPhiELorentzVector SingleTopSystematicsJetsDumper::top4Momentum(float leptonPx, float leptonPy, float leptonPz, float leptonE, float jetPx, float jetPy, float jetPz,float jetE, float metPx, float metPy){
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
math::XYZTLorentzVector SingleTopSystematicsJetsDumper::NuMomentum(float leptonPx, float leptonPy, float leptonPz, float leptonPt, float leptonE, float metPx, float metPy ){

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
double SingleTopSystematicsJetsDumper::jetUncertainty(double eta, double ptCorr, int flavour){
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
void SingleTopSystematicsJetsDumper::endJob(){
  

}
  
//B-C weight as function of jet flavour, systematics and scale factors: 
//WILL BE CHANGED VERY SOON ACCORDING TO NEW PRESCRIPTIONS 
double SingleTopSystematicsJetsDumper::BScaleFactor(string algo,string syst_name){
  
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


double SingleTopSystematicsJetsDumper::EventScaleFactor(string algo,string syst_name){//,double sf, double eff, double sferr){

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

double SingleTopSystematicsJetsDumper::EventAntiScaleFactor(string algo,string syst_name ){
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
double SingleTopSystematicsJetsDumper::MisTagScaleFactor(string algo,string syst_name,double sf, double eff, double sferr){
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

double SingleTopSystematicsJetsDumper::SFMap(string algo ){
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

double SingleTopSystematicsJetsDumper::SFErrMap(string algo ){
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

double SingleTopSystematicsJetsDumper::EFFMap(string algo ){
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



double SingleTopSystematicsJetsDumper::EFFErrMap(string algo ){
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


double SingleTopSystematicsJetsDumper::EventScaleFactorMap(string algo, string syst ){

  
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


void SingleTopSystematicsJetsDumper::InitializeEventScaleFactorMap(){

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
double SingleTopSystematicsJetsDumper::AntiBScaleFactor(string algo,string syst_name){
  
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
double SingleTopSystematicsJetsDumper::AntiMisTagScaleFactor(string algo,string syst_name,double sf, double eff, double sferr){
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


double SingleTopSystematicsJetsDumper::turnOnWeight (std::vector<double> probabilities, int njets_req =1){
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


bool SingleTopSystematicsJetsDumper::flavourFilter(string ch, int nb, int nc, int nl){
  
  if(ch == "WJets_wbb" || ch == "ZJets_wbb") return (nb>0 );
  if(ch == "WJets_wcc" || ch == "ZJets_wcc") return (nb==0 && nc>0);
  if(ch == "WJets_wlight" || ch == "ZJets_wlight") return (nb==0 && nc==0);
   
  return true;
}

/*double SingleTopSystematicsJetsDumper::jetprob(double pt, double btag){
  double prob=0.993*(exp(-51.0*exp(-0.160*pt)));
  prob*=0.902*exp((-5.995*exp(-0.604*btag)));
  return prob;
  }*/

double SingleTopSystematicsJetsDumper::jetprob(double pt, double btag){
  double prob=0.982*exp(-30.6*exp(-0.151*pt));//PT turnOn
  prob*=0.844*exp((-6.72*exp(-0.720*btag)));//BTag turnOn
  return prob;
}


//BTag weighter
bool SingleTopSystematicsJetsDumper::BTagWeight::filter(int t)
{
  return (t >= minTags && t <= maxTags);
}

float SingleTopSystematicsJetsDumper::BTagWeight::weight(vector<JetInfo> jets, int tags)
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
DEFINE_FWK_MODULE(SingleTopSystematicsJetsDumper);


