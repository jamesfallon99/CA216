#I have stated in the comments which lines/functions were from other people's work
#Code written by James Fallon

#This program creates inputfilename-key.txt and inputfilename-decrypted.txt
#Make sure dictionary.txt is in the same directory as this program in order for it to run(provided in the same gitlab repo as this file)
#Cipher text file is passed through as a command line argument
#This should work for substitution cipher text files and caesar cipher text files. I wrote it intending it to be tested with a substitution cipher text file

#With some text files, an error can occur as follows:
#UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 7743: character maps to <undefined>
#UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 429: character maps to <undefined>
#With os-sub-cipher.txt and os-caesar-cipher.txt (from loop) these errors occur and will run when the characters at position 7743 and 429 are removed(I think it's the quotes (" ") that it doesn't like)
#These files have been refined and placed in the test code section of the gitlab repo.

import sys, re, time, queue
from threading import Thread

patterns = {} #Dictionary that will map every word to their number pattern.

def main():
    start_time = time.time()
    make_dictionary = Thread(target=make_dictionary_number_patterns) #A thread on the make_dictionary_number_patterns function.
    make_dictionary.start()# Start the thread.
    make_dictionary.join() # As I don’t know what text-files will be used to grade this project I will leave .join() in my code but I am aware that this isn’t as efficient (in some cases) as not using it. It will allow all text files regardless of length to run

    with open(sys.argv[1], 'r') as f: # Take in the cipher text file using a command line argument
        cipher_text = f.read() #Read this file.
    print("Decrypting")

    q = queue.Queue() # A queue used to store the result of the thread it's working on so as to use that result in other functions. 
    map_letters = Thread(target=get_final_mapping, args=(cipher_text, q)) # Use a thread to get the dictionary that maps the encrypted letters to english letters
    map_letters.start() # Start the thread
    map_letters.join()
    map_of_letters = q.get() #The result of the thread is stored in this variable

    key = creating_key(map_of_letters) # Get the key(in string form)

    list_of_decrypted_key = creating_list_key(key, map_of_letters) # Get a list of the key and the value it relates to

    key_file = sys.argv[1][:-4] + "-key" + sys.argv[1][-4:]
    with open(key_file, 'w') as f:
        for entry in list_of_decrypted_key:
            f.write(entry + "\n") # Write the decrypted message to a file
    print("Decrypted key written to {}".format(key_file)) # Tell the user where the decrypted message is

    decrypted_text = decrypting_cipher_text(cipher_text, key, map_of_letters)

    decrypted_text_file = sys.argv[1][:-4] + "-decrypted" + sys.argv[1][-4:]
    with open(decrypted_text_file, 'w') as f:
        for word in decrypted_text:
            f.write("".join(word)) # Write the decrypted message to a file
    print("Decrypted text written to {}".format(decrypted_text_file))

    end_time = time.time()
    print("{:.4f} seconds".format(end_time - start_time))

def make_dictionary_number_patterns():#We want to find the number pattern for every word in the 'dictionary.txt' file. E.g. dog = 012, doggy = 01223, copper = 012234
    file = open('dictionary.txt') # This text file needs to be in the same directory as this program in order for this program to run.
    file = file.read()
    list_of_words = file.split("\n") # Split words up into a list of strings
    for i in range(len(list_of_words)):
        number_pattern = make_number_pattern_from_word(list_of_words[i]) # Pass the word through the function in order to get its pattern.
        if number_pattern not in patterns: #If the number pattern isn't in the dictioanry:
            patterns[number_pattern] = [list_of_words[i]] #Map the pattern to the word and put this word into a list(so other words with the same pattern can then be appended to this list).
        else:
            patterns[number_pattern].append(list_of_words[i]) # If the number pattern is already in the dictionary, then append the word so it's not duplicating the pattern

 
