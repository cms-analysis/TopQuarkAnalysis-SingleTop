#include "TopQuarkAnalysis/SingleTop/interface/CutFlowTable.h"
#include <iostream> 
#include "stdlib.h"
#include <sstream>
using namespace std;
using namespace CatoCMS;
CutFlowTable::CutFlowTable(int columns) 
{
	foo_map = new CutMap("cut", columns); 

	CutMap *m = new CutMap("All",columns);

	m_columns = columns;
	
	m_map.insert(make_pair("All",m));

	foo_map->init("Total");
	foo_map->init("Preselected");
	//	foo_map->init("relIso");
	//	foo_map->init("$\\ge$ 1 Tight Std. Lepton");
	//	foo_map->init("Loose Lepton Cut");
	
}
CutFlowTable::CutFlowTable(ifstream& is)
{
	int rows=1;
	int val=0;
	int size=0;
	string cut;
	string map;
	string line;
	
	CutMap *m;
	getline(is,line);
	m_columns = atoi(line.c_str());
	cout <<"columns: "<< m_columns << endl;
	getline(is,line);
	size = atoi(line.c_str());

	getline(is,map);
	getline(is,line);
	rows = atoi(line.c_str());

	foo_map = new CutMap(map,m_columns);
	for(int r=0;r<rows;r++){
		getline(is,cut);
		foo_map->init(cut);
		getline(is,line);
		istringstream s(line);
		for(int c=0;c<m_columns;c++){
			s >> val;			
			if(cut=="Total") addEvent(val);
			add(map,cut,c,val);
		}
	}		
	
	for(int s=0;s<size;s++){
		if(is.fail())
			break;
		getline(is,map);
		getline(is,line);
		rows = atoi(line.c_str());
		m = new CutMap(map,m_columns);
		m_map.insert(make_pair(map,m));
		for(int r=0;r<rows;r++){
			getline(is,cut);
			m->init(cut);
			getline(is,line);
			istringstream s(line);	
			if(map=="All")
				continue;
			for(int c = 0;c<m_columns;c++){
				s >> val;
				add(map,cut,c,val);
			}
		}		
	}
}
void CutFlowTable::AddTableFromFile(ifstream& is)
{
	int rows=1;
	int val=0;
	int size=0;
	string cut;
	string map;
	string line;
	
	getline(is,line);
//	m_columns = atoi(line.c_str());
	getline(is,line);
	size = atoi(line.c_str());

	getline(is,map);
	getline(is,line);
	rows = atoi(line.c_str());

	for(int r=0;r<rows;r++){
		getline(is,cut);
		getline(is,line);
		istringstream s(line);
		for(int c=0;c<m_columns;c++){
			s >> val;			
			if(cut=="Total") addEvent(val);
			add(map,cut,c,val);
		}
	}		
	
	for(int s=0;s<size;s++){
		if(is.fail())
			break;
		getline(is,map);
		getline(is,line);
		rows = atoi(line.c_str());
		for(int r=0;r<rows;r++){
			getline(is,cut);
			getline(is,line);
			istringstream s(line);	
			if(map=="All")
				continue;
			for(int c = 0;c<m_columns;c++){ //why m_columns-1????
				s >> val;
				add(map,cut,c,val);
			}
		}		
	}
}
CutFlowTable::~CutFlowTable()
{
	delete foo_map;
	for(map<string, CutMap*>::iterator it=m_map.begin(); it!=m_map.end();it++)
		delete it->second;

}
void CutFlowTable::AddTable(string name)
{
	m_map.insert(make_pair(name,new CutMap(name,m_columns)));
}
void CutFlowTable::init(string scut)
{
	for(map<string, CutMap*>::iterator it=m_map.begin(); it!=m_map.end();it++)
		it->second->init(scut);
}
void CutFlowTable::add(string table,string scut, int map_number, int val)
{
  //last col is >= m_columns -1 Jets
  if(map_number >= (m_columns-1)) map_number = m_columns -1;
  
  //this is not the right way to do it!!!
  if(table == "cut")
    {
      foo_map->add(scut,map_number,val);
      return;
    }
  
  map<string, CutMap*>::iterator item = m_map.find(table);
  map<string, CutMap*>::iterator item2 = m_map.find("All");
  if(item!=m_map.end() && item2!=m_map.end())
    {
      item->second->add(scut,map_number,val);
      item2->second->add(scut,map_number,val);
    }
  else
    cerr << "Counting failed for item " << table << endl;
}
void CutFlowTable::addEvent(int events)
{
	foo_map->addEvent(events);
	for(map<string, CutMap*>::iterator it=m_map.begin(); it!=m_map.end();it++)
		it->second->addEvent(events);
}
void CutFlowTable::print(int level)
{
	for(map<string, CutMap*>::iterator it=m_map.begin(); it!=m_map.end();it++)
		it->second->print(level);
}
void CutFlowTable::txt_output(std::fstream& os)
{
	os << m_columns << endl;
	os << m_map.size() << endl;
	//foo table sections
	os << foo_map->getMasterName() << endl;
	foo_map->create_txt_output(os);
	//zeilen beschriftungen
	for(map<string, CutMap*>::iterator it=m_map.begin(); it!=m_map.end();it++)
	{
		os << it->first << endl;
		it->second->create_txt_output(os);
	}
}
void CutFlowTable::OpenTxt(std::fstream& is)
{
}
void CutFlowTable::tex_output(std::fstream& os)
{
  os << "  \\begin {tabular}{|l|";
  for(int i=0;i<=m_columns; i++)
	os << "c|";
  os << "}" << endl;
  os << "    \\hline" << endl;
  
  os << "    Cut &";
  for(int i=0;i<m_columns; i++)
	os << i << " jet &";
  os << "total\\\\"<<endl;
  os<<"    \\hline"<<endl;

 foo_map->create_tex_body_without_name(os);
 for(map<string, CutMap*>::iterator it=m_map.begin(); it!=m_map.end();it++)
		it->second->create_tex_body(os);

  os << "\\end{tabular}" << endl;

 
}

