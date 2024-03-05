import turtle

# Set up screen
screen = turtle.Screen()
screen.setup(width=600, height=600)
screen.title("Tic Tac Toe")
screen.bgcolor("lightblue")

# Create turtle for drawing
pen = turtle.Turtle()
pen.speed(0)  # Set speed to fastest
pen.pensize(4)
pen.hideturtle()

# Define game variables
board = [[None for _ in range(3)] for _ in range(3)]
current_player = "X"  # Initialize current_player

# Draw the game board
def draw_board():
    pen.penup()
    pen.goto(-150, 150)
    pen.pendown()
    for _ in range(2):
        pen.forward(300)
        pen.right(90)
        pen.forward(300)
        pen.right(90)

# Check for a winner
def check_winner():
    for row in board:
        if all(cell == "X" for cell in row):
            return "X"
        if all(cell == "O" for cell in row):
            return "O"
    for col in range(3):
        if all(board[row][col] == "X" for row in range(3)):
            return "X"
        if all(board[row][col] == "O" for row in range(3)):
            return "O"
    if all(board[i][i] == "X" for i in range(3)) or all(board[i][2 - i] == "X" for i in range(3)):
        return "X"
    if all(board[i][i] == "O" for i in range(3)) or all(board[i][2 - i] == "O" for i in range(3)):
        return "O"
    return None

# Handle player clicks
def handle_click(x, y):
    global game_over  # Declare game_over as global (alternative: pass it as an argument)
    row = int(y // 100)
    col = int(x // 100)
    if board[row][col] is None and not game_over:
        pen.penup()
        pen.goto(col * 100 - 50, row * 100 - 50)
        pen.write(current_player, align="center", font=("Arial", 80, "normal"))
        board[row][col] = current_player
        winner = check_winner()
        if winner:
            game_over = True
            pen.goto(0, 0)
            pen.write(f"{winner} wins!", align="center", font=("Arial", 40, "normal"))
        elif all(cell is not None for row in board for cell in row):
            game_over = True
            pen.goto(0, 0)
            pen.write("It's a tie!", align="center", font=("Arial", 40, "normal"))
        else:
            current_player = "O" if current_player == "X" else "X"

# Start the game
draw_board()
game_over = False  # Initialize game_over here
screen.onclick(handle_click)
screen.mainloop()