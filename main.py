# import enchant
import string
from formatting import command_line_colors

WORD_LENGTH = 5
FIVE_WORD_DICT = "five_letter_words.txt"


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


def modify_alphabet(alphabet: list[str], must_have: dict[str, list[bool, list[bool]]], word: str, score: str) -> tuple[list[str], dict[str, int]]:
    for i in range(WORD_LENGTH):
        letter = word[i]
        if score[i] == "g": # green
            alphabet[i] = word[i]

        elif score[i] == "y": # yellow
            alphabet[i] = alphabet[i].replace(letter, "", 1)
            if not must_have[letter][0]:
                must_have[letter][0] = True
            must_have[letter][1][i] = False

        else: # black
            for j in range(WORD_LENGTH):
                alphabet[j] = alphabet[j].replace(letter, "", 1)
    print(must_have)
    return alphabet, must_have


def update_possible_words(possible_words: set[str], alphabet: list[str], must_have):
    print(alphabet)
    new_possible_words = set()
    for word in possible_words:
        valid = True
        for i in range(WORD_LENGTH):
            letter = word[i]
            if letter not in alphabet[i]:
                valid = False
                break
        for letter in string.ascii_lowercase:
            if must_have[letter][0]:
                has_letter = False
                for i in range(WORD_LENGTH):
                    if must_have[letter][1][i] and word[i] == letter:
                        has_letter = True
                        break
            if not has_letter:
                valid = False
                break
        if valid:
            new_possible_words.add(word)
    return new_possible_words


def format_guess(word: str, score: str):
    output = ""
    for i in range(WORD_LENGTH):
        if score[i] == "g":
            output += command_line_colors.text.green + word[i]
        elif score[i] == "y":
            output += command_line_colors.text.yellow + word[i]
        else:
            output += command_line_colors.text.black + word[i]
    output += command_line_colors.reset
    return output


def print_round(guesses, possible_words: set[str], won: bool):
    num_dashes = 20
    words_per_line = 15
    print("\n"*5)
    print("-"*num_dashes + "\n" + "Guesses" + "\n" + "-"*num_dashes)
    for i in range(WORD_LENGTH):
        print(f"{i+1} ||  {guesses[i]}")
    print("\n")
    if won:
        print("Congrats!")
    else:
        print("-"*num_dashes + "\n" + "Possible Words" + "\n" + "-"*num_dashes)
        possible_words_list = list(sorted(possible_words))
        for i in range(0, len(possible_words), words_per_line):
            print(*possible_words_list[i:i+words_per_line], sep=", ")
        print("\n")


def main():
    alphabet = [string.ascii_lowercase for _ in range(WORD_LENGTH)]
    must_have = {letter: [False, [True for _ in range(WORD_LENGTH)]] for letter in string.ascii_lowercase}
    guesses = ["" for _ in range(WORD_LENGTH)]

    # get all possible 5-letter words
    possible_words = set()
    with open(FIVE_WORD_DICT, "r") as f:
        all_words = f.read().split()
        for w in all_words:
            possible_words.add(w)

    num_guesses = 0
    won = False
    while (num_guesses < 6):
        word, score = get_guess()
        alphabet, must_have = modify_alphabet(alphabet, must_have, word, score)
        possible_words = update_possible_words(possible_words, alphabet, must_have)
        guesses[num_guesses] = format_guess(word,score)
        if score == "ggggg":
            won = True
        print_round(guesses, possible_words, won)
        num_guesses += 1
        if won:
            break

if __name__=="__main__":
    main()