cd ../../

cvs co -r V06-05-01      DataFormats/PatCandidates                        
cvs co -r V08-09-06      PhysicsTools/PatAlgos                            
cvs co -r V00-05-25      PhysicsTools/PatExamples   
cvs co -r V00-00-08      -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools
cd EGamma/EGammaAnalysisTools/data
cat download.url | xargs wget                      

cd ../../

