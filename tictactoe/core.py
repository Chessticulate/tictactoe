"""Core Tic Tac Toe Game Logic Module"""
import json
from enum import Enum
from typing import Iterator, Optional
from pydantic import validate_call, conlist


class PlayerEnum(str, Enum):
    """Player Enum Type"""

    X: str = "X"
    O: str = "O"


class TicTacToe:
    """Tic Tac Toe Game Class"""

    @validate_call
    def __init__(
        self,
        whomst: PlayerEnum = PlayerEnum.X,
        board: Optional[list[list[str]]] = None,
    ):
        self._whomst = whomst
        self._board = (
            board if board else [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        )
        self._over = False
        self._tie = False
        self._winner = False

        self.evaluate()

    @validate_call
    def __getitem__(self, row: int) -> list[str]:
        return self._board[row]

    def __iter__(self) -> Iterator[list[str]]:
        return iter(self._board)

    def __str__(self) -> str:
        return (
            "-----\n".join(["|".join(row) + "\n" for row in self])
            + self.whomst
            + "'s turn"
        )

    @property
    def whomst(self) -> str:
        """String representing the player whose turn is next."""
        return self._whomst

    @property
    def winner(self) -> str:
        """String representing the winner (if the game has ended)."""
        return self._winner

    @property
    def over(self) -> bool:
        """Game over flag."""
        return self._over

    @property
    def tie(self) -> bool:
        """Indicate whether game ended in a tie."""
        return self._tie

    def to_json(self) -> str:
        """Returns a JSON representation of the game."""
        return json.dumps(
            {
                "board": self._board,
                "whomst": self._whomst,
            }
        )

    @validate_call
    @classmethod
    def from_json(cls, json_str: str) -> "TicTacToe":
        """Creates a TicTacToe instance from a given JSON string."""
        kwargs = json.loads(json_str)
        return cls(**kwargs)

    @validate_call
    def _check_path(self, path: conlist(str, min_length=3, max_length=3)) -> bool:
        """Checks if a given path contains a win."""
        other = PlayerEnum.O if self._whomst == PlayerEnum.X else PlayerEnum.X
        return " " not in path and other not in path

    def evaluate(self) -> bool:
        """Check for win or tie game."""
        if self._over:
            return True

        # check rows and columns
        for i in range(3):
            row = self[i]
            col = [_row[i] for _row in self]
            if self._check_path(row) or self._check_path(col):
                self._over = True
                self._winner = self._whomst
                return True

        # check diagonals
        from_top_left = [self[i][i] for i in range(3)]
        from_top_right = [self[i][2 - i] for i in range(3)]
        if self._check_path(from_top_left) or self._check_path(from_top_right):
            self._over = True
            self._winner = self._whomst
            return True

        # check if there are any spaces left
        if " " not in [col for col in row for row in self]:
            self._over = True
            self._tie = True
            return True

        return False

    @validate_call
    def move(self, location: conlist(int, min_length=2, max_length=2)) -> bool:
        """Executes a move given an x/y coordinate pair."""
        if self._over:
            raise ValueError("The game is over")

        col, row = location
        if self[row][col] != " ":
            raise ValueError("Space is not free")

        # do the move
        self[row][col] = self._whomst

        # check for end game
        if self.evaluate():
            return True

        # flip player turn
        if self._whomst == PlayerEnum.X:
            self._whomst = PlayerEnum.O
        else:
            self._whomst = PlayerEnum.X

        return False
