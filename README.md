
# HANGMAN

## How to run project

1. Go to Hangman directory.
    ```
    cd Hangman
    ```
2. Create virtual enviroment and run it:
    ```
    python -m venv .venv
    source .venv/Scripts/activate
    ```
3. Install requirements from requirements.txt file:
    ```
    pip install -r requirements.txt
    ```
4. Install and run MongoDB on Docker:
    ```
    docker run -d -p 27017:27017 --name example-mongo mongo:latest
    ```
5. Run application:
    ```
    python app/app.py
    ```

It will run on http://127.0.0.1:5000


## Task requirements
Full task (maximum score 10):

Create a Hangman Game (GUI/terminal version). https://www.youtube.com/watch?v=leW9ZotUVYo

- Maximum guess attempts: 10.
- Maximum wrong guesses: 6.
- Ability to guess a word or a letter. If a guess is incorrect, user loses 1 life.
- If user has 0 guesses (lifes) left, game is lost. (Give options to see all time results or start new game)
- Ability to guess the word.

REQUIREMENTS: 
- Create a new GITHUB project, virtual env, README, .gitignore, etc.
- Use OOP structures (classes, inheritance, dataclasses, modules) to construct game backend logic.
- For a front end part you can use CLI, but Flask applicaton is preferible. 
- Create user registration (name,surname, email),store it using SQL database.
- Use Mongo DB to store all necessary game data.
- At least one of the system part (front-end/back end) should be dockerized.
- Use type annotations, error handling thoughout the code.
- Use a logging library to log out information (terminal and files).
- Unit tests to cover most important functionality.
- After the game session, show a table with user information: games played today , games won/lost today, guesses made.

 
Nice to have:
 - All system parts should be dockerized
 - Shell script to run the program automatically
 - Show TOP 10 performances of all accounts (create a button to see that table from game panel) 
 - music sounds on good/bad guesses.