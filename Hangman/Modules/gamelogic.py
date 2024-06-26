"""
Module: gamelogic

This module contains the implementation of the Hangman game logic.
It defines the GameLogic class, which handles the core game mechanics
such as selecting a secret word, processing user guesses, and determining
the game outcome. The GameLogic class provides methods for starting a new
game, guessing letters, resetting the game state, calculating scores,
and checking if the game is won or lost. Additionally, it includes helper
methods for incrementing wrong guesses and determining game outcome conditions.

"""

import random

class GameLogic:
    def __init__(self, word_list):
      self.word_list = word_list
      self.start_new_game()

    def start_new_game(self):
      self.secret_word = self.select_secret_word()
      self.guessed_letters = []
      self.wrong_guesses = 0
      self.max_guesses = 9

    def select_secret_word(self):
      return random.choice(self.word_list)

    def reset_game(self):
      self.start_new_game()


    def guess_letter(self, letter):
      if not letter.isalpha() or len(letter) > 1:
        return "Invalid input. Please enter a single letter."
      letter = letter.upper()

      if letter in self.guessed_letters:
        return "Letter already guessed."

      self.guessed_letters.append(letter)

      if letter not in self.secret_word.upper():
        self.increment_guesses()
        if self.is_lost():
          print(f"Wrong guess. No more guesses left. The word was {self.secret_word}.")
          return False
        else:
            return f"Wrong guess. You have {self.max_guesses - self.wrong_guesses} guesses left."

      if self.is_won():
        print("Congratulations! You've guessed the word correctly.")
        return True
      else:
        return "Correct guess. Keep going!"

    def increment_guesses(self):
      self.wrong_guesses += 1

    def is_won(self):
      return all(letter in self.guessed_letters for letter in self.secret_word.upper())

    def is_lost(self):
      return self.wrong_guesses >= self.max_guesses

    def calculate_score(self):
      if self.max_guesses - self.wrong_guesses == 0:
        return 0
      return 10
