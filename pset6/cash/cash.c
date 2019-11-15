#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    // Prompt user for change owed
    float f;
    do{
        f = get_float("Change : ");
    }
    while (f <= 0.00);

    // Convert this input from float to int
    int cents = round(f*100);

    // Coins possible
    int quarter = round(0.25*100);
    int dime = round(0.10*100);
    int nickel = round(0.05*100);
    int penny = round(0.01*100);

     // Initialize count of coins
     int count = 0;

    // Check if coins are less or equal to cents
    while(quarter <= cents){
        count = count + 1;
        cents = cents - quarter;
    }
    while(dime <= cents){
        count = count + 1;
        cents = cents - dime;
    }
    while(nickel <= cents){
        count = count + 1;
        cents = cents - nickel;
    }
    while(penny <= cents){
        count = count + 1;
        cents = cents - penny;
    }

    // The minimum number of coins with with that change can be made
    printf("%i \n", count);
}
