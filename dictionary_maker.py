import json
import string

# https://github.com/matthewreagan/WebstersEnglishDictionary

with open("dictionary.json", "r") as english_words_file:
    with open("five_letter_words", "w") as five_letter_words_file:
        data = json.load(english_words_file)

        for word in data:
            if len(word) == 5 and :
                five_letter_words_file.write(word + "\n")