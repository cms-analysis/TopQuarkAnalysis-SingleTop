//cato header
#include "TopQuarkAnalysis/SingleTop/interface/QCDMC.h"

using namespace CatoCMS;
QCDMC::QCDMC()
{
	p4El.SetCoordinates(0.0,0.0,0.0,0.0);
	p4ElMother.SetCoordinates(0.0,0.0,0.0,0.0);
	p4Mu.SetCoordinates(0.0,0.0,0.0,0.0);
	p4MuMother.SetCoordinates(0.0,0.0,0.0,0.0);
	mcElId=0;
	mcElMotherId=0;
	mcMuId=0;
	mcMuMotherId=0;
	QEl=0;
	QMu=0;
	QElMother=0;
	QMuMother=0;
	p4P.clear();
	mcPId.clear();
}
QCDMC::~QCDMC()
{

}
void QCDMC::Reset()
{
	p4El.SetCoordinates(0.0,0.0,0.0,0.0);
	p4ElMother.SetCoordinates(0.0,0.0,0.0,0.0);
	p4Mu.SetCoordinates(0.0,0.0,0.0,0.0);
	p4MuMother.SetCoordinates(0.0,0.0,0.0,0.0);
	mcElId=0;
	mcElMotherId=0;
	mcMuId=0;
	mcMuMotherId=0;
	QEl=0;
	QMu=0;
	QElMother=0;
	QMuMother=0;
	p4P.clear();
	mcPId.clear();

}
