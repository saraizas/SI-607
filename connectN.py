from enum import Enum

'''
This is the start of the HW.
If there is any conflict between the doc string and the HW document,
please follow the instruction in the HW document.
Good Luck and have fun !
'''

class Notation(Enum):
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2

class Player:
    def __init__(self, playerName, playerNotation, curScore):
        self.__playerName = playerName
        self.__playerNotation = playerNotation
        self.__curScore = curScore

    def display(self) -> str:
        return f"Name: {self.__playerName}, Notation: {self.__playerNotation}, Score: {self.__curScore}"

    def addScoreByOne(self):
        self.__curScore += 1

    def getScore(self):
        return self.__curScore

    def getName(self):
        return self.__playerName

    def getNotation(self):
        return self.__playerNotation

class Board:
    def __init__(self, rowNum, colNum):
        self.__rowNum = rowNum
        self.__colNum = colNum
        self.__grid = []

    def initGrid(self):
        self.__grid = [[Notation.EMPTY] * self.__colNum for _ in range(self.__rowNum)]

    def getColNum(self):
        return self.__colNum

    def placeMark(self, colNum, mark):
        if colNum >= self.__colNum:
            return False
        for row in range(self.__rowNum - 1, -1, -1):
            if self.__grid[row][colNum] == Notation.EMPTY:
                self.__grid[row][colNum] = mark
                return True
        return False

    def checkFull(self):
        return all(self.__grid[row][col] != Notation.EMPTY for row in range(self.__rowNum) for col in range(self.__colNum))

    def display(self):
        for row in self.__grid:
            print(' '.join(map(lambda x: str(x.value), row)))
        print()

    def __checkWinHorizontal(self, target):
        for row in range(self.__rowNum):
            for col in range(self.__colNum - target + 1):
                if all(self.__grid[row][col + i] == self.__grid[row][col] and self.__grid[row][col] != Notation.EMPTY for i in range(target)):
                    return self.__grid[row][col]
        return None

    def __checkWinVertical(self, target):
        for col in range(self.__colNum):
            for row in range(self.__rowNum - target + 1):
                if all(self.__grid[row + i][col] == self.__grid[row][col] and self.__grid[row][col] != Notation.EMPTY for i in range(target)):
                    return self.__grid[row][col]
        return None

    def __checkWinOneDiag(self, target, rowNum, colNum):
        if rowNum + target <= self.__rowNum and colNum + target <= self.__colNum:
            if all(self.__grid[rowNum + i][colNum + i] == self.__grid[rowNum][colNum] and self.__grid[rowNum][colNum] != Notation.EMPTY for i in range(target)):
                return self.__grid[rowNum][colNum]
        return None

    def __checkWinAntiOneDiag(self, target, rowNum, colNum):
        if rowNum - target >= -1 and colNum + target <= self.__colNum:
            if all(self.__grid[rowNum - i][colNum + i] == self.__grid[rowNum][colNum] and self.__grid[rowNum][colNum] != Notation.EMPTY for i in range(target)):
                return self.__grid[rowNum][colNum]
        return None

    def __checkWinDiagonal(self, target):
        for row in range(self.__rowNum):
            for col in range(self.__colNum):
                if self.__checkWinOneDiag(target, row, col) or self.__checkWinAntiOneDiag(target, row, col):
                    return self.__grid[row][col]
        return None

    def checkWin(self, target):
        return self.__checkWinHorizontal(target) or self.__checkWinVertical(target) or self.__checkWinDiagonal(target)

class Game:
    def __init__(self, rowNum, colNum, connectN, targetScore, playerName1, playerName2):
        self.__player1 = Player(playerName1, Notation.PLAYER1, 0)
        self.__player2 = Player(playerName2, Notation.PLAYER2, 0)
        self.__board = Board(rowNum, colNum)
        self.__connectN = connectN
        self.__targetScore = targetScore
        self.__currentPlayer = self.__player1

    def __playBoard(self, curPlayer):
        while True:
            col = int(input(f"{curPlayer.getName()}, enter column number to place your mark (0-{self.__board.getColNum() - 1}): "))
            if 0 <= col < self.__board.getColNum():
                if self.__board.placeMark(col, curPlayer.getNotation()):
                    self.__board.display()
                    break
                else:
                    print("Column is full, try again.")
            else:
                print("Invalid column number, try again.")

    def __changeTurn(self):
        if self.__currentPlayer == self.__player1:
            self.__currentPlayer = self.__player2
        else:
            self.__currentPlayer = self.__player1

    def playRound(self):
        self.__board.initGrid()
        while True:
            self.__playBoard(self.__currentPlayer)
            if self.__board.checkWin(self.__connectN) == Notation.PLAYER1:
                print(f"{self.__player1.getName()} wins!")
                self.__player1.addScoreByOne()
                break
            elif self.__board.checkWin(self.__connectN) == Notation.PLAYER2:
                print(f"{self.__player2.getName()} wins!")
                self.__player2.addScoreByOne()
                break
            elif self.__board.checkFull():
                print("It's a draw!")
                break
            self.__changeTurn()

    def play(self):
        while max(self.__player1.getScore(), self.__player2.getScore()) < self.__targetScore:
            self.playRound()
            print(f"Scores - {self.__player1.getName()}: {self.__player1.getScore()}, {self.__player2.getName()}: {self.__player2.getScore()}")

def main():
    game = Game(4, 4, 3, 2, 'P1', 'P2')  # Initialize game with 4 rows, 4 columns, connect 3, target score of 2
    game.play()

if __name__ == "__main__":
    main()
