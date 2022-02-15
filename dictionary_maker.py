import json
import string

WORD_LENGTH = 5

# https://github.com/matthewreagan/WebstersEnglishDictionary

with open("dictionary.json", "r") as english_words_file:
    with open("five_letter_words.txt", "w") as five_letter_words_file:
        data = json.load(english_words_file)
        first_word = True
        for word in data:
            if len(word) == WORD_LENGTH:
                for i in range(WORD_LENGTH):
                    if word[i] not in string.ascii_lowercase:
                        break
                    if i == WORD_LENGTH - 1:
                        if first_word:
                            five_letter_words_file.write(word)
                            first_word = False
                        else:
                            five_letter_words_file.write("\n" + word)