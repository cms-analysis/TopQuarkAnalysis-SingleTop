#!/usr/bin/env python

import sys
if not '-b' in sys.argv:
    sys.argv.append( '-b' )
    
from ROOT import *
from setTDRStyle import *
from array import array

import glob
import os

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
setTDRStyle()
gStyle.SetErrorX(0.5)

AllowedRegions = ['ZpeakLepSel']

region = 'ZpeakLepSel'
runPicked = False
RunA = False
RunB = False
RunC = False

TotalLumi = 0.

channelPicked = False
emuChan = False
mumuChan = False
eeChan = False

versionPicked = False

specialName = 'ZjetMET/'

noPlots = False

totals = list()
errors = list()
#for i in range(1,len(sys.argv)):
i = 1
while i < len(sys.argv):
    arg=sys.argv[i]
    if arg == '-b':
        i += 1
        continue
    elif 'plotVariables.p' in arg:
        i += 1
        continue
    elif arg in AllowedRegions:
        region = arg
    elif arg == 'A':
        RunA = True
        runPicked = True
    elif arg == 'B':
        RunB = True
        runPicked = True
    elif arg == 'C':
        RunC = True
        runPicked = True
    elif arg == 'emu':
        emuChan = True
        channelPicked = True
    elif arg == 'mumu':
        mumuChan = True
        channelPicked = True
    elif arg == 'ee':
        eeChan = True
        channelPicked = True        
    elif arg == '-v':
        i += 1
        versionPicked = True
        vFolder = sys.argv[i]
    elif arg == '-special':
        i+= 1
        specialName = specialName + sys.argv[i]        
        if not specialName[-1] == '/':
            specialName = specialName + '/'
    elif arg == 'noPlots':
        noPlots = True
    elif arg == 'help':
        print "------------------------"
        print "Help Menu"
        print "------------------------"
        print "Allowed arguments"
        print "   One of the following regions:"
        print "     ",AllowedRegions
        print "   'A' - use Run A"
        print "   'B' - use Run B"
        print "   'C' - use Run C"
        print "   'emu'  - do emu channel"
        print "   'mumu' - do mumu channel"
        print "   'ee'   - do ee channel"
        print "   '-v Folder' - specify the version folder inside tmvaFiles to be used"
        print "Default mode:"
        print " 1j1t region, using Runs A, B, & C, all three channels"
        exit()
    else:
        print "Unknown argument", arg," will be ignored"
    i += 1

        
if not runPicked:
    RunA = True
    RunB = True
    RunC = True

if not channelPicked:
    emuChan = True
    mumuChan = True
    eeChan = True

if not versionPicked:
    versionList = glob.glob("tmvaFiles/v*")
    versionList.sort(key=lambda a:int(a.split('/v')[-1]))
    vFolder = versionList[-1].split('/')[-1]    
    print vFolder

if RunA:
    TotalLumi = TotalLumi + 808.472+82.136
if RunB:
    TotalLumi = TotalLumi + 4429.
if RunC:
    TotalLumi = TotalLumi + 495.003+6383.

TotalLumi = TotalLumi/1000.

labelcms = TPaveText(0.1,0.88,0.6,0.92,"NDCBR")
labelcms.SetTextAlign(12);
labelcms.SetTextSize(0.045);
labelcms.SetFillColor(kWhite);
labelcms.AddText("CMS Preliminary, #sqrt{s} = 8 TeV");
labelcms.SetBorderSize(0);



doChannel = [emuChan, mumuChan, eeChan]
    
plotInfo = [['met', 60, 0, 300,'MET [GeV]']
            ]

fileList = ['TWChannel.root',
            'TTbar.root',
            'TChannel.root',
            'SChannel.root',
            'ZJets.root',
            'WJets.root',
            'WW.root',
            'WZ.root',
            'ZZ.root',
            'DATA']

Colors = [kWhite,
          kRed+1,
          kGreen-3,
          kAzure-3,
          kAzure-2,
          kGreen-3,
          kGreen-3,
          kGreen-3,
          kGreen-3,
          kBlack]



