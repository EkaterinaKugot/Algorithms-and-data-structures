#include <iostream>
#include <map>
#include <cmath>
#include <chrono>
using namespace std;

int main(void){
    std::map<int, int> counter;
    int n;
    for (int i = 0; i < 8; i++){
        counter.clear();
        n = ceil(pow(10, i));
        auto t1 = chrono::high_resolution_clock::now();
        for (int j = 1; j <= n; j++) {
            counter[j] = j;
        }
        auto t2 = chrono::high_resolution_clock::now();
        chrono::duration<double, std::milli> elapsed = (t2 - t1) * pow(10, 3);
        cout << n << " " << sizeof(int) * counter.size() * 2 << " " << elapsed.count()<< " ";
    }
    return 0;
}