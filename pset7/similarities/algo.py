from nltk.tokenize import sent_tokenize

def main():

    def convert_to_substring(x, n):

        string = x
        subslength = n

        i = 0
        j = subslength + i

        my_range = len(string) - subslength + 1

        list_of_sub = []
        for i in range(my_range) :
            substring = string[i:subslength+i]

            list_of_sub.append(substring)

        #print('liste of subs ', list_of_sub)
        return list_of_sub

    a = "Salutations"
    b = "Hionellooalu"
    n = 3

    first_sub = convert_to_substring(a, n)
    second_sub = convert_to_substring(b, n)

    print('first ', first_sub)
    print('second ', second_sub)

    my_final_sub = []

    for sub in first_sub :
        if sub in second_sub :
            my_final_sub.append(sub)

    # remove duplicates from the list
    my_final_sub = list(dict.fromkeys(my_final_sub))

    print("final substring list : ", my_final_sub)

    return my_final_sub

if __name__ == "__main__":
    main()
