import numpy as np


def encrypt(plaintext):

    # Ask for key to get k matrix
    k = createKey()

    # Ask for plaintext to get p matrix
    P = createMatrixFromStringToInt(plaintext)

    # Calculate C = P * K mod 26
    c = ""
    for i in range(2):
        # Dot product
        row_0 = P[0][i] * k[0][0] + P[1][i] * k[0][1]
        # Modulate and add 65 to get back to the A-Z range in ascii
        integer = int(row_0 % 26 + 65)
        # Change back to chr type and add to text
        c += chr(integer)
        # Repeat for the second column
        row_1 = P[0][i] * k[1][0] + P[1][i] * k[1][1]
        integer = int(row_1 % 26 + 65)
        c += chr(integer)
    return c

def decrypt(ciphertext):

    # Ask for key to get k matrix and check for multiplicative inverse if valid
    k = createKey()

    # call back multiplicative inverse that's already valid to calc k inverse
    determinant = k[0][0] * k[1][1] - k[0][1] * k[1][0]
    determinant = determinant % 26
    multiplicative_inverse = find_multiplicative_inverse(determinant)

    # make adj matrix
    adj = k
    # Swap
    adj[0][0], adj[1][1] = adj[1, 1], adj[0, 0]
    # multiply by -1
    adj[0][1] *= -1
    adj[1][0] *= -1
    print("adj=", adj)

    # calculate k inverse
    k_inverse = adj
    for row in range(2):
        for column in range(2):
            k_inverse[row][column] = multiplicative_inverse * adj[row][column]
            k_inverse[row][column] = k_inverse[row][column] % 26

    # Calculate P= k_inverse * c mod 26

    # Ask for ciphertext to get c matrix
    c = createMatrixFromStringToInt(ciphertext)
    p = ""
    for i in range(2):
        # Dot product
        column_0 = c[0][i] * k_inverse[0][0] + c[1][i] * k_inverse[0][1]
        # Modulate and add 65 to get back to the A-Z range in ascii
        integer = int(column_0 % 26 + 65)
        # Change back to chr type and add to text
        p += chr(integer)
        # Repeat for the second column
        column_1 = c[0][i] * k_inverse[1][0] + c[1][i] * k_inverse[1][1]
        integer = int(column_1 % 26 + 65)
        p += chr(integer)

    return p

def find_multiplicative_inverse(determinant):
    multiplicative_inverse = -1
    for i in range(26):
        inverse = determinant * i
        if inverse % 26 == 1:
            multiplicative_inverse = i
            break
    return multiplicative_inverse


def createKey():
    # creates k matrix and checks if key is valid

    determinant = 0
    matrix = None
    while True:
        try:
            print("Enter 4 integers to be used as a key matrix in a single line (rowwise separated by space): ")
            #get user input as integer and make it in a list
            entries = list(map(int, input().split()))
            #convert list into matrix
            matrix = np.array(entries).reshape(2, 2)

            #calc determinant
            determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
            determinant = determinant % 26

            #get multiplicative inverse of the determinant
            inverse_element = find_multiplicative_inverse(determinant)

            #if no multipicative inverse
            if inverse_element == -1:
                print("invalid key, determinant is not relatively prime to 26")
                continue
            else:
                print("inverse {}".format(inverse_element))
                break
        #if user enters a value that's not integer
        except ValueError:
            print("please enter integer value")
            continue
    return matrix

def createMatrixFromStringToInt(string):
    # Map string to a list of integers
    integers = [chr_to_int(c) for c in string]
    # initiate zeros matrix 2*2
    M = np.zeros((2,2), dtype=np.int32)
    iterator = 0
    #start populate the matrix from integers list
    for column in range(2):
        for row in range(2):
            M[row][column] = integers[iterator]
            iterator += 1
    return M

def chr_to_int(char):
    # Uppercase the char to get into range 65-90 in ascii table
    char = char.upper()
    # Cast chr to int and subtract 65 to get 0-25
    integer = ord(char) - 65
    return integer


if __name__ == "__main__":
    while True:
        try:
            user_input = int(input("Welcome to Hill Cipher algorithm!, please enter a number: 1-Encrypt 2-Decrypt "))

            if user_input == 1:
                while True:
                    try:
                        plaintext = str(input("Plaintext to be encrypted: (4 letters) "))
                        # check hill cipher 2*2
                        if (len(plaintext) != 4):
                            print("invalid input, please enter 4 letters!")
                            continue
                        #if user enters a value that's not string
                        elif plaintext.isdigit():
                            print("invalid input, please enter string input!")
                            continue
                        # breaks from loop if input true
                        else:
                            P = createMatrixFromStringToInt(plaintext)
                            print("p=\n", P)
                            break
                    #this condition actually never enters
                    #but has to be written
                    except ValueError:
                        print("please enter a valid input!")
                        continue
                ciphertext = encrypt(plaintext)
                print("C=",ciphertext)

                restart = input('\nWould you like to restart? Enter yes or no.\n')
                if restart.lower() != 'yes':
                    break
            elif user_input == 2:
                while True:
                    try:
                        ciphertext = str(input("Ciphertext to be decrypted: (4 letters)"))
                        # check hill cipher 2*2
                        if (len(ciphertext) != 4):
                            print("invalid input, please enter 4 letters!")
                            continue
                        #if user enters a value that's not string
                        elif ciphertext.isdigit():
                            print("invalid input, please enter string input!")
                            continue
                        # breaks from loop if input true
                        else:
                            c = createMatrixFromStringToInt(ciphertext)
                            print("c=\n", c)
                            break
                    #this condition actually never enters
                    #but has to be written
                    except ValueError:
                        print("please enter a valid input!")
                        continue
                plaintext = decrypt(ciphertext)
                print("P=",plaintext)

                restart = input('\nWould you like to restart? Enter yes or no.\n')
                if restart.lower() != 'yes':
                    break
            # outer loop condition if user enter any number other than (1 or 2)
            else:
                print("please enter number 1 or 2!")
                continue

        # outer loop condition if user didn't enter integer input (1 or 2)
        except ValueError:
            print("please enter an integer value")
            continue
