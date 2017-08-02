import helpers
import itertools


class Matrix:

    def __init__(self, browser, size):
        self.browser = browser
        self.size = size
        self.vectorTypes = ('row', 'col')
        self.totalCount = 0

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
            self.values.append(row)

    # Print the current matrix
    def print(self):
        print('Printing matrix...')
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(self.values[i][j])
            print(row)
        print()

    # Set cell value
    def setCell(self, i, j, val):
        if val is None:
            return
        if self.values[i][j] is not None:
            return

        print('Setting cell (' + str(i) + ', ' + str(j) + ') to ' + str(val))
        self.values[i][j] = val
        self.totalCount += 1
        helpers.setValue(self.browser, i, j, val)

    # Check if the matrix is complete
    def isComplete(self):
        return self.totalCount == self.size * self.size

    # Check if the matrix solution is correct
    def isCorrect(self):
        if not self.isComplete():
            return False
        # TODO:
        # 1. Check square completeness
        # 2. Check row completeness
        # 3. Check col completeness
        return True

    # Check if index is in range
    def indexIsInRange(self, row, col):
        if row < 0 or row > self.size-1:
            return False
        if col < 0 or col > self.size-1:
            return False
        return True

    # Get row and col indexes given vector type
    def getRowAndColIndexes(self, vectorType, i, j):
        if vectorType == 'row':
            return (i, j)
        elif vectorType == 'col':
            return (j, i)
        else:
            raise Exception('Unknown vector type!')
