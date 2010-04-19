#ifndef __CATO_CMS_VEC_H__
#define __CATO_CMS_VEC_H__

#include "Math/GenVector/PositionVector3D.h"
#include "Math/Point3D.h"
#include "Math/GenVector/CoordinateSystemTags.h"
typedef ROOT::Math::PositionVector3D<ROOT::Math::Cartesian3D<double> > Point3;

/* #include "Math/DisplacementVector2D.h" */
/* typedef ROOT::Math::XYVector<ROOT::Math::Cartesian2D<double> > Vector2; */

#include "Math/PxPyPzE4D.h"
#include "Math/LorentzVector.h"
typedef ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double> > LorentzVector;

#endif
