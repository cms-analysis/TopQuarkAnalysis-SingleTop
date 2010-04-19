#include "TopQuarkAnalysis/SingleTop/interface/SampleInfo.h"

using namespace CatoCMS;

SampleInfo::SampleInfo()
{
  cross_section=0.00;
  TotalEvents=0;
  Name="";
  
  // set hardcoded vector elements: 
  // WJets:
  LostEvts.push_back(std::make_pair(1000,0));
  LostEvts.push_back(std::make_pair(1001,0));
  LostEvts.push_back(std::make_pair(1002,0));
  LostEvts.push_back(std::make_pair(1003,0));
  LostEvts.push_back(std::make_pair(1004,0));
  LostEvts.push_back(std::make_pair(1005,0));
  // ZJets:
  LostEvts.push_back(std::make_pair(2000,0));
  LostEvts.push_back(std::make_pair(2001,0));
  LostEvts.push_back(std::make_pair(2002,0));
  LostEvts.push_back(std::make_pair(2003,0));
  LostEvts.push_back(std::make_pair(2004,0));
  LostEvts.push_back(std::make_pair(2005,0));
  // ttbar:
  LostEvts.push_back(std::make_pair(3000,0));
  LostEvts.push_back(std::make_pair(3001,0));
  LostEvts.push_back(std::make_pair(3002,0));
  LostEvts.push_back(std::make_pair(3003,0));
  LostEvts.push_back(std::make_pair(3004,0));
}

SampleInfo::~SampleInfo()
{
}


