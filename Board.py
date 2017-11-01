import helpers
import itertools
import math
from collections import deque
import itertools


class Board:

    def __init__(self, browser, size):
        self.browser = browser
        self.size = size
        self.squareSize = int(math.sqrt(size))

        self.values = []
        self.emptyCells = deque([])
        self.emptyCellsTree = None
        self.squares = self.getSquares()
        self.load()
        self.print()

    # Load board from game
    def load(self):
        xpath = './/table[@id="puzzle_grid"]//input'
        cells = self.browser.find_elements_by_xpath(xpath)
        for i in range(self.size):
            row = []
            for j in range(self.size):
                stringValue = cells[i * self.size + j].get_attribute('value')
                intValue = int(stringValue) if stringValue.strip() else None
                row.append(intValue)
                if intValue is None:
                    self.emptyCells.append((i, j))
            self.values.append(row)
        self.emptyCellsTree = self.emptyCells.copy()

    # Print the current board
    def print(self):
        print('Printing board...')
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(self.values[i][j])
            print(row)
        if len(self.emptyCells) > 0:
            print('There are ' + str(len(self.emptyCells)) + ' empty cells.')

    # Divide board into 3 by 3 squares
    def getSquares(self):
        squares = []
        for i in range(self.squareSize):
            for j in range(self.squareSize):
                square = []
                for a in range(self.squareSize):
                    for b in range(self.squareSize):
                        square.append(
                            (i * self.squareSize + a, j * self.squareSize + b)
                        )
                squares.append(square)
        return squares

    # Get all possible values for current cell
    def getCellPossibleValues(self, cur_i, cur_j):
        result = list(range(1, self.size + 1))

        # Check square
        square_index = int(cur_i / self.squareSize) * \
            self.squareSize + int(cur_j / self.squareSize)
        square = self.squares[square_index]
        for (i, j) in square:
            if self.values[i][j] is not None and self.values[i][j] in result:
                result.remove(self.values[i][j])

        for i in range(self.size):
            # Check column
            if self.values[i][cur_j] is not None and self.values[i][cur_j] in result:
                result.remove(self.values[i][cur_j])
            # Check row
            if self.values[cur_i][i] is not None and self.values[cur_i][i] in result:
                result.remove(self.values[cur_i][i])

        return result

    def recountEmptyCells(self, i, j):
        cur_i = self.emptyCellsTree.index((i, j)) + 1
        prev_i = self.emptyCellsTree.index(self.emptyCells[0])
        self.emptyCells = deque(list(itertools.islice(
            self.emptyCellsTree, cur_i, None)))
        # Unset the new empty cells
        for i in range(cur_i, prev_i):
            (x, y) = self.emptyCellsTree[i]
            self.unsetCell(x, y)

    # Set cell value
    def setCell(self, i, j, val):
        if val is None:
            return

        print('Set cell (' + str(i) + ', ' + str(j) + ') to ' + str(val))
        self.values[i][j] = val
        helpers.setValue(self.browser, i, j, val)

    # Unset cell value
    def unsetCell(self, i, j):
        if self.values[i][j] is None:
            return

        print('Unset cell (' + str(i) + ', ' + str(j) + ')')
        self.values[i][j] = None
        helpers.setValue(self.browser, i, j, '')
