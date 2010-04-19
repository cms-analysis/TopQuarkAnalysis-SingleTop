#include "TopQuarkAnalysis/SingleTop/interface/CutMap.h"
#include <iostream>
#include <fstream>

using namespace CatoCMS;

CutMap::CutMap( string name, int n_maps )
{
  master_name  = name;
  number_of_maps = n_maps;
  cut_count = 0;
  events    = 0;
  
  count_map = new  map< string, int >[number_of_maps];

  map_names = new string[number_of_maps];
}


CutMap::~CutMap()
{

  delete [] count_map;
  delete [] map_names;
  
}
string CutMap::getMasterName()
{
	return master_name;
}
int CutMap::findItemByKey( const string scut, int map_number )
{
  int value = 0;    
  if (map_number < number_of_maps) {

    map<string, int>::iterator it = count_map[map_number].find ( scut );
    
    if ( it != count_map[map_number].end() ) 
      value = it->second; 
  }
  else
    cerr << " CutMap::findItemByKey : map number out of range" <<endl;
  
  return value;		
}


void CutMap::add(string scut, int map_number, int val)
{

  if (map_number < number_of_maps) {
      // get old value
      int value = findItemByKey( scut , map_number); 

      // get position
      map<string, int>::iterator it = count_map[map_number].find ( scut );

      // delete old entry
      if (it != count_map[map_number].end())
        count_map[map_number].erase( it ); 

      // put new value into map
      value += val;
      pair<string,int> cp(scut, value);
      count_map[map_number].insert(cp); 
    }
  else
    cerr << " CutMap::add : map number out of range" <<endl;
}

void CutMap::addEvent(int nevents)
{
  events+=nevents;
}


void CutMap::init(const string scut)
{

   for (int imap = 0; imap < number_of_maps; imap++) {
     pair<string,int> cp(scut,0);
     count_map[imap].insert(cp); 
     
     pair<int, string> np(cut_count,scut);
     name_map.insert(np); 
     
   }
   cut_count++;
}

void CutMap::print(int level)
{
  // level 0 : only count;
  // level 1 : additional percent
  
  cout<<endl;
  cout<<endl;    
  cout<< "/-------- Statistics for "<< master_name << " -------\\ "<<endl;
  cout<<endl;
  cout<< " Analysed Events : " << events << endl;
  cout<<endl;

  for (int imap = 0; imap < number_of_maps; imap++) {
    cout << "\t" << map_names[imap];
    if (level == 1)
      cout<<"\t";
  }

  if ( number_of_maps > 1 )
    cout<<"\t sum"<<endl;
  else
    cout<<endl;

  cout<<endl;

  for (int imap = 0; imap < number_of_maps+1; imap++)    
    cout<<"---------";
  cout<<endl;
  

  for(map<int, string>::const_iterator i = name_map.begin() ; i != name_map.end() ; ++i) {
    int sum = 0;
    cout << i->second << "\t";
    for (int imap = 0; imap < number_of_maps; imap++)   {
      cout<<findItemByKey(i->second,imap)<<"\t";
      sum += findItemByKey(i->second,imap);
    }
    
    if ( number_of_maps > 1 )
      cout<<sum<<endl;
    else
      cout<<endl;
  }
  
/*       for(map<string,int>::const_iterator i = count_map[imap].begin() ; i != count_map[imap].end() ; ++i) */
/*      cout << i->first << ":" << i->second << '\n'; */
  
  
  cout<<endl;
  cout<< "\\---------";
  for (unsigned int i=0; i<master_name.length()+15; i++)
    cout<<"-";
  cout<< "--------/ "<<endl;
  cout<<endl;
     
  
}

void CutMap::create_tex_head(std::fstream& out_file)
{
  out_file << "  \\begin {tabular}{|l|";
  for(int i=0;i<=number_of_maps; i++)
	out_file << "c|";
  out_file << "}" << endl;
  out_file << "    \\hline" << endl;
  
  out_file << "    Cut &";
  for(int i=0;i<number_of_maps; i++)
	out_file << i << " jet &";
  out_file << "total\\\\"<<endl;
  out_file << "    \\hline"<<endl;
	
}
void CutMap::create_tex_body(std::fstream& out_file)
{
   out_file << "  \\multicolumn{" << number_of_maps+2 << "}{c}{" << master_name << "}\\\\" << endl;
	out_file << "\\hline" << endl;	
	create_tex_body_without_name(out_file);
}
void CutMap::txt_out_map_entry_names(std::fstream& os)
{
	
      os << name_map.size() << endl;	
 for(map<int, string>::const_iterator i = name_map.begin() ; i != name_map.end() ; ++i)
    {	    
      os << i->second << endl;
    }
}

void CutMap::create_txt_output(std::fstream& os)
{
    os << name_map.size() << endl;
    for(map<int, string>::const_iterator i = name_map.begin() ; i != name_map.end() ; ++i)
    {
      os << i->second << endl;
      for (int imap = 0; imap < number_of_maps; imap++)
        {
          if (imap <= 5)
            os<<findItemByKey(i->second,imap)<<"\t";
        }
      os<<endl;
    }
 
}
void CutMap::create_tex_body_without_name(std::fstream& out_file)
{

  for(map<int, string>::const_iterator i = name_map.begin() ; i != name_map.end() ; ++i)
    {
      int sum = 0;
      int g4_sum = 0;
      out_file << i->second << "&";
      for (int imap = 0; imap < number_of_maps; imap++)
        {
          if (imap < 5)
            out_file<<findItemByKey(i->second,imap)<<"&";
          else
            g4_sum += findItemByKey(i->second,imap);
          
          sum += findItemByKey(i->second,imap);
        }
      out_file<<g4_sum<<"&"<<sum<<"\\\\"<<endl;
      out_file << "\\hline" << endl;
    }
  out_file<<endl;

}

void CutMap::create_tex_foot(std::fstream& out_file)
{
	out_file << "\\end{tabular}" << endl;
}

void CutMap::create_tex(char* filename)
{
  ofstream out_file(filename);
  //out_file<<"\\begin{table}[h]"<<endl;
  //out_file<<"  \\begin {tabular}{|l|c|c|c|c|c|c|c|}"<<endl;
  //   out_file<<"    \\hline"<<endl;
  //out_file<<"    Cut & 0 jet & 1 jet & 2 jet & 3 jet & 4 jet & $>$ 4 jet & total\\\\"<<endl;
  //out_file<<"    \\hline"<<endl;


/*   for (int imap = 0; imap < number_of_maps; imap++)     */
/*     { */
/*       out_file << map_names[imap] <<"&&&&&&&"<<endl; */
/*     } */
/*   out_file<<"\\hline"<<endl; */


  for(map<int, string>::const_iterator i = name_map.begin() ; i != name_map.end() ; ++i)
    {
      int sum = 0;
      int g4_sum = 0;
      out_file << i->second << "&";
      for (int imap = 0; imap < number_of_maps; imap++)
        {
          if (imap < 5)
            out_file<<findItemByKey(i->second,imap)<<"&";
          else
            g4_sum += findItemByKey(i->second,imap);
          
          sum += findItemByKey(i->second,imap);
        }
      out_file<<g4_sum<<"&"<<sum<<"\\\\"<<endl;
    }
  out_file<<endl;
  
  out_file.close();   
  
}


void CutMap::setMapNames(string* array_of_names)
{
  map_names = array_of_names;
}




