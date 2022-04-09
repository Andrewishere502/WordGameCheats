import os
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


def get_adj_indices(i, width, height):
    """Return a list of adjacent indices."""
    col_num = i % width
    row_num = i // width

    is_left_col = col_num == 0
    is_right_col = col_num == width - 1
    is_top_row = row_num == 0
    is_bottom_row = row_num == height - 1

    adj_indices = []
    # Horizontals
    if not is_left_col:
        # include left
        adj_indices.append(i - 1)
    if not is_right_col:
        # include right
        adj_indices.append(i + 1)

    # Verticals
    if not is_top_row:
        # include top_row
        adj_indices.append(i - width)
    if not is_bottom_row:
        # include bottom_row
        adj_indices.append(i + width)

    # Left diagonals
    if not is_left_col and not is_top_row:
        # include top left
        adj_indices.append(i - width - 1)
    if not is_left_col and not is_bottom_row:
        # include bottom left
        adj_indices.append(i + width - 1)

    # Right diagonals
    if not is_right_col and not is_top_row:
        # include top right
        adj_indices.append(i - width + 1)
    if not is_right_col and not is_bottom_row:
        # include bottom right
        adj_indices.append(i + width + 1)

    return adj_indices


def try_branch(check_i, letters, letter_matrix, width, height, letter_i=1, exclude=[]):
    """Return True if the given string of letters can be formed, else
    return False.
    """

    adj_indices = get_adj_indices(check_i, width, height)

    # Remove any 
    for excluded_i in exclude:
        try:
            adj_indices.remove(excluded_i)
        except ValueError:
            pass

    for adj_i in adj_indices:
        if letter_matrix[adj_i] == letters[letter_i]:
            # print(letter_matrix[adj_i], letters[letter_i])
            if letter_i == len(letters) - 1:
                return True
            else:
                exclude.append(adj_i)
                return True and try_branch(adj_i, letters, letter_matrix, width, height, letter_i=letter_i+1, exclude=exclude)
    return False


def is_word_possible(word, letter_matrix, width, height):
    """Recursively check if the word is possible by checking each
    letter's adjacent letters.
    """
    start_indices = [i for i, letter in enumerate(letter_matrix)
                     if letter == word[0]]
    # print("Start indices:", start_indices)
    for i in start_indices:
        if try_branch(i, word, letter_matrix, width, height, exclude=[i]):
            return True  # word is possible, stop looking and return true
    return False  # word could not be found in the letter_matrix


def get_valid_words(min_len, max_len, letter_counts, shape):
    with open("Collins_Scrabble_Words_2019.txt", "r") as file:
        lines = file.readlines()
    words = [line[:-1] for line in lines]
    print("Total words:", len(words))

    valid_words = []
    for word in words:
        is_valid_len = is_valid_length(word, min_len, max_len)
        is_valid_letters = has_valid_letters(word, letter_counts)
        is_possible = is_word_possible(word, letter_matrix, *shape)

        if is_valid_len and is_valid_letters and is_possible:
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


def display_words(words):
    padding = 3
    words_per_col = 6

    max_len = max({len(word) for word in words})

    for i, word in enumerate(words):
        if i % words_per_col == words_per_col - 1:
            end = "|\n"
        else:
            end = "|" + " " * padding
        output = "{0:{1}}".format(word, max_len)
        print(output, end=end)
    return max_len


if __name__ == "__main__":
    letter_matrix = input("Please enter the letters:  ").strip().upper()
    shape = (4, 4)
    if len(letter_matrix) != shape[0] * shape[1]:
        raise ValueError("Invalid number ({}) of letters for shape {}x{}".format(len(letter_matrix), *shape))

    letter_counts = count_letters(letter_matrix)

    min_len = 3
    max_len = 15
    valid_words = get_valid_words(min_len, max_len, letter_counts, shape)
    
    # best_words = get_best_words(valid_words)
    # print(best_words)

    shuffled_words = shuffle(valid_words)
    # print(shuffled_words)

    os.system("clear")
    
    display_words(shuffled_words)
