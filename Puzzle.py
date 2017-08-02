import helpers
import sys
import random
import math
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
                for i in range(self.size):
                    self.completeVector(v, i)
            for square in self.getSquares():
                self.completeSquare(square)
            # TODO: remove exit and implement guess combo function
            sys.exit(1)

        if self.matrix.isCorrect():
            print('Yay! We did it!')
        else:
            print('Crap the solution is incorrect!')

        self.matrix.print()

    # Divide the grid into squares
    def getSquares(self):
        squareSize = int(math.sqrt(self.size))
        squares = []
        for i in range(squareSize):
            for j in range(squareSize):
                square = []
                for a in range(squareSize):
                    for b in range(squareSize):
                        square.append(
                            (i*squareSize + a, j*squareSize + b)
                        )
                squares.append(square)
        return squares

    # Complete row and column:
    # Each row and each column should contain all the numbers 1 to self.size
    def completeVector(self, v, i):
        print('Checking ' + v + str(i) + '...')
        numbers = []
        for j in range(self.size):
            numbers.append(self.matrix.getRowAndColIndexes(v, i, j))
        self.completeSpace(numbers)

    # Complete square:
    # Each square should contain all the numbers 1 to self.size
    def completeSquare(self, square):
        (row, col) = square[0]
        print('Checking square with top left at (' + str(row) + ', ' + str(col) + ')')
        self.completeSpace(square)

    # Complete numbers in a given space (row, col, or square)
    def completeSpace(self, numbers):
        if len(numbers) != self.size:
            raise Exception('Number out of range!')

        missingNumbers = list(range(1, self.size+1))
        for (row, col) in numbers:
            val = self.matrix.values[row][col]
            if val is not None:
                print('We already have ' + str(val))
                missingNumbers.remove(val)
            else:
                missNumRow = row
                missNumCol = col
        # Current vector/square only misses one number
        if len(missingNumbers) == 1:
            self.matrix.setCell(
                missNumRow, missNumCol, missingNumbers[0])
        else:
            print('Too many missing numbers..')
            print(missingNumbers)
