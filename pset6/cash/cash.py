from cs50 import get_float

def main():
    change = get_positive_float("Change : ")

    print('input change : ', change)
# Convert this input from float to int
    cents = round(change*100)
    print('input round : ', cents)

# Coins possible
    quarter = round(0.25*100)
    dime = round(0.10*100)
    nickel = round(0.05*100)
    penny = round(0.01*100)

# Count of coins
    count = 0

    while quarter <= cents :
        count = count + 1
        cents = cents - quarter

    while dime <= cents :
        count = count + 1
        cents = cents - dime

    while nickel <= cents :
        count = count + 1
        cents = cents - nickel

    while penny <= cents :
        count = count + 1
        cents = cents - penny

    print(count, end="\n")

def get_positive_float(prompt):
    """Prompt user for positive float"""
    while True:
        n = get_float(prompt)
        if n > 0 :
            break
    return n

if __name__ == "__main__":
    main()
