#ifndef BASE_OBJECT_H
#define BASE_OBJECT_H
// stl
#include <string>
#include <vector>
#include <sstream>
#include <cmath>
#include <algorithm>


class baseObject
{
    public:

        /// Each derived has access to two bools, that tell it whether to print messagesor not,
        /// We provide NO default constructors...

        baseObject(const bool* show_messages_ptr,const bool * show_debug_messages_ptr );
//        /// protected destructor to make sure this class is never instantiated
//        ///  the compiler won't let us call delete on any base class pointers

        ~baseObject();

    protected:

        /// These are const pointers set at instantiation. They point to bools held in the controller

        const bool * SHOW_DEBUG_MESSAGES_PTR, * SHOW_MESSAGES_PTR;

        /// using default template types makes this easy, ( c++11 feature !? )
        /// these functions allow you to pass up to 7 arguments for a message,
        /// if you would want more just extend etc.

        template<typename T = std::string, typename U = std::string, typename V = std::string, typename W = std::string , typename X = std::string  , typename Y = std::string  , typename Z = std::string, typename A = std::string   >
        void debugMessage(const T p1, const U p2 = "" , const V p3 = "",const W p4 = "", const X p5 = "",const  Y p6 = "", const Z p7 = "", const A p8 = "" )
        {
            if( *SHOW_DEBUG_MESSAGES_PTR )
                printMessage( p1, p2, p3, p4, p5, p6, p7, p8);
        }

        template<typename T = std::string, typename U = std::string, typename V = std::string, typename W = std::string , typename X = std::string  , typename Y = std::string  , typename Z = std::string, typename A = std::string   >
        void message(const T p1,const  U p2 = "" ,const  V p3 = "",const  W p4 = "",const  X p5 = "",const  Y p6 = "", const Z p7 = "",  const A p8 = "" )
        {
            if( *SHOW_MESSAGES_PTR )
                printMessage( p1, p2, p3, p4, p5, p6, p7, p8);
        }

        template<typename T = std::string, typename U = std::string, typename V = std::string, typename W = std::string , typename X = std::string  , typename Y = std::string, typename Z = std::string, typename A = std::string  >
        void printMessage( const T p1,const  U p2 = "" , const V p3 = "",const  W p4 = "", const X p5 = "", const Y p6 = "",const Z p7 = "",  const A p8 = "" )
        {
            std::stringstream ss;
            ss << p1 << p2 << p3 << p4 << p5 << p6 << p7 << p8 <<"\n";
            printf( ss.str().c_str() );
        }

        template<typename T = double >
        double average( const std::vector< T > & v)
        {
            T sum=0;
            for(auto i=0;i!=v.size();++i){
                sum+=v[i];
            }
            return sum/v.size();
        }

        template<typename T = double >
        double dotProduct( const std::vector< T > & v1, const std::vector< T > & v2)
        {
            if(areSame((int)v1.size(),(int)v2.size())){
                T out=0;
                for(auto i=0; i<v1.size();++i){
                    out+=v1[i]*v2[i];
                }
                return out;
            }
            else{debugMessage("Dot product of two vectors could not be completed as they were not the same length."); return 0.;}

        }

        template<typename T = double >
        std::vector< T > subtractVectors( const std::vector< T > & v1, const std::vector< T > & v2)
        {
            std::vector< T > v3;
            if(areSame((int)v1.size(),(int)v2.size())){
                for(auto i=0; i<v1.size();++i){
                    v3.push_back(v1[i]-v2[i]);
                }
            }
            else{debugMessage("Subtraction could not be completed as vectors were not the same length.");}
            return v3;
        }


        template<typename T = int >
        bool areSame( const T a, const T b, const T epsilon = 0)
        {
            if( a == b )
                return true;
            else
                return std::abs( a - b ) < epsilon;
        }

        template<typename T = int >
        bool areNotSame(const  T a, const T b, const T epsilon = 0)
        {
            return !areSame(a, b, epsilon);
        }

        bool polaritiesMatch( const std::vector< double > & vals );

        template<typename T = double >
        double roundToN( const T a, const size_t n )
        {
            double p = pow (10, n);  /// MAGIC_NUMBER
            return std::round(a * p) / p;
        }

        template<typename T = std::string >
        void getSetDifference( const std::vector< T > & a, const std::vector< T > & b, std::vector< T > & c  )
        {
            c.clear();
            std::vector< T > aCopy = a;
            std::vector< T > bCopy = b;

            std::sort( aCopy.begin(), aCopy.end() );
            std::sort( bCopy.begin(), bCopy.end() );


            if( aCopy.size() > bCopy.size()  )
                c.resize( aCopy.size() );
            else
                c.resize( bCopy.size() );
            auto it = std::set_difference( aCopy.begin(), aCopy.end(), bCopy.begin(), bCopy.end(), c.begin());
            c.resize( it - c.begin());
        }



        std::string currentDateTime();

//        template<typename T >
//        bool waitFor( ABoolMemFn f1, velaRFGunInterface & obj, std::string & m,  time_t waitTime)
//        {
//            return waitFor( f1, obj, m.c_str(), waitTime);
//        }
//
//        bool velaRFGunInterface::waitFor( ABoolMemFn f1, velaRFGunInterface & obj, const char * m,  time_t waitTime)
//        {
//            time_t startTime = time( 0 );
//
//            bool timedOut    = false;
//
//            bool state = false;
//
//            while( true )
//            {
//                if( CALL_MEMBER_FN(obj, f1)() )
//                    break;
//
//                else if( time(0) > startTime + waitTime )
//                    timedOut = true;
//
//                if( timedOut )
//                {
//                    message( m );
//                    break;
//                }
//            }
//            return !timedOut;
//        }




    private:
};
#endif //BASE_OBJECT_H
