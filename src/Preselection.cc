// =================================
//   CMS - single top preselection
// =================================

#define DEBUG    0 // 0=false
#define MC_DEBUG 0 // 0=false   else -> dont process preselection
#define C_DEBUG  0 // currently debuging


#include "TopQuarkAnalysis/SingleTop/interface/Preselection.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/Framework/interface/TriggerNames.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"

Preselection::Preselection(const edm::ParameterSet& iConfig)
{
#if DEBUG
  cout << "constructor" << endl;
#endif

  // -------------  get cfg file information:
  
  doPresel      = iConfig.getParameter<bool>("doPresel");
  no0jets       = iConfig.getParameter<bool>("no0jets");
  triggerInfo      = iConfig.getParameter<bool>("triggerInfo");
  
  // first fill muon trigger, then ele trigger!
  triggernames.push_back(iConfig.getParameter<string>("muTriggerTag"));
  triggernames.push_back(iConfig.getParameter<string>("eleTriggerTag"));
  
  electronProducer = iConfig.getParameter<InputTag>("electronProducer");
  electron_cut_pt = iConfig.getParameter<double>("electron_cut_pt");
  electron_cut_eta = iConfig.getParameter<double>("electron_cut_eta");
  
  muonProducer = iConfig.getParameter<InputTag>("muonProducer");
  muon_cut_pt = iConfig.getParameter<double>("muon_cut_pt");
  muon_cut_eta = iConfig.getParameter<double>("muon_cut_eta");
  
  jetProducer = iConfig.getParameter<InputTag>("jetProducer");
  jetAlgo = iConfig.getParameter<string>("jetAlgo");
 
  jet_loosecut_pt = iConfig.getParameter<double>("jet_loosecut_pt");
  jet_tightcut_pt = iConfig.getParameter<double>("jet_tightcut_pt");
  jet_cut_eta = iConfig.getParameter<double>("jet_cut_eta");
  
  metProducer = iConfig.getParameter<InputTag>("metProducer");
  
  vertexProducer = iConfig.getParameter<InputTag>("vertexProducer");
  trackProducer = iConfig.getParameter<InputTag>("trackProducer");
  
  EventType = iConfig.getParameter<InputTag>("EventType");
  AnaType = iConfig.getParameter<InputTag>("AnaType");
  MiniTreeName = iConfig.getParameter<string>("MiniTreeName");
  ResultDir = iConfig.getParameter<string>("ResultDir");

  info = new CatoCMSSampleInfo();
  info->Name = iConfig.getParameter<string>("SampleName");
  info->cross_section = iConfig.getParameter<double>("SampleCrossSection");
  
  MuTrigIdx  = 999;
  EleTrigIdx = 999;
  
  miniTree = NULL;
  
  cev  = new CatoCMSEvent();
  stp  = new STParton();
  ssp  = new SSParton();
  ttp  = new TTbarParton();
  wjp  = new WJetParton();
  qcdp = new QCDParton();
  mcST = new CatoCMSSingleTopMC();
  mcSS = new CatoCMSSchannelMC();
  mcTT = new CatoCMSTTbarMC();
  mcWJ = new CatoCMSWJetsMC();
  mcQCD= new CatoCMSQCDMC();

  // set up Cut Flow Table:

  cft = new CatoCMSCutFlowTable(6);
  //addTable muss vor init aufgerufen
  cft->AddTable("Barrel Electrons");
  cft->AddTable("Endcap Electrons");
  cft->AddTable("Muons");

  //init 
  
  lepJetEv=0;
  tauJetEv=0;
  diLepEv=0;
  hadEv=0;
  remainingLepJetsEv=0;
  remainingTauJetsEv=0;
  remainingDiLepEv=0;
  remainingHadEv=0;
  DecChan= -1;

#if DEBUG
  cout << "constructor done \n";
#endif

#if DEBUG
  cout << "begin job" << endl;
#endif  
  //  TTree *tmp;
  //  CatoCMSSampleInfo *stmp;
  edm::Service<TFileService> tfs;
  tfs->file().cd("/");

  miniTree = new TTree(MiniTreeName.c_str(),
		       "A tree with preselected mini events", 3);
  // CMSEvent branch:
  miniTree->Branch("CatoCMSEvent", "CatoCMS::Event", &cev, 32000, 3);
  
  // CMSMCTruth branches:
  if(EventType.label() == string("SingleTopT"))
    {
      cout << EventType.encode() <<" MCTruth Info" << endl;
      miniTree->Branch("CatoCMSSingleTopMC","CatoCMS::SingleTopMC", &mcST, 32000, 3);
    }
  
  else if(EventType.label() == string("SingleTopS"))
    {
      cout << EventType.encode() <<" MCTruth Info" << endl;
      miniTree->Branch("CatoCMSSchannelMC","CatoCMS::SchannelMC", &mcSS, 32000, 3);
    }
  
  else if(EventType.label() == string("WJets"))
    {
      cout << EventType.label() << " MCTruth Info" << endl;
      miniTree->Branch("CatoCMSWJetsMC", "CatoCMS::WJetsMC", &mcWJ, 32000, 3);
      
    }
  else if(EventType.label() == string("TTBar"))
    {
      cout << EventType.label() << " MCTruth Info" << endl;
      miniTree->Branch("CatoTTbarMC", "CatoCMS::TTbarMC", &mcTT, 32000, 3);
      
    } 
  else if(EventType.label() == string("QCD"))
    {
      cout << EventType.label() << " MCTruth Info" << endl;
      miniTree->Branch("CatoQCDMC", "CatoCMS::QCDMC", &mcQCD, 32000, 3);
      
    }
  else 
    if(EventType.label() == string("NoMCInfo"))
      cout << "No MC Info processed!" << endl;
    else
      cout << "Wrong EventType in CFG File: " << EventType.label() << endl;
  
  cout << "================\n\n\n";
}


