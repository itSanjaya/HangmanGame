import sqlite3

class PlayerInterface:
    def __init__(self):
        self.db_path = 'Database/hangman'

    def get_database_connection(self):
        return sqlite3.connect(self.db_path)

    def promptUser(self):
        with self.get_database_connection() as conn:
            cursor = conn.cursor()
            userInput = input("Hello Player, Enter your Username: ")
            self.getUserName(cursor, userInput)
            return userInput

    def getUserName(self, cursor, userInput):
        cursor.execute("SELECT player_name FROM scores WHERE player_name = ?", (userInput,))
        if cursor.fetchone():
            print(f"Welcome back, {userInput}!")
        else:
            defaultScore = 0
            cursor.execute("INSERT INTO scores (player_name, score) VALUES (?, ?)", (userInput, defaultScore))
            print(f"Username created successfully. Welcome, {userInput}!")

    def hangmanList(self):
        hangmanDraw = [
        r"""
        ---------------
                      |
                      |
                      |
                      |
                      |
                      |
        """,
        r"""
        ---------------
              |       |
                      |
                      |
                      |
                      |
                      |
        """,
        r"""
        ---------------
              |       |
              O       |
                      |
                      |
                      |
                      |
        """,
        r"""
        ---------------
              |       |
              O       |
              |       |
                      |
                      |
                      |
        """,
        r"""
        ---------------
              |       |
              O       |
             \|       |
                      |
                      |
                      |
        """,
        r"""
        ---------------
              |       |
              O       |
             \|/      |
                      |
                      |
                      |
        """,
        r"""
        ---------------
              |       |
              O       |
             \|/      |
              |       |
                      |
                      |
        """,
        r"""
        ---------------
              |       |
              O       |
             \|/      |
              |       |
              |       |
                      |
        """,
        r"""
        ---------------
              |       |
              O       |
             \|/      |
              |       |
              |       |
             /        |
        """,
        r"""
        ---------------
              |       |
              O       |
             \|/      |
              |       |
              |       |
             / \      |
        """
        ]

        return hangmanDraw


    def displayHangman(self, wrongGuesses):
        hangman = self.hangmanList()
        return hangman[wrongGuesses]


    def displayGuessedLetters(self, secretWord, guessedLetters):
        return " ".join([letter if letter in guessedLetters else "_" for letter in secretWord.upper()])

    def secretWordLength(self, secretWord):
        return len(secretWord)

    def getUserGuessLetter(self):
        return input("Enter a letter: ")

    def playGameAgain(self):
        playAgain = input("Do you want to play again? Press y: ")
        if playAgain is not None and playAgain.lower() == 'y':
            return True
        return False
