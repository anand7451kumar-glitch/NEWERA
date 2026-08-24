#include <iostream>
using namespace std;

int main () {
    int n;
    cout << "enter a number: ";
    cin >>n;

    int original = n;
    int reversed =0;

    while (n != 0) {
        int digit = n % 10;
        reversed = reversed * 10 + digit;
        n /= 10;
    }

    if (original == reversed)
        cout << "Palindrome number" << endl;
    else
        cout << "Not a palindrome number" << endl;
    return 0;
}
    
