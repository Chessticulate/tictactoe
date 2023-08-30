"""Tic Tac Toe 'Main' entry point"""
from tictactoe.core import TicTacToe

game = TicTacToe()

while True:
    print(game)
    move = input("enter your move:")
    try:
        x, y = move.split(",")
        x = int(x)
        y = int(y)
    except ValueError:
        print("expecting move format 'x,y'")
        continue
    try:
        game.move((x, y))
    except ValueError as ve:
        print(ve.args[0])
