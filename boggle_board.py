from random import Random
from typing import List, Set

from vector import Vector
from words import Words


def word_score(word):
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


class BoggleBoard:
    def __init__(self, board: List[List[str]]) -> None:
        self.board = board
        self.dimensions = Vector(len(board[0]), len(board))
        self.letter_frequency = dict()
        for i in self.board:
            for j in i:
                if j in self.letter_frequency:
                    self.letter_frequency[j] += 1
                else:
                    self.letter_frequency[j] = 1

    @staticmethod
    def rand_board(dims: Vector):
        board = []
        for col in range(dims.values[0]):
            board.append(
                Random().choices(Words.alphabet, weights=list(Words.letter_frequencies.values()), k=dims.values[1]))
        return BoggleBoard(board)

    def in_bounds(self, point: Vector) -> bool:
        return not any([p >= d or p <= -1 for (p, d) in list(zip(point.values, self.dimensions.values))])

    def find_neighbors(self, pos: Vector) -> List[Vector]:
        neighbor_offsets = [Vector(-1, -1), Vector(-1, 0), Vector(-1, 1),
                            Vector(0, -1), Vector(0, 1),
                            Vector(1, -1), Vector(1, 0), Vector(1, 1)]
        neighbors = [pos + offset for offset in neighbor_offsets if self.in_bounds(pos + offset)]
        return neighbors

    def __getitem__(self, pos: Vector) -> chr:
        if not self.in_bounds(pos):
            raise IndexError("Position out of range")
        return self.board[pos.values[1]][pos.values[0]]

    def __setitem__(self, key: Vector, value: str) -> None:
        if not self.in_bounds(key):
            raise IndexError("Position out of range")
        assert len(value) == 1, "must be of length 1"
        self.board[key.values[1]][key.values[0]] = value

    def __contains__(self, target: str):
        target_frequency = Words.get_frequency(target)
        for letter in target_frequency:
            if letter not in self.letter_frequency or target_frequency[letter] > self.letter_frequency[letter]:
                return False
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                pos = Vector(col, row)
                if self.checker_helper(target, pos):
                    return True
        return False

    def checker_helper(self, target: str, pos: Vector, used: Set[Vector] = None) -> bool:
        if used is None:
            used = set()
        if len(target) < 1:
            return False
        if pos in used:
            return False
        if self[pos] != target[0]:
            return False
        if len(target) == 1:
            return True
        used = used.union({pos})
        neighbors = self.find_neighbors(pos)
        for neighbor in neighbors:
            if self.checker_helper(target[1:], neighbor, used):
                return True
        return False

    def __str__(self):
        out = ""
        for i in self.board:
            out += (" ".join(i) + "\n")
        return out

    def get_score(self):
        total_score = 0
        word_count = 0
        used_words = []
        letter_frequency = dict()
        for index, word in enumerate(Words.words):
            if len(word) < 3:
                pass
            elif word in self:
                total_score += word_score(word)
                word_count += 1
                used_words.append(word)

        for word in used_words:
            for letter in word:
                if letter in letter_frequency:
                    letter_frequency[letter] += 1
                else:
                    letter_frequency[letter] = 1

        return total_score, word_count, letter_frequency

    def copy(self):
        return BoggleBoard(self.board)

    def mutate(self):
        rand = Random()
        new_board = None
        for i in range(rand.randint(1, 3)):
            pos = Vector(rand.randrange(0, self.dimensions.values[0]), rand.randrange(0, self.dimensions.values[1]))
            new_board = self.copy()
            new_board[pos] = rand.choices(Words.alphabet, weights=list(Words.letter_frequencies.values()), k=1)[0]
        return new_board

    @staticmethod
    def create_child(parent1, parent2, letter_frequency):
        assert parent1.dimensions == parent2.dimensions, "Parent dimensions must match"
        p1 = parent1.copy()
        p2 = parent2.copy()
        child = parent1.copy()

        for row in range(len(p1.board)):
            for col in range(len(p1.board[row])):
                pos = Vector(col, row)
                if letter_frequency[p1[pos]] >= letter_frequency[p2[pos]]:
                    child[pos] = p1[pos]
                else:
                    child[pos] = p2[pos]
        return child.mutate()
