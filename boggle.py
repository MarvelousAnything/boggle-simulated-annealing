from boggle_board import BoggleBoard
from vector import Vector
from words import Words


def score(word):
    length = len(word)
    if length < 3:
        return 0
    if length <= 4:
        return 1
    if length == 5:
        return 2
    if length == 6:
        return 3
    if length == 7:
        return 4
    if length >= 8:
        return 11


if __name__ == "__main__":
    # board = BoggleBoard([
    #     ["a", "s", "r", "d", "i"],
    #     ["n", "r", "l", "o", "n"],
    #     ["i", "i", "s", "a", "y"],
    #     ["p", "n", "c", "i", "i"],
    #     ["r", "g", "l", "n", "r"]])
    board = BoggleBoard.rand_board(Vector(4, 4))
    total_score = 0
    word_count = 0
    print(board)
    print("----------------------------------\n")
    used_words = []
    letter_frequencies = dict()
    total_words = len(Words.words)
    for index, word in enumerate(Words.words):
        if len(word) < 3:
            pass
        elif word in board:
            total_score += score(word)
            word_count += 1
            used_words.append(word)
            print(f"{index+1}/{total_words} - {word}", word_count, total_score)

    for word in used_words:
        for letter in word:
            if letter in letter_frequencies:
                letter_frequencies[letter] += 1
            else:
                letter_frequencies[letter] = 1
    print(board)
    print("--------------------------")
    print(total_score, word_count, total_score / word_count)
    for i in letter_frequencies.keys():
        print(str(i) + ": " + str(letter_frequencies[i]))
