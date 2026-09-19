#include <stdio.h>
#include <cs50.h>

int main (void)
{
    string strings[] = {"Hello", "World", "CS50", "is", "awesome!"};

    string s = get_string("string: ");
    for (int i = 0; i<6; i++)
    {
        if (strings[i] == s)
        {
            printf("Found!\n");
            return 0;
            

        }
    }
}
