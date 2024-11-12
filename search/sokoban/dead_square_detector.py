#!/usr/bin/env python3
from game.board import Board, ETile
from typing import List
from queue import Queue


def detect(board: Board) -> List[List[bool]]:
    """
    Returns 2D matrix containing true for dead squares.

    Dead squares are squares, from which a box cannot possibly
     be pushed to any goal (even if Sokoban could teleport
     to any location and there was only one box).

    You should prune the search at any point
     where a box is pushed to a dead square.

    Returned data structure is
        [board_width] lists
            of [board_height] lists
                of bool values.
    (This structure can be indexed "struct[x][y]"
     to get value on position (x, y).)
    """
    def in_range(x1, y1):
        return 0 <= x1 < board.width and 0 <= y1 < board.height
    
    dead_end = True
    result = [[dead_end for _ in range(board.height)] for _ in range(board.width)]

    q = Queue()
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for i in range(board.width):
        for j in range(board.height):
            if ETile.is_target(board.tile(i, j)):
                result[i][j] = not dead_end
                q.put((i, j))

    visited = set()

    while not q.empty():
        x,y = q.get()
        result[x][y] = not dead_end
        visited.add((x, y))

        for dx, dy in moves:
            nx, ny = x + dx, y + dy
            sx, sy = x + 2 * dx, y + 2 * dy
            if in_range(sx, sy) and not ETile.is_wall(board.tile(nx, ny)) and not ETile.is_wall(board.tile(sx, sy)) and (nx, ny) not in visited:
                q.put((nx, ny))

    return result
