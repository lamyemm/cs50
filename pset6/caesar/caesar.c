// CLI argument that will be the key
// So check argv[1] to check if it's only digits - convert from string to an int
// Prompt plaintext
// Iterate over each charachter
// if(uppercase) then rotate preserving case then print out - if(lowercase) then rotate preserving case then print out
// else print as is
// Render ciphertext(printf)

#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

int digits_only(const char *s);

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    char *s = argv[1];
    int isdigit = digits_only(s);
    if(isdigit == 1){
        printf("Usage: ./caesar key\n");
        return 1;
    }
    // atoi converts the string argument str to an integer
    int key = atoi(s);
    printf("The chosen key is %i\n", key);

    string plain = get_string("plaintext: ");
    printf("ciphertext: ");

    for (int i = 0; i < strlen(plain); i++)
    {
       int result =  (int) plain[i] + key;

        // if these are lower cases
        if ((int)(plain[i]) >=  97 && (int)(plain[i])<= 122)
        {
             // if we reach Z and have to start back at A
            if(result > 122){
                int left = result - 122;
                result = 97 + (left-1);
            }
            printf("%c", result);
        }

        // if the letter is an upper case
        else if ((int)(plain[i]) >= 65 && (int)(plain[i])<= 90)
        {
                // if we reach Z and have to start back at A
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


int digits_only(const char *s)
{
    while (*s) {
        if (isdigit(*s++) == 0) return 1;
    }

    return 0;
}
