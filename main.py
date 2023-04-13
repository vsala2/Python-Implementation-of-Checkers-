# FINAL PROJECT
# Vaishnavi Salaskar & 00729695
# This is a Python implementation of classic game "Checkers". The response here is OOD. The board for checkers is 8*8 i.e, 8 rows and 8 columns for total of 64 grid squares.
# The Grid here is red and black in colors. All the players piece is on Black color grid. The grid here have row letters and column number.
# Rows are A-H and columns are 1-8. Each Player has 12 pieces.
# Player1 piece is "x" and player2 piece is "o".
# Initially both the players have to enter their name, we also check if entered name is empty. If so you have to reenter the name.
# The player will also be asked to begin the game, and if the jump is mandatory in the game or no.
# Initially, the pieces will only move left or right diagonally. looking if there is a piece of any other player diagonally placed.
# If there is a piece of any other player diagonally placed, we will jump a step ahead but diagonally. And the piece which is been jumped will be removed from the matrix.
# The piece is only allowed to move one step diagonally forward.
# The piece that reaches to the end of the row opposite to it, will be queen piece i.e, it can move diagonally backward and forward. The queen piece is also allowed to move one step at a time.
# You can also quit the the game by pressing q. The Player whose pieces are no more left or there is no legal steps to move or wants to q, will lose.
# We are also creating a file with name of both the players and date and time when the game is started. The players moves, start and end move, jump result, invalid input, illegal input and matrix is stored in this file. 


# copy Deepcopy is first constructing a new collection object and then recursively populating it with copies of the child objects 
from copy import deepcopy
# importing datetime
import datetime 
# importing os module provides functions for creating and removing a directory (folder)
import os

# creating a piece class
class Piece:
    #constructor for the piece class
    def __init__(self, board, move=None, parent=None, value=None):
        self.board = board
        self.value = value
        self.move = move
        self.parent = parent


    def get_children(self, minimizing_player, mandatory_jumping):
        current_state = deepcopy(self.board)
        available_moves = []
        children_states = []
        big_letter = ""
        queen_row = 0
        # checking if the pieces are on queen row 
        if minimizing_player is True:
            # checking if there is any available move with the parameters current state and mandatory jump
            available_moves = Board.find__available_moves_player1(current_state, mandatory_jumping)
            big_letter = "X"
            queen_row = 7
        else:
            # checking if there is any available move with the parameters current state and mandatory jump
            available_moves = Board.find__available_moves_player2(current_state, mandatory_jumping)
            big_letter = "O"
            queen_row = 0
        
        for i in range(len(available_moves)):
            old_i = available_moves[i][0]
            old_j = available_moves[i][1]
            new_i = available_moves[i][2]
            new_j = available_moves[i][3]
            state = deepcopy(current_state)
            # class board using a move 
            Board.make_move(state, old_i, old_j, new_i, new_j, big_letter, queen_row)
            children_states.append(Piece(state, [old_i, old_j, new_i, new_j]))
        return children_states

    # set a value
    def set_value(self, value):
        self.value = value

    # get a value
    def get_value(self):
        return self.value

    # get board
    def get_board(self):
        return self.board

    # get parent
    def get_parent(self):
        return self.parent

    # set parent
    def set_parent(self, parent):
        self.parent = parent

