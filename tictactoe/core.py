"""Core Tic Tac Toe Game Logic Module"""
import json
from enum import Enum
from pydantic import validate_call


class PlayerEnum(str, Enum):
    """Player Enum Type"""

    X: str = "X"
    O: str = "O"


class TicTacToe:
    """Tic Tac Toe Game Class"""

    @validate_call
    def __init__(self, whomst: Optional[PlayerEnum] = None, board: Optional[list[list[str]]] = None):
        """
        This is the TicTacToe class constructor.
        It is used to setup the initial state of the object.
        """
        self.whomst = next_turn if next_turn else PlayerEnum.X
        self.board = board if board else [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

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

    @classmethod
    def from_json(cls, json_str: str) -> TicTacToe:
        """Creates a TicTacToe instance from a given JSON string."""
        kwargs = json.loads(json_str)
        return cls(**kwargs)

    def move(self, location: tuple[int]) -> int:
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