Preselection::~Preselection()
{
  edm::Service<TFileService> tfs;
  tfs->file().cd("/");
  tfs->file().WriteObjectAny(info,"CatoCMS::SampleInfo","SampleInfo");
  
  string filename;
  fstream fs;
  
  for(std::map<std::string,TH1*>::const_iterator hist=h.begin(); hist!=h.end(); hist++) 
    hist->second->Write();
  
  // ------------------------------- 
  //   write out cut flow table(s)
  // ------------------------------- 
  
  filename = ResultDir + MiniTreeName + "_CutFlowTable.cft";
  fs.open(filename.c_str(),ios_base::out);
  if(fs.good())
    cft->txt_output(fs);
  else
    cout << "Could not write " << filename << endl;
  fs.close();  
  
  // ------------------------------------
  //  write out log of presel settings:
  // ------------------------------------
  filename = ResultDir + MiniTreeName + "_settings.log";
  fs.open(filename.c_str(),ios_base::out);
  if(fs.good())
    {
      fs << "\nConfiguration File Settings" << endl << endl
	 << "Outputfile :\n\t"
	 << ResultDir << MiniTreeName << endl << endl
	 << "triggerInfo = " << triggerInfo << endl
	
	 << "EventType = "           << EventType.label()        << endl 
	 << "SampleName = "          << info->Name               << endl
	 << "SampleCrossSection = "  << info->cross_section      << endl << endl

	 << "electronProducer = "    << electronProducer.label() << endl
	 << "\t electron_cut_pt  = " << electron_cut_pt          << endl
	 << "\t electron_cut_eta = " << electron_cut_eta         << endl 
	
	 << "muonProducer = "        << muonProducer.label()     << endl
	 << "\t muon_cut_pt  = "     << muon_cut_pt              << endl
	 << "\t muon_cut_eta = "     << muon_cut_eta             << endl 
	
	 << "metProducer = "         << metProducer.label()      << endl
	
	 << "jetProducer = "         << jetProducer .label()     << endl
	 << "\t jet_loosecut_pt= "   << jet_loosecut_pt          << endl
	 << "\t jet_tightcut_pt= "   << jet_tightcut_pt          << endl
	 << "\t jet_cut_eta    = "   << jet_cut_eta              << endl << endl
	
	 << "muon trigger = "        << triggernames[0]          << endl
	 << "ele trigger = "         << triggernames[1]          << endl << endl
	
	 << endl << endl<< endl;
      
      if(EventType.label() == string("SingleTopT"))
  	{
	  MCStatOut(cout);
	  MCStatOut(fs);
  	}
      else if(EventType.label() == string("TTBar"))
  	{
	  MCStatOut(cout);
	  MCStatOut(fs);
  	}
      else if(EventType.label() == string("SingleTopS"))
  	{
	  MCStatOut(cout);
	  MCStatOut(fs);
  	}
    }
  else
    cout << "Could not write" << filename << endl;
  fs.close();  

  delete info;
  delete cev;
  delete stp;
  delete ssp;
  delete ttp;
  delete wjp;
  delete qcdp;
  delete mcST;
  delete mcSS;
  delete mcTT;
  delete mcWJ;
  delete mcQCD;
}

