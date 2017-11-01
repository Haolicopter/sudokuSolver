import helpers
import itertools
import math


class Board:

    def __init__(self, browser, size):
        self.browser = browser
        self.size = size
        self.squareSize = int(math.sqrt(size))

        self.values = []
        self.emptyCells = []
        self.squares = self.getSquares()
        self.load()
        self.print()

    # Load matrix from game
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

    # Print the current matrix
    def print(self):
        print('Printing matrix...')
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(self.values[i][j])
            print(row)

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
    def getCellPossibleValues(cur_i, cur_j):
        result = list(range(1, self.size + 1))
        # Check square
        square_index = int(i / self.squareSize) * \
            self.squareSize + int(j / self.squareSize)
        square = self.squares[square_index]
        for (i, j) in square:
            if self.values[i][j] is not None and if self.values[i][j] is in result:
                result.remove(self.values[i][j])

        for i in range(self.size):
            # Check column
            if self.values[i][cur_j] is not None and if self.values[i][cur_j] is in result:
                result.remove(self.values[i][cur_j])
            # Check row
            if self.values[cur_i][i] is not None and if self.values[cur_i][i] is in result:
                result.remove(self.values[cur_i][i])

        return result

    # Set cell value
    def setCell(self, i, j, val):
        if val is None or self.values[i][j] is not None:
            return

        print('Set cell (' + str(i) + ', ' + str(j) + ') to ' + str(val))
        self.values[i][j] = val
        # Remove from empty cell list if exist
        if (i, j) is in self.emptyCells:
            self.emptyCells.remove((i, j))
        helpers.setValue(self.browser, i, j, val)

    # Unset cell value
    def unsetCell(self, i, j):
        if self.values[i][j] is None:
            return

        print('Unset cell (' + str(i) + ', ' + str(j) + ')')
        self.values[i][j] = None
        # Add to empty cell list if not already exist
        if (i, j) is not in self.emptyCells:
            self.emptyCells.append((i, j))
        helpers.setValue(self.browser, i, j, None)
