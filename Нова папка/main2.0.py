import tkinter as tk

from game import start_game, is_winning_combination, display_board, computer_move

# Розмір ігрового поля
SIZE = 3

# Символи гравців
PLAYER_SYMBOL = "X"
COMPUTER_SYMBOL = "O"

# Створення вікна
window = tk.Tk()
window.title("Хрестики нулики")

# Створення ігрового поля
board_frame = tk.Frame(window)
board_frame.pack()

# Створення кнопок для ігрового поля
buttons = []
for i in range(SIZE):
  for j in range(SIZE):
    button = tk.Button(board_frame, text=" ", width=4, height=2)
    button.grid(row=i, column=j)
    buttons.append(button)

# Функція оновлення візуального представлення ходу
def update_board(board):
  for i in range(SIZE):
    for j in range(SIZE):
      buttons[i * SIZE + j]["text"] = board[i * SIZE + j]

# Функція ходу гравця
def player_move(button):
  """
  Функція, що обробляє хід гравця.
  """
  button["text"] = PLAYER_SYMBOL
  board[buttons.index(button)] = PLAYER_SYMBOL
  is_winning_combination(board, PLAYER_SYMBOL)
  computer_move()

# Функція ходу комп'ютера
def computer_move():
  """
  Функція, що імітує хід комп'ютера.
  """
  move = random.choice([i for i in range(SIZE * SIZE) if buttons[i]["text"] == " "])
  buttons[move]["text"] = COMPUTER_SYMBOL
  board[move] = COMPUTER_SYMBOL
  is_winning_combination(board, COMPUTER_SYMBOL)

# Запуск гри
start_game()
update_board(board)

# Прив'язка функції ходу гравця до кнопок
for button in buttons:
  button["command"] = lambda button=button: player_move(button)

# Запуск циклу обробки подій
window.mainloop()
