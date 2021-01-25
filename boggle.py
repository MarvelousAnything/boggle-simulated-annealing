dimensions = (4, 4)


def boggle_checker_helper(board, target, row, col, used) -> bool:
    if (row, col) in used:
        return False
    if board[row][col] != target[0]:
        return False
    if len(target) == 1:
        return True
    used = used.union({(row, col)})
    neighbors = find_neighbors(board, row, col)
    print(target, row, col)
    for i, j in neighbors:
        if boggle_checker_helper(board, target[1:], i, j, used):
            return True
    return False


def boggle_checker(board, target):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if boggle_checker_helper(board, target, row, col, set()):
                return True
    return False


def find_neighbors(board, row, col):
    neighbor_offsets = [(-1, -1), (-1, 0), (-1, 1),
                        (0, -1), (0, 1),
                        (1, -1), (1, 0), (1, 1)]
    neighbors = [(row + offset[0], col + offset[1]) for offset in neighbor_offsets if not (
                (row + offset[0] in dimensions or row + offset[0] == -1) or (
                    col + offset[1] in dimensions or col + offset[1] == -1))]
    return neighbors


if __name__ == "__main__":
    board = ["aaaa",
             "aaaa",
             "aaaa",
             "aaaa"]
    print(boggle_checker(board, 17*"a"))