
#ifndef CONFIG_READER_YAG_H
#define CONFIG_READER_YAG_H
// stl
#include <string>
#include <vector>
#include <map>
// me
#include "configReader.h"
#include "imageStructs.h"



class configReaderYAG : public configReader
{
    public:
        configReaderYAG( const bool* show_messages_ptr, const  bool * show_debug_messages_ptr  );
        ~configReaderYAG();

        bool readYAGConfig(const std::string& yag);

        imageDataStruct getConfigData();


    protected:
        imageDataStruct dataFromConfig;
    private:

};
#endif //UTL_FILE_IO_H
