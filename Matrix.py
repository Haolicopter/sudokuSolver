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
        self.incompleteVectors = []

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

        for v in self.vectorTypes:
            self.updateVectorCompleteness(v, i)

    def updateCount(self, i, j, val):
        self.totalCount += 1
        self.count['row'][i].append((i, j, val))
        self.count['col'][j].append((i, j, val))
        squareIndex = int(i/self.squareSize)*self.squareSize + \
            int(j/self.squareSize)
        self.count['square'][squareIndex].append((i, j, val))
        for v in self.vectorTypes:
            self.updateVectorCompleteness(v, i)

    # Check for complete and near complete for current row/col/square
    def updateVectorCompleteness(self, vectorType, i):
        vectorMissingCells = self.size - len(self.count[vectorType][i])
        vector = (vectorType, i, vectorMissingCells)
        # This vector is complete
        if vectorMissingCells == 0:
            if self.isVectorValid(self.count[vectorType][i]) is False:
                raise Exception(vectorType + ' ' + str(i) + ' is not correct!')
            print(vectorType + ' ' + str(i) + ' is complete')
            # Add to complete vector list if does not exist
            if vector not in self.completeVectors:
                print('adding to the complete vectors')
                self.completeVectors.append(vector)
            # Remove from near complete vector list if exists
            self.incompleteVectors = list(filter(
                lambda v: not (v[0] == vectorType and v[1] == i),
                self.incompleteVectors))
        # This vector is near complete
        elif vectorMissingCells <= self.maxComboSize:
            oldVector = None
            for (vv, ii, mm) in self.incompleteVectors:
                if vv == vectorType and ii == i:
                    oldVector = (vv, ii, mm)
            if oldVector is not None:
                self.incompleteVectors.remove(oldVector)
            self.incompleteVectors.append(vector)
            # Sort by number of missing cells
            self.incompleteVectors.sort(key=lambda row: row[2])

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
                if not self.isVectorComplete(self.count[v][i]):
                    return False

        return True

    # Check if vector (row, col, or square) is valid
    # Aka, it should contain pat of or all numbers from 1 to self.size
    def isVectorValid(self, vector):
        if len(vector) != len(set(vector)):
            return False

        for (i, j, val) in vector:
            if val < 1 or val > self.size:
                return False

        return True

    # Check if vector is complete
    # Aka, it should contain all numbers from 1 to self.size
    def isVectorComplete(self, vector):
        return (self.isVectorValid(self, vector) and
                len(vector) == self.size)

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

    def getFullVector(self, v, i):
        fullVector = []
        if v == 'row' or v == 'col':
            for j in range(self.size):
                fullVector.append(self.getRowAndColIndexes(v, i, j))
        elif v == 'square':
            fullVector = self.getSquares()[i]
        else:
            raise Exception('Unknown vector type!')

        return fullVector

    def getMissingNumbers(self, vectorType, i):
        missingNumbers = list(range(1, self.size+1))
        for (row, col, val) in self.count[vectorType][i]:
            if val is not None:
                missingNumbers.remove(val)
        return missingNumbers

    # Generate all permutations given a string of numbers
    def getCombo(self, numbers):
        return list(set(list(itertools.permutations(numbers))))

    def getCandidates(self, vectorType, i):
        candidates = []
        numbers = ''
        for num in self.getMissingNumbers(vectorType, i):
            numbers += str(num)
        combos = self.getCombo(numbers)
        for combo in combos:
            count = 0
            candidate = []
            fullVector = self.getFullVector(vectorType, i)
            for (row, col) in fullVector:
                # Load from combo
                if self.values[row][col] is None:
                    val = int(combo[count])
                    count += 1
                    isGuess = True
                # Load from current cell
                else:
                    val = self.values[row][col]
                    isGuess = False

                candidate.append({
                    'row': row,
                    'col': col,
                    'val': val,
                    'isGuess': isGuess
                })
            if self.isCandidateValid(candidate):
                candidates.append(candidate)

        return candidates

    def isCandidateValid(self, candidate):
        vector = []
        for x in range(len(candidate)):
            vector.append((
                candidate[x]['row'],
                candidate[x]['col'],
                candidate[x]['val'],
            ))

        return self.isVectorValid(vector)
