// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

int digits_only(const char *s);

int main(int argc, string argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: ./resize n infile outfile, argc error\n");

        return 1;
    }

    char *s = argv[1];
    int isdigit = digits_only(s);
    if (isdigit == 1)
    {
        printf("Usage: ./resize n infile outfile, number error\n");
        printf("isdigit: %d \n", isdigit);
        return 1;
    }

    // atoi converts the string argument str to an integer
    int resizenumber = atoi(s);
    if (resizenumber < 1 || resizenumber >= 100)
    {
        printf("Usage: ./resize n infile outfile, number error\n");
        return 1;
    }


    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);
    printf("bitmapfileheader : %lx \n", sizeof(BITMAPFILEHEADER));
    // sizeof(BITMAPFILEHEADER) = e (14bytes)

    //fread = read x bytes of information from the file pointed to by inptr and we store those x bytes somewhere where we have set aside x bytes worth of memory
    //so we declare like an array or something

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);
    printf("width : %x\nheight : %x\ntotal size of image in bytes, biSizeImage : %x\n", bi.biWidth, bi.biHeight, bi.biSizeImage);



    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    // Calculte new width, height, padding, biSizeImage, bfSize

    printf("first height %d\n", bi.biHeight);

    int oldPadding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    int oldBiWidth = bi.biWidth;

    bi.biWidth = bi.biWidth * resizenumber;

    int oldBiHeight = abs(bi.biHeight);
    printf("abs first height %d\n", oldBiHeight);
    int newHeight = bi.biHeight * resizenumber;
    printf("with the factor, abs(bi.biHeight)*resizenumber %d\n", newHeight);
    bi.biHeight = newHeight;

    int newPadding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    bi.biSizeImage = ((sizeof(RGBTRIPLE) * bi.biWidth) + newPadding) * abs(newHeight);

    bf.bfSize =  bi.biSizeImage + sizeof(BITMAPINFOHEADER) + sizeof(BITMAPFILEHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

    //printf("old padding : %x\nnew padding : %x\n", oldPadding, newPadding);

    // determine padding for scanlines
    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    // array of RGBTRIPLEs that can hold n pixels
    RGBTRIPLE outfilerow[bi.biWidth];

    // iterate over infile's scanlines
    for (int i = 0, biHeight = abs(oldBiHeight); i < biHeight; i++)
    {
        printf("new scanline %d\n", i);
        int q = 0;

        // iterate over pixels in scanline
        for (int j = 0; j < oldBiWidth; j++)
        {
            // temporary storage
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

            // write infile's pixels to array n times
            for (int k = 0; k < resizenumber; k++)
            {
                outfilerow[q] = triple;
                q++;
            }
        }

        for (int l = 0; l < resizenumber; l++)
        {
            printf("doing it as many times as the resizenumber %d\n", l);

            for (int m = 0; m < bi.biWidth; m++)
            {
                // write from array to outfile
                fwrite(&outfilerow[m], sizeof(RGBTRIPLE), 1, outptr);
                printf("writing 1 pix horizontally %d\n", m);
            }

            for (int p = 0; p < newPadding; p++)
            {
                // write new padding
                fputc(0x00, outptr);
                printf("adding padding %d\n", p);
            }

        }

        // skip over padding, if any
        fseek(inptr, oldPadding, SEEK_CUR);

    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}


int digits_only(const char *s)
{
    while (*s)
    {
    if (isdigit(*s++) == 0)
        return 1;
    }
    return 0;
}
