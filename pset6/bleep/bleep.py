from cs50 import get_string
from sys import argv
import sys


def main():

    if len(sys.argv) != 2 :
        print("Usage: python bleep.py file.txt")
        sys.exit([1])

    f = sys.argv[1]

    dictionary = set()

    file = open(f, "r")

    if file.mode == "r":
        contents = file.readlines()
        for word in contents:
            dictionary.add(word.rstrip())

    message = get_string('What message would you like to censor? ')

    my_list = message.split()

    for token in my_list :
        if token in dictionary :
            for c in token :
                print("*", end="")
            print(" ", end="")
        else :
            print(token, end=" ")

    print()

if __name__ == "__main__":
    main()
