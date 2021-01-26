import time

from boggle_board import BoggleBoard
from vector import Vector
import threading

count = 0

results = dict()

remaining_tests = 50


def get_scores():
    global results, count, remaining_tests

    while remaining_tests > 0:
        remaining_tests -= 1
        count += 1
        local_count = count
        print(f"Started game {count} on thread: {threading.current_thread()}\n")
        board, data = BoggleBoard.rand_board(Vector(4, 4)).get_score()
        results[board] = data
        print(f"Finished game {local_count} on thread: {threading.current_thread()}\n")


def do_simulations(n):
    threads = []
    for _ in range(n):
        x = threading.Thread(target=get_scores)
        x.start()
        threads.append(x)

    for t in threads:
        t.join()


def sum_frequency(a, b):
    out = a.copy()
    for letter in b:
        if letter in out:
            out[letter] += b[letter]
        else:
            out[letter] = b[letter]
    return out


if __name__ == "__main__":
    p1 = BoggleBoard.rand_board(Vector(4, 4))
    p2 = BoggleBoard.rand_board(Vector(4, 4))
    print(p1)
    print(p2)
    r1 = p1.get_score()
    r2 = p2.get_score()

    print(r1)
    print(r2)
    child = BoggleBoard.create_child(p1, p2, sum_frequency(r1[2], r2[2]))
    print(child)