void Preselection::analyze(const Event& iEvent, const EventSetup& iSetup)
{

#if DEBUG
  cout << "--------- new event ---------" << endl;
  cout << "EventNumber: " << info->TotalEvents+1 << endl;
#endif

  CatoCMSPDFInfo cpdfinfo;
  if(EventType.label() != string("NoMCInfo")) {
    
    // --------------------
    //    Fill PDF info
    // --------------------
    Handle<GenEventInfoProduct> genevinfo;
    iEvent.getByType(genevinfo);
    const gen::PdfInfo *pdfstuff = genevinfo->pdf();
    if(pdfstuff == NULL) {
      cout << "pdfinfo null pointer" << endl;
      throw cms::Exception("fail","pdfinfo null pointer");
    }
  
    cpdfinfo.x1 = pdfstuff->x.first;
    cpdfinfo.x2 = pdfstuff->x.second;
    cpdfinfo.id1 = static_cast<int>(pdfstuff->id.first);
    cpdfinfo.id2 = static_cast<int>(pdfstuff->id.second);	
    cpdfinfo.scalePDF = pdfstuff->scalePDF; 
  

    // --------------------
    //    Fill MC Truth 
    // --------------------
    double weight = 1.;
    
    Handle<std::vector<reco::GenParticle> > genParticles;
    try {
      iEvent.getByLabel("genParticles",genParticles);
    } catch (...) {;}
    
    Handle<double> genEventWeight;
    try {
      iEvent.getByLabel( "genEventWeight", genEventWeight );
      weight = *genEventWeight; 
    } catch (...) {;}
  
    if(EventType.label() == string("SingleTopT")){  
      //    stp->printList(genParticles,3);
      stp->GetSingleTopTruth(genParticles, weight, mcST);
      DecChan = mcST->DecChan;
      
      if(mcST->DecChan == 0 || (mcST->DecChan)%10 == 0)
	lepJetEv++;
      else if(mcST->DecChan == 1 || (mcST->DecChan)%10 == 1)
	tauJetEv++;
      else if(mcST->DecChan == 2 || (mcST->DecChan)%10 == 2)
	hadEv++;
      else
	diLepEv++;
      
    }
  
    else if(EventType.label() == string("SingleTopS")){  
      ssp->GetSchannelTruth(genParticles, weight, mcSS);
      DecChan = mcSS->DecChan;
      
      if(mcSS->DecChan == 0 || (mcSS->DecChan)%10 == 0)
	lepJetEv++;
      else if(mcSS->DecChan == 1 || (mcSS->DecChan)%10 == 1)
	tauJetEv++;
      else if(mcSS->DecChan == 2 || (mcSS->DecChan)%10 == 2)
	hadEv++;
      else
	diLepEv++;
    }
    
    else if(EventType.label() == string("WJets")){
      wjp->GetWJetTruth(genParticles, weight, mcWJ);
      
      if(mcWJ->DecChan == 0 || (mcWJ->DecChan)%10 == 0)
	lepJetEv++;
      else if(mcWJ->DecChan == 1 || (mcWJ->DecChan)%10 == 1)
	tauJetEv++;
      else if(mcWJ->DecChan == 2 || (mcWJ->DecChan)%10 == 2)
	hadEv++;
      else
	diLepEv++;
    }	
    
    
    else if(EventType.label() == string("TTBar")){
      ttp->GetTTbarTruth(genParticles, weight,mcTT);
      DecChan = mcTT->DecChan;
      if(mcTT->DecChan == 0 || (mcTT->DecChan)%10 == 0)
	lepJetEv++;
      else if(mcTT->DecChan == 1 || (mcTT->DecChan)%10 == 1)
	tauJetEv++;
      else if(mcTT->DecChan == 2 || (mcTT->DecChan)%10 == 2)
	hadEv++;
      else
	diLepEv++;
    } 
  
    else if(EventType.label() == string("QCD")){
      qcdp->GetQCDTruth(genParticles, weight,mcQCD);
    } 
    
#if MC_DEBUG
    if(AnaType.label() == string("MCTruth")){
      miniTree->Fill();
      cout << "this is MCTruth !!" << endl;
      return;
    }
#endif
  } // end of IF for MC events

#if DEBUG
  cout << "this is not MCTruth !!" << endl;
#endif

  CatoCMSCutFlowTable *mycft = NULL;    // cft for this event ...
  mycft=cft;
  
  cev->Reset();
  
  //// TO BE ADDED ASAP: run/event/lumisection numbers in the Event block
  
  cev->eventWeight = 1;
  
  
  
  
  // vertices:
  Handle<VertexCollection> vertices;
  iEvent.getByLabel(vertexProducer, vertices);
  
  cev->nZvtx = vertices->size();

  //// TO BE ADDED ASAP: a Vertex block, with all the variables being used in 900 GeV analyses to select the event


  // -------------------------
  //      Leptons (ele, mu)
  // -------------------------
  
  CatoCMSLepton*  lepton;

  
  // cut flags:
  bool eleKin(0);
  bool muKin(0);
  unsigned int countGoodElectrons=0;
  unsigned int countGoodMuons=0;

  // Electrons ----------------------------------------------------------------


  Handle<vector<pat::Electron> > elHa;
  iEvent.getByLabel(electronProducer, elHa);
  const vector<pat::Electron>* ele = elHa.product();
  
  for(vector<pat::Electron>::const_iterator it = ele->begin(); 
      it!=ele->end(); it++){
    
    const pat::Electron* elec = &*it;
    eleKin= false;

    if (elec->pt() > electron_cut_pt 
     	&& fabs(elec->eta()) < electron_cut_eta) {
      eleKin=true;
      countGoodElectrons++;

      lepton = cev->NewLepton();
      lepton->isTightEle = elec->electronID("eidTight");
      lepton->v4.SetCoordinates(elec->px(), elec->py(), elec->pz(), elec->energy());
      lepton->vertex.SetCoordinates(elec->vx(),elec->vy(),elec->vz());
      lepton->P      = elec->p();
      lepton->Et     = elec->et();
      lepton->Charge = elec->charge();
      
      lepton->TrkZ0    = elec->TrackPositionAtVtx().Z();
      lepton->TrkPt    = sqrt(elec->trackMomentumAtVtx().perp2());
      lepton->TrkIso   = elec->trackIso();
      lepton->CaloIso  = elec->caloIso();
      
      // only for electrons:
      lepton->caloEnergy                     = elec->caloEnergy();
      lepton->eSuperClusterOverP             = elec->eSuperClusterOverP();
      lepton->deltaEtaSeedClusterTrackAtCalo = elec->deltaEtaSeedClusterTrackAtCalo();
      lepton->deltaPhiSeedClusterTrackAtCalo = elec->deltaPhiSeedClusterTrackAtCalo();
      lepton->hadronicOverEm                 = elec->hadronicOverEm();
      lepton->classification                 = elec->classification();
      
      lepton->TrkNhits       = elec->gsfTrack()->numberOfValidHits();
      lepton->TrkChi2        = elec->gsfTrack()->chi2()/elec->gsfTrack()->ndof();
      if (vertices->size() != 0) {
	lepton->Trkd0          = elec->gsfTrack()->dxy( vertices->begin()->position() );
	lepton->SigmaD0        = elec->gsfTrack()->dxyError();
      } else {
	lepton->Trkd0          = elec->gsfTrack()->d0();
	lepton->SigmaD0        = elec->gsfTrack()->d0Error();
      }

      lepton->NumberOfTracks   = elec->numberOfTracks();
      
      lepton->id = CatoCMSDef::ELECTRON;   
    }

#if DEBUG
    cout << "ele pT = " << elec->pt() 
	 << "\t ele eta = " << elec->eta() 
    	 << endl;
#endif
  }		
  
  info->TotalEvents++;
  
  // Muons --------------------------------------------------------------------
  Handle<vector<pat::Muon> > muHa;
  iEvent.getByLabel(muonProducer, muHa);
  const vector<pat::Muon>* mus = muHa.product();
  
  for(vector<pat::Muon>::const_iterator it = mus->begin();
      it != mus->end(); it++){
    
    const pat::Muon* muon = &*it;

    if(!muon->isGlobalMuon()) continue; // use only global muons!

    muKin = false;


    if(muon->pt() > muon_cut_pt
       && fabs(muon->eta()) < muon_cut_eta) {
      muKin = true;
      countGoodMuons++;

      lepton = cev->NewLepton();
      
      lepton->v4.SetCoordinates(muon->px(), muon->py(), muon->pz(), muon->energy());
      lepton->vertex.SetCoordinates(muon->vx(),muon->vy(),muon->vz());
      lepton->P = muon->p();
      lepton->Et = muon->et();
      lepton->Charge = muon->charge();
      
      lepton->TrkIso = muon->trackIso();
      lepton->CaloIso   = muon->caloIso();
      
      // new MIP variables: deposit of the muon in calorimeter 
      //          (needed for veto cone cut)
      // FIXME: segfaults here
      //lepton->isoDepECal = muon->ecalIsoDeposit()->candEnergy();
      //lepton->isoDepHCal = muon->hcalIsoDeposit()->candEnergy();
      lepton->isoDepECal = muon->ecalIso();
      lepton->isoDepHCal = muon->hcalIso();
      
      // -- TRACK --- 
      // be aware: muon->track() gives the tracker track (= innerTrack)
      //           muon->globalTrack gives the global track!

      // get global track:
      reco::TrackRef globalTrkRef = muon->globalTrack();
      lepton->TrkNhits = globalTrkRef->numberOfValidHits();
      lepton->TrkChi2  = globalTrkRef->chi2()/globalTrkRef->ndof();
      
      if (vertices->size() != 0) {
       	lepton->Trkd0          = globalTrkRef->dxy( vertices->begin()->position() );
       	lepton->SigmaD0        = globalTrkRef->dxyError();
      } 
      else {
       	lepton->Trkd0    = globalTrkRef->d0();
       	lepton->SigmaD0  = globalTrkRef->d0Error();
      }
      
      // get silicon fit track (= inner track):
      reco::TrackRef innerTrkRef = muon->innerTrack();
      lepton->innerTrkNhits = innerTrkRef->numberOfValidHits();
      lepton->innerTrkChi2  = innerTrkRef->chi2()/innerTrkRef->ndof();
      
      if (vertices->size() != 0) {
       	lepton->innerTrkd0          = innerTrkRef->dxy( vertices->begin()->position() );
       	lepton->innerSigmaD0        = innerTrkRef->dxyError();
      } 
      else {
       	lepton->innerTrkd0    = innerTrkRef->d0();
       	lepton->innerSigmaD0  = innerTrkRef->d0Error();
      }
      
      lepton->NumberOfTracks =  muon->numberOfTracks();
      lepton->id = CatoCMSDef::MUON; 
			lepton->isGlobalTightMu = muon::isGoodMuon(*muon, muon::GlobalMuonPromptTight);
    }
    
#if DEBUG
    cout << "muon pT = " << muon->pt() 
	 << "\t muon eta = " << muon->eta() << endl;
#endif
  }
  
#if DEBUG
  cout << "number of leptons = " << cev->lepVec.size() << endl;
#endif
    
  
  // ------------------
  //   trigger query
  // ------------------

#if DEBUG
	cout << "this is trigger" << endl;
#endif

  CatoCMSTrigger ctrigger;
  ctrigger.Reset();

  if(triggerInfo){
    Handle<TriggerResults> h_trigRes;
    //  iEvent.getByLabel(InputTag("TriggerResults::HLT"), h_trigRes);
    iEvent.getByLabel(edm::InputTag("TriggerResults", "", "HLT"), h_trigRes); // Claudio
    if ( h_trigRes.failedToGet() ) throw cms::Exception("fail", "failed to get trigRes");
    edm::TriggerNames trgNames;
    trgNames.init(*h_trigRes);
    MuTrigIdx = trgNames.triggerIndex(triggernames[0]);
    EleTrigIdx = trgNames.triggerIndex(triggernames[1]);
    
    if ( MuTrigIdx==trgNames.size() ) throw cms::Exception("fail", "mu trig");
    else ctrigger.mu = h_trigRes->accept(MuTrigIdx);
    
    if ( EleTrigIdx==trgNames.size() ) throw cms::Exception("fail", "ele trig");
    else ctrigger.el = h_trigRes->accept(EleTrigIdx);
    
    TriggerResults tr;
    tr = *h_trigRes;
    
    vector<string> triggerList;
    
    // dump trigger list at first event
    if (info->TotalEvents == 1){
      Service<service::TriggerNamesService> tns;
      bool foundNames = tns->getTrigPaths(tr,triggerList);
      if (!foundNames) 
	cout <<"could not get trigger names!\n";
      if (tr.size()!=triggerList.size()) 
	cout << "ERROR: length of names and paths not the same: " << triggerList.size() << "," << tr.size() << endl;
      cout << "List of triggers: \n";
      for(unsigned int i=0; i< triggerList.size(); i++) {
	cout.width(3); cout << i;
	cout << " - " << triggerList[i] << endl;
      }
      cout << "*** What I am using right now as muon trigger is index " << MuTrigIdx << endl;
    }

  } // end of IF for trigger info

  
  //------------------
  // JetMET
  //------------------
  
  CatoCMSMET cmet;
  cmet.Reset();
  
  // MET -----------------

#if DEBUG
	cout << "this is met" << endl;
#endif
  
  Handle<vector<pat::MET> > metHa;
  iEvent.getByLabel(metProducer, metHa);
  const vector<pat::MET>* mets = metHa.product();
  const pat::MET met = mets->front();
  
 
  cmet.v4.SetCoordinates(met.px(), met.py(),0.0,0.0);
  
  // MET Corrections:
  cmet.dmEx = ((MET)met).dmEx();         
  cmet.dmEy = ((MET)met).dmEy();
  
  //  cmet.sumEt = ((MET)met).sumEt();
  cmet.sumEt = met.sumEt();
  

#if DEBUG
  cout << "MET = " << met.pt()<< "\n" << endl;
#endif
  
  // Jets ------------------
  Handle<vector<pat::Jet> > jetHa;
  iEvent.getByLabel(jetProducer, jetHa);
  const vector<pat::Jet>* jets = jetHa.product();
  
  CatoCMSJet *catoJet = 0;
  
  int nJets = 0, nLooseJets = 0;
  
  // ---- jet loop 
  for(vector<pat::Jet>::const_iterator it = jets->begin();
      it != jets->end(); it++){
    
    double scale = 1.;
    if (it->hasCorrFactors()) {
      std::string correction = "RAW";
      scale = it->corrFactor(correction);
      //      cout << "jetCorrName: " << it->jetCorrName() << endl;
    } 
    else {
      cout << "This jet has no jet correction factors" << endl;
    }
    
    double jetPT = it->pt();
    

    
    if(jetPT >= jet_loosecut_pt && fabs(it->eta())< jet_cut_eta){
      
      if(jetPT > jet_tightcut_pt){
	//create Jet --------------
	catoJet = cev->NewJet();
	nJets++;
      }
      else{
	//create LooseJet ----------------
	catoJet = cev->NewLooseJet();
	nLooseJets++;
      }
      if(!catoJet){
	cout << "!!!!!!!!!!!!!jetPointer not valid..?????????????????????\n"
	     << "continue with next jet\n";
	continue;
      }
      
      //fill jet infos --------------------
      catoJet->v4.SetCoordinates(it->px(), it->py(), 
			     it->pz(), it->energy());
			     
      catoJet->scale = scale;

      std::pair<std::string, double> tag;

      //FIXME: names changed, need to check ?
      // see RecoBTag/Configuration/python/RecoBTag_EventContent_cff.py
      tag.first  = "trackCountingHighEffBJetTags";
      tag.second = it->bDiscriminator(tag.first);
      catoJet->tags.insert(tag);
      
      tag.first  = "combinedSecondaryVertexBJetTags";
      tag.second = it->bDiscriminator(tag.first);
      catoJet->tags.insert(tag);
      
      tag.first  = "combinedSecondaryVertexMVABJetTags";
      tag.second = it->bDiscriminator(tag.first);
      catoJet->tags.insert(tag);

      tag.first	 = "simpleSecondaryVertexBJetTags";
      tag.second = it->bDiscriminator(tag.first);
      catoJet->tags.insert(tag);
      
      //tag.first  = "impactParameterMVABJetTags"; // ?
      //tag.second = it->bDiscriminator(tag.first);
      //catoJet->tags.insert(tag);
      
      tag.first  = "jetProbabilityBJetTags";
      tag.second = it->bDiscriminator(tag.first);
      catoJet->tags.insert(tag);
      
      tag.first  = "softElectronBJetTags";
      tag.second = it->bDiscriminator(tag.first);
      catoJet->tags.insert(tag);
      
      tag.first  = "softMuonBJetTags";
      tag.second = it->bDiscriminator(tag.first);
      catoJet->tags.insert(tag);

      //tag.first  = "softMuonNoIPBJetTags"; // ?
      //tag.second = it->bDiscriminator(tag.first);
      //catoJet->tags.insert(tag);

      tag.first  = "trackCountingHighPurBJetTags";
      tag.second = it->bDiscriminator(tag.first);
      catoJet->tags.insert(tag);

      catoJet->emEnergyFraction = it->emEnergyFraction();
      catoJet->nTracks = it->associatedTracks().size();

      catoJet->partonFlavour = it->partonFlavour();
      
      catoJet->vertex.SetCoordinates(it->vx(),it->vy(),it->vz());
      
      cev->sumEtJet += it->et();
      cev->sumEtJetRaw += it->et()/scale;

#if DEBUG
      cout << "btag  " << it->bDiscriminator("trackCountingHighPurBJetTags") 
	   <<  "\n";
#endif
    }
  }
  
  //==================
  //     Fill PDF Info
  //==================
  cev->pdfinfo = cpdfinfo;


  // ===================
  //     Fill Trigger Info
  // ===================
  cev->trigger = ctrigger;
  
  // ===================
  //     Fill MET Info
  // ===================
  cev->met = cmet;
  
  // =================================
  //   --- accept / reject event (OPTIONAL) ---
  // =================================

  
  // fill "Total" cut flow table:
  int JetN = cev->jetVec.size();
  mycft->addEvent();
  mycft->add("cut","Total",JetN);
  
  if (doPresel && countGoodElectrons==0 && countGoodMuons==0) return;
 
  // fill "Preselected" cft:
  if(countGoodElectrons>0 || countGoodMuons>0)
    mycft->add("cut","Preselected",JetN);

  // > 0jets!
  /*
  if(cev->jetVec.size() > 0 || cev->looseJetVec.size() >0){
    cev->nJets = cev->jetVec.size(); 
    cev->nLooseJets = cev->looseJetVec.size();
    cev->nBtags = 0;
    cev->nLooseBtags = 0;
  }
  else
    return;
  */
  if (doPresel && no0jets && (cev->jetVec.size()==0 || cev->looseJetVec.size()==0)) return;

  cev->nJets = cev->jetVec.size(); 
  cev->nLooseJets = cev->looseJetVec.size();
  cev->nBtags = 0;
  cev->nLooseBtags = 0;
 
  
  if(DecChan == 0 || DecChan%10 == 0)
    remainingLepJetsEv++;

  else if(DecChan == 1 || DecChan%10 == 1)
    remainingTauJetsEv++;

  else if(DecChan == 2 || DecChan%10 == 2)
    remainingHadEv++;

  else
    remainingDiLepEv++;
  

  miniTree->Fill();
  
}

