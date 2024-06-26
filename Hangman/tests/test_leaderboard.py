import unittest
from unittest.mock import MagicMock, patch
from Modules.leaderboard import Leaderboard
import sqlite3
from unittest.mock import MagicMock, patch, call
from io import StringIO
from unittest.mock import patch, call
import unittest
from Modules.leaderboard import Leaderboard
import io
import sys


class TestLeaderboard(unittest.TestCase):
    @patch('Modules.leaderboard.sqlite3.connect')
    def test_insert_score_successfully(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        leaderboard = Leaderboard('dummy')
        leaderboard.insert_score('Player1', 100)
        mock_cursor.execute.assert_called_with(
            "INSERT INTO scores (player_name, score) VALUES (?, ?)",
            ('Player1', 100)
        )
             
    @patch('Modules.leaderboard.sqlite3.connect')
    def test_insert_score_db_connection_error(self, mock_connect):
        mock_connect.side_effect = sqlite3.Error("DB connection failed")
        leaderboard = Leaderboard('dummy')
        with self.assertRaises(sqlite3.Error):
            leaderboard.insert_score('Player1', 100)
   

    @patch('Modules.leaderboard.sqlite3.connect')
    def test_generate_leaderboard_with_exact_limit(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [('Player', i) for i in range(10)] 
        leaderboard = Leaderboard('dummy')
        leaderboard.generate_leaderboard()
        
    @patch('Modules.leaderboard.sqlite3.connect')
    def test_current_player_rank_not_in_top_10(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        top_players = [('Player' + str(i), i * 10) for i in range(1, 11)]
        all_players_scores_and_ranks = [('Player' + str(i), i * 10, i) for i in range(1, 16)]
        all_players_scores_and_ranks.append(('CurrentPlayer', 5, 16)) 
        mock_cursor.fetchall.side_effect = [top_players, all_players_scores_and_ranks]
        leaderboard = Leaderboard('dummy')
        leaderboard.generate_leaderboard(current_player='CurrentPlayer')
       
       
    @patch('Modules.leaderboard.sqlite3.connect')
    def test_handle_scores_with_tie_breaks(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [('Alice', 100), ('Bob', 100)]  # Assuming tie-breaking logic is in place
        leaderboard = Leaderboard('dummy')
        leaderboard.generate_leaderboard()
        
        
    @patch('Modules.leaderboard.sqlite3.connect')
    def test_current_player_rank_in_top_10(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        top_players = [('Player' + str(i), i * 10) for i in range(1, 11)]
        all_players_scores_and_ranks = [('Player' + str(i), i * 10, i) for i in range(1, 16)]
        all_players_scores_and_ranks.append(('CurrentPlayer', 50, 5))  # Assuming CurrentPlayer is in 5th place
        mock_cursor.fetchall.side_effect = [top_players, all_players_scores_and_ranks]
        leaderboard = Leaderboard('dummy')
        leaderboard.generate_leaderboard(current_player='CurrentPlayer')
    
    
    @patch('Modules.leaderboard.sqlite3.connect')
    def test_sql_query_format_for_leaderboard(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        leaderboard = Leaderboard('test_db')
        leaderboard.generate_leaderboard()
        expected_sql = " ".join("SELECT player_name, SUM(score) AS total_score FROM scores GROUP BY player_name ORDER BY total_score DESC LIMIT 10".split())
        actual_sql = " ".join(mock_cursor.execute.call_args[0][0].split())
        
        self.assertEqual(actual_sql, expected_sql)
        
    @patch('Modules.leaderboard.sqlite3.connect')
    def test_current_player_rank_logic(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.side_effect = [
            [('Player1', 300)],  
            [('Player1', 300, 1), ('CurrentPlayer', 250, 11)]  
        ]
        leaderboard = Leaderboard('test_db')
        leaderboard.generate_leaderboard(current_player='CurrentPlayer')


    @patch('Modules.leaderboard.sqlite3.connect')
    def test_display_logic_for_players_around_top_10(self, mock_connect):
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        top_players = [('Player' + str(i), i * 10) for i in range(1, 11)]
        all_players_scores_and_ranks = [('Player' + str(i), i * 10, i) for i in range(1, 12)]
        mock_cursor.fetchall.side_effect = [top_players, all_players_scores_and_ranks]
        leaderboard = Leaderboard('dummy')
        leaderboard.generate_leaderboard(current_player='Player11')
    
    @patch('Modules.leaderboard.sqlite3.connect')
    def test_handle_exception_during_score_insertion(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.execute.side_effect = sqlite3.Error("DB insert failed")
        leaderboard = Leaderboard('test_db')
        with self.assertRaises(sqlite3.Error):
            leaderboard.insert_score('Player1', 100)

    @patch('Modules.leaderboard.sqlite3.connect', side_effect=sqlite3.Error)
    def test_leaderboard_connection_failure_raises_exception(self, mock_connect):
        leaderboard = Leaderboard('test_db')
        with self.assertRaises(sqlite3.Error):
            leaderboard.connection()

    def test_leaderboard_init_with_invalid_db_raises_exception(self):
        with self.assertRaises(ValueError) as context:
            Leaderboard(None)
        self.assertIn("Database cannot be None or empty", str(context.exception))
        
        
    @patch('Modules.leaderboard.sqlite3.connect')
    def test_sql_query_executed_correctly(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        leaderboard = Leaderboard('dummy_db')
        leaderboard.generate_leaderboard()
        actual_sql_call = mock_cursor.execute.call_args[0][0]
        expected_sql = "SELECT player_name, SUM(score) AS total_score FROM scores GROUP BY player_name ORDER BY total_score DESC LIMIT 10".replace(' ', '')
        actual_sql = ''.join(actual_sql_call.split())
        self.assertEqual(actual_sql, expected_sql)

    def test_init_with_empty_string_database_raises_value_error(self):
        with self.assertRaises(ValueError) as context:
            Leaderboard("")
        self.assertEqual("Database cannot be None or empty.", str(context.exception))
        
    
    def test_db_initialization(self):
        test_db_name = 'test_db.sqlite'
        leaderboard = Leaderboard(test_db_name)
        self.assertEqual(leaderboard.db, test_db_name,
                         "The db attribute should be correctly assigned the provided database name.")

    @patch('Modules.leaderboard.sqlite3.connect')
    def test_connection_method_uses_correct_db(self, mock_connect):
        test_db_name = 'test_db.sqlite'
        leaderboard = Leaderboard(test_db_name)
        try:
            conn = leaderboard.connection()
        except Exception as e:
            self.fail(f"Unexpected exception during connection: {e}")
        mock_connect.assert_called_with(test_db_name)
        
if __name__ == '__main__':
    unittest.main()

