import threading
from random import Random
from typing import List

from boggle import BoggleBoard
from vector import Vector


class Simulator:

    def __init__(self, initial_boards: List[BoggleBoard], total_threads: int, bar, count):
        self.boards = initial_boards.copy()
        self.remaining_boards = initial_boards.copy()
        self.board_dims = self.boards[0].dimensions
        self.results = dict()
        self.total_threads = total_threads
        self.threads = []
        self.bar = bar
        self.count = count

    def get_random_board(self):
        return BoggleBoard.rand_board(self.board_dims)

    def randomize_boards(self):
        for board in range(len(self.remaining_boards)):
            self.remaining_boards[board] = BoggleBoard.rand_board(self.board_dims)

    @staticmethod
    def get_random_boards(n, dims):
        out = []
        for _ in range(n):
            out.append(BoggleBoard.rand_board(dims))
        return out

    def start(self):
        if len(self.threads) < self.total_threads:
            for t in range(self.total_threads):
                x = threading.Thread(target=self.do_simulations, name=f"xThread-{t}")
                x.start()
                self.threads.append(x)
        else:
            for t in self.threads:
                t.run()
        for t in self.threads:
            t.join()

    def do_simulations(self):
        while len(self.remaining_boards) > 0:
            self.count += 1
            self.bar.update(self.count)
            # local_count = self.count
            # print(f"Started game {self.count} on thread: {threading.current_thread()}\n")
            board = self.remaining_boards.pop(0)
            data = board.get_score()
            self.count += 1
            self.bar.update(self.count)
            self.results[board] = data
            # print(f"Finished game {local_count} on thread: {threading.current_thread()}\n")

    def sort_results(self):
        return {k: self.results[k] for k in sorted(self.results, key=lambda x: self.results[x][0], reverse=True)}

    def kill_weaklings(self):
        sorted_results = self.sort_results()
        self.results = dict(list(sorted_results.items())[:len(sorted_results) // 2])
        self.boards = list(self.results.keys())

    @staticmethod
    def sum_frequency(a, b):
        out = a.copy()
        for letter in b:
            if letter in out:
                out[letter] += b[letter]
            else:
                out[letter] = b[letter]
        return out

    def select_random_pair(self):
        rand = Random()
        p1, p2 = rand.choice(self.boards), rand.choice(self.boards)
        while p1 == p2:
            p1, p2 = rand.choice(self.boards), rand.choice(self.boards)
        return p1, p2

    def next_generation(self):
        self.kill_weaklings()
        children = []
        used_pairs = []
        for _ in range(len(self.results.keys()) * 2):
            p1, p2 = self.select_random_pair()
            while (p1, p2) in used_pairs:
                p1, p2 = self.select_random_pair()
            used_pairs.append((p1, p2))
            children.append(
                BoggleBoard.create_child((p1, self.results[p1]), (p2, self.results[p2]), self.sum_frequency(self.results[p1][2], self.results[p2][2])))
        return children
