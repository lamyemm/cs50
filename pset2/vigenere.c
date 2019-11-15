#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int shift(char c);

int alpha_only(const char *s);


int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }
    
    char *s = argv[1];
    int isalpha = alpha_only(s);
    if(isalpha == 1)
     {
        printf("Usage: ./vigenere keyword\n");
        return 1;
     }

    string plain = get_string("plaintext: ");
    printf("ciphertext: ");

    int length = strlen(argv[1]);
       
    // counter for iterating over they plaintext
    int j = 0;
    for (int i = 0; i < strlen(plain); i++)
    {           
        int key = argv[1][j];
            
        j = j + 1; 
            
        if (j == length){
        j = 0;
    }
            
    int value = 0;
    if (key >=  97 && key<= 122)
    {
        value = key-97;
    }
    else
    {
        value = key-65;
    }
        
    int result =  (int) plain[i] + value;
      
    if ((int)(plain[i]) >=  97 && (int)(plain[i])<= 122)
    {
        if(result > 122){
            int left = result - 122;
            result = 97 + (left-1);
        }
        printf("%c", result);
    }
    else if ((int)(plain[i]) >= 65 && (int)(plain[i])<= 90)
    {
        if(result > 90){
            int left = result - 90;
            result = 65 + (left-1);
        }
        printf("%c", result);
    }

    else {
        printf("%c", plain[i]);
    }

    }
    printf("\n");
    
    return 0;
}


int alpha_only(const char *s)
{
    while (*s) {
        if (isalpha(*s++) == 0) return 1;
    }

    return 0;
}

// Function that gives a number from 0 to 25 to the alphabet
int shift(char c)
{
    // transforms first letter of the keyword into an integer
    int key = c;
    int value = 0;
    if (key >=  97 && key <= 122)
        {
            value = key - 97;
        } else {
             value = key - 65;
        }
    
        return value;
}

