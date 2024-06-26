
import unittest
from unittest.mock import MagicMock, patch
from Modules.leaderboard import Leaderboard
from app import HangmanGame 
from app import main

class TestHangmanGame(unittest.TestCase):
    def setUp(self):
        self.mock_leaderboard = MagicMock()
        self.mock_pi = MagicMock()
        self.mock_gl = MagicMock()
        self.hangman_game = HangmanGame(self.mock_leaderboard, self.mock_pi, self.mock_gl)

    def test_start_new_game_calls_prompt_user(self):
        """Test if starting a new game calls promptUser to get the current player."""
        self.hangman_game.start_new_game()
        self.mock_pi.promptUser.assert_called_once()
        
    def test_start_new_game_calls_start_new_game(self):
        """Test if starting a new game calls start_new_game on the game logic."""
        self.hangman_game.start_new_game()
        self.mock_gl.start_new_game.assert_called_once()

    def test_modules_instance(self):
            leaderboard_mock = MagicMock(spec=Leaderboard)
            player_interface_mock = MagicMock()
            game_logic_mock = MagicMock()

            game = HangmanGame(leaderboard_mock, player_interface_mock, game_logic_mock)

            self.assertIs(game.leaderboard, leaderboard_mock)
            self.assertIs(game.pi, player_interface_mock)
            self.assertIs(game.gl, game_logic_mock)
            
            self.assertEqual(game.current_player, None)           
        
if __name__ == "__main__":
    unittest.main()