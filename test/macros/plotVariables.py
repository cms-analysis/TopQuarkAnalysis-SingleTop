#!/usr/bin/env python                                                                                          \

import sys
from ROOT import *

plotInfo = [['ptjet',60,0,300],
            ['ptlep0',60,0,300],
            ['ptlep1',60,0,300],
            ['jetCSV',100,0,1],
            ['ht',100,0,500],
            ['htNoMet',100,0,500],
            ['msys',60,0,600],
            ['mjll',60,0,600],
            ['mjl0',60,0,600],
            ['mjl1',60,0,600],
            ['ptsys',60,0,300],
            ['ptjll',60,0,300],
            ['ptjl0',60,0,300],
            ['ptjl1',60,0,300],
            ['ptleps',60,0,300],
            ['htleps',60,0,300],
            ['ptsys_ht',100,0,1],
            ['ptjet_ht',100,0,1],
            ['ptlep0_ht',100,0,1],
            ['ptlep1_ht',100,0,1],
            ['ptleps_ht',100,0,1],
            ['htleps_ht',100,0,1],
            ['NlooseJet15Central',10,0,10],
            ['NlooseJet15Forward',10,0,10],
            ['NlooseJet20Central',10,0,10],
            ['NlooseJet20Forward',10,0,10],
            ['NlooseJet25Central',10,0,10],
            ['NlooseJet25Forward',10,0,10],
            ['NtightJetForward',10,0,10],            
            ['NlooseJet15',10,0,10],
            ['NlooseJet20',10,0,10],
            ['NlooseJet25',10,0,10],
            ['NbtaggedlooseJet15',4,0,4],
            ['NbtaggedlooseJet20',4,0,4],
            ['NbtaggedlooseJet25',4,0,4],
            ['unweightedEta_Avg', 300,0,30],
            ['unweightedEta_Vecjll', 300,0,30],
            ['unweightedEta_Vecsys', 300,0,30],
            ['unweightedPhi_Avg', 300,0,30],
            ['unweightedPhi_Vecjll', 300,0,30],
            ['unweightedPhi_Vecsys', 300,0,30],
            ['avgEta', 100, 0,5],
            ['sysEta', 100, 0,5],
            ['jllEta', 100, 0,5],
            ['dRleps', 100, 0,10],
            ['dRjlmin', 100, 0,10],
            ['dRjlmax', 100, 0,10],
            ['dEtaleps', 100, 0,10],
            ['dEtajlmin', 100, 0,10],
            ['dEtajlmax', 100, 0,10],
            ['dPhileps', 100, 0,3.15],
            ['dPhijlmin', 100, 0,3.15],
            ['dPhijlmax', 100, 0,3.15],
            ['dPhimetlmin',100,0,3.15],
            ['dPhimetlmax',100,0,3.15],
            ['dPhijmet',100,0,3.15],
            ['met', 60, 0, 300],
            ['etajet', 100, 0, 5],
            ['etalep0', 100, 0, 5],
            ['etalep1', 100, 0, 5],
            ['phijet', 100, -3.15, 3.15],
            ['philep0', 100, -3.15, 3.15],
            ['philep1', 100, -3.15, 3.15],
            ['phimet', 100, -3.15, 3.15],
            ['sumeta2', 100, 0, 15],
            ['loosejetPt', 60, 0, 300],
            ['loosejetCSV', 175, -0.75, 1.0],
            ['centralityJLL',100,0,1],
            ['centralityJLLM',100,0,1],
            ['centralityJLLWithLoose',100,0,1],
            ['centralityJLLMWithLoose',100,0,1],
            ['sphericityJLL',100,0,1],
            ['sphericityJLLM',100,0,1],
            ['sphericityJLLWithLoose',100,0,1],
            ['sphericityJLLMWithLoose',100,0,1],
            ['aplanarityJLL',100,0,.5],
            ['aplanarityJLLM',100,0,.5],
            ['aplanarityJLLWithLoose',100,0,.5],
            ['aplanarityJLLMWithLoose',100,0,.5],

            ]

fileLists = ['TWChannel.root',
             'TTbar.root',
             'TChannel.root',
             'SChanel.root',
             'ZJets.root',
             'WJets.root',
             'WW.root',
             'WZ.root',
             'ZZ.root']

