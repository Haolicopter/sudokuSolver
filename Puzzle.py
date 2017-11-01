import helpers
import os
import sys
import random
from Board import Board


class Puzzle:
    DIFFICULTY = {
        'easy': 1,
        'medium': 2,
        'hard': 3,
        'evil': 4
    }

    def __init__(self):
        # Get Selenium Chrome Driver
        self.browser = helpers.getChromeDriver()

    # Standard sudoku is 9*9
    # There seems to be unlimited levels but we will stick to 1 - 1000
    def set(self, difficulty, level=random.randint(1, 1000), size=9):
        self.difficulty = difficulty
        self.level = level
        self.size = size
        self.showConfig()
        # Load game into browser
        self.browser.get(self.getUrl())
        # Load board
        self.board = Board(self.browser, self.size)

    # Construct puzzle URL
    # The parameters are confusing because they call difficulty level
    # and level is called set_id
    def getUrl(self):
        # The main website uses iframe to embed the actual game
        # Main url is http://websudoku.com
        # but the iframe pulls from http://show.websudoku.com
        return 'http://show.websudoku.com/?' \
            + 'level=' + str(self.difficulty) \
            + '&set_id=' + str(self.level)

    # Show puzzle configuration
    def showConfig(self):
        print('Difficulty = ' + str(self.difficulty))
        print('Level = ' + str(self.level))

    # Let's play!
    def play(self):
        stack = []
        (i, j) = self.board.emptyCells.popleft()
        for value in self.board.getCellPossibleValues(i, j):
            stack.append((i, j, value))
        while len(stack) > 0:
            # Pick a possible value
            (i, j, val) = stack.pop()
            self.board.setCell(i, j, val)

            (next_i, next_j) = self.board.emptyCells.popleft()
            possibleValues = self.board.getCellPossibleValues(next_i, next_j)
            # This candidate value is invalid
            if len(possibleValues) == 0:
                # Unset current cell and move to the next possible value
                self.board.unsetCell(i, j)
            else:
                for possibleValue in possibleValues:
                    stack.append((next_i, next_j, possibleValue))

        self.matrix.print()
