#ifndef __CATO_CMS_CUTMAP_H__
#define __CATO_CMS_CUTMAP_H__

#include <string>
#include <map>

using namespace std;

namespace CatoCMS
{
	class CutMap 
	{
		protected:
	  string master_name;  
  	string* map_names;            // Array of string to hold names for each map
		int number_of_maps;
		int events;
		int cut_count;
		map<string,int>* count_map;
		map<int, string> name_map;

		int  findItemByKey( string scut , int map_number = 0);

		public:

		CutMap(string name = "cut_map", int n_maps = 1);
		~CutMap();
		string getMasterName(); 
		void init( string scut );
		void add( string scut , int map_number = 0, int val=1);
		void addEvent(int nevents=1);
		void print(int level = 0);
		void create_tex_head(std::fstream&);
		void create_tex_body(std::fstream&);
		void create_tex_body_without_name(std::fstream&);
		void create_tex_foot(std::fstream&);
		void create_tex(char* filename);
		void setMapNames(string* array_of_names);
		void create_txt_output(std::fstream&);
		void txt_out_map_entry_names(std::fstream&);	
	};
}
#endif


