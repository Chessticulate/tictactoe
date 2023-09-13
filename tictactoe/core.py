"""Core Tic Tac Toe Game Logic Module"""
import json
from enum import Enum
from typing import Iterator, Optional, ForwardRef
from pydantic import validate_call, conlist


class PlayerEnum(str, Enum):
    """Player Enum Type"""

    X: str = "X"
    O: str = "O"
    NONE: str = " "


# TicTacToe.from_json() returns TicTacToe
TicTacToe = ForwardRef("TicTacToe")


class TicTacToe:
    """Tic Tac Toe Game Class"""

    @validate_call
    def __init__(
        self,
        whomst: PlayerEnum = PlayerEnum.X,
        board: Optional[
            conlist(
                conlist(str, min_length=3, max_length=3), min_length=3, max_length=3
            )
        ] = None,
        history: Optional[
            conlist(conlist(int, min_length=2, max_length=2), max_length=9)
        ] = None,
    ):
        self._whomst = whomst
        self._board = (
            board if board else [[PlayerEnum.NONE for j in range(3)] for i in range(3)]
        )
        self._history = history if history else []
        self._over = False
        self._tie = False
        self._winner = None

        self.evaluate()

    @validate_call
    def __getitem__(self, row: int) -> list[str]:
        return self._board[row]

    def __iter__(self) -> Iterator[list[str]]:
        return iter(self._board)

    def __str__(self) -> str:
        summary = f"{self._whomst}'s turn"
        if self._tie:
            summary = "tie game!"
        elif self._over:
            summary = f"{self._winner} won!"
        return "-----\n".join(["|".join(row) + "\n" for row in self]) + summary

    @property
    def whomst(self) -> str:
        """String representing the player whose turn is next."""
        return self._whomst

    @property
    def winner(self) -> Optional[str]:
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

    @property
    def history(self) -> conlist(conlist(int, min_length=2, max_length=2)):
        """Move history"""
        return self._history

    def to_json(self) -> str:
        """Returns a JSON representation of the game."""
        return json.dumps(
            {
                "board": self._board,
                "history": self._history,
                "whomst": self._whomst,
                "game_over": self._over,
                "tie_game": self._tie,
                "winner": self._winner,
            }
        )

    @classmethod
    @validate_call
    def from_json(cls, json_str: str) -> TicTacToe:
        """Creates a TicTacToe instance from a given JSON string."""
        kwargs = json.loads(json_str)
        return cls(
            whomst=kwargs.get("whomst"),
            board=kwargs.get("board"),
            history=kwargs.get("history"),
        )

    @validate_call
    def _check_path(self, path: conlist(str, min_length=3, max_length=3)) -> bool:
        """Checks if a given path contains a win."""
        return PlayerEnum.NONE not in path and len(set(path)) == 1

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
                self._winner = (
                    PlayerEnum.X if self._whomst == PlayerEnum.O else PlayerEnum.O
                )
                return True

        # check diagonals
        from_top_left = [self[i][i] for i in range(3)]
        from_top_right = [self[i][2 - i] for i in range(3)]
        if self._check_path(from_top_left) or self._check_path(from_top_right):
            self._over = True
            self._winner = (
                PlayerEnum.X if self._whomst == PlayerEnum.O else PlayerEnum.O
            )
            return True

        # check if there are any spaces left
        if PlayerEnum.NONE not in [col for col in row for row in self]:
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
        if self[row][col] != PlayerEnum.NONE:
            raise ValueError("Space is not free")

        # do the move
        self[row][col] = self._whomst
        self._history.append(location)

        # flip player turn
        if self._whomst == PlayerEnum.X:
            self._whomst = PlayerEnum.O
        else:
            self._whomst = PlayerEnum.X

        # check for end game
        if self.evaluate():
            return True

        return False

    def undo(self) -> bool:
        """Undo the previous move."""
        if len(self._history) == 0:
            return False
        move = self._history.pop()
        self[move[1]][move[0]] = PlayerEnum.NONE

        # flip player turn
        if self._whomst == PlayerEnum.X:
            self._whomst = PlayerEnum.O
        else:
            self._whomst = PlayerEnum.X

        self._tie = False
        self._over = False
        self._winner = None

        return True
