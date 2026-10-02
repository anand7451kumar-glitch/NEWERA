#include <iostream>
#include <fstream>
#include <string>
using namespace std;

class PasswordManager {
private:
    string filename = "passwords.txt";

public:
    void
     addPassword() {
        string website, username, password;

        cout << "Website: ";
        cin >> website;

        cout << "Username: ";
        cin >> username;

        cout << "Password: ";
        cin >> password;

        ofstream field(filename, ios::app);
        file << website << " " << username << " " << password << "\n";

        cout << "Saved!\n";
    }

    void showPasswords() {
        ifstream file(filename);

        string website, username, password;   
        
        while (file >> website >> username >> password) {
            cout << "\nWebsite: " << website;
            cout << ""
        }



}