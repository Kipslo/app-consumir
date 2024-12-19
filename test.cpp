#include <iostream>

using namespace std;

int cont(int x = 3, int y = 2){
    return x + y;
}

int main(){
    cout << cont();
    return 0;
}