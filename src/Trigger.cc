#include "TopQuarkAnalysis/SingleTop/interface/Trigger.h"


using namespace CatoCMS;

Trigger::Trigger():
  mu(-1), el(-1)
{
}

Trigger::~Trigger()
{
}

void Trigger::Reset()
{
  mu = -1; // -1: unavailable info
  el = -1; // -1: unavailable info
}
