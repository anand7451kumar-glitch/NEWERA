#include <iostream>
using namespace std;

int main() {
    int n;
    cout << "Enter a number: ";
    cin >> n;

    bool prime = true;

    if (n <= 1) {
        prime = false;
    } else {
        for (int i = 2; i * i <= n; i++) {
            if (n % i == 0) {
                prime = false;
                break;
            }
        }
    }

    if (prime)
        cout << n << " is a prime number" << endl;
    else
        cout << n << " is not a prime number" << endl;

    return 0;
}
