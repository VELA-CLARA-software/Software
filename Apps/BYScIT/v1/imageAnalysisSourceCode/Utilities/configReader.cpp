#include "configReader.h"
//stl
#include <iostream>
#include <sstream>
#include <time.h>
#include <algorithm>
#include "configReader.h"
//stl
#include <iostream>
#include <sstream>
#include <time.h>
#include <algorithm>
#include <fstream>
//djs
#include "configDefinitions.h"
#include "velaStructs.h"

configReader::configReader( const bool* show_messages_ptr, const  bool * show_debug_messages_ptr )
: configVersion( -1 ), numObjs( -1 ), numIlocks( -1 ), configFile_Path( "" ), baseObject( show_messages_ptr, show_debug_messages_ptr )
{}
configReader::configReader( const std::string & configFile_Location, const bool* show_messages_ptr, const  bool * show_debug_messages_ptr )
: configVersion( -1 ), numObjs( -1 ), numIlocks( -1 ), configFile_Path( configFile_Location ), baseObject( show_messages_ptr, show_debug_messages_ptr )
{}
//______________________________________________________________________________
configReader::~configReader(){}
//______________________________________________________________________________
void configReader::setConfigFilePath( const std::string & path )
{
    configFile_Path = path;
}
//______________________________________________________________________________
std::string  configReader::getAfterEqualsSign( const std::string & str )
{
    std::size_t found = str.find_last_of( UTL::EQUALS_SIGN );
    return str.substr( found + 1, str.size()  );
}
//______________________________________________________________________________
void configReader::getVersion( const std::string & str )
{
    std::string num = getAfterEqualsSign( str );
    configVersion = atoi(num.c_str());
}
//______________________________________________________________________________
void configReader::getNumObjs(const  std::string & str )
{
    std::string num = getAfterEqualsSign( str );
    numObjs = atoi(num.c_str());
}
//______________________________________________________________________________
void configReader::getNumIlocks( const std::string & str )
{
    std::string num = getAfterEqualsSign( str );
    numIlocks = atoi(num.c_str());
}
//______________________________________________________________________________
int configReader::getNum( const std::string & str )
{
    std::string num = getAfterEqualsSign( str );
    return atoi( num.c_str() );
}
//______________________________________________________________________________
size_t configReader::getSize( const std::string & str )
{
    return (size_t)getNum( str );
}
//______________________________________________________________________________
double configReader::getNumD( const  std::string & str )
{
    return atof( str.c_str() );
}
//______________________________________________________________________________
std::string configReader::trimToDelimiter( std::string const & str, const std::string & STOPDELIMITER )
{
    size_t last = str.find_first_of( STOPDELIMITER );
    return str.substr( 0, last );
}
//______________________________________________________________________________
std::string & configReader::trimAllWhiteSpace( std::string & str)
{
    str.erase( std::remove_if( str.begin(), str.end(), isspace), str.end());
    return str;
}
//______________________________________________________________________________
bool configReader::stringIsSubString( const std::string & stringToCheck, const std::string & stringToLookFor )
{
    return stringToCheck.find( stringToLookFor) != std::string::npos;
}
//______________________________________________________________________________
std::string configReader::getSubString( std::string & str, std::string & STARTDELIMITER, std::string & STOPDELIMITER  )
{
    unsigned first = str.find( STARTDELIMITER );
    unsigned last  = str.find( STOPDELIMITER );

    std::string temp = str.substr( first + 1, last - first - 1 );

    return   trimWhiteSpaces( temp );
}
//______________________________________________________________________________
std::string configReader::trimWhiteSpaces( const  std::string & str )
{
    size_t first = str.find_first_not_of(' ');
    size_t last  = str.find_last_not_of(' ');
    return str.substr(first, (last-first+1));
}
std::string configReader::trimBetween( std::string & str, std::string & STARTDELIMITER, std::string & STOPDELIMITER  )
{
    size_t first = str.find_first_not_of(STARTDELIMITER);
    size_t last  = str.find_last_not_of(STOPDELIMITER);
    return str.substr(first, (last-first+1));
}
//______________________________________________________________________________
std::vector<std::string> configReader::getKeyVal( const  std::string & trimmedLine, const char delim )
{
    std::stringstream ss(trimmedLine);
    std::string item;
    std::vector<std::string> entry;
    while( std::getline(ss, item, delim ) )
        entry.push_back( item );
//    for( int i = 0; i < entry.size(); ++i )
//        std::cout << "entry "<< i << " = " <<  entry[ i ] << std::endl;
    return entry;
}
//______________________________________________________________________________
std::vector< double >  configReader::getDoubleVector( const std::string & str )
{
    std::vector< double > ret;
    std::stringstream ss( str );
    std::string s;

    while( ss )
    {
        if( !getline( ss, s, ',' ) )
            break;
        else
            ret.push_back( atof( s.c_str() ) );
    }
    return ret;
}
//______________________________________________________________________________
unsigned long configReader::getMASK(const  std::string & val )
{
    unsigned long r = DBE_VALUE; /// init to something
        /// ladder it?
    if( val == UTL::DBE_VALUE_STR )
        r = DBE_VALUE;
    else if( val == UTL::DBE_LOG_STR )
        r = DBE_LOG;
    else if( val == UTL::DBE_ALARM_STR )
        r = DBE_ALARM;
    return r;
}
//______________________________________________________________________________
unsigned long configReader::getCOUNT( const std::string & val )
{
    return  std::stoul( val.c_str() );
}
//______________________________________________________________________________
chtype configReader::getCHTYPE( const  std::string & val )
{
  unsigned long r = DBR_CLASS_NAME; /// init to something not often used?

    /// ladder it?

    if( val == UTL::DBR_STRING_STR )
        r = DBR_STRING;
    else if( val == UTL::DBR_INT_STR )
        r = DBR_INT;
    else if( val == UTL::DBR_SHORT_STR )
        r = DBR_SHORT;
    else if( val == UTL::DBR_FLOAT_STR )
        r = DBR_FLOAT;
    else if( val == UTL::DBR_ENUM_STR )
        r = DBR_ENUM;
    else if( val == UTL::DBR_CHAR_STR )
        r = DBR_CHAR;
    else if( val == UTL::DBR_LONG_STR )
        r = DBR_LONG;
    else if( val == UTL::DBR_DOUBLE_STR )
        r = DBR_DOUBLE;
    else if( val == UTL::DBR_TIME_STRING_STR )
        r = DBR_TIME_STRING;
    else if( val == UTL::DBR_TIME_INT_STR )
        r = DBR_TIME_INT;
    else if( val == UTL::DBR_TIME_SHORT_STR )
        r = DBR_TIME_SHORT;
    else if( val == UTL::DBR_TIME_FLOAT_STR )
        r = DBR_TIME_FLOAT;
    else if( val == UTL::DBR_TIME_ENUM_STR )
        r = DBR_TIME_ENUM;
    else if( val == UTL::DBR_TIME_CHAR_STR )
        r = DBR_TIME_CHAR;
    else if( val == UTL::DBR_TIME_LONG_STR )
        r = DBR_TIME_LONG;
    else if( val == UTL::DBR_TIME_DOUBLE_STR )
        r = DBR_TIME_DOUBLE;
    return r;
}
//______________________________________________________________________________

