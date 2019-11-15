#include <stdio.h>
#include <stdlib.h>

#define BLOCK 512

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover image\n");
        return 1;
    }

    // open file
    FILE* file = fopen(argv[1], "r");

    if (file == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 2;
    }

    // file pointer we will be writing into
    FILE* resultfile;

    // define array that will contain 512 bytes
    unsigned char buffer[BLOCK];

    // initiate counter for the different images
    int counter = 0;

    // char array to store the new string containing the name of the file
    char name[8];

    // while blocks are equal to 512 bytes, we haven't reached the EOF
    while(fread(buffer, sizeof(buffer), 1, file) == 1)
    {
        // checking if the 4 first bytes of the block are a header
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
            {
                // checks if we already found a header, in which case we need to close the previous file
                if (counter > 0)
                {
                    // close the file that is open
                    fclose(resultfile);

                    // creating a filename - the %03i means 'print at least X' digits
                    sprintf(name, "%03d.jpg", counter);

                    // increment counter
                    counter++;

                    // open new file
                    resultfile = fopen(name, "w");

                    // write to outfile
                    fwrite(buffer, sizeof(buffer), 1, resultfile);
                }
                // if this is the first header, no need to close anything before creating the file
                if (counter == 0)
                {
                    // creating a filename - the %03i means 'print at least X' digits
                    sprintf(name, "%03d.jpg", counter);

                    // increment counter
                    counter++;

                    // open new file
                    resultfile = fopen(name, "w");

                    // write to outfile
                    fwrite(buffer, sizeof(buffer), 1, resultfile);
                }
                //printf("new header found! début header : %x %x %x %x \n",buffer[0], buffer[1], buffer[2], buffer[3]);
            }
        // copies the remaining bytes to the file that is already open
        else if (counter > 0)
        {
            fwrite(buffer, sizeof(buffer), 1, resultfile);
        }
    }
    fclose(resultfile);
    fclose(file);
}
