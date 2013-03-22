cd ../../
addpkg DataFormats/PatCandidates   V06-05-06-07
addpkg PhysicsTools/PatAlgos       V08-09-52
addpkg PhysicsTools/PatUtils       V03-09-28
addpkg DataFormats/StdDictionaries V00-02-14
addpkg FWCore/GuiBrowsers          V00-00-70
addpkg RecoMET/METProducers        V03-03-12-02
addpkg RecoMET/METAnalyzers        V00-00-08
addpkg RecoMET/METFilters          V00-00-13
addpkg RecoMET/METProducers        V03-03-12-02
addpkg RecoParticleFlow/PFProducer V15-02-06
cvs co -r V00-00-30      -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools
cd EGamma/EGammaAnalysisTools/data
cat download.url | xargs wget                      

cd ../../../

cvs co -r V00-02-05 -d CMGTools/External UserCode/CMG/CMGTools/External

cp TopQuarkAnalysis/SingleTop/python/pfIsolation_fix.py CommonTools/ParticleFlow/python/Tools/pfIsolation.py

#cp TopQuarkAnalysis/SingleTop/test/lhapdfwrapnew.xml $CMSSW_BASE/config/toolbox/$SCRAM_ARCH/tools/selected/lhapdfwrap.xml
#cp TopQuarkAnalysis/SingleTop/test/lhapdfnew.xml $CMSSW_BASE/config/toolbox/$SCRAM_ARCH/tools/selected/lhapdf.xml
#cp TopQuarkAnalysis/SingleTop/test/lhapdffullnew.xml $CMSSW_BASE/config/toolbox/$SCRAM_ARCH/tools/selected/lhapdffull.xml

cmsenv
scram setup lhapdffull
cmsenv

scram b -j 9 > & step1.log &
