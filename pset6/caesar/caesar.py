from cs50 import get_string
import sys

def main():

    if len(sys.argv) != 2 :
        print("Usage: ./caesar key")
        sys.exit([1])

    key = int(sys.argv[1])
    plain = get_string('plaintext : ')

    print("ciphertext: ", end="")

    for c in plain :
        if c.isalpha() == True :

            result = ord(c) + key

            # lower cases
            if c.islower() == True :

                # if we reach z we have to start back at a
                if result > 122 :
                    keyalphabet = (ord(c)-97 + key) % 26
                    result = 97 + (keyalphabet)

                print(chr(result), end="")

            # upper cases
            else :

                if result > 90 :
                    keyalphabet = (ord(c)-65 + key) % 26
                    print('keyalphabet : ', keyalphabet)
                    result = 65 + (keyalphabet)

                print(chr(result), end="")

        else :
            print(c, end="")
    print()



if __name__ == "__main__":
    main()

