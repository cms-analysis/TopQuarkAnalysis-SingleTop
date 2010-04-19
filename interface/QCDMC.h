#ifndef __CATO_CMS_QCD_MC__
#define __CATO_CMS_QCD_MC__
//root header
#include "Vec.h"
#include <vector>
namespace CatoCMS
{
	class QCDMC{
		public:
			QCDMC();
			~QCDMC();
			void Reset();
			LorentzVector p4El;
			LorentzVector p4ElMother;
			LorentzVector p4Mu;
			LorentzVector p4MuMother;
			int	mcElId;
			int 	mcElMotherId;
			int	mcMuId;
			int 	mcMuMotherId;
			int	QEl;
			int 	QElMother;
			int	QMu;
			int 	QMuMother;
			std::vector<int>	mcPId;
			std::vector<LorentzVector>	p4P;
	};
}
#endif //__CATO_CMS_QCD_MC_ _
