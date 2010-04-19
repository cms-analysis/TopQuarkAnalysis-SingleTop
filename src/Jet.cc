//-------------------------------------------------------------------------------
//
// CVS revision record:
// $Author: weinelt $
// $Date: 2010/01/14 16:39:11 $
// $Revision: 1.1 $
// 
//-------------------------------------------------------------------------------

#include "TopQuarkAnalysis/SingleTop/interface/Jet.h"

using namespace CatoCMS;

Jet::Jet():
  scale(0.0),
  emEnergyFraction(0.0),
  nTracks(0),
  partonFlavour(0),
  isTagged(0)
{
}

Jet::~Jet() 
{
}

void Jet::Reset()
{
  v4.SetCoordinates(0.0, 0.0, 0.0, 0.0);
  scale =0;
  
  tags.clear();
  
  emEnergyFraction =0.0;
  nTracks =0;
  partonFlavour =0;
  isTagged = 0;

  vertex.SetCoordinates(-999.0,-999.0,-999.0);
}

// get tag value for certain tagging algorithm:
double Jet::GetTag(std::string label)
{
  // new:
  double tagVal = -10.;
  if (label == "default")
    label = "trackProbabilityJetTags";
  
  std::map<std::string, double>::iterator iter = tags.find(label);
  if(iter != tags.end())
    tagVal = iter->second;

  return tagVal;
  
  //   double tagVal = -10.;
  //   if (label == "default") 
  //     label = "trackProbabilityJetTags";
  //   for(size_t i=0; i!=tags.size(); i++){
  //     if(tags.at(i).first == label){
  // 		 	tagVal = tags.at(i).second;
  // 			break;
  //     }
  // 	}
  //   return tagVal;
}


void Jet::PrintTags()
{
  if(tags.size())
    for(std::map<std::string, double>::iterator iter = tags.begin();
        iter != tags.end(); iter++)
      std::cout << iter->first << " :\t" << iter->second << "\n";
  else
    std::cout << "NO tags found!!\n";
  
  //   if(tags.size())
  //     for(size_t i=0; i<tags.size(); i++)
  //       std::cout << tags.at(i).first << " :\t" << tags.at(i).second << "\n";
  //   else
  //     std::cout << "NO tags found!!\n";
}

