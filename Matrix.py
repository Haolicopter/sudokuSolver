import helpers
import itertools
import math


class Matrix:

    def __init__(self, browser, size):
        self.browser = browser
        self.size = size
        self.squareSize = int(math.sqrt(size))
        self.vectorTypes = ('row', 'col', 'square')
        self.totalCount = 0
        self.count = {}
        for v in self.vectorTypes:
            self.count[v] = []
            for i in range(size):
                self.count[v].append([])
        self.completeVectors = []
        self.nearCompleteVectors = []

        # We can guess up to this many missing cells
        self.maxComboSize = 7

        self.load()
        self.print()

    # Load matrix from game
    def load(self):
        xpath = './/table[@id="puzzle_grid"]//input'
        cells = self.browser.find_elements_by_xpath(xpath)
        self.values = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                stringValue = cells[i*self.size+j].get_attribute('value')
                intValue = int(stringValue) if stringValue.strip() else None
                row.append(intValue)
                if intValue is not None:
                    self.updateCount(i, j, intValue)
            self.values.append(row)

    def updateCount(self, i, j, val):
        self.totalCount += 1
        self.count['row'][i].append((i, j, val))
        self.count['col'][j].append((i, j, val))
        squareIndex = int(i/self.squareSize)*self.squareSize + \
            int(j/self.squareSize)
        self.count['square'][squareIndex].append((i, j, val))

    # Print the current matrix
    def print(self):
        print('Printing matrix...')
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(self.values[i][j])
            print(row)

    # Divide matrix into squares
    def getSquares(self):
        squares = []
        for i in range(self.squareSize):
            for j in range(self.squareSize):
                square = []
                for a in range(self.squareSize):
                    for b in range(self.squareSize):
                        square.append(
                            (i*self.squareSize + a, j*self.squareSize + b)
                        )
                squares.append(square)
        return squares

    # Set cell value
    def setCell(self, i, j, val):
        if val is None or self.values[i][j] is not None:
            return

        print('Setting cell (' + str(i) + ', ' + str(j) + ') to ' + str(val))
        self.values[i][j] = val
        self.updateCount(i, j, val)
        helpers.setValue(self.browser, i, j, val)

    # Check if the matrix solution is correct
    def isComplete(self):
        if self.totalCount != self.size * self.size:
            return False

        for i in range(self.size):
            for v in self.vectorTypes:
                if not self.isVectorComplete(v, i):
                    return False

        return True

    # Check if vector (row, col, or square) is valid
    # Aka, it should contain pat of or all numbers from 1 to self.size
    def isVectorValid(self, vectorType, i):
        vector = self.count[vectorType][i]
        if len(vector) != len(set(vector)):
            return False

        for (i, j, val) in vector:
            if val < 1 or val > self.size:
                return False

        return True

    # Check if vector is complete
    # Aka, it should contain all numbers from 1 to self.size
    def isVectorComplete(self, vectorType, i):
        return (self.isVectorValid(self, vectorType, i) and
                len(self.count[vectorType][i]) == self.size)

    # Get row and col indexes given vector type
    def getRowAndColIndexes(self, vectorType, i, j):
        if vectorType == 'row':
            return (i, j)
        elif vectorType == 'col':
            return (j, i)
        elif vectorType == 'square':
            raise Exception('Unhandled vector type!')
        else:
            raise Exception('Unknown vector type!')
