#!/usr/bin/env cmsRun
import FWCore.ParameterSet.Config as cms
import os,sys,re,shutil


#Original config file
fileName = "SingleTopSystematicsWithTrigger_cfg.py"
#fileName = "SingleTopPDFWithTrigger_cfg.py"
#fileName = "SingleTopSystematics_cfg.py"
#fileName = "SingleTopSystematics_split_cfg.py"
#fileName = "SingleTopNEvents_cfg.py"

#Channels to include
channels = [
#"TbarChannel",
#"TChannel_part_1","TChannel_part_2","TChannel_part_3",
#"TbarChannel_part_1","TbarChannel_part_2","TbarChannel_part_3",
#"TChannel",
#"ZJets",
"ZJets_part_1", "ZJets_part_2", "ZJets_part_3", "ZJets_part_4", "ZJets_part_5",
#"SChannel_part_1", "SChannel_part_2", "SChannel_part_3", "SChannel_part_4", "SChannel_part_5",
#"SbarChannel_part_1", "SbarChannel_part_2", "SbarChannel_part_3", "SbarChannel_part_4", "SbarChannel_part_5",
#"ZZ_part_1", "ZZ_part_2", "ZZ_part_3", "ZZ_part_4", "ZZ_part_5",
#"WZ_part_1", "WZ_part_2", "WZ_part_3", "WZ_part_4", "WZ_part_5",
#"WW_part_1", "WW_part_2", "WW_part_3", "WW_part_4", "WW_part_5",
#"QCDMuBig",
#"WJetsBig_part_1","WJetsBig_part_2","WJetsBig_part_3","WJetsBig_part_4","WJetsBig_part_5","WJetsBig_part_6","WJetsBig_part_7","WJetsBig_part_8","WJetsBig_part_9","WJetsBig_part_10",
#"WJetsBig_part_11","WJetsBig_part_12","WJetsBig_part_13","WJetsBig_part_14","WJetsBig_part_15","WJetsBig_part_16","WJetsBig_part_17","WJetsBig_part_18","WJetsBig_part_19","WJetsBig_part_20",
#"WJetsBig_part_21","WJetsBig_part_22",
#"WJets_part_1","WJets_part_2","WJets_part_3","WJets_part_4","WJets_part_5","WJets_part_6","WJets_part_7","WJets_part_8","WJets_part_9","WJets_part_10","WJets_part_11",
#"Mu_A13Jul_part_1","Mu_A13Jul_part_2","Mu_A13Jul_part_3","Mu_A13Jul_part_4","Mu_A13Jul_part_5","Mu_A13Jul_part_6","Mu_A13Jul_part_7","Mu_A13Jul_part_8","Mu_A13Jul_part_9","Mu_A13Jul_part_10","Mu_A13Jul_part_11","Mu_A13Jul_part_12","Mu_A13Jul_part_13","Mu_A13Jul_part_14","Mu_A13Jul_part_15","Mu_A13Jul_part_16","Mu_A13Jul_part_17","Mu_A13Jul_part_18","Mu_A13Jul_part_19","Mu_A13Jul_part_20","Mu_A13Jul_part_21","Mu_A13Jul_part_22",
#"Mu_B13Jul_part_1","Mu_B13Jul_part_2","Mu_B13Jul_part_3","Mu_B13Jul_part_4","Mu_B13Jul_part_5","Mu_B13Jul_part_6","Mu_B13Jul_part_7","Mu_B13Jul_part_8","Mu_B13Jul_part_9","Mu_B13Jul_part_10","Mu_B13Jul_part_11","Mu_B13Jul_part_12","Mu_B13Jul_part_13","Mu_B13Jul_part_14","Mu_B13Jul_part_15","Mu_B13Jul_part_16","Mu_B13Jul_part_17","Mu_B13Jul_part_18","Mu_B13Jul_part_19","Mu_B13Jul_part_20","Mu_B13Jul_part_21","Mu_B13Jul_part_22",
#"Mu_A06Aug_part_1","Mu_A06Aug_part_2","Mu_A06Aug_part_3",
#"TChannel", "TbarChannel",
#"SChannel", "SbarChannel",
## "TTBar_Q2Up",# "TTBar_Q2Down",
#"WW_part_1","WW_part_2","WW_part_3",
#"WW",
#"WZ","ZZ",
#"TWChannel", "TbarWChannel",
#"TTBar_part_1", "TTBar_part_2","TTBar_part_3","TTBar_part_4", "TTBar_part_5", "TTBar_part_6", "TTBar_part_7", "TTBar_part_11", "TTBar_part_10", "TTBar_part_8", "TTBar_part_9",
#"Mu_v1_A_part_1", "Mu_v1_A_part_2", "Mu_v1_A_part_3", "Mu_v1_A_part_4", "Mu_v1_A_part_5", "Mu_v1_A_part_6", "Mu_v1_A_part_7",

#"Mu_v1_B1_part_1", "Mu_v1_B1_part_2", "Mu_v1_B1_part_3", "Mu_v1_B1_part_4", "Mu_v1_B1_part_5", "Mu_v1_B1_part_6", "Mu_v1_B1_part_7", "Mu_v1_B1_part_8", "Mu_v1_B1_part_9","Mu_v1_B1_part_11", "Mu_v1_B1_part_12", "Mu_v1_B1_part_13", "Mu_v1_B1_part_14", "Mu_v1_B1_part_15", "Mu_v1_B1_part_16", "Mu_v1_B1_part_17", "Mu_v1_B1_part_18", "Mu_v1_B1_part_10", "Mu_v1_B1_part_20","Mu_v1_B1_part_19","Mu_v1_B1_part_21",

#"Ele_v1_A_part_1", "Ele_v1_A_part_2", "Ele_v1_A_part_3", "Ele_v1_A_part_4", "Ele_v1_A_part_5", "Ele_v1_A_part_6", "Ele_v1_A_part_7"
# "Mu_v1_B2_part_1", "Mu_v1_B2_part_2", "Mu_v1_B2_part_3", "Mu_v1_B2_part_4", "Mu_v1_B2_part_5", "Mu_v1_B2_part_6", "Mu_v1_B2_part_7", "Mu_v1_B2_part_8", "Mu_v1_B2_part_9","Mu_v1_B2_part_10","Mu_v1_B2_part_11",

# "Ele_v1_B2_part_1", "Ele_v1_B2_part_2", "Ele_v1_B2_part_3", "Ele_v1_B2_part_4", "Ele_v1_B2_part_5", "Ele_v1_B2_part_6", "Ele_v1_B2_part_7", "Ele_v1_B2_part_8", "Ele_v1_B2_part_9",
# "TbarWChannel", "TWChannel",
# "TbarChannel_Q2Up", "TbarChannel_Q2Down",
# "WW", "ZZ", "WZ",
#"ZJets",
 ]

