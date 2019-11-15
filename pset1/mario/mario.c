#include <cs50.h>
#include <stdio.h>

int get_positive_int(string prompt);

int main(void)
{
    int h = get_positive_int("Height: ");
    printf("Height : %i \n", h);
    
    int max = 1;

        for (int i = 0; i < h; i++)
        {
            int dots = (h-i);
            for (int k = 1; k < dots; k++)
            {
                    printf(" ");
            }
            
            for (int j = 1; j<= max; j++)
            {
                  printf("#");
            }
          max++;
            
          printf("\n");
        }
}

// Prompt user for a height between 1 and 9
int get_positive_int(string prompt)
{
    int height;
    do{
        height = get_int("%s", prompt);
    }
    while (height < 1 || height > 8);
   // printf("Height value is %d\n", height);
    
    return height;
}