DataChannel = ['MuEG','DoubleMu','DoubleElectron']
Folder = ['emuChannel','mumuChannel','eeChannel']
ChanName = ['emu','mumu','ee']
ChanLabels = [', e#mu channel',', #mu#mu channel',', ee channel']
lumiLabel = "%.1f fb^{-1}" % TotalLumi

# DataRun = ['Run2012A','Run2012B','Run2012C']


for mode in range(1,3):

    if not doChannel[mode]:
        continue

    HistoLists = list()

    for i in range(len(fileList)):
        Histos = dict()

        fileName = fileList[i].split('.')[0]
        for plot in plotInfo:
            Histos[plot[0]] = TH1F(plot[0]+fileName+ChanName[mode]," ",plot[1],plot[2],plot[3])
            Histos[plot[0]].SetFillColor(Colors[i])
            Histos[plot[0]].SetLineColor(kBlack)
            Histos[plot[0]].SetLineWidth(1)
            Histos[plot[0]].SetMarkerSize(0.0001)
            Histos[plot[0]].Sumw2()
        HistoLists.append(Histos)

    for plot in plotInfo:
        HistoLists[-1][plot[0]].SetMarkerStyle(20)
        HistoLists[-1][plot[0]].SetMarkerSize(1.2)
        HistoLists[-1][plot[0]].SetLineWidth(2)
        HistoLists[-1][plot[0]].SetMarkerColor(kBlack)
        HistoLists[-1][plot[0]].SetLineColor(kBlack)
    
    for i in range(len(fileList)):

        print fileList[i]

        tree = TChain(Folder[mode]+'/'+region)

        if fileList[i] == 'DATA':
            if RunA:
                tree.Add('tmvaFiles/'+vFolder+'/Data_'+DataChannel[mode]+'_Run2012A.root')
            if RunB:
                tree.Add('tmvaFiles/'+vFolder+'/Data_'+DataChannel[mode]+'_Run2012B.root')
            if RunC:
                tree.Add('tmvaFiles/'+vFolder+'/Data_'+DataChannel[mode]+'_Run2012C.root')

        else:
            tree.Add('tmvaFiles/'+vFolder+'/'+fileList[i])
#             fName = 'tmvaFiles/'+fileList[i]
#             print fName
#             file = TFile(fName,'r')

#             file.cd(Folder[mode])
#             treeName = region
#             print 

