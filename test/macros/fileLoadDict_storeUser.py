#!/usr/bin/env python                                                                                                                  

storeUser = '~/storeUser/tW_8TeV/Ntuples/'

fileLists = { 'TWDilepton':['TWChannelDilepton',
                            [storeUser+'ntuple_SysTrees_TWChannelDilepton.root',
                             storeUser+'ntuple_SysTrees_TbarWChannelDilepton.root'],
                            'TWDilepton.root'],
              'TTbarDilepton':['TTBarDilepton',
                               [storeUser+'ntuple_SysTrees_TTBarDilepton.root'],
                               'TTbarDilepton.root'],
              'TWChannel':['TWChannel',
                           [storeUser+'ntuple_SysTrees_TWChannel.root'],
                           'TWChannel.root'],
              'TTbar':['TTBar',
                       [storeUser+'ntuple_SysTrees_TTBar.root'],
                       'TTbar.root'],
              'TChannel':['TChannel',
                          [storeUser+'ntuple_SysTrees_TChannel.root',
                           storeUser+'ntuple_SysTrees_TbarChannel.root'],
                          'TChannel.root'],
              'SChannel':['SChannel',
                          [storeUser+'ntuple_SysTrees_SChannel.root',
                           storeUser+'ntuple_SysTrees_SbarChannel.root'],
                          'SChannel.root'],
              'ZJets':['ZJets',
                       [storeUser+'ntuple_SysTrees_ZJets.root',
                        storeUser+'ntuple_SysTrees_ZJetsLowMass'],
                       'ZJets.root'],
              'WJets':['WJets',
                       [storeUser+'ntuple_SysTrees_WJets.root'],
                       'WJets.root'],
              'WW':['WW',
                    [storeUser+'ntuple_SysTrees_WW.root'],
                    'WW.root'],
              'ZZ':['ZZ',
                    [storeUser+'ntuple_SysTrees_ZZ.root'],
                    'ZZ.root'],
              'WZ':['WZ',
                    [storeUser+'ntuple_SysTrees_WZ.root'],
                    'WZ.root'],
              'TWChannel_DS':['TWChannel',
                              [storeUser+'ntuple_SysTrees_TWChannel_DS.root',
                               storeUser+'ntuple_SysTrees_TbarWChannel_DS.root'],
                              'TWChannel_DS.root'],
              'TWChannel_Q2Up':['TWChannel_Q2Up',
                                [storeUser+'ntuple_SysTrees_TWChannel_Q2Up.root',
                                 storeUser+'ntuple_SysTrees_TbarWChannel_Q2Up.root'],
                                'TWChannel_Q2Up.root'],
              'TWChannel_Q2Down':['TWChannel_Q2Down',
                                  [storeUser+'ntuple_SysTrees_TWChannel_Q2Down.root',
                                   storeUser+'ntuple_SysTrees_TbarWChannel_Q2Down.root'],
                                  'TWChannel_Q2Down.root'],
              'TTBar_Q2Up':['TTBar_Q2Up',
                            [storeUser+'ntuple_SysTrees_TTBar_Q2Up.root'],
                            'TTBar_Q2Up.root'],
              'TTBar_Q2Down':['TTBar_Q2Down',
                              [storeUser+'ntuple_SysTrees_TTBar_Q2Down.root'],
                              'TTBar_Q2Down.root'],
              'TTBar_MatchingUp':['TTBar_MatchingUp',
                                  [storeUser+'ntuple_SysTrees_TTBar_MatchingUp.root'],
                                  'TTBar_MatchingUp.root'],
              'TTBar_MatchingDown':['TTBar_MatchingDown',
                                    [storeUser+'ntuple_SysTrees_TTBar_MatchingDown.root'],
                                    'TTBar_MatchingDown.root'],
              'TTBar_Mass166_5':['TTBar_Mass166_5',
                                 [storeUser+'ntuple_SysTrees_TTBar_Mass166_5.root'],
                                 'TTBar_Mass166_5.root'],
              'TTBar_Mass178_5':['TTBar_Mass178_5',
                                 [storeUser+'ntuple_SysTrees_TTBar_Mass178_5.root'],'TTBar_Mass178_5.root'],
              'TWChannel_Mass166_5':['TWChannel_Mass166_5',
                                     [storeUser+'ntuple_SysTrees_TWChannel_Mass166_5.root',
                                      storeUser+'ntuple_SysTrees_TbarWChannel_Mass166_5.root'],
                                     'TWChannel_Mass166_5.root'],
              'TWChannel_Mass178_5':['TWChannel_Mass178_5',
                                     [storeUser+'ntuple_SysTrees_TWChannel_Mass178_5.root',
                                      storeUser+'ntuple_SysTrees_TbarWChannel_Mass178_5.root'],
                                     'TWChannel_Mass178_5.root'],



              'Data_MuEG_Run2012A':['Data',
                                    [storeUser+'ntuple_SysTrees_MuEG_Run2012A-13July2012.root',
                                     storeUser+'ntuple_SysTrees_MuEG_Run2012A-recover-06Aug2012.root'],
                                    'Data_MuEG_Run2012A.root'],
              'Data_MuEG_Run2012B':['Data',
                                    [storeUser+'ntuple_SysTrees_MuEG_Run2012B-13July2012.root'],
                                    'Data_MuEG_Run2012A.root'],
              'Data_MuEG_Run2012A':['Data',
                                    [storeUser+'ntuple_SysTrees_MuEG_Run2012C-24Aug2012.root',
                                     storeUser+'ntuple_SysTrees_MuEG_Run2012C-PromptReco.root'],
                                    'Data_MuEG_Run2012A.root'],
              
              'Data_DoubleMu_Run2012A':['Data',
                                        [storeUser+'ntuple_SysTrees_DoubleMu_Run2012A-13July2012.root',
                                         storeUser+'ntuple_SysTrees_DoubleMu_Run2012A-recover-06Aug2012.root'],
                                        'Data_DoubleMu_Run2012A.root'],
              'Data_DoubleMu_Run2012B':['Data',
                                        [storeUser+'ntuple_SysTrees_DoubleMu_Run2012B-13July2012.root'],
                                        'Data_DoubleMu_Run2012A.root'],
              'Data_DoubleMu_Run2012A':['Data',
                                        [storeUser+'ntuple_SysTrees_DoubleMu_Run2012C-24Aug2012.root',
                                         storeUser+'ntuple_SysTrees_DoubleMu_Run2012C-PromptReco.root'],
                                        'Data_DoubleMu_Run2012A.root'],

              'Data_DoubleElectron_Run2012A':['Data',
                                              [storeUser+'ntuple_SysTrees_DoubleElectron_Run2012A-13July2012.root',
                                               storeUser+'ntuple_SysTrees_DoubleElectron_Run2012A-recover-06Aug2012.root'],
                                              'Data_DoubleElectron_Run2012A.root'],
              'Data_DoubleElectron_Run2012B':['Data',
                                              [storeUser+'ntuple_SysTrees_DoubleElectron_Run2012B-13July2012.root'],
                                              'Data_DoubleElectron_Run2012A.root'],
              'Data_DoubleElectron_Run2012A':['Data',
                                              [storeUser+'ntuple_SysTrees_DoubleElectron_Run2012C-24Aug2012.root',
                                               storeUser+'ntuple_SysTrees_DoubleElectron_Run2012C-PromptReco.root'],
                                              'Data_DoubleElectron_Run2012A.root'],
              
              
              }
