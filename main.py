import enchant
d = enchant.Dict("en_US")

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