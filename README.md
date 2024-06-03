# Word Hunt Game
This is a word hunt game that I created using Python.
In this game, you will have a 10x10 grid filled with letters and a word search list.
You can click-drag over the letters to form words where letters are connected in any direction.
The minimum number of letters per word is three.
If you find a word from the list, it will be highlighted in the grid.
If you find a word that is not in the list, you will get credit for a bonus word.
You win the game by finding all the words in the list.

## How to Run the Game:
1. Clone the Repository
2. Navigate to the Project Directory
3. Create a Virtual Environment:     
        ```python -m venv venv```
4. Activate the Virtual Environment:     
        On Windows: ```venv\Scripts\activate```     
        On macOS/Linux: ```source venv/bin/activate```
5. Install the Required Packages:     
        ```pip install -r requirements.txt``` 
7. Navigate to the backend folder:     
        ```cd backend``` 
9. Run the Flask Application:     
        ```python app.py``` 
11. Open your web browser and navigate to http://127.0.0.1:5000/ to start playing the game.

## Work In Progress:
- Fix Bugs with generating wordsearch grid: Occasionally words on the list will not be in the word search grid. There are way too many of the same letters on the grid and in sequence.
- Add a button next to the counter to show all bonus words that have been found in alphabetical order.
- Add text popups to say when words are invalid, have already been found, or are too short.
- Add "End Game" button and final popup with stats and message.
- Add home screen with options to start game and view instructions.
- Make title of game fun and colorful.
- Change word list container to not have scroll bar. Add a second column when necessary.
- Make word search list longer.
- Make words generated from smaller words?

## Features to be added when game is functional:
- Add web scraping to define the words found.
- Change the word occurance chances/options.
- Change it so that there is an Original mode (with word search and bonuses), and a ZEN mode that does not give a word search list at all but does checks to make sure the user has not found all possible words (no words will stay highlighted in this mode). Make sure to add the button options before the grid appears.
- Add mode that allows a timed edition with a score per word depending on the size of the word (bigger the word, higher the value of the word). No words will stay highlighted.
- Add difficulty settings that can either change the word difficulty or the grid size/max word length.
- Add a themed challenge mode that has a list of words per theme at random. If Original mode, the theme will be displayed at the top. If Secret mode, there will be no word search list showing to the user, but the words in the secret themed list will be highlighted when found. At the end, the theme will be displayed or the user needs to guess the theme. Bonus words are still allowed in this mode. 
- Customization options for the grid and word search list such as colors, custom words, font, etc.

## Current bugs:
- Highlight lines move off grid when moving window.
- Search functions to verify that all the words are in the grid don't work.
- Words from the search list can be found in multiple locations/variations.
- Words can be the same color next to each other.
- Occasionally a word will not be highlighted when found and the word will be crossed out in the list but stays black. May have a correlation to final words or last words in the list?
