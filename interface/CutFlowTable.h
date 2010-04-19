#ifndef __CATO_CMS_CUTFLOWTABLE__
#define __CATO_CMS_CUTFLOWTABLE__

#include "CutMap.h"
#include <fstream>
#include <map>

namespace CatoCMS
{
	class CutFlowTable
	{
		protected:
			std::map<string, CutMap*> m_map;
			int m_columns;
			CutMap *foo_map;
		
		public:
		CutFlowTable(int columns);
		CutFlowTable(std::ifstream&);
		~CutFlowTable();
		void init(string scut);
		void add(string table, string scut, int map_number = 0, int val=1);
		void addEvent(int events=1);
		void AddTable(string name);
		void print(int level = 0);
		void tex_output(std::fstream&);
		void txt_output(std::fstream&);
		void OpenTxt(std::fstream&);
		void AddTableFromFile(std::ifstream&);
	};
}
#endif



