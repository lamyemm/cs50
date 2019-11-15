# Abstraction and scope

from cs50 import get_int


def main():
    height = get_positive_int("Positive number between 1 and 8 : ")

    max = 1
# Print out that many bricks
    for i in range(height):
        dots = (height-i-1)
        for j in range(dots):
            print(" ", end="")

        for k in range(max):
            print("#", end="")
        print()
        max += 1

def get_positive_int(prompt):
    """Prompt user for positive integer"""
    while True:
        n = get_int(prompt)
        if n > 0 and n < 9 :
            break
    return n




if __name__ == "__main__":
    main()

