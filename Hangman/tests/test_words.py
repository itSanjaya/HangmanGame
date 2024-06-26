from unittest.mock import MagicMock, patch, call
from Modules.words import insert_words_to_database
from Modules.words import retrieve_all_words
from Modules.words import create_connection

database_path = 'Database/hangman'


@patch('Modules.words.sqlite3.connect')
def test_create_connection(mock_connect):
    # Return a MagicMock object, to simulate the connection
    mock_connect.return_value = MagicMock()

    # Call function to be tested
    conn = create_connection()

    # Assert that sqlite3.connect was called with the path
    mock_connect.assert_called_once_with(database_path)

    # Assert that the returned object is the mock connection object (what is expected)
    assert conn == mock_connect.return_value, "create_connection should return a mock connection object"


@patch('Modules.words.sqlite3.connect')
def test_insert_words(mock_connect):
    # Mock the connection and the cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    
    # Return a MagicMock object, to simulate the connection
    mock_connect.return_value = mock_conn

    mock_conn.cursor.return_value = mock_cursor

    # The word to be inserted
    words_to_insert = ["apple"]

    # Call function to be tested
    insert_words_to_database(words_to_insert)

    # Assert that sqlite3.connect was called with the path
    mock_connect.assert_called_once_with(database_path)
    
    # Assert the cursor.execute() method was called correctly
    calls = [call("INSERT INTO Words(word) VALUES(?)", (word,)) for word in words_to_insert]
    
    # cursor.execute() should be called once for each word in the list
    mock_cursor.execute.assert_has_calls(calls, any_order=True)

    # Assert that commit was called on the connection
    mock_conn.commit.assert_called_once()


@patch('Modules.words.sqlite3.connect')
def test_retrieve_all_words(mock_connect):
    # Mock the connection and the cursor
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    # Mock the return value
    mock_cursor.fetchall.return_value = [("apple",), ("banana",), ("cherry",)]

    # Return a MagicMock object, to simulate the connection
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Call function to be tested
    fetched_words = retrieve_all_words()

    # Assert that sqlite3.connect was called with the path 
    mock_connect.assert_called_once_with(database_path)
    
    # Assert the cursor.execute() method was called correctly
    mock_cursor.execute.assert_called_once_with("SELECT word FROM Words")
    
    # Assert that the returned values match what is expected (the array of words)
    assert fetched_words == ["apple", "banana", "cherry"], "The function should return the list [apple, banana, cherry]"