def make_number_pattern_from_word(word): #Want to find the number pattern for every word
    number_pattern_of_word = "" # A string that will store the number pattern.
    num = 0 #This is the number that will be used when a new letter is found. It will increment after a new letter is found.
    mapping_of_letters_to_nums = {} #Dictionary which will map a letter to a number.
    word = word.upper() # As this function will be used on lower case letters later in the program, have every word in upper case will make it simpler
    for letter in word: #For each letter in the word,
        if letter not in mapping_of_letters_to_nums: #If not in mapping:
            mapping_of_letters_to_nums[letter] = str(num) # Then map that letter to a number.
            num = num + 1 #Increment the number so when a new letter is found, it won't re-use the same number.
        number_pattern_of_word += mapping_of_letters_to_nums[letter] #add the string of numbers associated with a word to the string called "number_pattern_of_word"
    return number_pattern_of_word

def map_potential_letters(map_letters, encrypted_word, english_word):
    # Map_letters is a dictionary mapping
    i = 0 # This will hold the position of each individual letter of the english and encrypted word.
    while i < len(encrypted_word):
        if english_word[i] not in map_letters[encrypted_word[i]]: # If the english letter is not already mapped to the encrypted letter
            map_letters[encrypted_word[i]].append(english_word[i]) # Then append it to the possible letters the encrypted letter might map to
        i += 1 # Increment i to go onto the next letter
    return map_letters # return this dictionary

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def empty_dictionary(): # Returns an empty dictionary mapping. The idea of having a function that does this came from inventwithpython.com. I decided to write my own version because it made sense to have a function that returns a dictionary as I realised I was defining a lot of them.

    empty_dictionary = {} # Create the dictionary
    for letter in letters: # For every letter in the alphabet
       empty_dictionary[letter] = [] # Let the alphabet letter equal an empty list
    return empty_dictionary

def get_common_letters_between_two_maps(dictionary1, dictionary2): # This function was taken from inventwithpython.com as I struggled to narrow down the letters myself. I modified the code to suit my understanding.
    #create a blank map, and then add only the potential decryption letters if they exist in both maps.
    common_letters = empty_dictionary() # Create an empty dictionary to map all the common letters
    for i in range(len(letters)): # For each letter in the string of alphabet letters at the top of the program
        if dictionary1[letters[i]] == []:
            common_letters[letters[i]] = dictionary2[letters[i]] # If an empty list occurs, just assign the letters of the other map to it.
        elif dictionary2[letters[i]] == []:
            common_letters[letters[i]] = dictionary1[letters[i]]
        else:
            for potential_letter in dictionary1[letters[i]]: #For the potential letter in the list of potential letters
                if potential_letter in dictionary2[letters[i]]: #If this letter is in dictionary2's potential letters
                    common_letters[letters[i]].append(potential_letter) # append this to the new dictionary
    return common_letters # Return this new dictionary

def find_encrypted_letters_that_map_to_only_one_letter(map_letters): # This function was taken from inventwithpython.com
    loop = True
    while loop:
        loop = False
        solved_letters = []
        for encrypted_letter in letters: #For every letter in the alphabet letters
            if len(map_letters[encrypted_letter]) == 1: # If the length of the list of potential letters is 1
                solved_letters.append(map_letters[encrypted_letter][0]) # Append this letter to the list of solved letters as there is nothing else it could map to
        for encrypted_letter in letters: # Create another loop to remove that letter from other encrypted letter's lists
            for letter in solved_letters: # Loop through the solved letters
                if len(map_letters[encrypted_letter]) > 1 and letter in map_letters[encrypted_letter]: # If the list is greater than 1 and it has one of the solved letters in it
                    map_letters[encrypted_letter].remove(letter) #remove this letter
                    if len(map_letters[encrypted_letter]) == 1: #If this then makes another list reduce to one letter
                        loop = True # loop again in order to catch this letter and put it in the solved letters list
    return map_letters

