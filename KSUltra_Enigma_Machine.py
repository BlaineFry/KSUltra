# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 21:02:05 2020

@author: Blaine Fry

Kansas State University
English 210: Espionage Literature
Digital Humanities Project

Project: KSU Ultra
Digitally replicate an Enigma Machine
"""

import numpy as np # this will be invaluable for handling matrices
from numpy.linalg import multi_dot # this is how we perform the long matrix multiplication representing the Enigma circuit

alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M',
            'N','O','P','Q','R','S','T','U','V','W','X','Y','Z'] # A list containing uppercase letters of the alphabet

def vectorize(letter): # map the alphabet into a vector space. An individual letter will be a column vector.
    L = str(letter) # make sure that a string is being passed
    L_up = L.upper() # convert the letter into uppercase, so we don't have to worry about cases
    if L_up not in alphabet: # just return the character, if it's not a letter (i.e. it's punctuation)
        return L
    else: # if we have a letter, now we want to turn it into a column vector
        idx = alphabet.index(L_up) # the position of our [1] in the vector is the index of the letter in the alphabet
        vector = np.zeros([26,1]) # set up a 26 row column vector, all zeros
        vector[idx][0] = 1 # set the appropriate position in the column vector to one
        return vector # return our letter, now in vector form!
    
def alphabetize(vector): # a function that converts vectors back into letters
    v_list = vector.tolist() # convert the vector to a list so we can use the .index() method
    idx = v_list.index([1.0]) # find the position of our one in the list, which tells us which letter the vector represents
    return alphabet[idx] # return the letter of the alphabet we want
    
def rotate(rotor,N_times): # a function that shifts matrix columns N_times, representing the rotation of a rotor
    new = np.zeros(np.shape(rotor)) # first, we need a blank slate, a matrix that's all zeros
    for i in range(np.shape(rotor)[1]): # np.shape(rotor)[1] is the number of columns in the rotor matrix
        new.T[i] = rotor.T[i-np.shape(rotor)[1]+N_times%np.shape(rotor)[1]] # this line shifts the columns
    return new # return the matrix with shifted columns

def set_matrix(transformation_list): # This function will make it easy to create our transformation matrices
    M = np.zeros((26,26)) # make a matrix of the correct shape, all zeros
    for t in transformation_list: # run through each transformation and set the proper element to 1
        i = alphabet.index(t[1].upper()) # which row?
        j = alphabet.index(t[0].upper()) # which column?
        M[i][j] = 1
    return M

E1_R1 = set_matrix([['A','E'],
                    ['B','K'],
                    ['C','M'],
                    ['D','F'],
                    ['E','L'],
                    ['F','G'],
                    ['G','D'],
                    ['H','Q'],
                    ['I','V'],
                    ['J','Z'],
                    ['K','N'],
                    ['L','T'],
                    ['M','O'],
                    ['N','W'],
                    ['O','Y'],
                    ['P','H'],
                    ['Q','X'],
                    ['R','U'],
                    ['S','S'],
                    ['T','P'],
                    ['U','A'],
                    ['V','I'],
                    ['W','B'],
                    ['X','R'],
                    ['Y','C'],
                    ['Z','J']]) # Enigma 1 Rotor 1

E1_R2 = set_matrix([['A','A'],
                    ['B','J'],
                    ['C','D'],
                    ['D','K'],
                    ['E','S'],
                    ['F','I'],
                    ['G','r'],
                    ['H','U'],
                    ['I','X'],
                    ['J','B'],
                    ['K','L'],
                    ['L','H'],
                    ['M','W'],
                    ['N','T'],
                    ['O','M'],
                    ['P','C'],
                    ['Q','Q'],
                    ['R','G'],
                    ['S','Z'],
                    ['T','N'],
                    ['U','P'],
                    ['V','Y'],
                    ['W','F'],
                    ['X','V'],
                    ['Y','O'],
                    ['Z','E']]) # Enigma 1 Rotor 2

E1_R3 = set_matrix([['A','B'],
                    ['B','D'],
                    ['C','F'],
                    ['D','H'],
                    ['E','J'],
                    ['F','L'],
                    ['G','C'],
                    ['H','P'],
                    ['I','R'],
                    ['J','T'],
                    ['K','X'],
                    ['L','V'],
                    ['M','Z'],
                    ['N','N'],
                    ['O','Y'],
                    ['P','E'],
                    ['Q','I'],
                    ['R','W'],
                    ['S','G'],
                    ['T','A'],
                    ['U','K'],
                    ['V','M'],
                    ['W','U'],
                    ['X','S'],
                    ['Y','Q'],
                    ['Z','O']]) # Enigma 1 Rotor 3

Ref_A = set_matrix([['A','E'],
                    ['B','J'],
                    ['C','M'],
                    ['D','Z'],
                    ['E','A'],
                    ['F','L'],
                    ['G','Y'],
                    ['H','X'],
                    ['I','V'],
                    ['J','B'],
                    ['K','W'],
                    ['L','F'],
                    ['M','C'],
                    ['N','R'],
                    ['O','Q'],
                    ['P','U'],
                    ['Q','O'],
                    ['R','N'],
                    ['S','T'],
                    ['T','S'],
                    ['U','P'],
                    ['V','I'],
                    ['W','K'],
                    ['X','H'],
                    ['Y','G'],
                    ['Z','D']]) # Reflector A

Ref_B = set_matrix([['A','Y'],
                    ['B','R'],
                    ['C','U'],
                    ['D','H'],
                    ['E','Q'],
                    ['F','S'],
                    ['G','L'],
                    ['H','D'],
                    ['I','P'],
                    ['J','X'],
                    ['K','N'],
                    ['L','G'],
                    ['M','O'],
                    ['N','K'],
                    ['O','M'],
                    ['P','I'],
                    ['Q','E'],
                    ['R','B'],
                    ['S','F'],
                    ['T','Z'],
                    ['U','C'],
                    ['V','W'],
                    ['W','V'],
                    ['X','J'],
                    ['Y','A'],
                    ['Z','T']]) # Reflector B

Ref_C = set_matrix([['A','F'],
                    ['B','V'],
                    ['C','P'],
                    ['D','J'],
                    ['E','I'],
                    ['F','A'],
                    ['G','O'],
                    ['H','Y'],
                    ['I','E'],
                    ['J','D'],
                    ['K','R'],
                    ['L','Z'],
                    ['M','X'],
                    ['N','W'],
                    ['O','G'],
                    ['P','C'],
                    ['Q','T'],
                    ['R','K'],
                    ['S','U'],
                    ['T','Q'],
                    ['U','S'],
                    ['V','B'],
                    ['W','N'],
                    ['X','M'],
                    ['Y','H'],
                    ['Z','L']]) # Reflector C

def set_plugboard(pairs): # This is similar to set_matrix(), but made more user friendly for generating the plugboard transformation
    P_matrix = np.identity(26) # create an identity matrix of the proper shape. We use an identity matrix, so unless otherwise stated, a letter is unchanged
    for p in pairs: # run through the input pairs
        i = alphabet.index(p[0].upper()) # which row/column
        j = alphabet.index(p[1].upper()) # which column/row
        P_matrix[i][i] = 0 # clear the diagonal
        P_matrix[j][j] = 0 # clear the diagonal
        P_matrix[i][j] = 1 # set the first element
        P_matrix[j][i] = 1 # set the second element
    return P_matrix

def enigma(message,
           which_refl=Ref_A, which_RI=E1_R1, which_RII=E1_R2, which_RIII=E1_R3,
           RI_pos=1, RII_pos=1, RIII_pos=1,
           plugboard_pairs=[['B','F'],['A','C']]):
    # set up some basic tools
    encoded_letters = [] # make an empty list to store the encoded letters as the message is gone through letter by letter
    counter = 0
    # initialize rotors
    Ref = which_refl  
    RI = rotate(which_RI,RI_pos-1)
    RII = rotate(which_RII,RII_pos-1)
    RIII = rotate(which_RIII,RIII_pos-1)  
    # set up the plugboard
    P = set_plugboard(plugboard_pairs) # generate the plugboard matrix, using set_plugboard() and the user inputs
    # run through the message and encode/decode it
    for m in message: # run through the input string one character at a time
        v = vectorize(m) # turn the character into a vector in our alphabet vector space
        if isinstance(v,np.ndarray): # check that vectorize() returned a vector (np.ndarray), meaning the character is a letter
            # rotate rotors
            counter += 1
            RI = rotate(RI,int((counter+550)/676%26)) # the formula is empirical... the left rotor rotates when RII advances from E to F (only strictly true for Enigma 1 Rotor III)
            RII = rotate(RII,int((counter+4)/26%26)) # the formula is empirical... the middle rotor rotates when RIII advances from V to W (only strictly true for Enigma 1 Rotor III)
            RIII = rotate(RIII,counter) # the rightmost rotor rotates with every key press
            # send the signal through the rotor assembly
            r = multi_dot([P.T,RIII.T,RII.T,RI.T,Ref,RI,RII,RIII,P,v]) # the resultant vector, after running through the rotor assembly
            a = alphabetize(r) # convert our coded vector into a letter
            encoded_letters.append(a) # store the letter in our list
        else: # if the character isn't a letter, i.e. a space or punctuation, send it straight through
            encoded_letters.append(m)
    encoded_message = ''.join(encoded_letters) # join the encoded letters to create a readable(?) message
    return encoded_message

test1 = """
Some say the world will end in fire,
Some say in ice.
From what I've tasted of desire
I hold with those who favor fire.
But if it had to perish twice,
I think I know enough of hate
To say that for destruction ice
Is also great
And would suffice.
""" # Fire and Ice, by Robert Frost

test2 = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'



