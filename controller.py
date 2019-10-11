# Xiaoxiang "Steven" Liu
# xl2948@columbia.edu
# Columbia SEAS, Class of 2022

import random
from tkinter import Tk, Canvas
from pynput.mouse import Listener

def create_board(width, height):
    board = [[None] * width for i in range(height)]
    return board


def bury_mines(gameboard, n):
    # Create an empty list
    list = []
    # Create n random, distinct numbers in the range of [0, width * height]
    while (len(list) < n):
        num = random.randint(0, len(gameboard) * len(gameboard[0]) - 1)
        for item in list:
            while (num == item):
                num = random.randint(1, len(gameboard) * len(gameboard[0]) - 1)
        # print(num)
        list.append(num)
    # Bury the mines
    for item in list:
        x = int(item / len(gameboard[0]))
        y = int(item % len(gameboard[0]))
        # print(x, " ", y)
        gameboard[x][y] = -1


def get_mine_count(gameboard, x, y):
    # print(x, " ", y)
    mine = 0
    if x > 0 and y > 0 and gameboard[x - 1][y - 1] == -1:
        mine += 1
    if x > 0 and gameboard[x - 1][y] == -1:
        mine += 1
    if x > 0 and y < len(gameboard[0]) - 1 and gameboard[x - 1][y + 1] == -1:
        mine += 1
    if y > 0 and gameboard[x][y - 1] == -1:
        mine += 1
    if y < len(gameboard[0]) - 1 and gameboard[x][y + 1] == -1:
        mine += 1
    if y > 0 and x < len(gameboard) - 1 and gameboard[x + 1][y - 1] == -1:
        mine += 1
    if x < len(gameboard) - 1 and gameboard[x + 1][y] == -1:
        mine += 1
    if x < len(gameboard) - 1 and y < len(gameboard[0]) - 1 and gameboard[x + 1][y + 1] == -1:
        mine += 1
    return mine


def print_mines(gameboard):
    for i in range(len(gameboard)):
        for j in range(len(gameboard[i])):
            if gameboard[i][j] == -1:
                print("*", end=" ")
            else:
                print(".", end=" ")
        print()  # New line


def print_board(gameboard):
    for i in range(len(gameboard)):
        for j in range(len(gameboard[i])):
            print(get_mine_count(gameboard, i, j), end=" ")
        print()


def print_status(gameboard):
    for i in range(len(gameboard)):
        for j in range(len(gameboard[i])):
            if gameboard[i][j] is None:
                print("X", end=" ")
            else:
                print(gameboard[i][j], end=" ")
        print()


def user_view(gameboard):
    print("   ", end=" ")
    for k in range(len(gameboard[0])):
        print(k, end=" ")
    print()
    print("   ", end=" ")
    for k in range(len(gameboard[0])):
        print("_", end=" ")
    print()
    for i in range(len(gameboard)):
        print(i, "|", end=" ")
        for j in range(len(gameboard[i])):
            if gameboard[i][j] == 0:
                print(".", end=" ")
            elif gameboard[i][j] == -1 or gameboard[i][j] is None:
                print("?", end=" ")
            else:
                print(gameboard[i][j], end=" ")
        print()


def final_view(gameboard):
    print("   ", end=" ")
    for k in range(len(gameboard[0])):
        print(k, end=" ")
    print()
    print("   ", end=" ")
    for k in range(len(gameboard[0])):
        print("_", end=" ")
    print()
    for i in range(len(gameboard)):
        print(i, "|", end=" ")
        for j in range(len(gameboard[i])):
            if gameboard[i][j] == 0:
                print(".", end=" ")
            elif gameboard[i][j] == -1:
                print("*", end=" ")
            elif gameboard[i][j] == None:
                print(".", end=" ")
            else:
                print(gameboard[i][j], end=" ")
        print()


def mark(gameboard, x, y):
    gameboard[x][y] = -2