#             tree = gROOT.FindObject(treeName)



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



            _met                       = event.met                     
            
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

            if fileList[i] == 'DATA':
                _weight = 1.


            HistoLists[i]['met'].Fill(                      _met                      , _weight )

        print

    errorHistTemp = TH1F("tempErr","tempErr",10,0,10)
    errorHistTemp.SetFillColor(kBlack)
    errorHistTemp.SetFillStyle(3003)
    
    leg = TLegend(0.66,0.66,0.94,0.94)
    leg.SetFillStyle(1)
    leg.SetFillColor(kWhite)
    leg.SetBorderSize(1)
    leg.AddEntry(HistoLists[-1]['met'], "Data", "p")
    leg.AddEntry(HistoLists[0]['met'], "tW", "f")
    leg.AddEntry(HistoLists[1]['met'], "t#bar{t}", "f")
    leg.AddEntry(HistoLists[4]['met'], "Z/#gamma*+jets", "f")
    leg.AddEntry(HistoLists[2]['met'], "Other", "f")
    leg.AddEntry(errorHistTemp, "Syst", "f")

    tot = list()
    err = list()

    for i in range(len(fileList)):
        tot.append(HistoLists[i]['met'].Integral())
        tempErr = 0
        for bin in range(1,plotInfo[0][1]+1):
            tempErr = tempErr + pow(HistoLists[i]['met'].GetBinError(bin),2)
        err.append(sqrt(tempErr))
    totals.append(tot)
    errors.append(err)


    if noPlots:
        continue

    labelcms2 = TPaveText(0.1,0.82,0.6,0.88,"NDCBR");
    labelcms2.SetTextAlign(12);
    labelcms2.SetTextSize(0.045);
    labelcms2.SetFillColor(kWhite);
    labelcms2.AddText(lumiLabel + ChanLabels[mode])
    labelcms2.SetBorderSize(0);

    labelcms3 = TPaveText(0.1,0.74,0.6,0.82,"NDCBR");
    labelcms3.SetTextAlign(12);
    labelcms3.SetTextSize(0.045);
    labelcms3.SetFillColor(kWhite);
    labelcms3.AddText(region)
    labelcms3.SetBorderSize(0);

    firstPlot = True


    bins = array('d',[0,5,10,15,20,25,30,40,50,75,100,150,200,300])
    bins = array('d',[0,5,10,15,20,25,30,40,50,75,300])
    plotInfo.append(['metBinned',1,0,1,'MET [GeV]'])
    for i in range(len(HistoLists)):            
        HistoLists[i]['metBinned'] = HistoLists[i]['met'].Rebin(len(bins)-1,'metBinned',bins)
        

    for plot in plotInfo:
        errorBand = HistoLists[0][plot[0]].Clone()
        for i in range(1,len(HistoLists)-1):
            errorBand.Add(HistoLists[i][plot[0]])
        for bin in range(errorBand.GetNbinsX()):
            error2 = 0
            for i in range(len(HistoLists)-1):
                error2 = error2 + pow(HistoLists[i][plot[0]].GetBinError(bin),2)
            error = sqrt(error2)
            errorBand.SetBinError(bin,error)
            
        errorBand.SetFillColor(kBlack)
        errorBand.SetFillStyle(3003)

        
        HistoLists[2][plot[0]].Add(HistoLists[3][plot[0]])
        HistoLists[2][plot[0]].Add(HistoLists[5][plot[0]])
        HistoLists[2][plot[0]].Add(HistoLists[6][plot[0]])
        HistoLists[2][plot[0]].Add(HistoLists[7][plot[0]])
        HistoLists[2][plot[0]].Add(HistoLists[8][plot[0]])
        
        hStack = THStack(plot[0],plot[0])
        hStack.Add(HistoLists[2][plot[0]])
        hStack.Add(HistoLists[4][plot[0]])
        hStack.Add(HistoLists[1][plot[0]])
        hStack.Add(HistoLists[0][plot[0]])
        
        c1 = TCanvas()
        max_ = max(hStack.GetMaximum(),HistoLists[-1][plot[0]].GetMaximum())
        hStack.Draw("histo")
        hStack.SetMaximum(max_*1.5)
        hStack.SetMinimum(0)
        errorBand.Draw("e2 same")
        hStack.GetYaxis().SetTitle("Events")
        hStack.GetYaxis().CenterTitle()
        hStack.GetXaxis().SetTitle(plot[4])
        HistoLists[-1][plot[0]].Draw("e x0, same")
        leg.Draw()        
        labelcms.Draw()
        labelcms2.Draw()
        labelcms3.Draw()

        if not os.path.exists("VariablePlots/"+specialName):
            command = "mkdir VariablePlots/"+specialName
            os.system(command)
        if not os.path.exists("VariablePlots/"+specialName + region):
            command = "mkdir VariablePlots/"+specialName+region
            os.system(command)
            
        
        c1.SaveAs("VariablePlots/"+specialName+region+"/"+plot[0]+"_"+region+"_"+ChanName[mode]+".pdf")

    zjet = HistoLists[4]['metBinned']
    other = HistoLists[0]['metBinned']
    data = HistoLists[-1]['metBinned']
    for i in range(1,len(HistoLists)-1):
        if i != 4:
            other.Add(HistoLists[i]['metBinned'])
    
    print "-------------------------------------------------------------------"
    print "ZJets Scale Factors", ChanName[mode]
    print "-------------------------------------------------------------------"
    print
    print "Bin Content"
    print "Bin range\t  Zjets\tOtherMC\tData"
    for bin in range(1,len(bins)):
        print bins[bin-1],"-",bins[bin],"\t:","%.1f" % zjet.GetBinContent(bin),"\t","%.1f" % other.GetBinContent(bin),"\t","%.1f" % data.GetBinContent(bin)
    print
    print "-------------------------------------------------------------------"
    print "Scale Factor"
    print "Bin range\tZjets\tOtherMC\tData"
    for bin in range(1,len(bins)):
        ZjetMC = zjet.GetBinContent(bin)
        ZjetData = data.GetBinContent(bin)-other.GetBinContent(bin)
        print bins[bin-1],"-",bins[bin],"\t:","%.4f" % (ZjetData/ZjetMC)
    print
    print "-------------------------------------------------------------------"
    
    
    
        


