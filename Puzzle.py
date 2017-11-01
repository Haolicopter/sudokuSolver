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
        possibleValues = self.board.getCellPossibleValues(i, j)
        print('Adding all possible values for cell (' + str(i) + ', ' +
              str(j) + ') to stack: ' + ', '.join(map(str, possibleValues)))
        for possibleValue in possibleValues:
            stack.append((i, j, possibleValue))

        while len(stack) > 0:
            # Pick a possible value
            (i, j, val) = stack.pop()
            print('Trying ' + str(val) +
                  ' for cell (' + str(i) + ', ' + str(j) + ')')
            self.board.setCell(i, j, val)

            if len(self.board.emptyCells) == 0:
                break

            # Recount empty cell on back trace
            self.board.recountEmptyCells(i, j)

            (next_i, next_j) = self.board.emptyCells.popleft()
            possibleValues = self.board.getCellPossibleValues(
                next_i, next_j)
            # This candidate value is invalid
            if len(possibleValues) == 0:
                # Unset current cell and move to the next possible value
                print('No possible value for cell (' +
                      str(next_i) + ', ' + str(next_j) + '), let\'s traceback.')
                self.board.unsetCell(i, j)
                print('Stack atm: ', stack)
            # This candidate value looks good
            else:
                print('Adding all possible values for cell (' + str(next_i) + ', ' +
                      str(next_j) + ') to stack: ' + ', '.join(map(str, possibleValues)))
                for possibleValue in possibleValues:
                    stack.append((next_i, next_j, possibleValue))

        print('Done!')
        self.board.print()
        helpers.submit(self.browser)
