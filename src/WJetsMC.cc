//cato header
#include "TopQuarkAnalysis/SingleTop/interface/WJetsMC.h"

using namespace CatoCMS;
WJetsMC::WJetsMC()
{
	p4Lep.SetCoordinates(0.0,0.0,0.0,0.0);
	p4W.SetCoordinates(0.0,0.0,0.0,0.0);
	p4Nu.SetCoordinates(0.0,0.0,0.0,0.0);
	p4TLep.SetCoordinates(0.0,0.0,0.0,0.0);
	p4TTNu.SetCoordinates(0.0,0.0,0.0,0.0);
	p4TLNu.SetCoordinates(0.0,0.0,0.0,0.0);

	mcLepId=0;
	mcNuId=0;
	mcWId=0;
	QLep=0;
	QW=0;
	Muontag=-1;
	Tautag=-1;
	DecChan=-1;
}
WJetsMC::~WJetsMC()
{

}
void WJetsMC::Reset()
{
	p4Lep.SetCoordinates(0.0,0.0,0.0,0.0);
	p4W.SetCoordinates(0.0,0.0,0.0,0.0);
	p4Nu.SetCoordinates(0.0,0.0,0.0,0.0);
	p4TLep.SetCoordinates(0.0,0.0,0.0,0.0);
	p4TTNu.SetCoordinates(0.0,0.0,0.0,0.0);
	p4TLNu.SetCoordinates(0.0,0.0,0.0,0.0);
	mcLepId=0;
	mcNuId=0;
	mcWId=0;
	QLep=0;
	QW=0;
	p4P.clear();
	mcPId.clear();
	Muontag=-1;
	Tautag=-1;
	DecChan=-1;

}
