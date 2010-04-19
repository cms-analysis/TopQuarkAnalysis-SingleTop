#ifndef __CATO_CMS_WJETS_MC__
#define __CATO_CMS_WJETS_MC__
//root header
#include "Vec.h"
#include <vector>
namespace CatoCMS
{
	class WJetsMC{
		public:
			WJetsMC();
			~WJetsMC();
			void Reset();
			LorentzVector p4Lep;
			LorentzVector p4W;
			LorentzVector p4Nu;
			LorentzVector p4TLep;		//Filled if Lepton is a tau 
			LorentzVector p4TLNu;
			LorentzVector p4TTNu;	
			int Muontag;                    // =1 if charged lepton is Muon
			// =0 else
			int Tautag;                     // =1 if charged lepton is Tau
			// =0 else
			int  DecChan;                   // =0 for e/mu/nu
			// =1 for tau/nu
			// =2 for qqbar (not included in MG samples!!)	
			int hadronic;
			int	mcLepId;
			int 	mcNuId;
			int 	mcWId;
			int	QLep;
			int 	QW;
			int 	NumberOfHardPartons;
			int	NumberOfParticlesInTauCone;
			std::vector<int>	mcPId;
			std::vector<LorentzVector>	p4P;
	};
}
#endif //__CATO_CMS_WJETS_MC_ _
