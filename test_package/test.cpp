#include <iostream>
#include "git2cpp/initializer.h"

using namespace std;

int main(int argc, char **argv){

    cout << "********* Testing libgit2cpp *********" << endl;

    try{
        git::Initializer initializer;
        cout << "ok" << endl;
    }
    catch(...){
        cout << "failed" << endl;
    }

    cout << "**************************************" << endl;

    return 0;
}
