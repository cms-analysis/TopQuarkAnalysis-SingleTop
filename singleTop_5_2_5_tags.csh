cd ../../


addpkg DataFormats/PatCandidates   V06-05-01
addpkg PhysicsTools/PatAlgos       V08-09-09
addpkg CommonTools/ParticleFlow    V00-03-11
addpkg JetMETCorrections/Type1MET  V04-06-05
addpkg PhysicsTools/PatUtils
cvs co -r b5_2_X_cvMEtCorr_2012May08 PhysicsTools/PatUtils/plugins
cvs up -r b5_2_X_cvMEtCorr_2012May08 PhysicsTools/PatUtils
cvs co -r V00-00-08      -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools
cd EGamma/EGammaAnalysisTools/data
cat download.url | xargs wget                      
cp python/pfIsolation_fix.py ../../CommonTools/ParticleFlow/python/Tools/pfIsolation.py


cd ../../

