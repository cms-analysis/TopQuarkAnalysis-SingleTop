cd ../../
addpkg DataFormats/PatCandidates V06-05-06-03
addpkg PhysicsTools/PatAlgos     V08-09-43
addpkg RecoParticleFlow/PFProducer V15-02-06
cvs co -r V00-00-13      -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools
cd EGamma/EGammaAnalysisTools/data
cat download.url | xargs wget                      

cd ../../../

cvs co -r V00-02-05 -d CMGTools/External UserCode/CMG/CMGTools/External

#MET Filters
cvs co -r V00-00-13 RecoMET/METFilters
cvs co -r V00-00-08 RecoMET/METAnalyzers
cvs co -r V00-03-23 CommonTools/RecoAlgos
cvs co -r V01-00-11-01 DPGAnalysis/Skims
cvs co -r V00-11-17 DPGAnalysis/SiStripTools
cvs co -r V00-00-08 DataFormats/TrackerCommon
cvs co -r V01-09-05 RecoLocalTracker/SubCollectionProducers
cvs co -r V01-00-04 EventFilter/HcalRawToDigi


#cp TopQuarkAnalysis/SingleTop/python/pfIsolation_fix.py CommonTools/ParticleFlow/python/Tools/pfIsolation.py

#cp TopQuarkAnalysis/SingleTop/test/lhapdfwrapnew.xml $CMSSW_BASE/config/toolbox/$SCRAM_ARCH/tools/selected/lhapdfwrap.xml
#cp TopQuarkAnalysis/SingleTop/test/lhapdfnew.xml $CMSSW_BASE/config/toolbox/$SCRAM_ARCH/tools/selected/lhapdf.xml
#cp TopQuarkAnalysis/SingleTop/test/lhapdffullnew.xml $CMSSW_BASE/config/toolbox/$SCRAM_ARCH/tools/selected/lhapdffull.xml

cmsenv
scram setup lhapdffull
cmsenv