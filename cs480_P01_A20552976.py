import sys
#TicTacToe Game
#Author: Mauricio Verduzco Chavira
#Version: 2.3
#Date: 26/10/2023

#General Specs about the solution:
#This code implements OOP to facilitate the solution of the game.abs
#Two clases were created: TicTacToeBoard and TicTacToeGame
#The first class help us operate and analyze the board in the most basic form.
#Also, on this first level we can calculate the best posible move... Meaning that the Minimax algorithms are contained in this class.
#The second class creates creates one object of the first type to use it as a game. This class is important for two main reasons. 
#First, this class recieves the arguments of the program and runs it as specified. Second, thes class has que play() function
# this play() function manages everything from calling the algorithms, setting the board, calling the winners and printing the results. 

class TicTacToeBoard:
    #Our constructor is empty as we only need the board.
    #Important consideration. The board is a nine element list and not a 3x3 matrix because this way will easier to map the users inputs. 
    def __init__(self):
        self.board = [' ' for _ in range(9)]#We create the board as empty by filling all spaces with ' '

    #As the name suggests, this function prints the board in an aesthetic way. 
    def print_board(self):
        for i in range(0, 9, 3):
            print("  |  ".join(self.board[i:i+3]))
            if i < 6:
                print("---+ --- +---")
        print("\n")

    #This function creates a list containting the index of every space on the board that is empty. 
    def get_legal_moves(self):
        legal_moves = []
        for position in range(1, 10):
            if self.board[position - 1] == ' ':
                legal_moves.append(position)
        return legal_moves

    #This funcitons recieves a player making a move and the position where he/she wants to place the move and updates the board withing the game.
    def make_move(self, position, player):
        position -= 1  # Convert to 0-based index
        if self.is_valid_move(position) and self.board[position] == ' ':
            self.board[position] = player
            return True
        else:
            return False
    
    #This function undo the move in the position given and sets it back to " ". 
    #This is used after exploring the diferent alternatives in the recusivity-.
    def undo_move(self, position):
        position -= 1  # Convert to 0-based index
        if position >= 0 and position < len(self.board) and self.board[position] != ' ':
            self.board[position] = ' '
            return True
        else:
            return False

    #This is a fancy rather unefficient way to know if the number given is actually a valid move.         
    def is_valid_move(self, position):
        return 0 <= position < 9

    #This function checks is certain player is a winner in that state.
    def is_winner(self, player):
        # Check rows for a win
        for i in range(0, 9, 3):
            if all(self.board[j] == player for j in range(i, i + 3)):
                return True
        # Check columns for a win
        for i in range(3):
            if all(self.board[i + j] == player for j in range(0, 9, 3)):
                return True
        # Check diagonals for a win
        if all(self.board[i] == player for i in range(0, 9, 4)):
            return True
        if all(self.board[i] == player for i in range(2, 7, 2)):
            return True
        #If there is not a Winner
        return False

    #This function asks if the other player is a winner, meaning that the original player is a looser. 
    def is_looser(self,player):
        if player == 'X':
            return self.is_winner('O')
        else:
            return self.is_winner('X')

    #This function evaluates if the board have some space left or not. 
    def is_full(self):
        return all(cell != ' ' for cell in self.board)

    #This is the main function to do the search. 
    #We have to know who is the player who invoqued it and if he/she is in Min or in Max (given by type).
    #This returns the best possible move and the counter of nodes. 
    def miniMax(self, player, type):
        depht_counter = 1
        if(type == 1):
            _, move, depht_counter = self.max_value(player, depht_counter)
        else:
            _, move, depht_counter = self.min_value(player,depht_counter)
        return move, depht_counter
    
    #This is the max function
    def max_value(self,player, count):
        if(self.is_full() or self.is_winner(player) or self.is_looser(player)):#We ask if the game is over and assign utilities. 
            if(self.is_winner(player)):
                v = 2
            elif (self.is_looser(player)):
                v = -2
            else:
                v = 0
            return v, None, count
        
        #We set some initial utility and move. 
        v = float('-inf')
        move = None

        #We explore the posible diferent outcomes asking for the alternate function in a recursive way.
        for a in self.get_legal_moves():
            count +=1#We increase the counter.
            if(player=='X'):
                alternatePlayer = 'O'
            else:
                alternatePlayer = 'X'
            self.make_move(a,player)#We make the move in question 
            v2,_,count = self.min_value(alternatePlayer,count)#We call the other function with this "new" board
            if v2 > v:#If we get a better utility we will save it and consider the acording move. 
                v = v2
                move = a
            self.undo_move(a)#We have to undo the exploration move
        return v, move, count
    
    #Min works as max but the other way arround
    def min_value(self,player,count):
        if(self.is_full() or self.is_winner(player) or self.is_looser(player)):
            if(self.is_winner(player)):
                v = -2
            elif (self.is_looser(player)):
                v = 2
            else:
                v = 0
            return v, None, count
    
        v = float('inf')
        move = None

        for a in self.get_legal_moves():
            count +=1
            if(player=='X'):
                alternatePlayer = 'O'
            else:
                alternatePlayer = 'X'
            self.make_move(a,player)
            v2,_,count = self.max_value(alternatePlayer,count)
            if v2 < v:
                v = v2
                move = a
            self.undo_move(a)
        return v, move, count

    #This is the same algorithm but with prunning
    def minimax_AlphaBeta(self, player,type):
        depht_counter = 1
        if(type == 1):
            _, move, depht_counter = self.max_valueAB(player, depht_counter, float('-inf'), float('inf'))
        else:
            _, move, depht_counter = self.min_valueAB(player, depht_counter, float('-inf'), float('inf'))
        return move, depht_counter
    
    def max_valueAB(self,player, count, alpha, beta):
        if(self.is_full() or self.is_winner(player) or self.is_looser(player)):
            if(self.is_winner(player)):
                v = 2
            elif (self.is_looser(player)):
                v = -2
            else:
                v = 0
            return v, None, count
        
        v = float('-inf')
        move = None

        for a in self.get_legal_moves():
            count +=1
            if(player=='X'):
                alternatePlayer = 'O'
            else:
                alternatePlayer = 'X'
            self.make_move(a,player)
            v2,_,count = self.min_valueAB(alternatePlayer,count, alpha, beta)
            if v2 > v:
                v = v2
                move = a
                alpha = max(alpha,v)
            self.undo_move(a)
            if(v>=beta):#If we get somwthing that surpasses our beta we know that we will not take that way so we can just go ahead an trim this.
                return v, move, count
        return v, move, count
    
    #Same thing as max
    def min_valueAB(self,player,count, alpha, beta):
        if(self.is_full() or self.is_winner(player) or self.is_looser(player)):
            if(self.is_winner(player)):
                v = -2
            elif (self.is_looser(player)):
                v = 2
            else:
                v = 0
            return v, None, count
    
        v = float('inf')
        move = None

        for a in self.get_legal_moves():
            count +=1
            if(player=='X'):
                alternatePlayer = 'O'
            else:
                alternatePlayer = 'X'
            self.make_move(a,player)
            v2,_,count = self.max_valueAB(alternatePlayer,count, alpha, beta)
            if v2 < v:
                v = v2
                move = a
                beta = min(beta,v)
            self.undo_move(a)
            if v<=alpha:
                return v, move, count
        return v, move, count

        
