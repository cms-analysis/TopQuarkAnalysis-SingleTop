cd ../../

addpkg DataFormats/PatCandidates   V06-05-01
addpkg PhysicsTools/PatAlgos       V08-09-10
addpkg CommonTools/ParticleFlow    V00-03-13
addpkg JetMETCorrections/Type1MET  V04-06-05
addpkg PhysicsTools/PatUtils V03-09-22
addpkg CommonTools/RecoUtils V00-00-08
cvs co -r V00-00-08      -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools
cd EGamma/EGammaAnalysisTools/data
cat download.url | xargs wget                      
cp python/pfIsolation_fix.py ../../CommonTools/ParticleFlow/python/Tools/pfIsolation.py

cd ../../

scram b -j 9 > & step1.log &
