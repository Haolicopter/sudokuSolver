import helpers
import os
import random
from Matrix import Matrix


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
        # Load matrix from game
        self.matrix = Matrix(self.browser, self.size)

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
        while not self.matrix.isComplete():
            for v in self.matrix.vectorTypes:
                self.completeVector(v)

        self.matrix.print()

    # Complete row, column and square:
    # Each row, column and square should contain all the numbers 1 to self.size
    def completeVector(self, v):
        squares = self.matrix.getSquares()
        for i in range(self.size):
            print('Checking ' + v + str(i) + '...')
            numbers = []
            if v == 'row' or v == 'col':
                for j in range(self.size):
                    numbers.append(self.matrix.getRowAndColIndexes(v, i, j))
            elif v == 'square':
                numbers = squares[i]
            self.completeSpace(numbers)

    # Complete numbers in a given space (row, col, or square)
    def completeSpace(self, numbers):
        if len(numbers) != self.size:
            raise Exception('Number out of range!')

        missingNumbers = list(range(1, self.size+1))
        for (row, col) in numbers:
            val = self.matrix.values[row][col]
            if val is not None:
                missingNumbers.remove(val)
            else:
                missNumRow = row
                missNumCol = col
        # Current vector/square only misses one number
        if len(missingNumbers) == 1:
            self.matrix.setCell(
                missNumRow, missNumCol, missingNumbers[0])
