from nltk.tokenize import sent_tokenize

def lines(a, b):
    """Return lines in both a and b"""

    string1 = a
    string2 = b

    new_string1 = string1.splitlines(0)
    new_string2 = string2.splitlines(0)

    my_list = []

    for line in new_string1 :
        if line in new_string2 :
            my_list.append(line)

    # remove duplicates from the list
    my_list = list(dict.fromkeys(my_list))

    return my_list


def sentences(a, b):
    """Return sentences in both a and b"""

    string1 = a
    string2 = b

    new_string1 = sent_tokenize(string1)
    new_string2 = sent_tokenize(string2)

    my_list = []

    for sentence in new_string1 :
        if sentence in new_string2 :
            my_list.append(sentence)

    # remove duplicates from the list
    my_list = list(dict.fromkeys(my_list))

    return my_list


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""


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

        return list_of_sub

    first_sub = convert_to_substring(a, n)
    second_sub = convert_to_substring(b, n)

    my_final_sub = []

    for sub in first_sub :
        if sub in second_sub :
            my_final_sub.append(sub)

    # remove duplicates from the list
    my_final_sub = list(dict.fromkeys(my_final_sub))

    return my_final_sub