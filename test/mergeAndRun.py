#!/usr/bin/env python
import os, sys
import glob
import subprocess

#Script to take the edmtuple output from a crab job (given by a directory name as an argument)
#and put them into a cfg file to make the systematics nTuples for that sample
#Two arguments needed, directory of crab output and the channel name

#ex:
# mergeAndRun.py tW_Synch T_tWChannel

channelName = ""
directory = ""
rootFileName = ""

appendVersion = ""

currentFileVersion = "v1"

okChannelNames = ['TChannel',
                  'TbarChannel',
                  'TWChannel',
                  'TbarWChannel',
                  'SChannel',
                  'SbarChannel',
                  'TTBar',
                  'ZJets',
                  'ZJetsLowMass',
                  'WJets',
                  'WW',
                  'WZ',
                  'ZZ',
                  'Data',
                  'TWChannelDilepton',
                  'TbarWChannelDilepton',
                  'TTBarDilepton',
                  'TestSample']


dataChannels = ['MuEG',
                'DoubleMu',
                'DoubleElectron']

dataRuns = ['Run2012A-13Jul2012',
            'Run2012A-recover-06Aug2012',
            'Run2012B-13Jul2012',
            'Run2012C-24Aug2012',
            'Run2012C-PromptReco']


#storeUser = "/home/t3-ku/dnoonan/storeUser/tW_8TeV/"
storeUser = "/mnt/hadoop/user/uscms01/pnfs/unl.edu/data4/cms/store/user/dnoonan/tW_8TeV/"    

ProcessNumber = -1
OutOf = -1

isData = False
if len(sys.argv) == 7:
    if sys.argv[2] == 'Data':
        if sys.argv[3] in dataChannels:
            if sys.argv[4] in dataRuns:
                channelName = sys.argv[2]
                rootFileName = sys.argv[3] + "_" + sys.argv[4]
                directory=storeUser + "Data/" + sys.argv[1]
                if not os.path.exists(directory):
                    print "Directory specified ("+directory+") does not exist"
                    exit()                
                isData = True
                ProcessNumber = int(sys.argv[5])
                OutOf = int(sys.argv[6])
            else:
                print "Must specify one of the following runs:"
                print dataRuns
                exit()
        else:
            print "Must specify one of the following channels for data:"
            print dataChannels
            exit()
                             
if not isData and len(sys.argv) != 5:    
    print "You need 2 arguments (directory and channel name). Something like:"
    print "mergeAndRun.py tW_Synch T_tWChannel"
    print "Or for data, 4 arguments must be specified (directory, data as channel name, and ) ! Something like:"
    print "mergeAndRun.py MuEG_Run2012B-13Jul2012-v1_v1 Data MuEG Run2012B-13Jul2012"
    exit()
elif not isData:
    directory=storeUser+"MC/"+sys.argv[1]
    if not os.path.exists(directory):
        print "Directory specified ("+directory+") does not exist"
        exit()
                      
    if sys.argv[2] in okChannelNames:
        channelName = sys.argv[2]
        rootFileName = sys.argv[2]
    else:
        print "Invalid channel name: " + sys.argv[2]
        exit()
    ProcessNumber = int(sys.argv[3])
    OutOf = int(sys.argv[4])

if ProcessNumber > OutOf:
    print "Asking for job", ProcessNumber, "out of only", OutOf,"jobs, please select a number in range of jobs"
    exit()
if ProcessNumber < 1:
    print "Asking for a job number below 1, please select a new job number"
    exit()

edmFileListStart = glob.glob(directory+"/edm*root")

edmFileListStart.sort()

edmFileListFull = list()

for i in range(len(edmFileListStart)):
    if i < len(edmFileListStart)-2:
        file_i = edmFileListStart[i].split('/')[-1]
        file_ip1 = edmFileListStart[i+1].split('/')[-1]
        jobNum = file_i.split('_')[1]
        jobIter = int(file_i.split('_')[2])
        jobIterp1 = int(file_ip1.split('_')[2])
        if jobNum == file_ip1.split('_')[1]:                
            if jobIter < jobIterp1:
                continue
            else:
                edmFileListFull.append(edmFileListStart[i])
        else:
            edmFileListFull.append(edmFileListStart[i])
    else:
        edmFileListFull.append(edmFileListStart[i])
        
edmFileListFull.sort()

if OutOf > len(edmFileListFull):
    print "More jobs than files; requesting",OutOf,"jobs from only", len(edmFileListFull),"files"
    print "Please select fewer than",len(edmFileListFull),"jobs"
    exit()
# for file in edmFileListFull:
#     print file

edmFileList = list()
if OutOf == 1:
    edmFileList = edmFileListFull[:]
else:
    total = len(edmFileListFull)
    perJob = int((total*1.)/(OutOf*1.))
    print OutOf, "jobs from",total,"files gives",perJob,"files per job"
    if ProcessNumber == OutOf:
        StartJob = (ProcessNumber-1)*perJob
        edmFileList = edmFileListFull[StartJob:]
    else:
        StartJob = (ProcessNumber-1)*perJob
        EndJob = (ProcessNumber)*perJob
        edmFileList = edmFileListFull[StartJob:EndJob]

for file in edmFileList:
    print file


TemplateCfg=open('SingleTopSystematicsWithTrigger_tW_TEMPLATE_cfg.py','r')
TemplateCfgLines=TemplateCfg.readlines()
TemplateCfg.close()

processCount = '_'+str(ProcessNumber)+'_'+str(OutOf)

NewCfg=open('SingleTopSystematicsWithTrigger_tW_'+rootFileName+processCount+'_cfg.py','w')

for cfgLine in TemplateCfgLines:
    if 'INSERTFILENAME' in cfgLine:
        newline = ''
        for file in edmFileList:
            newline = newline+cfgLine.replace('INSERTFILENAME',file)
    elif 'REPLACECHANNELNAME' in cfgLine:        
        newline = cfgLine.replace('REPLACECHANNELNAME',channelName)
    elif 'REPLACEROOTFILENAME' in cfgLine:        
        newline = cfgLine.replace('REPLACEROOTFILENAME',rootFileName +processCount+ appendVersion)
    elif channelName == 'Data' and 'MC_instruction = True' in cfgLine:
        newline = cfgLine.replace('True','False')
    elif channelName == 'Data' and 'channel_instruction = ' in cfgLine:
        newline = cfgLine.replace('allmc','data')
    else:
        newline = cfgLine

    NewCfg.write(newline)

NewCfg.close()

command = 'cmsRun SingleTopSystematicsWithTrigger_tW_'+rootFileName+processCount+'_cfg.py'
print command
os.system(command)

command = "mv output/ntuple_SysTrees_"+rootFileName+processCount+".root "+storeUser+"Ntuples/."
print command
os.system(command)

command = 'mv SingleTopSystematicsWithTrigger_tW_'+rootFileName+processCount+'_cfg.py OldNtupleCfgs/.'
print command
os.system(command)
