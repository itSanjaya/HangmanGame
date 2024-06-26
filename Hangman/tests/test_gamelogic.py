import pytest

from Modules.gamelogic import GameLogic

@pytest.fixture
def game_logic():
    return GameLogic(['HANGMAN', 'TEST'])

def test_start_new_game(game_logic):
    game_logic.start_new_game()
    assert game_logic.secret_word in ['HANGMAN', 'TEST']
    assert game_logic.guessed_letters == []
    assert game_logic.wrong_guesses == 0
    assert game_logic.max_guesses == 9

def test_reset_game(game_logic):
    game_logic.start_new_game()
    game_logic.guessed_letters = ['A', 'B', 'C']
    game_logic.wrong_guesses = 3
    game_logic.reset_game()
    assert game_logic.secret_word in ['HANGMAN', 'TEST']
    assert game_logic.guessed_letters == []
    assert game_logic.wrong_guesses == 0
    assert game_logic.max_guesses == 9


def test_guess_letter_correct(game_logic):
    secret_word = 'PYTHON'
    game_logic.secret_word = secret_word
    letter = 'P'
    assert game_logic.guess_letter(letter) == "Correct guess. Keep going!"
    assert letter in game_logic.guessed_letters
    assert game_logic.wrong_guesses == 0

def test_guess_letter_incorrect(game_logic):
    secret_word = 'PYTHON'
    game_logic.secret_word = secret_word
    letter = 'A'
    assert game_logic.guess_letter(letter) == f"Wrong guess. You have {game_logic.max_guesses - game_logic.wrong_guesses} guesses left."
    assert letter not in game_logic.secret_word
    assert game_logic.wrong_guesses == 1

def test_guess_letter_already_guessed(game_logic):
    secret_word = 'PYTHON'
    game_logic.secret_word = secret_word
    letter = 'P'
    assert game_logic.guess_letter(letter) == "Correct guess. Keep going!"
    assert game_logic.guess_letter(letter) == "Letter already guessed."

def test_invalid_input_single_digit(game_logic):
    assert game_logic.guess_letter('1') == "Invalid input. Please enter a single letter."

def test_invalid_input_special_char(game_logic):
    assert game_logic.guess_letter('!') == "Invalid input. Please enter a single letter."

def test_invalid_input_multiple_letters(game_logic):
    assert game_logic.guess_letter('AB') == "Invalid input. Please enter a single letter."

def test_win_condition_met(game_logic, capsys):
    for letter in set(game_logic.secret_word):
        game_logic.guess_letter(letter)
    assert game_logic.is_won()
    
    captured = capsys.readouterr()
    assert captured.out == "Congratulations! You've guessed the word correctly.\n"
    assert game_logic.is_won() == True

def test_guess_letter_game_won(game_logic):
    game_logic.secret_word = "ABCD"
    game_logic.max_guesses = 4    
    game_logic.guess_letter("A")
    game_logic.guess_letter("B")
    game_logic.guess_letter("C")
    result = game_logic.guess_letter("D")
    assert result == True

def test_loss_condition_met(game_logic,capsys):
    correct_letters = set(game_logic.secret_word.upper())
    all_letters = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    wrong_letters = list(all_letters - correct_letters)

    for letter in wrong_letters[:game_logic.max_guesses]:
        game_logic.guess_letter(letter)
    
    captured = capsys.readouterr()
    assert captured.out == f"Wrong guess. No more guesses left. The word was {game_logic.secret_word.upper()}.\n"
    assert game_logic.is_lost() == True
    
def test_guess_letter_game_lost(game_logic):
    game_logic.secret_word = "PYTHON"
    game_logic.max_guesses = 4    
    game_logic.guess_letter("A")
    game_logic.guess_letter("B")
    game_logic.guess_letter("C")
    result = game_logic.guess_letter("D")
    assert result == False

def test_calculate_score_max_wrong_guesses(game_logic):
    game_logic.start_new_game()
    game_logic.max_guesses = 5
    game_logic.wrong_guesses = 5
    assert game_logic.calculate_score() == 0, "Score should be 0 when all guesses are wrong"

def test_calculate_score_less_than_max_wrong_guesses(game_logic):
    game_logic.start_new_game()
    game_logic.max_guesses = 5
    game_logic.wrong_guesses = 3
    assert game_logic.calculate_score() == 10, "Score should be 10 when not all guesses are wrong"
