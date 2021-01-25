from random import Random
from typing import List, Set

from vector import Vector
from words import Words


class BoggleBoard:

    def __init__(self, board: List[List[str]]) -> None:
        self.board = board
        self.dimensions = Vector(len(board[0]), len(board))

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
