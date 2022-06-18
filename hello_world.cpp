#include <iostream>
#include <gem5/m5ops.h>
using namespace std;


class test
{
    public:
    int count[1000]={0};
    int test1(){

        m5_work_begin(100,100);
        cout << "begin inner coumputing " << endl;
        
        for (size_t i = 0; i < 10; i++)
        {
            count[i]=(i+100)*i;
            for(int j= i;j<1000;j++){
                count[j]=count[i]+count[j];
            }
        }

        cout << "end inner coumputing " << endl;
        m5_work_end(100,101);

        return 0;
    }
};



int main(){

    cout << "enter test1" << endl;
    test mytest;
    for (int i=0;i<10;i++){
        mytest.test1();
    }
    cout << "exit test1" << endl;

    cout << "begin outer coumputing " << endl;
    int count[1000]={0};
    for (size_t i = 0; i < 10; i++)
    {
        count[i]=(i+100)*i;
        for(int j= i;j<1000;j++){
            count[j]=count[i]+count[j];
        }
    }
    cout << "end outer coumputing " << endl;

    return 0;

}


