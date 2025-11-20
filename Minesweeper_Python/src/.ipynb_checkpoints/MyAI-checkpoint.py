# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action


class MyAI(AI):

    def __init__(self, rowDimension, colDimension, totalMines, startX, startY):

        ########################################################################
        #							YOUR CODE BEGINS						   #
        ########################################################################
        self.__rowDimension = rowDimension
        self.__colDimension = colDimension
        self.__totalMines = totalMines
        self.__startX = startX
        self.__startY = startY

        # Initialization of board to keep track of current state
        self.__board = [[None for _ in range(colDimension)] for _ in range(rowDimension)]

        self.__firstMove = True  # First Move
        self.__lastMove = (startX, startY)  # Keep track of last move

        self.__numMoves = 0  # Tracking number of moves
        self.__maxMoves = rowDimension * colDimension

    # pass
    ########################################################################
    #							YOUR CODE ENDS							   #
    ########################################################################

    def getAction(self, number: int) -> "Action Object":

        ########################################################################
        #							YOUR CODE BEGINS						   #
        ######################################################################

        # if self.finalMove():
        # self.finalAction()

        # print("First move at: ", self.__startX, self.__startY)

        # print("getAction called with number:", number)

        # Update the board based on the number revealed after the first move
        lastX, lastY = self.__lastMove  # Last position which was uncovered
        # print(f"Updating board at position: ({lastX}, {lastY}) with number: {number}")

        # Call updateBoard and print before and after
        self.updateBoard(lastX, lastY, number)  # Update board state with the new number

        # Proceed to determine the next action
        # print("Determining next move...")
        action = self.nextMove()  # Decide on the next move
        # print(f"Next action determined: {action.getMove()}")

        # print("Board updated successfully.")
        self.printBoard()

        return action  # Return the action to be performed

    ########################################################################
    #							YOUR CODE ENDS							   #
    ########################################################################

    # Uncovers the first tile, specified by startX and startY
    def firstMove(self) -> "Action Object":
        return Action(1, self.__startX, self.__startY)

    # Adjusts position to format for MyAI.__board
    def adjustedPos(self, x: int, y: int) -> (int, int):
        return (self.__rowDimension - 1 - y, x)

    # Gets all the valid neighboring values of a position
    def getNeighbors(self, x, y):
        neighbors = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if i == 0 and j == 0:
                    continue
                xi, yj = x + i, y + j
                if 0 <= xi < self.__rowDimension and 0 <= yj < self.__colDimension:
                    neighbors.append((xi, yj))
        return neighbors

    # Updates board based on inputs
    def updateBoard(self, x, y, number):
        boardX, boardY = (y, x)
        self.__board[boardX][boardY] = number
        if number == 0:
            for i, j in self.getNeighbors(boardX, boardY):
                if (self.__board[i][j] == None or self.__board[i][j] < 0):
                    self.__board[i][j] = 9  # Represents that this tile can be uncovered without worry
        else:
            for i, j in self.getNeighbors(boardX, boardY):
                if self.__board[i][j] == None:  # If tile is covered still
                    self.__board[i][j] = -1  # Dangerous tile (the smaller the negative number, the more dangerous it is)
                elif self.__board[i][j] == -9: # If tile marked as a mine
                    pass # Ignore
                elif self.__board[i][j] <= -1:  # If already marked as dangerous
                    self.__board[i][j] -= 1  # Show that it is more likely to be the mine

    def checkOneBorder(self, x, y):
        if x - 1 < self.__rowDimensions:
            pass
        if x + 1 >= self.__rowDimensions:
            pass
        if y - 1 < self.__colDimensions:
            pass
        if y + 1 >= self.__colDimensions:
            pass

    # Determining next move, aka uncovering the next tile
    def nextMove(self) -> "Action Object":
        action = AI.Action.UNCOVER
        greatestSmallest = -99
        greatestSmallestX, greatestSmallestY = -1, -1
        self.__numMoves += 1
        for x in range(self.__rowDimension):
            for y in range(self.__colDimension):
                self.checkSafety(x, y)
                if self.__board[x][y] == 9:  # If spot is guaranteed to be safe
                    self.__lastMove = (y, x)
                    return Action(action, y, x)
                elif self.__board[x][y] != None and self.__board[x][y] > greatestSmallest and self.__board[x][
                    y] < 0:  # If no safe spot available
                    greatestSmallest = self.__board[x][y]  # Get greatest negative number (least likely to be a mine)
                    greatestSmallestX, greatestSmallestY = x, y
        check11XAction = self.check11XPattern() # 1 - 1 - X Pattern (https://minesweepergame.com/strategy/patterns.php)
        if check11XAction is not None:
            return check11XAction
        print("Greatest Smallest: ", greatestSmallest, greatestSmallestX + 1, greatestSmallestY + 1)
        self.__lastMove = (greatestSmallestY, greatestSmallestX)
        return Action(action, greatestSmallestY, greatestSmallestX)

    # 1 - 1 - X Pattern (https://minesweepergame.com/strategy/patterns.php)
    # IMPORTANT NOTE, MUST ADJUST CODE TO WORK FOR DIFFERENT NUMBER OF ROW AND COLUMN
    def check11XPattern(self) -> "Action Object":
        action = AI.Action.UNCOVER
        for a in range(self.__rowDimension): # For Rows
            if self.__board[a][0] == 1 and self.__board[a][1] == 1:
                if 0 <= a + 1 < self.__rowDimension and self.__board[a + 1][2] == None:
                    self.__lastMove = (2, a + 1)
                    return Action(action, 2, a + 1)
                if 0 <= a - 1 < self.__rowDimension and self.__board[a - 1][2] == None:
                    self.__lastMove = (2, a - 1)
                    return Action(action, 2, a - 1)
            if self.__board[a][self.__colDimension - 1] == 1 and self.__board[a][self.__colDimension - 2] == 1:
                if 0 <= a + 1 < self.__rowDimension and self.__board[a + 1][self.__colDimension - 3] < 0:
                    self.__lastMove = (self.__colDimension - 3, a + 1)
                    return Action(action, self.__colDimension - 3, a + 1)
                if 0 <= a - 1 < self.__rowDimension and self.__board[a - 1][self.__colDimension - 3] < 0:
                    self.__lastMove = (self.__colDimension - 3, a - 1)
                    return Action(action, self.__colDimension - 3, a - 1)
        for b in range(self.__colDimension): # For Cols
            if self.__board[0][b] == 1 and self.__board[1][b] == 1:
                if 0 <= b + 1 < self.__colDimension and self.__board[2][b + 1] == None:
                    self.__lastMove = (b + 1, 2)
                    return Action(action, b + 1, 2)
                if 0 <= b - 1 < self.__colDimension and self.__board[2][b - 1] == None:
                    self.__lastMove = (b - 1, 2)
                    return Action(action, b - 1, 2)
            if self.__board[self.__rowDimension - 1][b] == 1 and self.__board[self.__rowDimension - 2][b] == 1:
                if 0 <= b + 1 < self.__colDimension and self.__board[self.__rowDimension - 3][b + 1] < 0:
                    self.__lastMove = (b + 1, self.__rowDimension - 3)
                    return Action(action, b + 1, self.__rowDimension - 3)
                if 0 <= b - 1 < self.__colDimension and self.__board[self.__rowDimension - 3][b - 1] < 0:
                    self.__lastMove = (b - 1, self.__rowDimension - 3)
                    return Action(action, b - 1, self.__rowDimension - 3)
        return None

    # Checks surrounding area of a tile given x and y position, -9 guaranteed mines
    # If all mines have been accounted for, will mark available spaces for guaranteed safety
    def checkSafety(self, x, y):
        if self.__board[x][y] is None or self.__board[x][y] == 9 or self.__board[x][y] < 0:
            # If tile is not checked yet, pass
            pass
        totalMines = self.__board[x][y]
        numOfMinesCounted = 0
        emptyNeighbors = []
        for i, j in self.getNeighbors(x, y):
            if self.__board[i][j] is None or self.__board[i][j] == 9 or (self.__board[i][j] < 0 and self.__board[i][j] > -9):
                emptyNeighbors.append((i, j))
            elif self.__board[i][j] <= -9: # If tile is -9 or lower (impossible), it is guaranteed to be a mine
                numOfMinesCounted += 1
        if len(emptyNeighbors) == 0:
            pass
        elif totalMines == numOfMinesCounted:
            # print("\tGuaranteed Safe", y+1, x+1, self.__board[x][y])
            for i, j in emptyNeighbors:
                # print("\tInputting Safe:", j+1, i+1)
                self.__board[i][j] = 9 # These tiles are guaranteed safe
        elif totalMines is not None and len(emptyNeighbors) == totalMines - numOfMinesCounted:
            # print("Guaranteed Mines", y+1, x+1, self.__board[x][y], "\tNum Of Mines Counted:", numOfMinesCounted)
            # print("Length of Empty Neighbors:", len(emptyNeighbors), "\tTotal Mines:", totalMines)
            # print("Get Neighbors:", self.getNeighbors(x, y))
            for i, j in emptyNeighbors:
                # print("\tInputting Mine:", j+1, i+1, "\t Sees Currently:", self.__board[i][j])
                # print("\tTotal Mines:", totalMines)
                self.__board[i][j] = -9 # These tiles are guaranteed mines

    # Returns true if this is final move, false otherwise
    # Checks by seeing number of moves made compared to how many mines left
    def finalMove(self) -> bool:
        return self.__maxMoves - self.__numMoves <= self.__totalMines

    # Final action done, leaving all the remaining mines
    def finalAction(self) -> "Action Object":
        action = AI.Action.LEAVE
        for x in range(self.__rowDimension):
            for y in range(self.__colDimension):
                if self.__board[x][y] < 0:
                    self.__board[x][y] = 10  # Represents that we left this tile
                    return Action(action, y, x)

    # How do I end the program when it ends?

    # def findGuaranteedMines(self) ->

    def printBoard(self):
        for x in range(self.__rowDimension-1, -1, -1):
            row_values = []
            for y in range(self.__colDimension):
                # Replace None with a hyphen for display
                value = self.__board[x][y] if self.__board[x][y] is not None else '-'
                # Format the value to ensure proper spacing
                if isinstance(value, int) and value < 0:
                    formatted_value = f"{value} "
                else:
                    formatted_value = f"{value:>2} "
                row_values.append(formatted_value)  # Convert to string for joining
            print("".join(row_values).rstrip())  # Print the row as a space-separated string and strip the trailing space
