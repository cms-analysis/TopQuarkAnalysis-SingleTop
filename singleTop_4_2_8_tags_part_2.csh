cvs co -r b4_2_X_cvMEtCorr_30Nov11 PhysicsTools/PatUtils
cvs co -r V04-05-07 JetMETCorrections/Type1MET
cvs co -r V02-03-00 JetMETCorrections/Algorithms
rm -f JetMETCorrections/Algorithms/interface/L1JPTOffsetCorrector.h
rm -f JetMETCorrections/Algorithms/src/L1JPTOffsetCorrector.cc
cvs co -r V03-01-00 JetMETCorrections/Objects
addpkg JetMETCorrections/Modules
cvs up -r 1.4 JetMETCorrections/Modules/plugins/JetCorrectorOnTheFly.cc
cvs up -r 1.6 JetMETCorrections/Modules/interface/JetCorrectionProducer.h
cvs co -r $CMSSW_VERSION PhysicsTools/PatAlgos
cvs up -r 1.64.2.4 PhysicsTools/PatAlgos/python/tools/jetTools.py


scram b -j 9 > & step2.log &

