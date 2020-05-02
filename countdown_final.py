import random
from itertools import combinations
#letter distributions according to http://www.thecountdownpage.com/letters.htm
CONSONANTS = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']
VOWELS = ['A', 'E', 'I', 'O', 'U']

C_WEIGHTS = [2,3,6,2,3,2,1,1,5,4,8,4,1,9,9,9,1,1,1,1,1]
V_WEIGHTS = [15,21,13,13,5]

def dictionary_reader(filename: str) -> list:
    """
    Reads txt file and populates a list with words between 1 and 9 characters in length.
    """
    with open(filename) as f:
        words = [x.upper() for x in [y for y in f.read().splitlines()] if len(x) < 10 and len(x) > 1]
    #sort words by length
    words.sort(key=len, reverse=True)
    #generate list of words with letters sorted alphabetically
    sorted_words = ["".join(sorted(x)) for x in words]
    print("Dictionary successfully loaded from file.")
    return words, sorted_words

def select_characters() -> str:
    """
    Forms a string of 9 random letters, consisting of a specific number of consonents or vowels selected by the user.
    """
    rand_letters = "" #string for appending letters to
    print("Please choose your 9 letters. Enter a 'c' for a consonant or a 'v' for a vowel.")
    while len(rand_letters) < 9:
        #lowercase user input to simplify following if statements
        inp = input("Current letters: %s\nLetter %s: "%(rand_letters, len(rand_letters)+1)).lower()
        if inp == "v":
            rand_letters += random.choices(population=VOWELS, weights=V_WEIGHTS, k=1)[0] #append random vowel when input 'v'
        elif inp == "c":
            rand_letters += random.choices(population=CONSONANTS, weights=C_WEIGHTS, k=1)[0] #append random consonant when input 'c'
        else:
            #catch incorrect inputs
            print("Invalid input. Please try again.")
    return rand_letters

def word_lookup(letters: str, words: list, sorted_words: list) -> list:
    """
    Generates a list of words contained in words that can be formed using the letters from letters in any order.
    """
    #order letters alphabetically
    sorted_letters = "".join(sorted(letters))
    #list for appending all alphabetic letter combinations
    letter_combinations = []
    #generate all alphabetic combinations of letters from length 9 to 2
    for i in range(9,1,-1):
        for substring_letter_list in combinations(sorted_letters,i):
            letter_combinations.append("".join(substring_letter_list))
    #list for appending valid words, will be returned
    valid_words = []
    for i in range(0,len(words)-1):
        if sorted_words[i] in letter_combinations: #check if any letter combinations match with a sorted word from the dictionary
            valid_words.append(words[i]) #append the original, unsorted word to the valid word list
    return valid_words

def print_title():
    print("""---------------------------------------------------------------------------------
 _______  _______           _       _________ ______   _______           _       
(  ____ \\(  ___  )|\\     /|( (    /|\\__   __/(  __  \\ (  ___  )|\\     /|( (    /|
| (    \\/| (   ) || )   ( ||  \\  ( |   ) (   | (  \\  )| (   ) || )   ( ||  \\  ( |
| |      | |   | || |   | ||   \\ | |   | |   | |   ) || |   | || | _ | ||   \\ | |
| |      | |   | || |   | || (\\ \\) |   | |   | |   | || |   | || |( )| || (\\ \\) |
| |      | |   | || |   | || | \\   |   | |   | |   ) || |   | || || || || | \\   |
| (____/\\| (___) || (___) || )  \\  |   | |   | (__/  )| (___) || () () || )  \\  |
(_______/(_______)(_______)|/    )_)   )_(   (______/ (_______)(_______)|/    )_)

---------------------------------------------------------------------------------""")

def print_spacer():
    print("---------------------------------------------------------------------------------")

def game() -> int:
    """
    Runs the countdown game. Will keep going until the user decides they wish to exit.
    """
    print_title()
    ply_total_points = 0 #int for summing player points
    ply_total_rounds = 0 #int for tracking number of rounds the player has played
    #ask user for name of file they wish to read
    words, sorted_words = dictionary_reader(input("Name of dictionary file to use: "))
    inp = ""
    while inp != "q":
        print_spacer()
        ply_total_rounds += 1 #begin next round
        characters = select_characters() #get 9 characters
        valid_words = word_lookup(characters, words, sorted_words) #get list of valid words that can be made with 9 characters
        print_spacer()
        #ask player for their guess
        player_guess = input("Your 9 characters are: %s\nPlease enter the longest word you can make with these letters: "%(characters)).upper()
        print_spacer()
        if player_guess in valid_words:
            ply_total_points += len(player_guess)
            #player gets points equal to the length of their word providing it is correct
            print("Great! %s points awarded. You now have %s points in total."%(len(player_guess), ply_total_points))
        else:
            #0 points awarded for incorrect word
            print("Invalid word. 0 points awarded. You have %s points in total."%(ply_total_points))
        #calculate and print the best (longest) words for the given round
        longest_words = [x for x in valid_words if len(x) == len(valid_words[0])]
        print("The best word(s) for this round:\n" + "\n".join(longest_words))
        #ask user if they wish to continue
        print_spacer()
        inp = input("Type q to end game. Press enter to continue to round %s.\n"%(ply_total_rounds+1))
    #return final stats for printing at the end of the game
    return ply_total_points, ply_total_rounds

if __name__ == "__main__":
    final_points, round_number = game()
    print_title()
    print("Thank you for playing! You scored a total of %s point(s) in %s round(s)."%(final_points, round_number))
