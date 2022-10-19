"""
Short Exercises #4
"""
SIZE = 3

class Board:

    def __init__(self):
        '''
        Constructor
        '''
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    
    def valid_move(self, row, col):
        '''
        Checks whether a move is valid

        Inputs:
            row: an integer
            col: an integer
        
        Returns: bool
        '''
        return row >= 0 and row < SIZE and col >= 0 and col < SIZE and not self.board[row][col].strip()
    
    def move(self, row, col, player):
        '''
        Updates the board *in-place*

        Inputs:
            row: an integer
            col: an integer
            player: a Player instance
        '''
        self.board[row][col] = player.symbol
    
    def winner(self, player):
        '''
        Checks whether a player is a winner

        Inputs:
            player: a Player instance
        
        Returns: bool
        '''
        for n in range(SIZE):
            if (self.board[0][n] == player.symbol and self.board[1][n] == player.symbol \
                and self.board[2][n] == player.symbol) or (self.board[n][0] == player.symbol and self.board[n][1] == player.symbol \
                and self.board[n][2] == player.symbol):
                return True
        
        if (self.board[0][0] == player.symbol and self.board[1][1] == player.symbol \
            and self.board[2][2] == player.symbol) or (self.board[0][2] == player.symbol \
            and self.board[1][1] == player.symbol and self.board[2][0] == player.symbol):
            return True
        
        return False
    
    def __repr__(self):
        '''
        Produces a string representation of a board
        '''
        # Good OOP Design: Always include a __repr__ method when creating classes
        return "|{}|{}|{}|\n--+-+--\n|{}|{}|{}|\n--+-+--\n|{}|{}|{}|".format(self.board[0][0], \
                self.board[0][1], self.board[0][2], self.board[1][0], self.board[1][1], self.board[1][2], \
                self.board[2][0], self.board[2][1], self.board[2][2])
"""
DO NOT MODIFY THE CODE BELOW
"""

"""
The Player class
""" 

class Player:

    def __init__(self, name, symbol):
        """
        Constructor for the Player class

        Player attributes:
          name (string): player's name
          symbol (string): player's symbol (one character)
        """
        self.name = name
        self.symbol = symbol

"""
The Game class
"""
class Game:

    def __init__(self):
        """
        Constructor for the Game class

        Game attributes:
          board (Board): the game board
          player1 (Player): player
          player2 (Player): player
          won (Boolean): True if game has a winner,
            False otherwise 
        """
        self.board = Board()
        self.player1 = None
        self.player2 = None
        self.winner = False

    def valid_input(self, keyboard):
        """
        Validate name and symbol:
          name is one string
          symbol is one character

        Input:
          keyboard (string): keyboard input

        Returns: True if valid, False otherwise
        """
        split = keyboard.split()
        return len(split) == 2 and len(split[1]) == 1

    def get_intput(self, player_num):
        """
        Get name and symbol from player

        Input:
          player_num (string): player 

        Returns:
          name (string): name of player
          symbol (string): player's symbol
        """
        s = "Player " + player_num + ": Enter you name and pick your symbol: "

        valid = False
        while not valid:
            keyboard = input(s)
            valid = self.valid_input(keyboard)
            if not valid:
                print("Player", player_num, "enter valid input this time...")
        name, symbol = keyboard.split()
        return name, symbol

    def start(self):
        """
        Method to start game 
          Collect keyboard input
          Initialize player1 and player2
        """
        print("\nReady to play tic-tac-toe?\n")

        name, symbol = self.get_intput("1")
        self.player1 = Player(name, symbol)
        name, symbol = self.get_intput("2")
        self.player2 = Player(name, symbol)

        print()

    def next_up(self, player):
        """
        Method to switch players

        Input:
          player (Player): current player

        Returns: next player
        """
        if player is self.player1:
            return self.player2
        else: 
            return self.player1

    def turn(self, player):
        """
        Method to play one turn of game
          Collect keyboard input
          Play move

        Input:
          player (Player): current player
        """
        valid = False
        while not valid:
            keyboard = input("Enter your move {}: ".format(player.name))
            row, col = keyboard.split()
            valid = self.board.valid_move(int(row), int(col))
            if not valid:
                print("Please play a valid move this time...")
        self.board.move(int(row), int(col), player)

    def play(self):
        """
        Method to run the game
          Start game
          Play turns 
          Check for winner
          Display result
        """
        self.start()
        player = self.player1

        for play in range(SIZE*SIZE):
            self.turn(player)
            print(self.board)
            if self.board.winner(player):
                print(player.name, "wins!")
                self.winner = True
                break
            player = self.next_up(player)

        if not self.winner:
            print("Tie game!")
        print("Nice game {} and {}!".format(self.player1.name, self.player2.name))

"""
Run game from the command line
"""
if __name__ == "__main__":
    g = Game()
    g.play()
