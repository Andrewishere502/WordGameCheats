import random


def is_valid_length(word, min_len, max_len):
    """Return true if the word is above or equal to the minimum length
    and below or equal to the maximum length.
    """
    return len(word) >= min_len and len(word) <= max_len


def count_letters(iterable):
    """Count the frequency of each letter in a given iterable, then
    return the results as a dictionary.
    """
    letter_counts = {}
    for letter in tuple(set(iterable)):
        count = iterable.count(letter)
        letter_counts[letter] = count
    return letter_counts


def has_valid_letters(word, letter_counts):
    """Return False any letter occurs more times in letter_counts than
    in word.
    """
    word_letters = tuple(set(word))
    for letter in word_letters:
        # There are more of a specific letter in this word than can
        # be chosen.
        if word.count(letter) > letter_counts.get(letter, 0):
            return False
    return True


def get_valid_words(min_len, max_len, letter_counts):
    with open("Collins_Scrabble_Words_2019.txt", "r") as file:
        lines = file.readlines()
    words = [line[:-1] for line in lines]
    print("Total words:", len(words))

    valid_words = []
    for word in words:
        is_valid_len = is_valid_length(word, min_len, max_len)

        if is_valid_len:
            is_valid_letters = has_valid_letters(word, letter_counts)
            if is_valid_letters:
                valid_words.append(word)

    print("Valid words:", len(valid_words))
    return valid_words


def get_best_words(words):
    """Return a list of words sorted by length in descending order."""
    return sorted(words, key=lambda word: len(word), reverse=True)


def shuffle(words):
    """Return a list copy of the given iterable and shuffle it so the
    elements are randomly assorted.
    """
    words_copy = [word for word in words]
    random.shuffle(words_copy)
    return words_copy


letters = input("Please enter the letter options:  ").strip().upper()

if len(letters) > 6:
    raise ValueError("Invalid number of letters: {}".format(len(letters)))

letter_counts = count_letters(letters)

valid_words = get_valid_words(3, 6, letter_counts)
print(shuffle(valid_words))