Colors = ['kWhite',
          'kRed',
          'kBlue',
          'kBlue',
          'kBlue',
          'kBlue',
          'kBlue',
          'kBlue',
          'kBlue']

# DataChannel = ['DoubleMu']
# DataRun = ['Run2012A','Run2012B','Run2012C']

HistoLists = list()

for i in range(len(fileList)):
    Histos = dict()

    for plot in plotInfo:
        Histos[plot[0]] = TH1F(plot[0],plot[0],plot[1],plot[2],plot[3])
        Histos[plot[0]].SetFillColor(Colors[i])
    HistoLists.append(Histos)


for i in range(len(fileList)):
    print fileList[i]
    
    file = TFile(fileList[i],'r')

    treeName = 'mumuChannel/2j0t'

    tree = gROOT.FindObject(treeName)

    nEvents = tWtree.GetEntries()*1.

    evtCount = 0.
    percent = 0.0
    progSlots = 25.    

    for event in tree:
        evtCount += 1.
        if evtCount/nEvents > percent:
            i = int(percent*progSlots)
            progress = '0%[' + '-' * i + ' ' * (int(progSlots)-i) + ']100%\r'
            sys.stdout.write(progress)
            sys.stdout.flush()
            percent += 1./progSlots





        _ptjet                     = event.ptjet                   
        _ptlep0                    = event.ptlep0                  
        _ptlep1                    = event.ptlep1                  
        _jetCSV                    = event.jetCSV                  
        _ht                        = event.ht                      
        _htNoMet                   = event.htNoMet                 
        _msys                      = event.msys                    
        _mjll                      = event.mjll                    
        _mjl0                      = event.mjl0                    
        _mjl1                      = event.mjl1                    
        _ptsys                     = event.ptsys                   
        _ptjll                     = event.ptjll                   
        _ptjl0                     = event.ptjl0                   
        _ptjl1                     = event.ptjl1                   
        _ptleps                    = event.ptleps                  
        _htleps                    = event.htleps                  
        _ptsys_ht                  = event.ptsys_ht                
        _ptjet_ht                  = event.ptjet_ht                
        _ptlep0_ht                 = event.ptlep0_ht               
        _ptlep1_ht                 = event.ptlep1_ht               
        _ptleps_ht                 = event.ptleps_ht               
        _htleps_ht                 = event.htleps_ht               
        _NlooseJet15Central        = event.NlooseJet15Central      
        _NlooseJet15Forward        = event.NlooseJet15Forward      
        _NlooseJet20Central        = event.NlooseJet20Central      
        _NlooseJet20Forward        = event.NlooseJet20Forward      
        _NlooseJet25Central        = event.NlooseJet25Central      
        _NlooseJet25Forward        = event.NlooseJet25Forward      
        _NtightJetForward          = event.NtightJetForward        
        _NlooseJet15               = event.NlooseJet15             
        _NlooseJet20               = event.NlooseJet20             
        _NlooseJet25               = event.NlooseJet25             
        _NbtaggedlooseJet15        = event.NbtaggedlooseJet15      
        _NbtaggedlooseJet20        = event.NbtaggedlooseJet20      
        _NbtaggedlooseJet25        = event.NbtaggedlooseJet25      
        _unweightedEta_Avg         = event.unweightedEta_Avg       
        _unweightedEta_Vecjll      = event.unweightedEta_Vecjll    
        _unweightedEta_Vecsys      = event.unweightedEta_Vecsys    
        _unweightedPhi_Avg         = event.unweightedPhi_Avg       
        _unweightedPhi_Vecjll      = event.unweightedPhi_Vecjll    
        _unweightedPhi_Vecsys      = event.unweightedPhi_Vecsys    
        _avgEta                    = event.avgEta                  
        _sysEta                    = event.sysEta                  
        _jllEta                    = event.jllEta                  
        _dRleps                    = event.dRleps                  
        _dRjlmin                   = event.dRjlmin                 
        _dRjlmax                   = event.dRjlmax                 
        _dEtaleps                  = event.dEtaleps                
        _dEtajlmin                 = event.dEtajlmin               
        _dEtajlmax                 = event.dEtajlmax               
        _dPhileps                  = event.dPhileps                
        _dPhijlmin                 = event.dPhijlmin               
        _dPhijlmax                 = event.dPhijlmax               
        _dPhimetlmin               = event.dPhimetlmin             
        _dPhimetlmax               = event.dPhimetlmax             
        _dPhijmet                  = event.dPhijmet                
        _met                       = event.met                     
        _etajet                    = event.etajet                  
        _etalep0                   = event.etalep0                 
        _etalep1                   = event.etalep1                 
        _phijet                    = event.phijet                  
        _philep0                   = event.philep0                 
        _philep1                   = event.philep1                 
        _phimet                    = event.phimet                  
        _sumeta2                   = event.sumeta2                 
        _loosejetPt                = event.loosejetPt              
        _loosejetCSV               = event.loosejetCSV             
        _centralityJLL             = event.centralityJLL           
        _centralityJLLM            = event.centralityJLLM          
        _centralityJLLWithLoose    = event.centralityJLLWithLoose  
        _centralityJLLMWithLoose   = event.centralityJLLMWithLoose 
        _sphericityJLL             = event.sphericityJLL           
        _sphericityJLLM            = event.sphericityJLLM          
        _sphericityJLLWithLoose    = event.sphericityJLLWithLoose  
        _sphericityJLLMWithLoose   = event.sphericityJLLMWithLoose 
        _aplanarityJLL             = event.aplanarityJLL           
        _aplanarityJLLM            = event.aplanarityJLLM          
        _aplanarityJLLWithLoose    = event.aplanarityJLLWithLoose  
        _aplanarityJLLMWithLoose   = event.aplanarityJLLMWithLoose 
        
        _weight                   = event.weight

        

        HistoLists[i]['ptjet'].Fill(                    _ptjet                    , _weight )
        HistoLists[i]['ptlep0'].Fill(                   _ptlep0                   , _weight )
        HistoLists[i]['ptlep1'].Fill(                   _ptlep1                   , _weight )
        HistoLists[i]['jetCSV'].Fill(                   _jetCSV                   , _weight )
        HistoLists[i]['ht'].Fill(                       _ht                       , _weight )
        HistoLists[i]['htNoMet'].Fill(                  _htNoMet                  , _weight )
        HistoLists[i]['msys'].Fill(                     _msys                     , _weight )
        HistoLists[i]['mjll'].Fill(                     _mjll                     , _weight )
        HistoLists[i]['mjl0'].Fill(                     _mjl0                     , _weight )
        HistoLists[i]['mjl1'].Fill(                     _mjl1                     , _weight )
        HistoLists[i]['ptsys'].Fill(                    _ptsys                    , _weight )
        HistoLists[i]['ptjll'].Fill(                    _ptjll                    , _weight )
        HistoLists[i]['ptjl0'].Fill(                    _ptjl0                    , _weight )
        HistoLists[i]['ptjl1'].Fill(                    _ptjl1                    , _weight )
        HistoLists[i]['ptleps'].Fill(                   _ptleps                   , _weight )
        HistoLists[i]['htleps'].Fill(                   _htleps                   , _weight )
        HistoLists[i]['ptsys_ht'].Fill(                 _ptsys_ht                 , _weight )
        HistoLists[i]['ptjet_ht'].Fill(                 _ptjet_ht                 , _weight )
        HistoLists[i]['ptlep0_ht'].Fill(                _ptlep0_ht                , _weight )
        HistoLists[i]['ptlep1_ht'].Fill(                _ptlep1_ht                , _weight )
        HistoLists[i]['ptleps_ht'].Fill(                _ptleps_ht                , _weight )
        HistoLists[i]['htleps_ht'].Fill(                _htleps_ht                , _weight )
        HistoLists[i]['NlooseJet15Central'].Fill(       _NlooseJet15Central       , _weight )
        HistoLists[i]['NlooseJet15Forward'].Fill(       _NlooseJet15Forward       , _weight )
        HistoLists[i]['NlooseJet20Central'].Fill(       _NlooseJet20Central       , _weight )
        HistoLists[i]['NlooseJet20Forward'].Fill(       _NlooseJet20Forward       , _weight )
        HistoLists[i]['NlooseJet25Central'].Fill(       _NlooseJet25Central       , _weight )
        HistoLists[i]['NlooseJet25Forward'].Fill(       _NlooseJet25Forward       , _weight )
        HistoLists[i]['NtightJetForward'].Fill(         _NtightJetForward         , _weight )
        HistoLists[i]['NlooseJet15'].Fill(              _NlooseJet15              , _weight )
        HistoLists[i]['NlooseJet20'].Fill(              _NlooseJet20              , _weight )
        HistoLists[i]['NlooseJet25'].Fill(              _NlooseJet25              , _weight )
        HistoLists[i]['NbtaggedlooseJet15'].Fill(       _NbtaggedlooseJet15       , _weight )
        HistoLists[i]['NbtaggedlooseJet20'].Fill(       _NbtaggedlooseJet20       , _weight )
        HistoLists[i]['NbtaggedlooseJet25'].Fill(       _NbtaggedlooseJet25       , _weight )
        HistoLists[i]['unweightedEta_Avg'].Fill(        _unweightedEta_Avg        , _weight )
        HistoLists[i]['unweightedEta_Vecjll'].Fill(     _unweightedEta_Vecjll     , _weight )
        HistoLists[i]['unweightedEta_Vecsys'].Fill(     _unweightedEta_Vecsys     , _weight )
        HistoLists[i]['unweightedPhi_Avg'].Fill(        _unweightedPhi_Avg        , _weight )
        HistoLists[i]['unweightedPhi_Vecjll'].Fill(     _unweightedPhi_Vecjll     , _weight )
        HistoLists[i]['unweightedPhi_Vecsys'].Fill(     _unweightedPhi_Vecsys     , _weight )
        HistoLists[i]['avgEta'].Fill(                   _avgEta                   , _weight )
        HistoLists[i]['sysEta'].Fill(                   _sysEta                   , _weight )
        HistoLists[i]['jllEta'].Fill(                   _jllEta                   , _weight )
        HistoLists[i]['dRleps'].Fill(                   _dRleps                   , _weight )
        HistoLists[i]['dRjlmin'].Fill(                  _dRjlmin                  , _weight )
        HistoLists[i]['dRjlmax'].Fill(                  _dRjlmax                  , _weight )
        HistoLists[i]['dEtaleps'].Fill(                 _dEtaleps                 , _weight )
        HistoLists[i]['dEtajlmin'].Fill(                _dEtajlmin                , _weight )
        HistoLists[i]['dEtajlmax'].Fill(                _dEtajlmax                , _weight )
        HistoLists[i]['dPhileps'].Fill(                 _dPhileps                 , _weight )
        HistoLists[i]['dPhijlmin'].Fill(                _dPhijlmin                , _weight )
        HistoLists[i]['dPhijlmax'].Fill(                _dPhijlmax                , _weight )
        HistoLists[i]['dPhimetlmin'].Fill(              _dPhimetlmin              , _weight )
        HistoLists[i]['dPhimetlmax'].Fill(              _dPhimetlmax              , _weight )
        HistoLists[i]['dPhijmet'].Fill(                 _dPhijmet                 , _weight )
        HistoLists[i]['met'].Fill(                      _met                      , _weight )
        HistoLists[i]['etajet'].Fill(                   _etajet                   , _weight )
        HistoLists[i]['etalep0'].Fill(                  _etalep0                  , _weight )
        HistoLists[i]['etalep1'].Fill(                  _etalep1                  , _weight )
        HistoLists[i]['phijet'].Fill(                   _phijet                   , _weight )
        HistoLists[i]['philep0'].Fill(                  _philep0                  , _weight )
        HistoLists[i]['philep1'].Fill(                  _philep1                  , _weight )
        HistoLists[i]['phimet'].Fill(                   _phimet                   , _weight )
        HistoLists[i]['sumeta2'].Fill(                  _sumeta2                  , _weight )
        HistoLists[i]['loosejetPt'].Fill(               _loosejetPt               , _weight )
        HistoLists[i]['loosejetCSV'].Fill(              _loosejetCSV              , _weight )
        HistoLists[i]['centralityJLL'].Fill(            _centralityJLL            , _weight )
        HistoLists[i]['centralityJLLM'].Fill(           _centralityJLLM           , _weight )
        HistoLists[i]['centralityJLLWithLoose'].Fill(   _centralityJLLWithLoose   , _weight )
        HistoLists[i]['centralityJLLMWithLoose'].Fill(  _centralityJLLMWithLoose  , _weight )
        HistoLists[i]['sphericityJLL'].Fill(            _sphericityJLL            , _weight )
        HistoLists[i]['sphericityJLLM'].Fill(           _sphericityJLLM           , _weight )
        HistoLists[i]['sphericityJLLWithLoose'].Fill(   _sphericityJLLWithLoose   , _weight )
        HistoLists[i]['sphericityJLLMWithLoose'].Fill(  _sphericityJLLMWithLoose  , _weight )
        HistoLists[i]['aplanarityJLL'].Fill(            _aplanarityJLL            , _weight )
        HistoLists[i]['aplanarityJLLM'].Fill(           _aplanarityJLLM           , _weight )
        HistoLists[i]['aplanarityJLLWithLoose'].Fill(   _aplanarityJLLWithLoose   , _weight )
        HistoLists[i]['aplanarityJLLMWithLoose'].Fill(  _aplanarityJLLMWithLoose  , _weight )


