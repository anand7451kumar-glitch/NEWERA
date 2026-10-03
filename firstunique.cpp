#include <iostream>
#include <unordered_map>
using namespace std;

char firstUnique(string s ) {
    unordered_map<char, int > frequency;

    for (char c: s )
        frequency[c]++;

    for (char c : s) {
        if (frequency[c] == 1)
        return c;

    }
    return '-';


}

int main() {
    string s = "leetcode";

    cout << firstUnique(s) << endl;
}