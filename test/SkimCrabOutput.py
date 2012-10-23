#!/usr/bin/env python
import os, sys
import glob


DoSummary = False
if '--summary' in sys.argv and len(sys.argv)==3:
    DoSummary = True
    if '--fullSummary' in sys.argv[1]:
        directory = sys.argv[2]
    else:
        directory = sys.argv[1]
elif len(sys.argv) != 2:
    print "Need to specify a crab output directory! Something like:"
    print "SkimCrabOutput.py tW_Synch"
    sys.exit()
else:
    directory = sys.argv[1]

if not os.path.exists(directory):
    print "Directory " + directory + " does not exist"

if not os.path.exists(directory + "/res"):
    print "Directory " + directory + "/res does not exist"

cmsswStdOutFiles = glob.glob(directory+"/res/CMSSW_*.stdout")

totalEvents = 0
passedEvents = 0

summary = list()
cmsswStdOutFilesSorted = sorted(cmsswStdOutFiles, key=lambda temp: int(temp.split('.std')[0].split('_')[-1]))

for fileName in cmsswStdOutFilesSorted:
    errorInFile = False
    foundEvents = False
    file = open(fileName)
    for i,line in enumerate(file):
        if "MSG-e" in line:
            if not errorInFile:
                print
                print "**************ERROR**************"
                print fileName
                errorInFile = True
            print "Line Number",i+1
            print line[:-1]
        if ' selection' in line and 'TrigReport' in line and not 'Modules in Path' in line:
            passedEvents += int(line.split()[4])
            filepassed = int(line.split()[4])
        if 'total = ' in line:
            totalEvents += int(line.split()[4])
            fileEvents = int(line.split()[4])
            foundEvents = True
    if foundEvents and DoSummary:
        summaryLine = fileName.split('/res/')[-1] + "  " + str(filepassed) + "/" + str(fileEvents)
        summary.append(summaryLine)
    if errorInFile:
        print "*********************************"
        
print

if DoSummary:
    i = 1
    for line in summary:
        if str(i) in line:
            print line
        else:
            print '------'
            print line
            i+=1
        i += 1
        
print "Total number of events passing skim =", passedEvents
print "Total number of events processed =", totalEvents

    
