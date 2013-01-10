#!/bin/bash
export SCRAM_ARCH=slc5_amd64_gcc462
source /opt/osg/app/cmssoft/cms/cmsset_default.sh
/bin/hostname
/bin/date
/bin/pwd
/bin/df
/bin/ls
/bin/ls -l /home
/bin/ls -l /home/t3-ku
/bin/sleep 30
cd /home/t3-ku/dnoonan/8TeV_ProductionTest/CMSSW_5_3_5/src/TopQuarkAnalysis/SingleTop/test/
eval $(scram runtime -sh)
cd /home/t3-ku/dnoonan/8TeV_ProductionTest/CMSSW_5_3_5/src/TopQuarkAnalysis/SingleTop/test/macros

case "$1" in
    0) ./TMVATupleCreator_v2.py TWChannel;;
    1) ./TMVATupleCreator_v2.py TTbar    ;;
    2) ./TMVATupleCreator_v2.py TChannel ;;
    3) ./TMVATupleCreator_v2.py SChannel ;;
    4) ./TMVATupleCreator_v2.py ZJets    ;;
    5) ./TMVATupleCreator_v2.py WJets    ;;
    6) ./TMVATupleCreator_v2.py WW       ;;
    7) ./TMVATupleCreator_v2.py WZ       ;;
    8) ./TMVATupleCreator_v2.py ZZ       ;;
    
    9) ./TMVATupleCreator_v2.py Data_MuEG_Run2012A ;;
    10) ./TMVATupleCreator_v2.py Data_MuEG_Run2012B;;
    11) ./TMVATupleCreator_v2.py Data_MuEG_Run2012C;;
    
    12) ./TMVATupleCreator_v2.py Data_DoubleMu_Run2012A;;
    13) ./TMVATupleCreator_v2.py Data_DoubleMu_Run2012B;;
    14) ./TMVATupleCreator_v2.py Data_DoubleMu_Run2012C;;
    
    15) ./TMVATupleCreator_v2.py Data_DoubleElectron_Run2012A;;
    16) ./TMVATupleCreator_v2.py Data_DoubleElectron_Run2012B;;
    17) ./TMVATupleCreator_v2.py Data_DoubleElectron_Run2012C;;
    
esac