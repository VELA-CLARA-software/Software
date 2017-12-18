#include "baseObject.h"
#include <time.h>

baseObject::baseObject( const bool* show_messages_ptr,const bool * show_debug_messages_ptr )
: SHOW_MESSAGES_PTR( show_messages_ptr ), SHOW_DEBUG_MESSAGES_PTR( show_debug_messages_ptr )
{}
//______________________________________________________________________________
baseObject::~baseObject(){}
//______________________________________________________________________________
bool baseObject::polaritiesMatch( const std::vector< double > & vals )
{/// to make this a template need to think about the test comapring to 0.0
    bool ret = true;
    std::vector< bool > signs;
    for( auto && it : vals )
        if( it != 0.0 ) /// zero can have either polarity
            signs.push_back( std::signbit( it ) );
    for( auto && it : signs )
        if( signs[0] != it  )
            ret = false;
    return ret;
}
//______________________________________________________________________________
std::string baseObject::currentDateTime()
{
    time_t     now = time(0);
    struct tm  tstruct;
    char       buf[80];
    tstruct = *localtime(&now);
    // Visit http://en.cppreference.com/w/cpp/chrono/c/strftime
    // for more information about date/time format
    strftime(buf, sizeof(buf), "%Y-%m-%d-%H%M", &tstruct);
    return buf;
}