all_non_letters = re.compile('[^A-Z\s]') # Regular expression which matches all non letters and whitespace characters. This regular expression was found on stackoverflow.com
def get_final_mapping(cipher_text, q): # I got help with this function from inventwithpython.com
    #Mapping encrypted word to all possible english words based on number pattern.
    #Map each letter of each encrypted word to each letter of english word.
    #Cross examine these maps to get common letters
    #Reduce down to single letters
    
    encrypted_words_list = all_non_letters.sub("", cipher_text.upper()).split() # substitute any occurences of non letters or space with an empty string, uppercase this and put into a list.
    map_of_common_letters = empty_dictionary()
    for encrypted_word in encrypted_words_list:
        _map = empty_dictionary() # Create new dictionary
        number_pattern_of_encrypted_word = make_number_pattern_from_word(encrypted_word) # Get number pattern of the encrypted word
        if number_pattern_of_encrypted_word not in patterns:
            continue # If that pattern isn't in the dictionary of patterns, then continue so program doesn't stop
        for english_word in patterns[number_pattern_of_encrypted_word]: # For every english word in the list of words in the dictionary that has the same number pattern as the encrypted word mapped to it
            _map = map_potential_letters(_map, encrypted_word, english_word) # The dictionary will map encrypted letters of the encrypted word to potential english letters of the english word.
        map_of_common_letters = get_common_letters_between_two_maps(map_of_common_letters, _map) # Find the letters that are common between both dictionaries
    q.put(find_encrypted_letters_that_map_to_only_one_letter(map_of_common_letters)) # Narrow down the solved letters and store this mapping in the queue.

def creating_key(map_letters):
    #Create the key that will be used to decrypt the encrypted text
    key = ["-"] * len(letters) # The key will be a list of 26 letters, use a list to be able to overwrite at a specific index. This line of code was inspired from inventwithpython.com, the rest of the function was designed by me.
    for encrypted_letter in letters:
        if len(map_letters[encrypted_letter]) == 1: # If the list of potential letters an encrypted letter could map to is 1
            letter = map_letters[encrypted_letter][0] # Get this letter which is at position 0 and store it in variable "letter"
            for i in range(len(letters)): # Go through the english alphabet letters
                if letters[i] == letter: # If the letter at position i is equal to the letter stored in variable letter
                    j = i # Let j take this index value 
                else:
                    continue # Otherwise continue through the loop
            key[j] = encrypted_letter # Replaces the "-" value with the encrypted letter at the correct index
        else:
            continue

    key = "".join(key) # Join the key in a string
    return key


def creating_list_key(key, map_letters): # This creates a list mapping the english alphabet letters to an encrypted letter. This will be the function used in main to write out this key to a file.
    list_key = [] # A list which will be used to store the key
    key = creating_key(map_letters) # Get the key from the previous function
    for i in range(len(letters)): # Go through the english alphabet letters
        list_key.append(letters[i] + " = " + key[i]) # appending the mapping of the english letter to the key letter
    return list_key

def decrypting_cipher_text(cipher_text, key, map_letters):
    key = creating_key(map_letters) # Get the key from the previous function
    mapping_key = {} # Dictionary used to store the key and values
    i = 0
    j = 0
    while i < len(key):
        while j < len(letters):
            mapping_key[key[i]] = letters[j] # Map the key letter to the english letter
            j += 1
            i += 1
    decrypt = [] # A list to store the decrypted text
    for char in cipher_text: # For each character in the cipher text
        if char.islower(): # If the character is lower case
            tmp = char.upper() # Create a temporary variable which changes it to upper case and stores it
            if tmp in mapping_key: # If it's in the dictionary
                lower_tmp = mapping_key[tmp] # Let that value be stored in a variable called lower_tmp(it hasn't been converted to lowercase yet)
                decrypt.append(lower_tmp.lower()) # Append the lower case letter to the list by converting it to lower case
            else: 
                decrypt.append("-") # append a hyphen
        elif char not in mapping_key: # If the character isn't in the dictionary e.g. commas, full stops etc
            decrypt.append(char) # Append that character to the list
        else:
            decrypt.append(mapping_key[char]) # Otherwise append the letter to the list
    return decrypt

if __name__ == '__main__':
    main()