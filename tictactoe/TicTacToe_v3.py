import shelve
import random
import os

class InvalidMoveException(Exception):
    pass

class Board:
    def __init__(self, size):
        self.cells = list([str(i + 1) for i in range(size * size)])
        self.size = size

    def __str__(self):

        board = ""

        for row in range(self.size - 1):
            board += '|'.join(list(map('{:^4s}'.format, self.cells[self.size * row : self.size * (row + 1)]))) + '\n'
            board += '-' * (self.size * 5) + '\n'

        board += '|'.join(list(map('{:^4s}'.format,self.cells[self.size * (self.size - 1) : self.size * self.size]))) + '\n'

        return board

    def isValidMove(self, pos):
        return 0 <= pos < self.size ** 2 and self.cells not in ['X', 'O']

    @property
    def availableMoves(self):
        return [int(x) for x in self.cells if x not in ['X', 'O']]

    def setCell(self, pos, value):
        self.cells[pos] = value

class Game:

    def __init__(self, restoreFile = None, **configs):
        def loadGame():
            with shelve.open('saves/' + restoreFile, 'r') as gameState:
                self.configs = gameState.configs
                self.board = gameState.board
                self.moveNumber = gameState.moveNumber
                self.moveHistory = gameState.moveHistory

        if restoreFile is not None:
            loadGame()

        else:
            self.configs = configs
            self.board = Board(self.configs['size'])
            self.moveNumber = 1
            self.moveHistory = []

        self.players = ('X', 'O')

    def save(self, saveFile):
        with shelve.open('saves/' + saveFile) as gameState:
            gameState.configs = self.configs
            gameState.board = self.board
            gameState.moveNumber = self.moveNumber
            gameState.moveHistory = self.moveHistory

    def isCPUMove(self):
        return self.configs['CPUMove'] is not None and ((self.moveNumber + 1) % 2 + 1) == self.configs['CPUMove']

    @property
    def currentPlayer(self):
        if self.isCPUMove():
            return 'CPU'
        else:
            return 'Player {}'.format((self.moveNumber + 1) % 2 + 1)

    def isValidMove(self, pos):
        return self.board.isValidMove(pos)

    def playMove(self, pos = None):
        def CPUMove():
            return random.choice(self.board.availableMoves)

        if pos is None:
            pos = CPUMove()

        else:
            if not self.isValidMove(pos - 1):
                raise InvalidMoveException

        player = self.players[(self.moveNumber + 1) % 2]
        self.board.setCell(pos - 1, player)

        self.moveHistory.append(pos - 1)

        return pos

    def undoMove(self):
        pos = self.moveHistory.pop()
        self.moveNumber -= 1
        self.board.setCell(pos, pos + 1)

    def checkForResult(self):
        def isWinner():

            player = self.players[(self.moveNumber + 1) % 2]

            # horizontal
            horizontal = any([all([self.board.cells[i] == player for i in range(j, j + self.board.size)]) for j in range (0, self.board.size ** 2, self.board.size)])

            # vertical
            vertical = any([all([self.board.cells[i] == player for i in range(j, j + self.board.size * (self.board.size - 1) + 1, self.board.size)])
                            for j in range (0, self.board.size)])

            # diagonal
            diagonal1 = all([self.board.cells[i] == player for i in range(0, self.board.size ** 2, self.board.size + 1)])
            diagonal2 = all([self.board.cells[i] == player for i in range(self.board.size - 1, self.board.size * (self.board.size - 1) + 1, self.board.size - 1)])

            return horizontal or vertical or diagonal1 or diagonal2

        def isTie():
            return self.moveNumber == self.board.size ** 2

        if isWinner():
            return '{} won!'.format(self.currentPlayer)

        elif isTie():
            return "It's a tie!"

        return False

    def __str__(self):
        return str(self.board)



def main():

    print('Welcome to Tic Tac Toe.')

    saveFiles = os.listdir('saves/')
    if len(saveFiles) > 0:
        print('You have existing games. Would you like to continue or start a new game?')
        choice = input("""1. Load game
        2. Start new game""")

        if choice == 1:
            for idx, file in enumerate(saveFiles):
                print('{}. {}'.format(idx + 1, file))
            print()
            response = input('Enter the index of the file you would like to load.')

            try:
                response = int(response)
                response = min(response, len(saveFiles))
                response = max(response, 1)
            except:
                print('You entered an invalid response. Loading file {}'.format(saveFiles[0]))
                response = 1

            game = Game(restoreFile = saveFiles[response - 1])

        else:
            print('Starting a new game.')
            try:
                size = int(input('Enter the size of the board. (Minimum 3)  '))
                size = max(size, 3)
            except:
                print('Invalid input. Setting size to 3.')

            cpu = input('Would you like to play against the computer? (y/n) ').lower() == 'y'

            if cpu:
                first = input('Would you like to go first? (y/n) ').lower() == 'y'
                if first:
                    CPUMove = 2
                else:
                    CPUMove = 1
            else:
                CPUMove = None

            game = Game(size = size, CPUMove = CPUMove)

    else:
        print('Starting a new game.')
        # print('**********************************')
        # print('Enter the position on the board to play a move.')
        # print("Enter 'u' to undo the previous move.")
        # print("Enter 'q' to quit the game.")
        # print('**********************************')

        try:
            size = int(input('Enter the size of the board. (Minimum 3)  '))
            size = max(size, 3)
        except:
            print('Invalid input. Setting size to 3.')

        cpu = input('Would you like to play against the computer? (y/n) ').lower() == 'y'

        if cpu:
            first = input('Would you like to go first? (y/n) ').lower() == 'y'
            if first:
                CPUMove = 2
            else:
                CPUMove = 1
        else:
            CPUMove = None

        game = Game(size = size, cpu = cpu, CPUMove = CPUMove)

    while True:

        print(game)

        if game.configs['cpu']:
            if game.isCPUMove():
                print("CPU's turn.")
                pos = game.playMove()
                print('CPU played at position {}.'.format(pos))

            else:
                print('Your turn.')
                choice = input("Enter a position to play a move or 'u' to undo the last move or 'q' to quit (and save). ")
                if choice == 'q':
                    save = input('Would you like to save your game before quitting? (y/n)').lower() == 'y'
                    if save:
                        saveFileName = input('Enter the name of the file to be saved: ')
                        game.save(saveFileName)
                    print('Quitting game.')
                    exit()

                if choice == 'u':
                    game.undoMove()

                while True:
                    try:
                        pos = int(choice)
                        game.playMove(pos)
                    except:
                        print('Invalid move. Please try again')
                        pos = input('Enter a position to play a move. ')
                    else:
                        break

        else:
            print("Player {}'s turn.".format((game.moveNumber + 1) % 2 + 1))
            choice = input("Enter a position to play a move or 'u' to undo the last move or 'q' to quit (and save). ")
            if choice == 'q':
                save = input('Would you like to save your game before quitting? (y/n)').lower() == 'y'
                if save:
                    saveFileName = input('Enter the name of the file to be saved: ')
                    game.save(saveFileName)
                print('Quitting game.')
                exit()

            if choice == 'u':
                game.undoMove()

            while True:
                try:
                    pos = int(choice)
                    game.playMove(pos)
                except:
                    print('Invalid move. Please try again')
                    pos = input('Enter a position to play a move. ')
                else:
                    break


        result = game.checkForResult()

        if result:
            print(result)
            print('Thank you for playing.')
            break

        game.moveNumber += 1

main()
