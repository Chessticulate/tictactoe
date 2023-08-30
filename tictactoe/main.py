from typing import Tuple
from enum import Enum


class PlayerEnum(str, Enum):
    X: str = "X"
    O: str = "O"


class TicTacToe:
    def __init__(self):
        """
        This is a python constructor.
        Use this method to setup the initial state of the object.

        e.g.
        self.x = 1
        self.name = 'Stu'
        """
        self.letter = PlayerEnum.X
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        # TODO: define attributes that will contain the state of the board (hint: 2D array)

    def __str__(self):
        "This is the 'toString()' equivalent in python. This should return a string representation of the current game."
        return (
            "-----\n".join(["|".join(row) + "\n" for row in self.board])
            + self.letter
            + "'s turn"
        )

    def to_json(self) -> str:
        "Returns a JSON representation of the game."
        # TODO: can be done much later down the line

    def move(self, location: Tuple[int]) -> int:
        "Executes a move given an x/y coordinate pair."
        if not isinstance(location, tuple):
            raise TypeError("location must be a tuple")
        if len(location) != 2:
            raise ValueError("location must have exactly 2 integer values")
        if not isinstance(location[0], int) or not isinstance(location[1], int):
            raise TypeError("location must contain only integers")
        if location[0] < 0 or location[0] > 2 or location[1] < 0 or location[1] > 2:
            raise ValueError("location coordinates out of bounds")
        x, y = location
        if self.board[y][x] != " ":
            raise ValueError("space is not free")
        self.board[y][x] = self.letter
        if self.letter == PlayerEnum.X:
            self.letter = PlayerEnum.O
        else:
            self.letter = PlayerEnum.X
