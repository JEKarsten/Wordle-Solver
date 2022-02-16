import string
import os
import sys
from formatting import command_line_formats

WORD_LENGTH = 5
NUM_ALLOWED_GUESSES = 6
FIVE_WORD_DICT = "five_letter_words.txt"


def load_words() -> set[str]:
    """ loads a .txt file with 1 word per line into a set

        Returns:
            possible_words: the initial set of all possible words
    """
    possible_words = set()

    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, FIVE_WORD_DICT)

    with open(file_path, "r") as f:
        all_words = f.read().split()
        for w in all_words:
            possible_words.add(w)

    return possible_words


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


def modify_alphabet(
        alphabet: list[str],
        must_have: dict[str, list[bool, list[bool]]],
        max_occurrences: dict[str, int],
        guess: str,
        score: str
        ) -> tuple[
            list[str],
            dict[str, list[bool, list[bool]]],
            dict[str, int]
            ]:
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

        # green: sets alphabet for the position to only be the single letter
        if score[i] == "g":
            alphabet[i] = guess[i]

        # yellow: 1) gets rid of letter from the alphabet for the current position
        #         2) adds letter to the must_haves, noting that it cannot appear in the current position
        elif score[i] == "y":
            alphabet[i] = alphabet[i].replace(letter, "", 1)
            if not must_have[letter][0]:
                must_have[letter][0] = True
            must_have[letter][1][i] = False

        # black: gets rid of letter from the alphabet for all positions execpt ones previously marked as green
        else:
            for position in range(WORD_LENGTH):
                # checks if letter has not already been marked green in the current position
                if len(alphabet[position]) > 1:
                    # checks if letter has been marked green or yellow in the same guess
                    num_occurrences = 0
                    for j in range(WORD_LENGTH):
                        if guess[j] == letter and score[j] in "gy":
                            num_occurrences += 1
                    # updates max_occurrences for letter to be the number of times it is green or yellow
                    max_occurrences[letter] = num_occurrences
                    if not num_occurrences:
                        alphabet[position] = alphabet[position].replace(letter, "", 1)

    return alphabet, must_have, max_occurrences


def update_possible_words(
        possible_words: set[str],
        alphabet: list[str],
        must_have: dict[str, list[bool, list[bool]]],
        max_occurrences: dict[str, int]
        ) -> set[str]:
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

        # checks if each letter is in the set of possible characters for each position
        for i in range(WORD_LENGTH):
            letter = word[i]
            if letter not in alphabet[i]:
                valid = False
                break
        if not valid:
            continue

        # for all letters in yellow, it checks that the letter appears at least once elsewhere in the word
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
        if not valid:
            continue

        # removes words in which a letter appears more time than its maximum allowance
        for letter in string.ascii_lowercase:
            letter_count = word.count(letter)
            if letter_count > max_occurrences[letter]:
                valid = False
        if not valid:
            continue

        # adds word to the set of valid words if it passes the above tests
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
    output = command_line_formats.intensity.BRIGHT
    for i in range(WORD_LENGTH):
        if score[i] == "g":
            output += command_line_formats.text_color.GREEN + guess[i]
        elif score[i] == "y":
            output += command_line_formats.text_color.YELLOW + guess[i]
        else:
            output += command_line_formats.text_color.BLACK + guess[i]
    output += command_line_formats.RESET_ALL
    return output


def print_round(guesses: list[str], possible_words: set[str], won: bool) -> None:
    """ pretty prints the list of guesses and possible words

        Arguments:
            guesses: a list of all guesses so far
            possible_words: a set of all possible words after the most recent guess
            won: a boolean indicating whether the most recent guess was the correct word
    """
    terminal_width = os.get_terminal_size().columns
    words_per_line = terminal_width // (WORD_LENGTH + 2)
    num_dashes = 20

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
    # variables that keep track of allowed letters
    alphabet = [string.ascii_lowercase for _ in range(WORD_LENGTH)]
    must_have = {letter: [False, [True for _ in range(WORD_LENGTH)]]
        for letter in string.ascii_lowercase}
    max_occurrences = {letter: WORD_LENGTH for letter in string.ascii_lowercase}

    # gets all possible 5-letter words
    possible_words = load_words()

    # initializes game variables
    guesses = ["" for _ in range(NUM_ALLOWED_GUESSES)]
    num_guesses = 0
    won = False

    # clears terminal
    print("\n" * os.get_terminal_size().lines)

    try:
        while (num_guesses < NUM_ALLOWED_GUESSES):
            # prints round number
            print(command_line_formats.style.BOLD + \
                f"ROUND {num_guesses+1}" + \
                command_line_formats.RESET_ALL)
            
            # get user input and checks for win
            guess, score = get_guess()
            if score == "ggggg":
                won = True
            
            # update alphabet and possible words
            alphabet, must_have, max_occurrences = modify_alphabet(
                alphabet, must_have, max_occurrences, guess, score)
            possible_words = update_possible_words(possible_words, alphabet, must_have, max_occurrences)

            # pretty prints guess and new possible words
            guesses[num_guesses] = format_guess(guess, score)
            print_round(guesses, possible_words, won)

            # updates guesses for next round (breaks if won)
            num_guesses += 1
            if won:
                break
    
    except KeyboardInterrupt:
        print("\n\nThank you for playing!\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
