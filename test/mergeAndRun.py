#!/usr/bin/env python
import os, sys
import glob
import subprocess

#Script to take the edmtuple output from a crab job (given by a directory name as an argument)
#and put them into a cfg file to make the systematics nTuples for that sample
#Two arguments needed, directory of crab output and the channel name

#ex:
# mergeAndRun.py tW_Synch T_tWChannel

if len(sys.argv) != 3:
    print "You need 3 arguments! Something like:"
    print "mergeAndRun.py tW_Synch T_tWChannel"
    exit
else:
    directory=sys.argv[1]
    if os.path.exists(directory):
        if not os.path.exists(directory+"/res"):
            print "Directory specified ("+directory+"/res) does not exist"
            exit
    else:
        print "Directory specified ("+directory+") does not exist"
        exit

    okChannelNames = ['TChannel',
                      'TbarChannel',
                      'TWChannel',
                      'TbarWChannel',
                      'SChannel',
                      'SbarChannel',
                      'TTbar',
                      'ZJets',
                      'WJets',
                      'WW',
                      'WZ',
                      'ZZ',
                      'Data']
                      
    if sys.argv[2] in okChannelNames:
        channelName = sys.argv[2]
    else:
        print "Invalid channel name :" + sys.argv[2]

edmFileList = glob.glob(directory+"/res/edm*root")

for file in edmFileList:
    print file


TemplateCfg=open('SingleTopSystematicsWithTrigger_tW_TEMPLATE_cfg.py','r')
TemplateCfgLines=TemplateCfg.readlines()
TemplateCfg.close()

NewCfg=open('SingleTopSystematicsWithTrigger_tW_'+channelName+'_cfg.py','w')

for cfgLine in TemplateCfgLines:
    if 'INSERTFILENAME' in cfgLine:
        newline = ''
        for file in edmFileList:
            newline = newline+cfgLine.replace('INSERTFILENAME',file)
    elif 'REPLACECHANNELNAME' in cfgLine:
        newline = cfgLine.replace('REPLACECHANNELNAME',channelName)
    elif channelName == 'Data' and 'MC_instruction = True' in cfgLine:
        newline = cfgLine.replace('True','False')
    else:
        newline = cfgLine

    NewCfg.write(newline)

NewCfg.close()

command = "cmsRun SingleTopSystematicsWithTrigger_tW_"+channelName+"_cfg.py"
print command

os.system(command)