class TicTacToeGame:
    def __init__(self, *args):
        #We create a constructor with the 3 arguments: type of algorithm, first player and mode. 
        #Out of the first player we can deduct the next player. 
        #We create a "TicTacToeBoard"
        self.board = TicTacToeBoard()
        if len(args)>0:
            self.algo = args[0]
            self.first = args[1]
            self.mode = args[2]
            if self.first == 'X':
                self.second = 'O'
            else:
                self.second = 'X'
        else:#This is the default. 
            self.algo = 1
            self.first = 'X'
            self.second = 'O'
            self.mode = 1
    
    #This function we call at the begining of the excecution of the program
    def print_Game_Situation(self):
        # Display game information
        print("Verduzco Chavira, Mauricio, A20552976 solution:")
        print("Algorithm:", "MiniMax with alpha-beta pruning" if self.algo == 2 else "MiniMax")
        print("First:", self.first)
        print("Mode:", "human versus computer" if self.mode == 1 else "computer versus computer")
        self.board.print_board()

    #This function we will call everytime a computer will be taking a move.
    def getComputerMove(self, algo, player, type):
        if algo == 1: #We use regular miniMax
            bestMove, depth_counter = self.board.miniMax(player,type)
        else: #We use minimax with pruning
            bestMove, depth_counter = self.board.minimax_AlphaBeta(player, type)
        return bestMove, depth_counter
    
    #This is a small try catch function to know if a value can be, or not, and int type. This we will use for the uer input.
    def is_castable_to_int(self,value):
        try:
            int(value)
            return True
        except (ValueError, TypeError):
            return False

    #Play is the most important function of the code because it manages everything.
    def play(self):
        self.print_Game_Situation()#We print the begining of the game
        myWinnerFlag = False#We know the game is not over yet. 
        if self.mode == 1: #Human vs Computer
            while not self.board.is_full():
                legalMoveFlag = False
                while not legalMoveFlag:
                    print(f"{str(self.first)}'s move. What is your move (possible moves at the moment are: {', '.join(map(str, self.board.get_legal_moves()))} | enter 0 to exit the game)? ")
                    human_move = input()#We get the user move 
                    if human_move == '0':
                        #print("You exited the game")
                        sys.exit(0)#We exit the gane
                        break
                    elif not self.is_castable_to_int(human_move):
                        legalMoveFlag=False#We know the input is not legal
                    elif int(human_move) in self.board.get_legal_moves():
                        legalMoveFlag = True #Only legal moves
                    else:
                        legalMoveFlag=False
                self.board.make_move(int(human_move), self.first)#If we get a legal move, we can make it. 
                self.board.print_board()
                myWinnerFlag = self.board.is_winner(self.first)
                if(myWinnerFlag):
                    print(self.first,"'s WON")
                    break
                if(self.board.is_full()):
                    print('TIE')
                    break

                #If the game didn´t end, we get the computer move. 
                computer_move, z = self.getComputerMove(self.algo, self.second, 2)
                print(f"{str(self.second)}'s selected move: {str(computer_move)}. Number of search tree nodes generated:  {str(z)}.")
                self.board.make_move(computer_move, self.second)
                self.board.print_board()
                myWinnerFlag = self.board.is_winner(self.second)
                if(myWinnerFlag):
                    print(self.second, "'s WON")
                    break
                if(self.board.is_full()):
                    print('TIE')
                    break
        else: #Computer vs Computer
            while not self.board.is_full() or not flag:
                computer_move1, z = self.getComputerMove(self.algo, self.first, 1)
                print(f"{str(self.first)}'s selected move: {str(computer_move1)}. Number of search tree nodes generated:  {str(z)}.")
                self.board.make_move(computer_move1, self.first)
                myWinnerFlag = self.board.is_winner(self.first)
                self.board.print_board()
                if(myWinnerFlag):
                    print(self.first, "'s WON")
                    break
                if(self.board.is_full()):
                    print('TIE')
                    break
                computer_move2, z = self.getComputerMove(self.algo, self.second, 2)
                print(f"{str(self.second)}'s selected move: {str(computer_move2)}. Number of search tree nodes generated:  {str(z)}.")
                self.board.make_move(computer_move2, self.second)
                self.board.print_board()
                myWinnerFlag = self.board.is_winner(self.second)
                if(myWinnerFlag):
                    print(self.second, "'s WON")
                    break
                if(self.board.is_full()):
                    print('TIE')
                    break

#My main
def main():
    if len(sys.argv) != 4:
        print("ERROR: Not enough/too many/illegal input arguments.")
        sys.exit(1)

    try:
        int(sys.argv[1])
        int(sys.argv[3])
    except (ValueError, TypeError):
        print("ERROR: Not enough/too many/illegal input arguments.")
        sys.exit(1)
    
    algo = int(sys.argv[1])
    first = sys.argv[2]
    mode = int(sys.argv[3])

    valid_algos = [1, 2]
    valid_first = ['X', 'O']
    valid_modes = [1, 2]
    
    if algo in valid_algos and first in valid_first and mode in valid_modes:
        a = TicTacToeGame(algo, first, mode)
        a.play()
    else:
        print("ERROR: Not enough/too many/illegal input arguments.")
        sys.exit(1)

if __name__ == "__main__":
    main()