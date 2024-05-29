# Word Hunt Game
This is a word hunt game that I created using Python.
In this game, you will have a 10x10 grid filled with letters and a word search list.
You can click-drag over the letters to form words where letters are connected in any direction.
The minimum number of letters per word is three.
If you find a word from the list, it will be highlighted in the grid.
If you find a word that is not in the list, you will get credit for a bonus word.
You win the game by finding all the words in the list.

## *Placeholder for Running Instructions*

## Features In Progress:
- Add opacity so that overlapping words are more obvious/clear.
- Add a counter on the screen that will count how many words have been found.
- Track which words have been found so the same word cannot be added to the score twice or be re-highlighted.
- Add text popups to say when words are invalid, have already been found, or are too short.
- If a word from the list is found, strike through the word and change font color to gray.
- Add "End Game" button and final popup with stats and message.
- Add home screen with options to start game and view instructions.
- Make title of game fun and colorful.

## Features to be added when game is functional:
- Change the word occurance chances/options.
- Change it so that there is an Original mode (with word search and bonuses), and a ZEN mode that does not give a word search list at all but does checks to make sure the user has not found all possible words (no words will stay highlighted in this mode). Make sure to add the button options before the grid appears.
- Add mode that allows a timed edition with a score per word depending on the size of the word (bigger the word, higher the value of the word). No words will stay highlighted.
- Add difficulty settings that can either change the word difficulty or the grid size/max word length.
- Add a themed challenge mode that has a list of words per theme at random. If Original mode, the theme will be displayed at the top. If Secret mode, there will be no word search list showing to the user, but the words in the secret themed list will be highlighted when found. At the end, the theme will be displayed or the user needs to guess the theme. Bonus words are still allowed in this mode. 
- Customization options for the grid and word search list such as colors, custom words, font, etc.

## Current bugs:
- There are way too many of the same letters on the grid and in sequence.
- Search functions to verify that all the words are in the grid don't work.
- Words from the search list can be found in multiple locations/variations.
- Words can be the same color next to each other.