from cs50 import get_string
import sys

def main():

    if len(sys.argv) != 2 :
        print("Usage: ./caesar key")
        sys.exit([1])

    key = int(sys.argv[1])
    print(key)

    plain = get_string('plaintext : ')
    print('ciphertext : ', end="")

    for c in plain :
        if c.isalpha() == True :
           # print('ord(c) : ', ord(c), 'result : ', result)
            if c.isupper() == True :
                print('its upper lol')
                result = (ord(c) + key) % 26
                result = chr(result)
                print(result, end="")

            else :
                result = (ord(c) + key) % 26
                print(chr(result), end="")

    print()

    print('test chr', chr(0))
    print(chr(97))


if __name__ == "__main__":
    main()