#Path to take data merged files
dataPath = "file:/tmp/oiorio/"

#Choose if you want to run or just prepare the configuration files
mode = ""
mode = "cmsRun"


#Use mu , ele or both

channel_instruction = "all"

#Implementation:

#Function to replace a sequence of characters channelOld to channelNew in a file 
def changeChannel(fileName,channelOld,channelNew,switch,isMC): 
    print " Channel test " + channelNew
    channelToReplace = channelNew
    channelToReplaceInTree = channelNew
    if "Data" in channelNew:#=="DataMu" or channelNew == "DataEle" or channelNew == "DataMuQCD" or channelNew =="DataEleQCD":
        channelToReplace = "Data"
    if ("Mu" in channelNew or "Ele" in channelNew) and not "QCDMu" in channelNew:#=="DataMu" or channelNew == "DataEle" or channelNew == "DataMuQCD" or channelNew =="DataEleQCD":
        channelToReplace = "Data"
    if "WJets_wlight" in channelNew:#=="DataMu" or channelNew == "DataEle" or channelNew == "DataMuQCD" or channelNew =="DataEleQCD":
        channelToReplace = "WJets_wlight"
    if "WJets_wcc" in channelNew:#=="DataMu" or channelNew == "DataEle" or channelNew == "DataMuQCD" or channelNew =="DataEleQCD":
        channelToReplace = "WJets_wcc"
    if "WJets_wbb" in channelNew:#=="DataMu" or channelNew == "DataEle" or channelNew == "DataMuQCD" or channelNew =="DataEleQCD":
        channelToReplace = "WJets_wbb"
    if "ZJets_wlight" in channelNew:#=="DataMu" or channelNew == "DataEle" or channelNew == "DataMuQCD" or channelNew =="DataEleQCD":
        channelToReplace = "ZJets_wlight"
    if "ZJets_wcc" in channelNew:#=="DataMu" or channelNew == "DataEle" or channelNew == "DataMuQCD" or channelNew =="DataEleQCD":
        channelToReplace = "ZJets_wcc"
    if "ZJets_wbb" in channelNew:#=="DataMu" or channelNew == "DataEle" or channelNew == "DataMuQCD" or channelNew =="DataEleQCD":
        channelToReplace = "ZJets_wbb"
    #    if "TTBar" in channelNew:#=="DataMu" or channelNew == "DataEle" or channelNew == "DataMuQCD" or channelNew =="DataEleQCD":
    #        channelToReplace = "TTBar"
    if "QCDMu" in channelNew:#=="DataMu" or channelNew == "DataEle" or channelNew == "DataMuQCD" or channelNew =="DataEleQCD":
        channelToReplace = "QCDMu"
    if "WJets" in channelNew:#=="DataMu" or channelNew == "DataEle" or channelNew == "DataMuQCD" or channelNew =="DataEleQCD":
        channelToReplace = "WJets"
    if "ZJets" in channelNew:#=="DataMu" or channelNew == "DataEle" or channelNew == "DataMuQCD" or channelNew =="DataEleQCD":
        channelToReplace = "ZJets"
    if "TTBar" in channelNew:#=="DataMu" or channelNew == "DataEle" or channelNew == "DataMuQCD" or channelNew =="DataEleQCD":
        channelToReplace = "TTBar"
    if "TChannel" in channelNew:#=="DataMu" or channelNew == "DataEle" or channelNew == "DataMuQCD" or channelNew =="DataEleQCD":
        channelToReplace = "TChannel"
    if "TbarChannel" in channelNew:#=="DataMu" or channelNew == "DataEle" or channelNew == "DataMuQCD" or channelNew =="DataEleQCD":
        channelToReplace = "TbarChannel"
    if "SChannel" in channelNew:#=="DataMu" or channelNew == "DataEle" or channelNew == "DataMuQCD" or channelNew =="DataEleQCD":
        channelToReplace = "SChannel"
    if "SbarChannel" in channelNew:#=="DataMu" or channelNew == "DataEle" or channelNew == "DataMuQCD" or channelNew =="DataEleQCD":
        channelToReplace = "SbarChannel"
    if "TTBarFullLep" in channelNew:
        channelToReplace = "TTBarFullLep"
    if "TTBarSemiLep" in channelNew:
        channelToReplace = "TTBarSemiLep"
    if "WW" in channelNew:#=="DataMu" or channelNew == "DataEle" or channelNew == "DataMuQCD" or channelNew =="DataEleQCD":
        channelToReplace = "WW"
    if "WZ" in channelNew:#=="DataMu" or channelNew == "DataEle" or channelNew == "DataMuQCD" or channelNew =="DataEleQCD":
        channelToReplace = "WZ"
    if "ZZ" in channelNew:#=="DataMu" or channelNew == "DataEle" or channelNew == "DataMuQCD" or channelNew =="DataEleQCD":
        channelToReplace = "ZZ"
          #if channelNew=="DataEle":
       # channelNew_2 = "Data"
    file = open(fileName)
    lines = file.readlines()
    o = open(channelNew+"_cfg.py","w") 
    for line in lines:
        if '"channel_instruction"' in line:
            print line
            line = line.replace('"channel_instruction"','"'+switch+'"')
            print line
        if "MC_instruction" in line and "False" in line:
       #     if "False" in line:
                print line
                line = line.replace("False",isMC)
                print line
        words = line.split()
        for word in words:
            if channelOld in word:  
                #                print " line old " + line
                if (not switch == "all") and ("process.TFileService" in line):
                    line = line.replace(word,word.replace(channelOld,channelNew))
                    print "process.TFileService in line,switch " + switch +" line: \n" +line
                    
                else:
                    line = line.replace(word,word.replace(channelOld,channelToReplace))
                
        o.write(line)   
    #if channel == "Data":#Temporary inelegant solution due to the separation of mu/e: will fix it at some point
        #        line = "process.source.fileNames = cms.untracked.vstring('"+dataPath+"DataMuMerged.root','"+dataPath+"DataEleMerged.root',)"
        #        line = "process.source.fileNames = cms.untracked.vstring('"+dataPath+"DataMuMerged.root',)"
        #       line = "process.source.fileNames = cms.untracked.vstring('"+dataPath+"Mu_v1Merged.root','"+dataPath+"Mu_v2Merged.root','"+dataPath+"Ele_v1Merged.root','"+dataPath+"Ele_v2Merged.root',)"
    if "WJets" in channelNew:# == "DataMu" or channelNew == "DataMuQCD":
        inputs = "process.source.fileNames = cms.untracked.vstring("
        inputs = inputs +"'"+dataPath+channel+"Merged.root',"
        inputs = inputs.replace(channelToReplace,"WJets")
        inputs = inputs +")"
        o.write(inputs)
    if "TChannel" in channelNew:# == "DataMu" or channelNew == "DataMuQCD":
        inputs = "process.source.fileNames = cms.untracked.vstring("
        inputs = inputs +"'"+dataPath+channel+"Merged.root',"
        inputs = inputs.replace(channelToReplace,"TChannel")
        inputs = inputs +")"
        o.write(inputs)
    if "TbarChannel" in channelNew:# == "DataMu" or channelNew == "DataMuQCD":
        inputs = "process.source.fileNames = cms.untracked.vstring("
        inputs = inputs +"'"+dataPath+channel+"Merged.root',"
        inputs = inputs.replace(channelToReplace,"TbarChannel")
        inputs = inputs +")"
        o.write(inputs)
    if "SChannel" in channelNew:# == "DataMu" or channelNew == "DataMuQCD":
        inputs = "process.source.fileNames = cms.untracked.vstring("
        inputs = inputs +"'"+dataPath+channel+"Merged.root',"
        inputs = inputs.replace(channelToReplace,"SChannel")
        inputs = inputs +")"
        o.write(inputs)
    if "SbarChannel" in channelNew:# == "DataMu" or channelNew == "DataMuQCD":
        inputs = "process.source.fileNames = cms.untracked.vstring("
        inputs = inputs +"'"+dataPath+channel+"Merged.root',"
        inputs = inputs.replace(channelToReplace,"SbarChannel")
        inputs = inputs +")"
        o.write(inputs)
    if "ZJets" in channelNew:# == "DataMu" or channelNew == "DataMuQCD":
        inputs = "process.source.fileNames = cms.untracked.vstring("
        inputs = inputs +"'"+dataPath+channel+"Merged.root',"
        inputs = inputs.replace(channelToReplace,"ZJets")
        inputs = inputs +")"
        o.write(inputs)
    if "TTBar" in channelNew:# == "DataMu" or channelNew == "DataMuQCD":
        inputs = "process.source.fileNames = cms.untracked.vstring("
        inputs = inputs +"'"+dataPath+channel+"Merged.root',"
        inputs = inputs.replace(channelToReplace,"TTBar")
        inputs = inputs +")"
        o.write(inputs)
    if "WW" in channelNew:# == "DataMu" or channelNew == "DataMuQCD":
        inputs = "process.source.fileNames = cms.untracked.vstring("
        inputs = inputs +"'"+dataPath+channel+"Merged.root',"
        inputs = inputs.replace(channelToReplace,"WW")
        inputs = inputs +")"
        o.write(inputs)
    if "WZ" in channelNew:# == "DataMu" or channelNew == "DataMuQCD":
        inputs = "process.source.fileNames = cms.untracked.vstring("
        inputs = inputs +"'"+dataPath+channel+"Merged.root',"
        inputs = inputs.replace(channelToReplace,"WZ")
        inputs = inputs +")"
        o.write(inputs)
    if "ZZ" in channelNew:# == "DataMu" or channelNew == "DataMuQCD":
        inputs = "process.source.fileNames = cms.untracked.vstring("
        inputs = inputs +"'"+dataPath+channel+"Merged.root',"
        inputs = inputs.replace(channelToReplace,"ZZ")
        inputs = inputs +")"
        o.write(inputs)
    if "Mu" in channelNew or "Ele" in channelNew:# == "DataMu" or channelNew == "DataMuQCD":
        inputs = "process.source.fileNames = cms.untracked.vstring("
        inputs = inputs +"'"+dataPath+channel+"Merged.root',"
