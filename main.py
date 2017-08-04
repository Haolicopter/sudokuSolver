#!/usr/bin/env python3

from Puzzle import Puzzle


puzzle = Puzzle()
puzzle.set(
    Puzzle.DIFFICULTY['easy'],
    27
)
puzzle.play()

# TODO: refactor Matrix to have Cell class
# it has three fields: row, col, val
# Matrix has three types of vectors: row, col, square
# it can returns:
# 1. full vector
# 2. vector with non-empty cells
# 3. vector with empty cells
# this saves work for updating and elimiate the need for count variables
