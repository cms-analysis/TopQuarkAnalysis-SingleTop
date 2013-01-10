#!/usr/bin/env python

import sys
if not '-b' in sys.argv:
    sys.argv.append( '-b' )
    
from ROOT import *

RunA = True
RunB = True
RunC = True
    
fileList = ['TWChannel.root',
            'TTbar.root',
            'TChannel.root',
            'SChannel.root',
#            'ZJets.root',
            'WJets.root',
            'WW.root',
            'WZ.root',
            'ZZ.root']#,
#            'DATA']


fileHistoInput = [0,
                  1,
                  2,
                  2,
                  2,
                  2,
                  2,
                  2]

DataChannel = ['MuEG','DoubleMu','DoubleElectron']
Folder = ['emuChannel','mumuChannel','eeChannel']
ChanName = ['emu','mumu','ee']

Systs = ['JER','JES','UnclusteredMET']

regions = ['1j1t','2j1t','2j2t']

HistoLists = list()
for chan in ChanName:
    chanList = list()
    for reg in regions:
        tw = TH1F(chan+reg+ "__twdr","",50,0,200)
        tw.Sumw2()
        tt = TH1F(chan+reg+ "__tt","",50,0,200)
        tt.Sumw2()
        other = TH1F(chan+reg+ "__other","",50,0,200)
        other.Sumw2()
        data = TH1F(chan+reg+ "__DATA","",50,0,200)
        twList = list()
        ttList = list()
        otherList = list()
        dataList = list()
        twsyst = list()
        ttsyst = list()
        othersyst = list()
        
        

        for syst in Systs:
            twsystUp = TH1F(chan+reg+ "__twdr__"+syst + "__plus","",50,0,200)
            twsystDown = TH1F(chan+reg+ "__twdr__"+syst + "__minus","",50,0,200)
            tempsystTW = [twsystUp,twsystDown]
            ttbarsystUp = TH1F(chan+reg+ "__tt__"+syst + "__plus","",50,0,200)
            ttbarsystDown = TH1F(chan+reg+ "__tt__"+syst + "__minus","",50,0,200)
            tempsystTT = [ttbarsystUp,ttbarsystDown]
            othersystUp = TH1F(chan+reg+ "__other__"+syst + "__plus","",50,0,200)
            othersystDown = TH1F(chan+reg+ "__other__"+syst + "__minus","",50,0,200)
            tempsystOTHER = [othersystUp,othersystDown]
            twsyst.append(tempsystTW)
            ttsyst.append(tempsystTT)
            othersyst.append(tempsystOTHER)
        twList.append(tw)
        twList.append(twsyst)
        ttList.append(tt)
        ttList.append(ttsyst)
        otherList.append(other)
        otherList.append(othersyst)
        dataList.append(data)
        regionList = list()
        regionList.append(twList)
        regionList.append(ttList)
        regionList.append(otherList)
        regionList.append(dataList)
        chanList.append(regionList)
    HistoLists.append(chanList)


for chan in range(3):
    for reg in range(3):
        for fileNum in range(len(fileList)):
            file = fileList[fileNum]

            tree = TChain(Folder[chan]+'/'+regions[reg])
            fileName = file
            print fileName
            tree.Add('tmvaFiles/'+fileName)


            nEvents = tree.GetEntries()*1.

            print nEvents
            
            evtCount = 0.
            percent = 0.0
            progSlots = 25.    
            
            for event in tree:
                evtCount += 1.
                if evtCount/nEvents > percent:
                    k = int(percent*progSlots)
                    progress = '0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                    sys.stdout.write(progress)
                    sys.stdout.flush()
                    percent += 1./progSlots



                _ptsys                     = event.ptsys                   
            
                _weightA                    = event.weightA
                _weightB                    = event.weightB
                _weightC                    = event.weightC

                _weight = 0

                if RunA:
                    _weight = _weight + _weightA
                if RunB:
                    _weight = _weight + _weightB
                if RunC:
                    _weight = _weight + _weightC

                HistoLists[chan][reg][fileHistoInput[fileNum]][0].Fill(_ptsys, _weight)
                HistoLists[chan][reg][-1][0].Fill(_ptsys, _weight)

            for s in range(len(Systs)):
                syst = Systs[s]
                tree = TChain(Folder[chan]+'/'+regions[reg])
                fileName = file.replace('.ro','_'+syst+'Up.ro')
                print fileName
                tree.Add('tmvaFiles/'+fileName)


                nEvents = tree.GetEntries()*1.

                print nEvents
            
                evtCount = 0.
                percent = 0.0
                progSlots = 25.    
            
                for event in tree:
                    evtCount += 1.
                    if evtCount/nEvents > percent:
                        k = int(percent*progSlots)
                        progress = '0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                        sys.stdout.write(progress)
                        sys.stdout.flush()
                        percent += 1./progSlots



                    _ptsys                     = event.ptsys                   
            
                    _weightA                    = event.weightA
                    _weightB                    = event.weightB
                    _weightC                    = event.weightC
                    
                    _weight = 0

                    if RunA:
                        _weight = _weight + _weightA
                    if RunB:
                        _weight = _weight + _weightB
                    if RunC:
                        _weight = _weight + _weightC

                    HistoLists[chan][reg][fileHistoInput[fileNum]][1][s][0].Fill(_ptsys, _weight)


                tree = TChain(Folder[chan]+'/'+regions[reg])
                fileName = file.replace('.ro','_'+syst+'Down.ro')
                print fileName
                tree.Add('tmvaFiles/'+fileName)


                nEvents = tree.GetEntries()*1.

                print nEvents
            
                evtCount = 0.
                percent = 0.0
                progSlots = 25.    
            
                for event in tree:
                    evtCount += 1.
                    if evtCount/nEvents > percent:
                        k = int(percent*progSlots)
                        progress = '0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                        sys.stdout.write(progress)
                        sys.stdout.flush()
                        percent += 1./progSlots



                    _ptsys                     = event.ptsys                   
            
                    _weightA                    = event.weightA
                    _weightB                    = event.weightB
                    _weightC                    = event.weightC
                    
                    _weight = 0

                    if RunA:
                        _weight = _weight + _weightA
                    if RunB:
                        _weight = _weight + _weightB
                    if RunC:
                        _weight = _weight + _weightC

                    HistoLists[chan][reg][fileHistoInput[fileNum]][1][s][1].Fill(_ptsys, _weight)

outFile = TFile('thetaInput_ptsysTEST.root','RECREATE')

for chan in HistoLists:
    for reg in chan:
        for sample in reg:
            sample[0].Write()

for chan in HistoLists:
    for reg in chan:
        for sample in reg:
            if len(sample) >1:
                for syst in sample[1]:
                    syst[0].Write()
                    syst[1].Write()


                    