#        inputs = inputs +"'"+dataPath+"Mu_v4p1Merged.root',"
#        inputs = inputs +"'"+dataPath+"Mu_v4p2Merged.root',"
#        inputs = inputs +"'"+dataPath+"Mu_v4p3Merged.root',"
#        inputs = inputs +"'"+dataPath+"Mu_v4Merged.root',"
#        inputs = inputs +"'"+dataPath+"Mu_v2Merged.root',"
        inputs = inputs +")"
        o.write(inputs)
    #if "TTBar" in channelNew:# == "DataMu" or channelNew == "DataMuQCD":
    #    inputs = "process.source.fileNames = cms.untracked.vstring("
    #    inputs = inputs +"'"+dataPath+channel+"Merged.root',"
    #    inputs = inputs.replace(channelToReplace,"TTBar")
    #    inputs = inputs +")"
    #    o.write(inputs)
#    if "Ele" in channelNew:#channelNew == "DataEle" or channelNew == "DataEleQCD":
#        inputs = "process.source.fileNames = cms.untracked.vstring("
#        inputs = inputs +"'"+dataPath+"Merged.root',"
##        inputs = inputs +"'"+dataPath+"Ele_v4.root',"
##        inputs = inputs +"'"+dataPath+"Ele_v2Merged.root',"
##        inputs = inputs +"'"+dataPath+"Ele_v1Merged.root',"
#        inputs = inputs +")"
#        o.write(inputs)
    o.close()
    return o