# creating a board class
class Board:

    # creating a constructor for the board class
    def __init__(self):
        # Creating list of list for the board
        self.matrix = [[], [], [], [], [], [], [], []]
        # alphabets for name of each column
        self.columnValue=['A','B','C','D','E','F','G','H']
        # numbers for name of each row
        self.rowValue=['1','2','3','4','5','6','7','8']
        # variable for name of player1
        self.name_player1 = ''
        # variable for name for player2
        self.name_player2 = ''
        # player is turned true
        self.player1_turn = True
        self.player2_turn = True
        # number of pieces for players
        self.pieces_player1 = 12
        self.pieces_player2 = 12
        self.available_moves = []
        # mandatory jumping for initial stage is set to false
        self.mandatory_jumping = False
        # variable for file name
        self.file_name = ''

        # setting value for matrix position R and B
        for row in self.matrix:
            for i in range(8):
                if i%2 == 1:
                    row.append("B")
                else:
                    row.append("R")
        # setting value for position in row 3
        self.matrix[3]=['B','R','B','R','B','R','B','R']

        # calling appropriate methods
        self.player1_available_position()
        self.player2_available_position()

    # setting values of martix position for player1
    def player1_available_position(self):
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.matrix[i][j] = ("x")
                else:
                    self.matrix[i][j] = ("R")

    # setting values of martix position for player2
    def player2_available_position(self):
        for i in range(5, 8, 1):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.matrix[i][j] = ("o")
                else:
                    self.matrix[i][j] = ("R")

    # method for printing matrix 
    def print_matrixGrid(self):
        print()
        for j in range(8):
            if j == 0:
                self.rowValue[j] = "    1"
            print(self.rowValue[j], end=" ")
        print("\n")
        i = 0
        for row in self.matrix:
            print(self.columnValue[i], end="  |")
            i += 1
            for elem in row:
                print(elem, end=" ")
            print()
        print()

    # method for getting input from player2
    def get_input_player2(self):
        # calling method to find available moves for player2
        available_moves = Board.find_available_moves_player2(self.matrix, self.mandatory_jumping)
        if len(available_moves) == 0:
            # if player1 has more pieces than player2
            if self.pieces_player1 > self.pieces_player2:
                print(f"{self.name_player2}, you have no moves left, and you have fewer pieces than the {self.name_player1}. YOU LOSE!")
                # open the file and appending the same as above in the file
                with  open(self.file_name,"a") as fileText:
                    content= f"\n{self.name_player2}, you have no more moves left, you have fewer pieces than the {self.name_player1}. YOU LOSE!"
                    fileText.write(content)
                exit()
            else:
                # when player2 has no more moves left
                print(f"{self.name_player2}, you have no available moves.\nGAME END!")
                # open the file and appending the same as above in the file
                with  open(self.file_name,"a") as fileText:
                    content= f"\n{self.name_player2}, you have no available moves.\nGAME END!"
                    fileText.write(content)
                exit()

        self.pieces_player1 = 0
        self.pieces_player2 = 0
        while True:
            # asking player 2 for where the piece is suppose to be moved
            co_value1 = input("Please Enter Your START Move in [i,j] Format: ")
            # if player2 wants to quit, press q
            if co_value1 == "q" or co_value1 == "Q":
                print(f"{self.name_player2}, you QUIT. \n{self.name_player1} WIN!")
                # open the file and appending the same as above in the file
                with  open(self.file_name,"a") as fileText:
                    content= f"{self.name_player2}, you QUIT. \n{self.name_player1} WIN!"
                    fileText.write(content)
                exit()
            co_value2 = input("Please Enter Your END Move in [i,j] Format:")
            # if player2 wants to quit, press q
            if co_value2 == "q" or co_value2 == "Q":
                print(f"{self.name_player2}, you QUIT. \n{self.name_player1} WIN!")
                # open the file and appending the same as above in the file
                with  open(self.file_name,"a") as fileText:
                    content= f"{self.name_player2}, you QUIT. \n{self.name_player1} WIN!"
                    fileText.write(content)
                exit()
            # spliting the co-ordinate by ','
            old = co_value1.split(",")
            new = co_value2.split(",")

            # Checking the length of input entered
            if len(old) != 2 or len(new) != 2:
                print("Illegal input. RE-ENTER")
                # open the file and appending the same as above in the file
                with  open(self.file_name,"a") as fileText:
                    content= f"\n{self.name_player2}, Illegal Input. RE-ENTER"
                    fileText.write(content)
            else:
                # storing the value for future
                for index, value in enumerate(self.columnValue):
                    if old[0]==value:
                        self.oldValue=index
                    if new[0]==value:
                        self.newValue=index
                old_i = str(self.oldValue)
                oldValue=int(old[1])
                oldValue=oldValue-1
                oldValue=str(oldValue)
                old_j = oldValue
                new_i = str(self.newValue)
                newValue=int(new[1])
                newValue=newValue-1
                newValue=str(newValue)
                new_j = newValue
                # checking input of the player
                if not old_i.isdigit() or not old_j.isdigit() or not new_i.isdigit() or not new_j.isdigit():
                    print("Illegal input. RE-ENTER")
                    # open the file and appending the same as above in the file
                    with  open(self.file_name,"a") as fileText:
                        content= f"\n{self.name_player2}, Illegal Input. RE-ENTER"
                        fileText.write(content)
                else:
                    # moving the pieces from old to new
                    movePos = [int(old_i), int(old_j), int(new_i), int(new_j)]
                    if movePos not in available_moves:
                        # open the file and appending the same as above in the file
                        with  open(self.file_name,"a") as fileText:
                            content= f"\n{self.name_player2}, Illegal Move. RE-ENTER"
                            fileText.write(content)
                        print("Illegal move!. RE-ENTER")
                    else:
                        # open the file and appending the move and storing the date and time the piece is moved
                        with open(self.file_name,"a") as fileText:
                            content=f"\n{self.name_player2} moved piece from {old[0]}, {old[1]} to {new[0]}, {new[1]}"
                            dateTime = content + f" : {datetime.datetime.now()}\n"
                            fileText.write(dateTime)
                            fileText.close()
                        Board.make_move(self.matrix, int(old_i), int(old_j), int(new_i), int(new_j), "O", 0)
                        for m in range(8):
                            for n in range(8):
                                if self.matrix[m][n][0] == "x" or self.matrix[m][n][0] == "X":
                                    self.pieces_player2 += 1
                                elif self.matrix[m][n][0] == "o" or self.matrix[m][n][0] == "O":
                                    self.pieces_player1 += 1
                        break

    # method for getting input from player1
    def get_input_player1(self):
        # calling method to find available moves for player1
        available_moves = Board.find__available_moves_player1(self.matrix, self.mandatory_jumping)
        if len(available_moves) == 0:
            # if player2 has more pieces than player1
            if self.pieces_player2 > self.pieces_player1:
                print(f"{self.name_player1}, you have no moves left, and you have fewer pieces than the {self.name_player2}. YOU LOSE!")
                # open the file and appending the same as above in the file
                with  open(self.file_name,"a") as fileText:
                    content= f"\n{self.name_player1}, you have no more moves left, you have fewer pieces than the {self.name_player2}. YOU LOSE!"
                    fileText.write(content)
                exit()
            else:
                # when player1 has no more moves left
                print(f"{self.name_player1}, you have no available moves.\nGAME END!")
                # open the file and appending the same as above in the fil
                with  open(self.file_name,"a") as fileText:
                    content= f"\n{self.name_player1}, you have no available moves.\nGAME END!"
                    fileText.write(content)
                exit()
        self.pieces_player1 = 0
        self.pieces_player2 = 0
        while True:
            # asking player 1 for where the piece is suppose to be moved
            co_value1 = input("Please Enter Your START Move in [i,j] Format: ")
            # if player2 wants to quit, press q
            if co_value1 == "q" or co_value1 == "Q":
                print(f"{self.name_player1}, you QUIT. {self.name_player2} WIN!")
                with  open(self.file_name,"a") as fileText:
                    content= f"{self.name_player1}, you QUIT. {self.name_player2} WIN!"
                    fileText.write(content)
                exit()
            co_value2 = input("Please Enter Your END Move in [i,j] Format:")
            # if player2 wants to quit, press q
            if co_value2 == "q" or co_value2 == "Q":
                print(f"{self.name_player1}, you QUIT. {self.name_player2} WIN!")
                with  open(self.file_name,"a") as fileText:
                    content= f"{self.name_player1}, you QUIT. {self.name_player2} WIN!"
                    fileText.write(content)
                exit()
            
            # spliting the co-ordinate by ','
            old = co_value1.split(",")
            new = co_value2.split(",")

            # Checking the length of input entered
            if len(old) != 2 or len(new) != 2:
                print("Illegal input. RE-ENTER")
                # open the file and appending the same as above in the file
                with  open(self.file_name,"a") as fileText:
                    content= f"\n{self.name_player1}, Illegal Input. RE-ENTER"
                    fileText.write(content)
            else:
                # storing the value for future
                for index, value in enumerate(self.columnValue):
                    if old[0]==value:
                        self.oldValue=index
                    if new[0]==value:
                        self.newValue=index
                old_i = str(self.oldValue)
                oldValue=int(old[1])
                oldValue=oldValue-1
                oldValue=str(oldValue)
                old_j = oldValue
                new_i = str(self.newValue)
                newValue=int(new[1])
                newValue=newValue-1
                newValue=str(newValue)
                new_j = newValue
                # checking input of the player
                if not old_i.isdigit() or not old_j.isdigit() or not new_i.isdigit() or not new_j.isdigit():
                    print("Illegal input. RE-ENTER")
                    # open the file and appending the same as above in the file
                    with  open(self.file_name,"a") as fileText:
                        content= f"\n{self.name_player1}, Illegal Input. RE-ENTER"
                        fileText.write(content)
                else:
                    # moving the pieces from old to new
                    movePos = [int(old_i), int(old_j), int(new_i), int(new_j)]
                    if movePos not in available_moves:
                        # open the file and appending the same as above in the file
                        with  open(self.file_name,"a") as fileText:
                            content= f"\n{self.name_player1}, Illegal Move. RE-ENTER"
                            fileText.write(content)
                        print("Illegal move! RE-ENTER")
                    else:
                         # open the file and appending the move and storing the date and time the piece is moved
                        with open(self.file_name,"a") as fileText:
                            content=f"\n{self.name_player1} moved piece from {old[0]}, {old[1]} to {new[0]}, {new[1]}"
                            dateTime = content + f" : {datetime.datetime.now()}\n"
                            fileText.write(dateTime)
                            fileText.close()
                        Board.make_move(self.matrix, int(old_i), int(old_j), int(new_i), int(new_j), "O", 0)
                        for m in range(8):
                            for n in range(8):
                                if self.matrix[m][n][0] == "x" or self.matrix[m][n][0] == "X":
                                    self.pieces_player2 += 1
                                elif self.matrix[m][n][0] == "o" or self.matrix[m][n][0] == "O":
                                    self.pieces_player1 += 1
                        break

    # checking for available moves for player1
    def find__available_moves_player1(board, mandatory_jumping):
        # available moves and available jumps are set empty
        available_moves = []
        available_jumps = []
        # for matrix 8*8 
        for m in range(8):
            for n in range(8):
                # checking there is x value in the matrix
                if board[m][n][0] == "x":
                    # checking for available moves diagonally forward
                    if Board.check_moves_player1(board, m, n, m + 1, n + 1):
                        available_moves.append([m, n, m + 1, n + 1])
                    if Board.check_moves_player1(board, m, n, m + 1, n - 1):
                        available_moves.append([m, n, m + 1, n - 1])
                    # checks for any jumps diagonally forward
                    if Board.check_jumps_player1(board, m, n, m + 1, n - 1, m + 2, n - 2):
                        available_jumps.append([m, n, m + 2, n - 2])
                    if Board.check_jumps_player1(board, m, n, m + 1, n + 1, m + 2, n + 2):
                        available_jumps.append([m, n, m + 2, n + 2])
                # if there is value X in the matrix
                elif board[m][n][0] == "X":
                    # Checking for available moves diagonally forward and backward
                    if Board.check_moves_player1(board, m, n, m + 1, n + 1):
                        available_moves.append([m, n, m + 1, n + 1])
                    if Board.check_moves_player1(board, m, n, m + 1, n - 1):
                        available_moves.append([m, n, m + 1, n - 1])
                    if Board.check_moves_player1(board, m, n, m - 1, n - 1):
                        available_moves.append([m, n, m - 1, n - 1])
                    if Board.check_moves_player1(board, m, n, m - 1, n + 1):
                        available_moves.append([m, n, m - 1, n + 1])
                    # checking for any jumps diagonally forward and backward
                    if Board.check_jumps_player1(board, m, n, m + 1, n - 1, m + 2, n - 2):
                        available_jumps.append([m, n, m + 2, n - 2])
                    if Board.check_jumps_player1(board, m, n, m - 1, n - 1, m - 2, n - 2):
                        available_jumps.append([m, n, m - 2, n - 2])
                    if Board.check_jumps_player1(board, m, n, m - 1, n + 1, m - 2, n + 2):
                        available_jumps.append([m, n, m - 2, n + 2])
                    if Board.check_jumps_player1(board, m, n, m + 1, n + 1, m + 2, n + 2):
                        available_jumps.append([m, n, m + 2, n + 2])
        # commands to run if jump is not mandatory 
        if mandatory_jumping is False:
            available_jumps.extend(available_moves)
            return available_jumps
        # commands to run if jump is mandatory 
        elif mandatory_jumping is True:
            if len(available_jumps) == 0:
                return available_moves
            else:
                return available_jumps

    # checking if there are any jumps for player 1
    def check_jumps_player1(board, old_i, old_j, via_i, via_j, new_i, new_j):
        # will not jump if input of new row is less than 0 or greater than 7
        if new_i > 7 or new_i < 0:
            return False
        # will not jump if input of new column is less than 0 or greater than 7
        if new_j > 7 or new_j < 0:
            return False
        # will not jump if there is B diagonally i.e no piece in between the jump
        if board[via_i][via_j] == "B":
            return False
        # will not jump if there is x i.e. player1 piece
        if board[via_i][via_j][0] == "X" or board[via_i][via_j][0] == "x":
            return False
        # will not jump if the jump to position is not B i.e, empty
        if board[new_i][new_j] != "B":
            return False
        # will not jump if jump from position is empty
        if board[old_i][old_j] == "B":
            return False
        # will not jump if jump from is a player1 piece
        if board[old_i][old_j][0] == "o" or board[old_i][old_j][0] == "O":
            return False
        return True

    # checking for player1 moves
    def check_moves_player1(board, old_i, old_j, new_i, new_j):
        # will not move if input of new row is less than 0 or greater than 7
        if new_i > 7 or new_i < 0:
            return False
        # will not jump if input of new column is less than 0 or greater than 7
        if new_j > 7 or new_j < 0:
            return False
        # will not move if move from position is empty
        if board[old_i][old_j] == "B":
            return False
        # will not move if move to position is empty
        if board[new_i][new_j] != "B":
            return False
        # will not move if move from is a player2 piece
        if board[old_i][old_j][0] == "o" or board[old_i][old_j][0] == "O":
            return False
        #will only move if new position entered is empty
        if board[new_i][new_j] == "B":
            return True

    # checking for available moves for player2
    def find_available_moves_player2(board, mandatory_jumping):
        # available moves and available jumps are set empty
        available_moves = []
        available_jumps = []
        # for matrix 8*8
        for m in range(8):
            for n in range(8):
                # checking there is o value in the matrix
                if board[m][n][0] == "o":
                    # checking for available moves diagonally forward
                    if Board.check_moves_player2(board, m, n, m - 1, n - 1):
                        available_moves.append([m, n, m - 1, n - 1])
                    if Board.check_moves_player2(board, m, n, m - 1, n + 1):
                        available_moves.append([m, n, m - 1, n + 1])
                    # checks for any jumps diagonally forward
                    if Board.check_jumps_player2(board, m, n, m - 1, n - 1, m - 2, n - 2):
                        available_jumps.append([m, n, m - 2, n - 2])
                    if Board.check_jumps_player2(board, m, n, m - 1, n + 1, m - 2, n + 2):
                        available_jumps.append([m, n, m - 2, n + 2])
                # if there is value O in the matrix
                elif board[m][n][0] == "O":
                    # Checking for available moves diagonally forward and backward
                    if Board.check_moves_player2(board, m, n, m - 1, n - 1):
                        available_moves.append([m, n, m - 1, n - 1])
                    if Board.check_moves_player2(board, m, n, m - 1, n + 1):
                        available_moves.append([m, n, m - 1, n + 1])
                    # checking for any jumps diagonally forward and backward
                    if Board.check_jumps_player2(board, m, n, m - 1, n - 1, m - 2, n - 2):
                        available_jumps.append([m, n, m - 2, n - 2])
                    if Board.check_jumps_player2(board, m, n, m - 1, n + 1, m - 2, n + 2):
                        available_jumps.append([m, n, m - 2, n + 2])
                    if Board.check_moves_player2(board, m, n, m + 1, n - 1):
                        available_moves.append([m, n, m + 1, n - 1])
                    if Board.check_jumps_player2(board, m, n, m + 1, n - 1, m + 2, n - 2):
                        available_jumps.append([m, n, m + 2, n - 2])
                    if Board.check_moves_player2(board, m, n, m + 1, n + 1):
                        available_moves.append([m, n, m + 1, n + 1])
                    if Board.check_jumps_player2(board, m, n, m + 1, n + 1, m + 2, n + 2):
                        available_jumps.append([m, n, m + 2, n + 2])
        # commands to run if jump is not mandatory                
        if mandatory_jumping is False:
            available_jumps.extend(available_moves)
            return available_jumps
        # commands to run if jump is mandatory 
        elif mandatory_jumping is True:
            if len(available_jumps) == 0:
                return available_moves
            else:
                return available_jumps

    # checking for player2 moves
    def check_moves_player2(board, old_i, old_j, new_i, new_j):
        # will not move if input of new row is less than 0 or greater than 7
        if new_i > 7 or new_i < 0:
            return False
        # will not jump if input of new column is less than 0 or greater than 7
        if new_j > 7 or new_j < 0:
            return False
        # will not move if move from position is empty
        if board[old_i][old_j] == "B":
            return False
        # will not move if move to position is empty
        if board[new_i][new_j] != "B":
            return False
        # will not move if move from is a player1 piece
        if board[old_i][old_j][0] == "x" or board[old_i][old_j][0] == "X":
            return False
        #will only move if new position entered is empty
        if board[new_i][new_j] == "B":
            return True

    # checking if there are any jumps for player 2
    def check_jumps_player2(board, old_i, old_j, via_i, via_j, new_i, new_j):
        # will not jump if input of new row is less than 0 or greater than
        if new_i > 7 or new_i < 0:
            return False
        # will not jump if input of new column is less than 0 or greater than
        if new_j > 7 or new_j < 0:
            return False
        # will not jump if there is B diagonally i.e no piece in between the jump
        if board[via_i][via_j] == "B":
            return False
        # will not jump if there is c i.e. player2 piece
        if board[via_i][via_j][0] == "O" or board[via_i][via_j][0] == "o":
            return False
        # will not jump if the jump to position is not B i.e, empty
        if board[new_i][new_j] != "B":
            return False
        # will not jump if jump from position is empt
        if board[old_i][old_j] == "B":
            return False
        # will not jump if jump from is a player1 piece
        if board[old_i][old_j][0] == "x" or board[old_i][old_j][0] == "X":
            return False
        return True

    # method for making a move
    def make_move(board, old_i, old_j, new_i, new_j, big_letterValue, queen_rowPos):
        letter = board[old_i][old_j][0]
        i_difference = old_i - new_i
        j_difference = old_j - new_j
        #checking if the diagonal places around the piece is B that is empty
        if i_difference == -2 and j_difference == 2:
            board[old_i + 1][old_j - 1] = "B"

        elif i_difference == 2 and j_difference == 2:
            board[old_i - 1][old_j - 1] = "B"

        elif i_difference == 2 and j_difference == -2:
            board[old_i - 1][old_j + 1] = "B"

        elif i_difference == -2 and j_difference == -2:
            board[old_i + 1][old_j + 1] = "B"

        #checking if piece has reached the queen row 
        if new_i == queen_rowPos:
            letter = big_letterValue
        board[old_i][old_j] = "B"
        board[new_i][new_j] = letter


    def game(self):
        print("##### CHECKERS GAME START ####")
        print("\nYou can QUIT at any time by pressing 'q'.\n")
        print("ENJOY THE GAME!\n")
        # asking for player 1 name
        while True:
            self.name_player1 = input("\nEnter Player 1 Name: ")
            # checking for invalid inputs
            if self.name_player1 == "":
                print("Invalid input!")
            else:
                break
        # asking for player 2 name
        while True:
            self.name_player2 = input("\nEnter Player 2 Name: ")
            # checking for invalid inputs
            if self.name_player2 == "":
                print("Invalid input!")
            else:
                break
        # asking to begin the game
        while True:
            begin = input("\nBegin Game Play(Y/N): ")
            # if Yes creating a file with file name of player1, player2 name and the date and time  
            if begin == "Y" or begin == "y":
                self.file_name=f"{self.name_player1}_{self.name_player2}_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%p')}.txt "
                with open("sample.txt", "w") as fs:
                    fs.write("\nCHECKERS GAME STARTED\n")
                os.rename("sample.txt",self.file_name)
                break
            # if NO still it creates a file and appends game end
            elif begin == "N" or begin == "n":
                self.file_name=f"{self.name_player1}_{self.name_player2}_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%p')}.txt "
                with open("sample.txt", "w") as fs:
                    fs.write("\nCHECKERS GAME END\n")
                os.rename("sample.txt",self.file_name)
                print("Game end!")
                exit()
            # checking for invalid inputs
            elif begin == "":
                print("Illegal input!")
            else:

                print("Illegal input!")
            
        # asking if the jump is mandatory or no
        while True:

            input_jump = input("\nFirst, we need to know, is jumping mandatory?[Y/n]: ")
            if input_jump == "Y" or input_jump == "y":
                self.mandatory_jumping = True
                break
            elif input_jump == "N" or input_jump == "n":
                self.mandatory_jumping = False
                break
            elif input_jump == "q" or input_jump == "Q":
                print("QUIT before the game even started.")
                exit()
            else:
                print("Illegal input!")
        
        while True:
            # for starting the game priting initial matrix in the terminal as well as in the file created 
            self.print_matrixGrid()
            with open(self.file_name, "a") as fileText:
                for item in self.matrix:
                    fileText.write(f"{item}\n")
                fileText.close()
            # player1 turn
            if self.player1_turn is True:
                print(f'\n{self.name_player1}`s turn (Player 1s pieces are "x".)')
                self.get_input_player1()
            # player2 turn
            else:
                print(f'\n{self.name_player2}`s turn (Player 2s pieces are "o")')
                self.get_input_player2()
            # checking if player1 has any pieces let
            if self.pieces_player1 == 0:
                self.print_matrixGrid()
                print("You have no pieces left.\nYOU LOSE!")
                exit()
            # checking if player2 has any pieces else
            elif self.pieces_player2 == 0:
                self.print_matrixGrid()
                print("You have no pieces left.\nYOU LOSE!")
                exit()
                 
            # if its player1 turns, player2 cannot play and vice versa 
            self.player1_turn = not self.player1_turn
            self.player2_turn = not self.player2_turn


if __name__ == '__main__':
    # class Board in variable main1
    main1 = Board()
    # calling the method game in board class
    main1.game()