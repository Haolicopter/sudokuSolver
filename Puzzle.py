import helpers
import os
import sys
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
            self.solveIncompleteVectors()

        self.matrix.print()

    # Complete row, column and square:
    # Each row, column and square should contain all the numbers 1 to self.size
    def completeVector(self, v):
        squares = self.matrix.getSquares()
        for i in range(self.size):
            # print('Checking ' + v + str(i) + '...')
            numbers = []
            if v == 'row' or v == 'col':
                for j in range(self.size):
                    numbers.append(self.matrix.getRowAndColIndexes(v, i, j))
            elif v == 'square':
                numbers = squares[i]
            self.setMissingCell(numbers)

    # Complete numbers in a given space (row, col, or square)
    def setMissingCell(self, numbers):
        if len(numbers) != self.size:
            raise Exception('Number out of range!')

        missingNumbers = list(range(1, self.size+1))
        for (row, col) in numbers:
            val = self.matrix.values[row][col]
            if val is not None:
                missingNumbers.remove(val)
            else:
                missingNumRow = row
                missingNumCol = col
        # Current vector/square only misses one number
        if len(missingNumbers) == 1:
            self.matrix.setCell(
                missingNumRow, missingNumCol, missingNumbers[0])

    # Try solving incomplete rows/cols/square
    def solveIncompleteVectors(self):
        if len(self.matrix.incompleteVectors) == 0:
            print('No incomplete vectors to solve')
            return
        self.eliminateImpossibleCombinations(self.matrix.incompleteVectors[0])

    # Eliminate impossible combinations
    def eliminateImpossibleCombinations(self, vectorType, i, missingCount):
        # Lay out all the possible combinations
        candidates = self.matrix.getCandidates(vectorType, i)

        candidatesCount = len(candidates)
        if candidatesCount == 0:
            print(vectorType + ' ' + str(i) + ' have zero valid candidate.')
            return

        hasMessage = False
        message = 'Using eliminateImpossibleCombinations method at ' + \
            vectorType + ' ' + str(i) + ' with ' + str(missingCount) + \
            ' missing cells, we nailed down to ' + str(candidatesCount) + \
            ' possible combo(s)' + os.linesep

        for candidate in candidates:
            line = ''
            for x in range(len(candidate)):
                line += str(candidate[x]['val']) + ', '
            message += line[:-2] + os.linesep

        if candidatesCount == 1:
            message += 'Since this is the only possible combination. ' + \
                'We solved entire ' + vectorType + ' ' + str(i) + os.linesep
            for cell in candidates[0]:
                if cell['isGuess']:
                    hasMessage = True
                    message += 'Setting cell (' + str(cell['row']) + ', ' + \
                        str(cell['col']) + ') to ' + str(cell['val']) + \
                        os.linesep
                    self.matrix.setCell(cell['row'], cell['col'], cell['val'])
        elif candidatesCount > 1:
            message += 'Finding missing cells that all combos agree on' + \
                os.linesep
            for x in range(len(candidates[0])):
                cell = candidates[0][x]
                if cell['isGuess'] is False:
                    continue
                isCommon = True
                for i in range(1, candidatesCount):
                    if cell['val'] != candidates[i][x]['val']:
                        isCommon = False
                        break
                if isCommon:
                    hasMessage = True
                    message += 'Setting cell (' + str(cell['row']) + ', ' + \
                        str(cell['col']) + ') to ' + str(cell['val']) + \
                        os.linesep
                    self.matrix.setCell(cell['row'], cell['col'], cell['val'])

        if hasMessage:
            print(message.rstrip())