#Implementation of the loop part:

#Channel in the original file
startChannel = "TChannel"#channels[0]

f= open(fileName)

tmpName = "temp.py"
shutil.copy(fileName,tmpName)

for channel in channels:

    isMC = "False"
    if "Mu" in channel and not "QCD" in channel:
        channel_instruction = "mu"
    elif "Ele" in channel and not "QCD" in channel:
        channel_instruction = "ele"
    elif "Ele" in channel and not "QCD" in channel:
        channel_instruction = "ele"
    elif "Mu" in channel and ("QCD" in channel or "Had" in channel) and not "QCDMu" in channel:
        channel_instruction = "muqcd"
    elif "Ele" in channel and "QCD" in channel:
        channel_instruction = "eleqcd"
    else : 
        channel_instruction = "allmc"   
        isMC = "True"
    channelOld = startChannel
    
    cfg_file = changeChannel(tmpName,channelOld,channel,channel_instruction,isMC)
    command = 'nohup cmsRun ./' + channel+'_cfg.py > /tmp/oiorio/'+channel+'.log &'
    
    print command

    if mode == "cmsRun":
        os.system(command ) 
#    os.system("bg") 
#    os.system('rm '+channel+'_cfg.py' ) 

os.system('rm '+tmpName) 
#changeChannel(f,aChannel,startChannel)

#os.system(command)



