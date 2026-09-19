#include <cs50.h>
#include <stdio.h>

int maun(void)
{
    int numbers[]= {20, 30, 40, 50, 60};

    int n = get_int("Number: ");
    for (int i = 0; i < 5; i++)
    {
        if (numbers[i] == n)
        {
            printf("Found\n");
            
        }
        else
        {
            printf("Not Found\n");
            return 0;
        }
    }
    printf("Not Found\n");
    return 1;


}