for plot in plotInfo:
    hStack = THStack(plot[0],plot[0])
    hStack.Add(HistosList[8])
    hStack.Add(HistosList[7])
    hStack.Add(HistosList[6])
    hStack.Add(HistosList[5])
    hStack.Add(HistosList[4])
    hStack.Add(HistosList[3])
    hStack.Add(HistosList[2])
    hStack.Add(HistosList[1])
    hStack.Add(HistosList[0])

    c1 = TCanvas()
    hStack.Draw("histo")
    c1.SaveAs("plots/"+plot[0]+".png")























































# __ptjet                    
# __ptlep0                   
# __ptlep1                   
# __jetCSV                   
# __ht                       
# __htNoMet                  
# __msys                     
# __mjll                     
# __mjl0                     
# __mjl1                     
# __ptsys                    
# __ptjll                    
# __ptjl0                    
# __ptjl1                    
# __ptleps                   
# __htleps                   
# __ptsys_ht                 
# __ptjet_ht                 
# __ptlep0_ht                
# __ptlep1_ht                
# __ptleps_ht                
# __htleps_ht                
# __NlooseJet15Central       
# __NlooseJet15Forward       
# __NlooseJet20Central       
# __NlooseJet20Forward       
# __NlooseJet25Central       
# __NlooseJet25Forward       
# __NtightJetForward         
# __NlooseJet15              
# __NlooseJet20              
# __NlooseJet25              
# __NbtaggedlooseJet15       
# __NbtaggedlooseJet20       
# __NbtaggedlooseJet25       
# __unweightedEta_Avg        
# __unweightedEta_Vecjll     
# __unweightedEta_Vecsys     
# __unweightedPhi_Avg        
# __unweightedPhi_Vecjll     
# __unweightedPhi_Vecsys     
# __avgEta                   
# __sysEta                   
# __jllEta                   
# __dRleps                   
# __dRjlmin                  
# __dRjlmax                  
# __dEtaleps                 
# __dEtajlmin                
# __dEtajlmax                
# __dPhileps                 
# __dPhijlmin                
# __dPhijlmax                
# __dPhimetlmin              
# __dPhimetlmax              
# __dPhijmet                 
# __met                      
# __etajet                   
# __etalep0                  
# __etalep1                  
# __phijet                   
# __philep0                  
# __philep1                  
# __phimet                   
# __sumeta2                  
# __loosejetPt               
# __loosejetCSV              
# __centralityJLL            
# __centralityJLLM           
# __centralityJLLWithLoose   
# __centralityJLLMWithLoose  
# __sphericityJLL            
# __sphericityJLLM           
# __sphericityJLLWithLoose   
# __sphericityJLLMWithLoose  
# __aplanarityJLL            
# __aplanarityJLLM           
# __aplanarityJLLWithLoose   
# __aplanarityJLLMWithLoose  