void Preselection::MCStatOut(ostream& os)
{ double totalEvents = lepJetEv + tauJetEv + diLepEv + hadEv;
  double eventsAfterSel = remainingLepJetsEv + remainingTauJetsEv + remainingDiLepEv + remainingHadEv;
    os << "Monte Carlo Statistics" << endl << endl
       << "total events  : " << totalEvents << "\t100 %\n"
       << "\t --------------------------\n"
       << "\t lep+jets : " << lepJetEv << "\t"
       << lepJetEv/totalEvents*100 << " %\n"

       << "\t tau+jets : " << tauJetEv << "\t"
       << tauJetEv/totalEvents*100 << " %\n"

       << "\t dilep    : " << diLepEv  << "\t"
       << diLepEv/totalEvents*100  << " %\n"

       << "\t had      : " << hadEv    << "\t"
       << hadEv/totalEvents*100    << " %\n"

       << "\t --------------------------\n"
       << "\t lost lep+jets : " << lepJetEv-remainingLepJetsEv  << "\n"
       << "\t lost tau+jets : " << tauJetEv-remainingTauJetsEv  << "\n\n"

       << "remaining events : " << eventsAfterSel 
       << "\t(all "     << eventsAfterSel/totalEvents*100 << "%)\n"

       << "\t --------------------------\n"
       << "\t rem lep+jets : " << remainingLepJetsEv
       << "\t" << remainingLepJetsEv/eventsAfterSel*100 << " %\n"

       << "\t rem tau+jets : " << remainingTauJetsEv
       << "\t" << remainingTauJetsEv/eventsAfterSel*100 << " %\n"

       << "\t rem dilep    : " << remainingDiLepEv
       << "\t" << remainingDiLepEv/eventsAfterSel*100   << " %\n"

       << "\t rem had      : " << remainingHadEv
       << "\t" << remainingHadEv/eventsAfterSel*100     << " %\n"
       << "\n\n";   
    

}

//define this as a plug-in
DEFINE_FWK_MODULE(Preselection);

