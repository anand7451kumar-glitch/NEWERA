#include <stdio.h>
#include <stdbool.h>

void draw(int n);

int main (void)
{
    int height = get_int("Height: ");
    draw(height);


}

void draw(int n)
{
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            printf(" ");
        }
        for (int k = 0; k < i + 2; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}