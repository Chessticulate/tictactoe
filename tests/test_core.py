"""Test Module for tictactoe.core"""
from tictactoe.core import TicTacToe, PlayerEnum

JSON_STR_INIT = (
    '{"board": [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]], "history": [],'
    ' "whomst": "X", "game_over": false, "tie_game": false, "winner": null}'
)
JSON_STR_FEW_TURNS = (
    '{"board": [["X", " ", "O"], ["X", " ", " "], ["O", " ", " "]], "history": [],'
    ' "whomst": "X", "game_over": false, "tie_game": false, "winner": null}'
)
JSON_STR_O_WINS = (
    '{"board": [["O", "X", "X"], [" ", "O", "X"], [" ", " ", "O"]], "history": [],'
    ' "whomst": "X", "game_over": true, "tie_game": false, "winner": "O"}'
)


def test_tictactoe_initial_game_state():
    game = TicTacToe()
    assert game.whomst == PlayerEnum.X
    assert game.over == False
    assert game.tie == False
    assert game.winner == None
    for row in game:
        for col in row:
            assert col == PlayerEnum.NONE


def test_tictactoe_to_str():
    game = TicTacToe()
    assert str(game) == " | | \n-----\n | | \n-----\n | | \nX's turn"

    game[0][0] = PlayerEnum.X
    game._whomst = PlayerEnum.O
    assert str(game) == "X| | \n-----\n | | \n-----\n | | \nO's turn"

    game._over = game._tie = True
    assert "tie game!" in str(game)

    game._tie = False
    game._winner = PlayerEnum.X
    assert "X won!" in str(game)


def test_tictactoe_to_json():
    game = TicTacToe()
    assert game.to_json() == JSON_STR_INIT

    game[0][0] = game[1][0] = PlayerEnum.X
    game[0][2] = game[2][0] = PlayerEnum.O
    assert game.to_json() == JSON_STR_FEW_TURNS


def test_tictactoe_evaluate():
    game = TicTacToe()
    assert not game.evaluate()
    game._board = [
        [PlayerEnum.X, PlayerEnum.X, PlayerEnum.O],
        [PlayerEnum.O, PlayerEnum.O, PlayerEnum.X],
        [PlayerEnum.X, PlayerEnum.X, PlayerEnum.O],
    ]
    assert game.evaluate()
    assert game.over
    assert game.tie
    assert not game.winner

    game = TicTacToe()
    game._board = [
        [PlayerEnum.O, PlayerEnum.O, PlayerEnum.O],
        [PlayerEnum.X, PlayerEnum.X, PlayerEnum.O],
        [PlayerEnum.NONE, PlayerEnum.X, PlayerEnum.X],
    ]
    game._whomst = PlayerEnum.X
    assert game.evaluate()
    assert game.over
    assert not game.tie
    assert game.winner == PlayerEnum.O

    game = TicTacToe()
    game._board = [
        [PlayerEnum.X, PlayerEnum.O, PlayerEnum.O],
        [PlayerEnum.NONE, PlayerEnum.X, PlayerEnum.O],
        [PlayerEnum.NONE, PlayerEnum.X, PlayerEnum.X],
    ]
    game._whomst = PlayerEnum.O
    assert game.evaluate()
    assert game.over
    assert not game.tie
    assert game.winner == PlayerEnum.X

    game = TicTacToe()
    game._board = [
        [PlayerEnum.X, PlayerEnum.X, PlayerEnum.O],
        [PlayerEnum.O, PlayerEnum.O, PlayerEnum.X],
        [PlayerEnum.O, PlayerEnum.NONE, PlayerEnum.X],
    ]
    game._whomst = PlayerEnum.O
    assert game.evaluate()
    assert game.over
    assert not game.tie
    assert game.winner == PlayerEnum.X


def test_tictactoe_from_json():
    game = TicTacToe.from_json(JSON_STR_INIT)
    assert game.whomst == PlayerEnum.X
    assert not game.over
    assert not game.tie
    assert game.winner == None
    for row in game:
        for col in row:
            assert col == PlayerEnum.NONE

    game = TicTacToe.from_json(JSON_STR_O_WINS)
    assert game.whomst == PlayerEnum.X
    assert game.over
    assert not game.tie
    assert game.winner == PlayerEnum.O


def test_tictactoe_move():
    game = TicTacToe()
    assert game.move([0, 0]) == False
    assert game.whomst == PlayerEnum.O
    assert game.move([1, 1]) == False
    assert game.whomst == PlayerEnum.X
    assert game.move([0, 1]) == False
    assert game.move([1, 0]) == False
    assert game.move([0, 2]) == True
    assert game.over
    assert not game.tie
    assert game.winner == PlayerEnum.X


def test_tictactoe_undo():
    game = TicTacToe()
    game.move([1, 1])
    game.move([0, 0])
    game.move([0, 2])
    game.move([1, 0])
    game.move([2, 0])

    assert game.over
    assert game.winner == PlayerEnum.X
    assert len(game.history) == 5
    assert game.whomst == PlayerEnum.O

    assert game.undo()

    assert not game.over
    assert game.whomst == PlayerEnum.X
    assert len(game.history) == 4

    assert game.undo()

    assert len(game.history) == 3
    assert not game.over
    assert game.whomst == PlayerEnum.O

    assert game.undo()
    assert game.undo()
    assert game.undo()
    assert not game.undo()

    assert len(game.history) == 0
    assert game.whomst == PlayerEnum.X
