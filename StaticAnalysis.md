# Task 1:  Errors/Warnings reported by each tool and The Category Names

## Pylint

[Pylint](https://pylint.org/) is a tool that checks for errors in Python code, tries to enforce a coding standard and looks for code smells. It reported around **300** errors/warnings in our [Hangman](/Hangman) folder which are mentioned in [Reports/Pylint](Reports/Pylint/pylint.txt) file. Most of these errors are  either `bad indentation` or `trailing whitespace` or `line too long`.

Installation `pip install pylint`

Run `pylint Hangman/`

In Pylint, the priority of a warning is not explicitly indicated within the warning message itself. However, the priority or severity of warnings could be categorized into different levels: High, Medium, Low, and Very Low based on conventions.

Pylint categorizes its messages into several categories: ` "C" indicates convention violations` , `"R" suggests opportunities for refactoring`,  `"W" highlights warnings or potential issues`, `"E" refers to Errors, indicating problems that may cause code execution failures`, and `"F" means Fatal errors, typically severe issues that prevent further analysis`. 

So, when you see messages like "C0301" or "R1705," the prefix letters denote the category of the message (Convention, Refactor, or Warning), and the numbers that follow provide specific identifiers for each message type within that category.

## Prospector

[Prospector](https://prospector.landscape.io/en/master/) is a tool  to analyse Python code and output information about errors, potential problems, convention violations and complexity. It brings together the functionality of other Python analysis tools such as Pylint, pycodestyle, and McCabe complexity.  
It reported  **140** errors/warnings for our project which are mentioned in [Reports/Prospector](Reports/Prospector/prospector.txt) file. Most of these errors are related to `code formatting`.

Installation `pip install prospector`

Run `prospector` in the root of the project.
or 
Run `prospector--strictness veryhigh` for higher strictness. We have run prospector with very high strictness.

Prospector includes the functionality of other Python analysis tools such as Pylint and pycodestyle and it structures the output by classfying each case with a specific tool. 



## PyFlakes

[PyFlakes](https://pypi.org/project/pyflakes/) is a tool designed for checking Python code for errors and potential issues. Pyflakes focuses purely on the logical errors in the code, rather than stylistic issues. It does not provide a numeric or categoric severity level for its warnings, reflecting its design philosophy that focuses on improving the logical consistency of Python code without delving into style preferences.
It performs static analysis of Python programs without actually executing them. The errors generated after running pyflakes included a redefinition of unused variables, imported but unused modules, and f-string missing placeholders.

Installation: `pip install pyflakes`

Run: `find . -name '*.py' -exec pyflakes {} +`

Pyflakes does not categorize its messages into categories like conventions or refactoring opportunities. Instead, it straightforwardly reports problems related to the cleanliness and correctness of the code, such as:

- Redefinition of Unused: This warning occurs when you declare a variable or import a module that was already declared but not used, and then redeclare it again.
- Imported but Unused: Indicates that a module or function is imported but never used within the code.
- Local Variable Unused: Points out when a variable is defined (assigned a value) but not subsequently used in any operation.
- F-string Issues: Identifies f-strings that are either malformed or do not contain any expressions, which should either be corrected or converted into regular strings if no formatting is needed.

# Task 2
## Similarities
There were only 2 errors/warnings that all three tools reported. 

- **Warning: Unused Import**- All three tools (Prospector, Pylint, Pyflakes) report unused imports, showcasing their ability to identify and flag unnecessary code which can be cleaned up to enhance code quality. Examples include unused imports like sqlite3.Error and random in words.py.
- **Warning: f-string is missing placeholders/f-string-without-interpolation** - Each tool flagged f-strings that lack placeholders, which are unnecessary and can be corrected to standard strings if no formatting is required. An example is line 43 in gamelogic.py
  
## Differences
- Pylint - **Warning: Missing module docstring** - Flagged in Line 1 of words.py. Important for maintaining well-documented code with comments.
- Pyflakes - **Warning: local variable ‘conn’is assigned to but never used** - Flagged in Line 155 of test_leaderboard.py. Detected an issue directly related to code logic and usage errors.
- Prospector - **Warning: N813 / camelcase 'Modules.gamelogic' imported as lowercase 'gamelogic'** - Flagged in Line 1 of app.py. This indicates a sensitivity to Python naming conventions and import styles.

# Task 3
The modules identified as the most problematic because they have the most errors across each tool
- **leaderboard.py (21 errors in Prospector, 21 errors in Pylint, 4 errors in Pylint):**
  - **Common Issues:** Across all tools there are problems regarding code formatting, cleanliness and standard practices, which affect performance and readability.
  - **Pyflakes:** Flags unused imports and improper f-string usage.
  - **Prospector:** Reports unused imports, excessive blank lines, improper naming styles for arguments, lines that are too long, whitespace issues, and missing final newlines.
  - **Pylint:** Identifies trailing whitespaces, missing final newlines, and missing function docstrings, alongside highlighting f-strings without interpolation and unused imports.
- **gamelogic.py (39 errors in Prospector, 47 errors in Pylint, 1 error in Pylint):**
  - **Common Issues:** This module is heavily flagged for syntax errors and poor code structure.
  - **Pyflakes:** Highlights issues with improper f-string usage.
  - **Prospector:** Flags incorrect numbers of blank lines, bad indentation, long line lengths and unnecessary "else" clauses after "return" statements.
  - **Pylint:** Reports similar concerns with bad indentation and unnecessary "else" after "return". Also points out missing docstrings for modules, classes, and functions.
- **playerinterface.py (30 errors in Prospector, 29 errors in Pylint, 0 errors in Pylint)**
  - **Common Issues:** This module struggles with naming conventions and code structuring principles, affecting readability and maintainability.
  - **Pyflakes:** (No specific issues listed under Pyflakes for this module.)
  - **Prospector:** Reports insufficient blank lines, non-standard (function, argument & method) naming, lines that are too long and outdented continuation lines. Also highlights unnecessary "else" clauses after "return" and suggests simplifying if-statements.
  - **Pylint:** Flags long lines, missing docstrings and non-standard method names. Also flags the unnecessary use of "else" after "return" and suggests more concise if-statements.

# Task 4: Analyze 10 reported problems

#### 1. Consider-Using-From-Import 

* Category: R0402 (Refactor)
* Priority: Medium
* File Name: [App.py](Hangman/app.py)
* Line Number: 1, 2, 4
* Description: The warning suggests using 'from Modules import playerinterface' instead of importing the module as 'import Modules.playerinterface'.
* Characterization: This warning suggests a more concise and clearer way of importing the 'playerinterface' module, which enhances readability and maintains code clarity.
* Fix: To address the warning, I modified the import statement in 'Hangman\app.py' from: `import Modules.playerinterface` to `from Modules import playerinterface`.

#### 2. Missing module docstring

* Category: C0114 (Convention)
* Priority: Very Low
* File Name: [gamelogic.py](Hangman/Modules/gamelogic.py)
* Line Number: 1
* Description: The warning indicates that there's a missing module docstring in the gamelogic.py file.
* Characterization: While it doesn't directly affect the functionality of the code, it's a violation of Python coding standards. A missing module docstring can make it harder for other developers to understand the purpose of the module, hindering code readability and maintainability.
* Fix: To address the warning, I added a module docstring at the beginning of the gamelogic.py file. The docstring provides an overview of the module's purpose, contents, and functionality, as well as any other relevant information.

#### 3. Unused Import
* Category: W0611 (Warning)
* Priority: Low
* File Name: [words.py](Hangman/Modules/words.py)
* Line Number: 3
* Description: The warning indicates that the imported module "random" is unused.
* Characterization: This warning alerts that the module "random" is imported but not utilized anywhere in the module "words.py". While this import statement doesn't directly affect the functionality of the module, it adds unnecessary clutter to the codebase and might mislead other developers into thinking that the "random" module is relevant to the functionality of the code.
* Fix: To resolve the warning, I removed the unused import statement for the "random" module from the module "words.py". By removing unused imports, the code becomes cleaner, easier to read, and less prone to confusion. This action contributes to maintaining a tidy and efficient codebase, enhancing maintainability and collaboration within the development team.

#### 4. no-else-return
* Category: R1705 (Refactor)
* Priority: Low
* File Name: [playerinterface.py](Hangman/Modules/playerinterface.py)
* Line Number: 139
* Description: unnecessary else statement in
* Characterization: This warning suggests that the code includes an unnecessary "else" statement after a "return" statement in the file playerinterface.py. In Python, when a "return" statement is encountered, the function exits immediately, so any code after the "return" statement within the same block will not be executed. Including an "else" statement after a "return" statement can lead to redundant code 
* Fix: To address the warning, I removed the unnecessary "else" statement and de-indent the code inside it to align with the previous "if" statement.

#### 5. invalid-name
* Prospector: Pylint: invalid-name 
* File name: database.py
* Line Number: 3
* Description: The name "path" should be in all caps because it's a constant, which means it doesn't change.
* Characterization: This is a real issue because using all caps for constants makes it easier to see that they are important and shouldn't change.
* Fix: Change "path" to "PATH" to follow the rule for naming constants.

#### 6. Spaces at the beginning of the Line
* Prospector: PyCodeStyle: E111
* File name: gamelogic.py
* Line Number : 5
* Description: The spaces at the beginning of the line are not right. They should be multiples of four to keep the code clean and easy to read.
* Characterization: This is a problem because having consistent spacing helps anyone reading the code to understand it better.
* Fix: Adjust the spaces at the beginning of the line so they are multiples of four.

#### 7. Line is too long
* Prospector: PyCodeStyle: E501 
* File name: playerinterface.py
* Line Number : 23
* Description: This line is too long, more than the recommended 79 characters, which makes it hard to read, especially on smaller screens.
* Characterization: It's a real issue but not a big one. Keeping lines short makes the code easier to read on all devices.
* Fix: Make the line shorter by breaking it into smaller parts or using variables to hold some of the information.

#### 8. Unused import 
* Category: Unused import
* Priority: Low
* File: test_leaderboard.py
* Line number: 6
* Description: 'io.StringIO' imported but unused.
* Characterization: This warning indicates an unused import statement. It's an actual problem because it adds unnecessary clutter to the codebase.
* Fix: Remove the unused import statement.

#### 9. Missing placeholder in f-string
* Category: String formatting
* Priority: Medium
* File: gamelogic.py
* Line number: 43
* Description: The f-string is missing placeholders.
* Characterization: This is an actual problem as missing placeholders could lead to incorrect string formatting or potential runtime errors.
* Fix: Add a placeholder in the f-string or replace it with a regular string concatenation.

#### 10. Unused local variable
* Category: Unused variable
* Priority: Medium
* File: test_leaderboard.py
* Line number: 155
* Description: Local variable 'conn' is assigned to but never used.
* Characterization: This is an actual problem as it indicates inefficient code by assigning a value to a variable that is never used.
* Fix: Remove the assignment to 'conn' or use the variable if it serves a purpose.
