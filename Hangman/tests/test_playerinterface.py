from Modules.playerinterface import PlayerInterface
from unittest.mock import patch, call, MagicMock
import sqlite3

def test_promptUser():
    with patch('builtins.input') as mock_input, \
         patch('Modules.playerinterface.PlayerInterface.get_database_connection', return_value=MagicMock()) as mock_connect:
        pi = PlayerInterface()
        pi.promptUser()
        mock_connect.assert_called_once()
        mock_input.assert_called_once_with("Hello Player, Enter your Username: ")


def test_getUserName_existing_user(capsys):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ('test_user',)
    pi = PlayerInterface()
    pi.getUserName(mock_cursor, 'test_user')
    mock_cursor.execute.assert_called_with("SELECT player_name FROM scores WHERE player_name = ?", ('test_user',))
    assert mock_cursor.execute.call_count == 1
    assert mock_cursor.fetchone.call_count == 1
    captured = capsys.readouterr()
    assert captured.out == "Welcome back, test_user!\n"

def test_getUserName_new_user(capsys):
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = None
    pi = PlayerInterface()
    pi.getUserName(mock_cursor, 'new_user')
    mock_cursor.execute.assert_called_with("INSERT INTO scores (player_name, score) VALUES (?, ?)", ('new_user', 0))
    assert mock_cursor.execute.call_count == 2
    assert mock_cursor.fetchone.call_count == 1
    captured = capsys.readouterr()
    assert captured.out == "Username created successfully. Welcome, new_user!\n"    
    

def test_hangman_list_length():
    pi = PlayerInterface()
    assert len(pi.hangmanList()) == 10

def test_display_hangman():
    pi = PlayerInterface()
    for i in range(10):
        assert isinstance(pi.displayHangman(i), str)


def test_display_guessed_letters():
    pi = PlayerInterface()
    secret_word = "TEST"
    guessed_letters = ['T', 'E']
    display = pi.displayGuessedLetters(secret_word, guessed_letters)
    assert display == "T E _ T"

def test_secret_word_length():
    pi = PlayerInterface()
    secret_word = "TEST"
    assert pi.secretWordLength(secret_word) == 4

@patch('builtins.input', return_value='a')
def test_get_user_guess_letter(mock_input):
    pi = PlayerInterface()
    assert pi.getUserGuessLetter() == 'a'


def test_user_guess():
    with patch('builtins.input') as mock_input:
        pi = PlayerInterface()
        pi.getUserGuessLetter()
        mock_input.assert_called_once_with("Enter a letter: ")

@patch('builtins.input', side_effect=['y', 'Y', 'n', 'N'])
def test_playGameAgain(mock_input):
    pi = PlayerInterface()
    assert pi.playGameAgain() == True
    assert pi.playGameAgain() == True
    assert pi.playGameAgain() == False
    assert pi.playGameAgain() == False

    # Check if the correct prompt is displayed
    mock_input.assert_any_call("Do you want to play again? Press y: ")