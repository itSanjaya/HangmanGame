from Modules import gamelogic
# import Modules.playerinterface as playerinterface
from Modules.leaderboard import Leaderboard
from Modules import words
from Modules import playerinterface

class HangmanGame:
    def __init__(self, leaderboard, player_interface, game_logic):
        self.leaderboard = leaderboard
        self.pi = player_interface
        self.gl = game_logic
        self.current_player = None

    def start_new_game(self):
        self.current_player = self.pi.promptUser()
        self.gl.start_new_game()

    def play_round(self):
        print("Welcome to Hangman!\n")
        self.start_new_game()

        print(self.pi.displayHangman(self.gl.wrong_guesses))
        print(f"The length of the word is {self.pi.secretWordLength(self.gl.secret_word)}")
        print(f"Word: {self.pi.displayGuessedLetters(self.gl.secret_word, self.gl.guessed_letters)}")

        while True:
            letter = self.pi.getUserGuessLetter()
            result = self.gl.guess_letter(letter)
            print(self.pi.displayHangman(self.gl.wrong_guesses))
            print(f"Word: {self.pi.displayGuessedLetters(self.gl.secret_word, self.gl.guessed_letters)}")
            print(result)
            if result in [True, False]:
                break
        
        score = self.gl.calculate_score()
        self.leaderboard.insert_score(self.current_player, score)
        self.leaderboard.generate_leaderboard(self.current_player)
        self.gl.reset_game()
    def run(self):
        while True:
            self.play_round()
            if not self.pi.playGameAgain():
                print("Thanks for playing Hangman!")
                break

def main():
    db_path = 'Database/hangman'
    leaderboard = Leaderboard(db_path)
    pi = playerinterface.PlayerInterface()
    gl = gamelogic.GameLogic(words.retrieve_all_words())
    game = HangmanGame(leaderboard, pi, gl)
    game.run()

if __name__ == '__main__':
    main()

