#!/usr/bin/env python                                                                                                                  

import sys

stepNames = {'lepSel':['lepSel','lepsel_info','lepSel'],
             'lepVeto':['lepVeto','info','lepSel']}

cutLevel = 'lepSel'
Rebeca = False
Duncan = False
if len(sys.argv) > 1:
    for i in range(1,len(sys.argv)):
        arg = sys.argv[i]
        if arg in stepNames:
            cutLevel = arg
        if arg == 'R':
            Rebeca = True
        if arg == 'D':
            Duncan = True
else:
    cutLevel = 'lepSel'


myFiles = [open(stepNames[cutLevel][0]+'Dump_emu.txt','r'),open(stepNames[cutLevel][0]+'Dump_mumu.txt','r'),open(stepNames[cutLevel][0]+'Dump_ee.txt','r')]
rebecaFiles = [open(stepNames[cutLevel][1]+'_run_lumi_event_0_tw_dr.txt','r'),open(stepNames[cutLevel][1]+'_run_lumi_event_1_tw_dr.txt','r'),open(stepNames[cutLevel][1]+'_run_lumi_event_2_tw_dr.txt','r')]
duncanFiles = [open('run_lumi_event_tw_emu_'+stepNames[cutLevel][2]+'_Brunel.txt','r'),open('run_lumi_event_tw_mumu_'+stepNames[cutLevel][2]+'_Brunel.txt','r'),open('run_lumi_event_tw_ee_'+stepNames[cutLevel][2]+'_Brunel.txt','r')]

diffMeRebecaFile  = [open('diff/MineNotRebecas_'+cutLevel+'_emu.txt','w'),open('diff/MineNotRebecas_'+cutLevel+'_mumu.txt','w'),open('diff/MineNotRebecas_'+cutLevel+'_ee.txt','w')]
diffMeDuncanFile  = [open('diff/MineNotDuncans_'+cutLevel+'_emu.txt','w'),open('diff/MineNotDuncans_'+cutLevel+'_mumu.txt','w'),open('diff/MineNotDuncans_'+cutLevel+'_ee.txt','w')]
diffRebecaFile = [open('diff/RebecasNotMine_'+cutLevel+'_emu.txt','w'),open('diff/RebecasNotMine_'+cutLevel+'_mumu.txt','w'),open('diff/RebecasNotMine_'+cutLevel+'_ee.txt','w')]
diffDuncanFile = [open('diff/DuncansNotMine_'+cutLevel+'_emu.txt','w'),open('diff/DuncansNotMine_'+cutLevel+'_mumu.txt','w'),open('diff/DuncansNotMine_'+cutLevel+'_ee.txt','w')]

channel = ['emu','mumu','ee']

for i in range(3):
    rebecasNotMine = 0
    mineNotRebecas = 0
    duncansNotMine = 0
    mineNotDuncans = 0
    sameRebeca = 0
    sameDuncan = 0
    
    myEvents = myFiles[i].readlines()
    rebecaEvents = rebecaFiles[i].readlines()
    duncanEvents = duncanFiles[i].readlines()

    for event in myEvents:
        if event in rebecaEvents:
            sameRebeca += 1
            continue
        else:
            diffMeRebecaFile[i].write(event)
            mineNotRebecas += 1

    for event in myEvents:
        if event in duncanEvents:
            sameDuncan += 1
            continue
        else:
            diffMeDuncanFile[i].write(event)
            mineNotDuncans += 1

    for event in rebecaEvents:
        if event in myEvents:
            continue
        else:
            diffRebecaFile[i].write(event)
            rebecasNotMine += 1

    for event in duncanEvents:
        if event in myEvents:
            continue
        else:
            diffDuncanFile[i].write(event)
            duncansNotMine += 1

    print channel[i]
    if Rebeca: print 'Rebecas', len(rebecaEvents)
    if Duncan: print 'Duncans', len(duncanEvents)
    print 'Mine', len(myEvents)
    if Rebeca: print 'SameRebeca', sameRebeca
    if Duncan: print 'SameDuncan', sameDuncan
    if Rebeca: print 'Mine Not Rebecas', mineNotRebecas
    if Rebeca: print 'Rebecas Not Mine', rebecasNotMine
    if Duncan: print 'Mine Not Duncans', mineNotDuncans
    if Duncan: print 'Duncans Not Mine', duncansNotMine
    print
    
