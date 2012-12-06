#!/bin/bash
 export SCRAM_ARCH=slc5_amd64_gcc434
 source /opt/osg/app/cmssoft/cms/cmsset_default.sh
 /bin/hostname
 /bin/date
 /bin/pwd
 /bin/df
 /bin/ls
 /bin/ls -l /home
 /bin/ls -l /home/t3-ku
 /bin/sleep 30
 cd /home/t3-ku/dnoonan/8TeV_ProductionTest/Test/CMSSW_5_3_5/src/TopQuarkAnalysis/SingleTop/test/
 eval $(scram runtime -sh)
 cd /home/t3-ku/dnoonan/8TeV_ProductionTest/Test/CMSSW_5_3_5/src/TopQuarkAnalysis/SingleTop/test/macros

 case "$1" in
     0) ./TMVATupleCreator.py TWChannel
     1) ./TMVATupleCreator.py TTbar
     2) ./TMVATupleCreator.py TChannel
     3) ./TMVATupleCreator.py SChannel
     4) ./TMVATupleCreator.py ZJets
     5) ./TMVATupleCreator.py WJets
     6) ./TMVATupleCreator.py WW
     7) ./TMVATupleCreator.py WZ
     8) ./TMVATupleCreator.py ZZ

     9) ./TMVATupleCreator.py Data_MuEG_Run2012A
     10) ./TMVATupleCreator.py Data_MuEG_Run2012B
     11) ./TMVATupleCreator.py Data_MuEG_Run2012C

     12) ./TMVATupleCreator.py Data_DoubleMu_Run2012A
     13) ./TMVATupleCreator.py Data_DoubleMu_Run2012B
     14) ./TMVATupleCreator.py Data_DoubleMu_Run2012C

     15) ./TMVATupleCreator.py Data_DoubleElectron_Run2012A
     16) ./TMVATupleCreator.py Data_DoubleElectron_Run2012B
     17) ./TMVATupleCreator.py Data_DoubleElectron_Run2012C
