import string
from formatting import command_line_formats

WORD_LENGTH = 5
NUM_ALLOWED_GUESSES = 6
FIVE_WORD_DICT = "five_letter_words.txt"


def get_guess() -> tuple[str, str]:
    """ gets and validates a user's guess word and its score from the command line

        Returns:
            guess: the most recent word guessed
            score: the score of guess, represented by the characters 'g' (green), 'y' (yellow), and 'b' (black)
    """
    # word
    valid_input = False
    guess = ""
    while not valid_input:
        # gets guess from stdin and converts it to lowercase
        guess = input("Enter guess: ").lower()

        # checks the length of the word
        if len(guess) != WORD_LENGTH:
            print(f"Oops! This word is not 5 letters long -- please try again!")
            continue

        # checks that every letter is in the alphabet
        i = 0
        for c in guess:
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

    return guess, score


def modify_alphabet(alphabet: list[str], must_have: dict[str, list[bool, list[bool]]], guess: str, score: str) -> tuple[list[str], dict[str, list[bool, list[bool]]]]:
    """ modifies the available alphabet for each position given new constraints

        Arguments:
            alphabet: a list of strings, with each string representing the available characters for a position in the word
            must_have: a dictionary with a key for each letter... TODO
            guess: the most recent word guessed
            score: the score of guess, represented by the characters 'g' (green), 'y' (yellow), and 'b' (black)

        Returns:
            alphabet: the updated input alphabet after eliminating characters
            must_have: TODO
    """
    for i in range(WORD_LENGTH):
        letter = guess[i]
        if score[i] == "g":  # green
            alphabet[i] = guess[i]

        elif score[i] == "y":  # yellow
            alphabet[i] = alphabet[i].replace(letter, "", 1)
            if not must_have[letter][0]:
                must_have[letter][0] = True
            must_have[letter][1][i] = False

        else:  # black
            for j in range(WORD_LENGTH):
                alphabet[j] = alphabet[j].replace(letter, "", 1)
    return alphabet, must_have


def update_possible_words(possible_words: set[str], alphabet: list[str], must_have: dict[str, list[bool, list[bool]]]) -> set[str]:
    """ updates the possible words by removing words that no longer fit the constraints

        Arguments:
            possible_words: a set of all possible words before the most recent guess
            alphabet: a list of strings, with each string representing the available characters for a position in the word
            must_have: TODO

        Returns:
            possible_words: a set of all possible words after eliminating words
    """
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


def format_guess(guess: str, score: str) -> str:
    """ formats a single word guess with colors to print to the command line

        Arguments:
            guess: the most recent word guessed
            score: the score of guess, represented by the characters 'g' (green), 'y' (yellow), and 'b' (black)

        Returns:
            output: the guess after being color formatted
    """
    output = ""
    for i in range(WORD_LENGTH):
        if score[i] == "g":
            output += command_line_formats.text.green + guess[i]
        elif score[i] == "y":
            output += command_line_formats.text.yellow + guess[i]
        else:
            output += command_line_formats.text.black + guess[i]
    output += command_line_formats.reset
    return output


def print_round(guesses: list[str], possible_words: set[str], won: bool) -> None:
    """ formats a single word guess with colors to print to the command line

        Arguments:
            guesses: a list of all guesses so far
            possible_words: a set of all possible words after the most recent guess
            won: a boolean indicating whether the most recent guess was the correct word
    """
    num_dashes = 20
    words_per_line = 15
    print("\n")
    print("-"*num_dashes + "\n" + "Guesses" + "\n" + "-"*num_dashes)
    for i in range(NUM_ALLOWED_GUESSES):
        print(f"{i+1} ||  {guesses[i]}")
    print("\n")
    if won:
        print("~ Congrats! ~\n\n")
    else:
        print("-"*num_dashes + "\n" + "Possible Words" + "\n" + "-"*num_dashes)
        possible_words_list = list(sorted(possible_words))
        for i in range(0, len(possible_words), words_per_line):
            print(*possible_words_list[i:i+words_per_line], sep=", ")
        print("\n")


def main():
    """ runs the game in the command line
    """
    alphabet = [string.ascii_lowercase for _ in range(WORD_LENGTH)]
    must_have = {letter: [False, [True for _ in range(WORD_LENGTH)]] for letter in string.ascii_lowercase}
    guesses = ["" for _ in range(NUM_ALLOWED_GUESSES)]

    # get all possible 5-letter words
    possible_words = set()
    with open(FIVE_WORD_DICT, "r") as f:
        all_words = f.read().split()
        for w in all_words:
            possible_words.add(w)

    print("\n"*50)

    num_guesses = 0
    won = False
    while (num_guesses < NUM_ALLOWED_GUESSES):
        print(command_line_formats.bold + f"ROUND {num_guesses+1}" + command_line_formats.reset)
        guess, score = get_guess()
        alphabet, must_have = modify_alphabet(alphabet, must_have, guess, score)
        possible_words = update_possible_words(possible_words, alphabet, must_have)
        guesses[num_guesses] = format_guess(guess, score)
        if score == "ggggg":
            won = True
        print_round(guesses, possible_words, won)
        num_guesses += 1
        if won:
            break

if __name__ == "__main__":
    main()