def uncover_board(gameboard, x, y):
    if gameboard[x][y] == -1:
        lose = True
    if gameboard[x][y] is None and get_mine_count(gameboard, x, y) == 0:
        gameboard[x][y] = 0
        # print("P2", gameboard[x][y])
        if x > 0 and y > 0 and gameboard[x - 1][y - 1] is None:
            uncover_board(gameboard, x - 1, y - 1)
        if x > 0 and gameboard[x - 1][y] is None:
            uncover_board(gameboard, x - 1, y)
        if x > 0 and y < len(gameboard[0]) - 1 and gameboard[x - 1][y + 1] is None:
            uncover_board(gameboard, x - 1, y + 1)
        if y > 0 and gameboard[x][y - 1] is None:
            uncover_board(gameboard, x, y - 1)
        if y < len(gameboard[0]) - 1 and gameboard[x][y + 1] is None:
            uncover_board(gameboard, x, y + 1)
        if y > 0 and x < len(gameboard) - 1 and gameboard[x + 1][y - 1] is None:
            uncover_board(gameboard, x + 1, y - 1)
        if x < len(gameboard) - 1 and gameboard[x + 1][y] is None:
            uncover_board(gameboard, x + 1, y)
        if x < len(gameboard) - 1 and y < len(gameboard[0]) - 1 and gameboard[x + 1][y + 1] is None:
            uncover_board(gameboard, x + 1, y + 1)
    if get_mine_count(gameboard, x, y) > 0 and gameboard[x][y] != -1:
        gameboard[x][y] = get_mine_count(gameboard, x, y)


def change(gameboard):
    gameboard[0][1] = -2


def check_won(gameboard):
    for i in range(len(gameboard)):
        for j in range(len(gameboard[i])):
            if gameboard[i][j] is None:
                return False
    return True


def game(height, width, n):
    status = 0
    list = create_board(height, width)
    bury_mines(list, n)
    user_view(list)
    while not check_won(list):
        # print_status(list)
        a = input("Input horizontal position: ")
        b = input("Input vertical position: ")
        while int(a) < 0 or int(a) >= len(list) or int(b) < 0 or int(b) >= len(list[0]) or (list[int(a)][int(b)] is not None and list[int(a)][int(b)] != -1):
            print("Illegal.")
            a = input("Input horizontal position: ")
            b = input("Input vertical position: ")
        if list[int(a)][int(b)] == -1:
            print("You lost!")
            status = -1
            break
        uncover_board(list, int(a), int(b))
        user_view(list)
    final_view(list)
    if status == -1:
        print("You lose!")
    else:
        print("You win!")

def display_board(board, canvas):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None or board[i][j] == -1:
                canvas.create_rectangle(j * 25, i * 25, j * 25 + 25, i * 25 + 25, fill="grey")
            if board[i][j] is not None and board[i][j] != -1:
                canvas.create_rectangle(j * 25, i * 25, j * 25 + 25, i * 25 + 25, fill="white")
                canvas.create_text(j * 25 + 10, i * 25 + 10, text = board[i][j])
    if check_won(board):
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == -1:
                    canvas.create_text(j * 25 + 10, i * 25 + 10, text="*")
                    canvas.create_rectangle(0, 0, 100, 25, fill="green")
                    canvas.create_text(50, 10, text="YOU WIN!!!", fill="white")
                    canvas.unbind("<Button-1>")

def run():
    status = 0
    board = create_board(10, 10)
    bury_mines(board, 4)
    root = Tk()
    root.wm_title("Minesweeper")
    heightpxls = len(board[0]) * 25
    widthpxls = len(board) * 25
    canvas = Canvas(master=root, height=heightpxls, width=widthpxls)
    canvas.pack()
    notice = Canvas(master=root, height=100, width=50)
    display_board(board, canvas)
    def handle_click(event):
        print("clicked at", int(event.y/25), int(event.x/25))
        uncover_board(board, int(event.y/25), int(event.x/25))
        user_view(board)
        print_status(board)
        display_board(board, canvas)
        if board[int(event.y/25)][int(event.x/25)] == -1:
            canvas.create_rectangle(0, 0, 100, 25, fill="red")
            canvas.create_text(50, 10, text="YOU LOST!!", fill="white")
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] == -1:
                        canvas.create_text(j * 25 + 10, i * 25 + 10, text="*")
            canvas.unbind("<Button-1>")
    canvas.bind("<Button-1>", handle_click)
    print_status(board)
    root.mainloop()


#Run the game
run()