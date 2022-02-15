# import enchant
import string

class command_line_colors:
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    class text:
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
    class bg:
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        lightgrey='\033[47m'

WORD_LENGTH = 5

def old():
    # d = enchant.Dict("en_US")

    possible_words = []

    available_letters = "qyuiodfklzxcvbn"

    letter_1 = available_letters
    letter_2 = "o"
    letter_3 = "u"
    letter_4 = "l"
    letter_5 = available_letters

    for c1 in letter_1:
        for c2 in letter_2:
            for c3 in letter_3:
                for c4 in letter_4:
                    for c5 in letter_5:
                        word = c1 + c2 + c3 + c4 + c5
                        print(word)
                        if d.check(word):
                            possible_words.append(word)

    print(possible_words)

def get_guess():

    # word
    valid_input = False
    word = ""
    while not valid_input:
        # gets word from stdin and converts it to lowercase
        print()
        word = input("Enter guess: ").lower()

        # checks the length of the word
        if len(word) != WORD_LENGTH:
            print("Oops! This word is not 5 letters long -- please try again!")
            continue

        # checks that every letter is in the alphabet
        i = 0
        for c in word:
            if c not in string.ascii_lowercase:
                print(f"Oops! A character entered ({c}) is not in the alphabet -- please try again!")
                break
            i += 1
            if i == WORD_LENGTH:
                valid_input = True
    
    valid_input = False

    # score
    valid_input = False
    score = ""
    while not valid_input:
        # gets score from stdin and converts it to lowercase
        print()
        score = input("Enter score: ").lower()

        # checks the length of the score
        if len(score) != WORD_LENGTH:
            print("Oops! This score is not 5 letters long -- please try again!")
            continue

        # checks that every letter is in the alphabet
        i = 0
        for c in score:
            if c not in "byg":
                print(f"Oops! A character entered ({c}) is not g, y, or b -- please try again!")
                break
            i += 1
            if i == WORD_LENGTH:
                valid_input = True
    
    return word, score


def modify_alphabet(alphabet, word, score):
    for i in range(WORD_LENGTH):
        match word[i]:
            case "g": alphabet[i] = word[i]

def main():
    num_guesses = 0
    alphabet = [string.ascii_lowercase for _ in range(WORD_LENGTH)]

    while (num_guesses < 6):
        word, score = get_guess()
        print(word)
        num_guesses += 1

if __name__=="__main__":
    main()