# signal = [0.,0.,0.]
# bkg = [0.,0.,0.]
# sigErr = [0.,0.,0.]
# bkgErr = [0.,0.,0.]

# print
# print "\\begin{tabular}{| l | c | c | c | c |}"
# print "\\hline"
# print "Channel & $\\mu\\mu$ & $ee$ & Combined \\\\"
# print "\\hline"

# for i in range(len(fileList) - 1):
#     print fileList[i],"&","%.1f" % totals[1][i],"$\pm$","%.1f" % errors[1][i],"&","%.1f" % totals[2][i],"$\pm$","%.1f" % errors[2][i],"&","%.1f" % (totals[1][i]+totals[2][i]),"$\pm$","%.1f" % sqrt(pow(errors[1][i],2)+pow(errors[2][i],2)),"\\\\"
#     if i == 0:
#         signal[1] += totals[1][i]
#         signal[2] += totals[2][i]
#         sigErr[1] = sqrt(pow(sigErr[1],2) + pow(errors[1][i],2))
#         sigErr[2] = sqrt(pow(sigErr[2],2) + pow(errors[2][i],2))
#     else:
#         bkg[1] += totals[1][i]
#         bkg[2] += totals[2][i]
#         bkgErr[1] = sqrt(pow(bkgErr[1],2) + pow(errors[1][i],2))
#         bkgErr[2] = sqrt(pow(bkgErr[2],2) + pow(errors[2][i],2))
        
# print "\\hline"
# print "Signal &","%.1f" % signal[1],"$\pm$","%.1f" % sigErr[1],"&","%.1f" % signal[2],"$\pm$","%.1f" % sigErr[2],"&","%.1f" % (signal[1]+signal[2]),"$\pm$","%.1f" % sqrt(pow(sigErr[1],2)+pow(sigErr[2],2)), " \\\\"
# print "Background &","%.1f" % bkg[1],"$\pm$","%.1f" % bkgErr[1],"&","%.1f" % bkg[2],"$\pm$","%.1f" % bkgErr[2],"&","%.1f" % (bkg[1]+bkg[2]),"$\pm$","%.1f" % sqrt(pow(bkgErr[1],2)+pow(bkgErr[2],2)), " \\\\"
# print "Data &","%.1f" % totals[1][-1],"$\pm$","%.1f" % errors[1][-1],"&","%.1f" % totals[2][-1],"$\pm$","%.1f" % errors[2][-1],"&","%.1f" % (totals[1][-1]+totals[2][-1]),"$\pm$","%.1f" % sqrt(pow(errors[1][-1],2)+pow(errors[2][-1],2)), " \\\\"

# # print "Background &","%.1f" % bkg[2],"&","%.1f" % (bkg[1]+bkg[2]), " \\\\"
# # print "Data &","%.1f" % totals[1][-1],"&","%.1f" % totals[2][-1],"&","%.1f" % (totals[1][-1]+totals[2][-1]), " \\\\"
# print "\\hline"
# print "S/B &","&","%.4f" % (signal[1]/bkg[1]),"&","%.4f" % (signal[2]/bkg[2]),"&","%.4f" % ((signal[1]+signal[2])/(+bkg[1]+bkg[2])), " \\\\"
# print "$S/\\sqrt{B}$ &","%.2f" % (signal[1]/sqrt(bkg[1])),"&","%.2f" % (signal[2]/sqrt(bkg[2])),"&","%.2f" % ((signal[1]+signal[2])/sqrt(bkg[1]+bkg[2])), " \\\\"
# print "\\hline"
# print "\\end{tabular}"

