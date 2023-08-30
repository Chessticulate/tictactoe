"""Core Tic Tac Toe Game Logic Module"""
import json
from typing import Tuple
from enum import Enum


class PlayerEnum(str, Enum):
    """Player Enum Type"""
    X: str = "X"
    O: str = "O"


class TicTacToe:
    """Tic Tac Toe Game Class"""

    def __init__(self):
        """
        This is the TicTacToe class constructor.
        It is used to setup the initial state of the object.
        """
        self.whomst = PlayerEnum.X
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

    def __str__(self):
        """
        This is the 'toString()' equivalent in python.
        This returns a string representation of the current game.
        """
        return (
            "-----\n".join(["|".join(row) + "\n" for row in self.board])
            + self.whomst
            + "'s turn"
        )

    def to_json(self) -> str:
        """Returns a JSON representation of the game."""
        return json.dumps(
            {
                "board": self.board,
                "whomst": self.whomst,
            }
        )

    def move(self, location: Tuple[int]) -> int:
        """Executes a move given an x/y coordinate pair."""
        if not isinstance(location, tuple):
            raise TypeError("location must be a tuple")
        if len(location) != 2:
            raise ValueError("location must have exactly 2 integer values")
        if not isinstance(location[0], int) or not isinstance(location[1], int):
            raise TypeError("location must contain only integers")
        if location[0] < 0 or location[0] > 2 or location[1] < 0 or location[1] > 2:
            raise ValueError("location coordinates out of bounds")
        x, y = location  # pylint: disable=invalid-name
        if self.board[y][x] != " ":
            raise ValueError("space is not free")
        self.board[y][x] = self.whomst
        if self.whomst == PlayerEnum.X:
            self.whomst = PlayerEnum.O
        else:
            self.whomst = PlayerEnum.X
