import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    return False

def is_board_full(board):
    return all(cell != " " for row in board for cell in row)

def get_empty_positions(board):
    return [(row, col) for row in range(3) for col in range(3) if board[row][col] == " "]

def player_move(board):
    while True:
        try:
            row, col = map(int, input("Enter your move (row col): ").split())
            if board[row][col] == " ":
                return row, col
            else:
                print("That position is already taken. Try again.")
        except ValueError:
            print("Invalid input. Please enter row and column numbers separated by space.")
        except IndexError:
            print("Invalid row or column number. Please enter numbers between 0 and 2.")

def computer_move(board):
    empty_positions = get_empty_positions(board)
    return random.choice(empty_positions)

def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    print("Welcome to Tic-Tac-Toe!")
    print_board(board)

    while True:
        player_row, player_col = player_move(board)
        board[player_row][player_col] = "X"
        print_board(board)
        if check_winner(board, "X"):
            print("Congratulations! You win!")
            break
        if is_board_full(board):
            print("It's a tie!")
            break

        print("Computer's turn:")
        computer_row, computer_col = computer_move(board)
        board[computer_row][computer_col] = "O"
        print_board(board)
        if check_winner(board, "O"):
            print("Sorry, you lose. Try again!")
            break
        if is_board_full(board):
            print("It's a tie!")
            break

if __name__ == "__main__":
    main()
