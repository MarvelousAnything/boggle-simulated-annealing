import time

from boggle import BoggleBoard
from simulator import Simulator
from vector import Vector
import progressbar
import time


if __name__ == "__main__":

    bar = progressbar.ProgressBar(max_value=202)
    count = 0

    initial_boards = Simulator.get_random_boards(10, Vector(4, 4))
    simulator = Simulator(initial_boards, 10, bar, count)
    with open("out.txt", "w") as o:
        o.write("")
        o.close()
    with open("out.txt", "a") as out:
        total_time_taken = 0
        for i in range(10):
            start_time = time.time()
            simulator.start()
            time_taken = (time.time() - start_time)
            total_time_taken += time_taken
            out.write(f"{time_taken} - " + str(simulator.sort_results()))
            out.write("\n")
            simulator = Simulator(simulator.next_generation(), simulator.total_threads, simulator.bar, simulator.count)
        out.write("\n\n")
        out.write(f"{total_time_taken}\n")
        for i in simulator.boards:
            out.write("-------------------------------\n")
            out.write(str(i) + "\n")
        out.close()
