from flask import Flask, render_template, jsonify
import random
import numpy as np
import nltk
import logging

# Download word list from nltk
nltk.download('words')
from nltk.corpus import words

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Filter the word list to include only words with 3 or more letters and convert to lowercase
word_list = [word.lower() for word in words.words() if len(word) >= 3]

DIRECTIONS = [
    (0, 1),  # Right
    (1, 0),  # Down
    (1, 1),  # Down-Right
    (-1, 1), # Up-Right
    (-1, -1),# Up-Left
    (1, -1), # Down-Left
    (0, -1), # Left
    (-1, 0)  # Up
]

def create_empty_grid(size):
    """Create an empty grid of the given size."""
    return np.full((size, size), '', dtype=str)

def get_random_direction():
    """Get a random direction for placing the next letter."""
    return random.choice(DIRECTIONS)

def can_place_letter(grid, row, col, used_cells):
    """Check if a letter can be placed on the grid at the specified position."""
    return (0 <= row < len(grid) and 0 <= col < len(grid[0])
            and (row, col) not in used_cells
            and grid[row, col] == '')

def place_words(grid, words):
    """Place multiple words on the grid and return the list of successfully placed words."""
    random.shuffle(words)
    placed_words = []
    for word in words:
        placed = False
        attempts = 0
        while not placed and attempts < 100:
            start_row, start_col = random.randint(0, len(grid) - 1), random.randint(0, len(grid) - 1)
            if try_place_word(grid, word, start_row, start_col):
                placed_words.append(word)
                placed = True
                logging.debug(f"Placed word: {word} starting at ({start_row}, {start_col})")
            attempts += 1
        if not placed:
            logging.warning(f"Failed to place word: {word}")
    fill_empty_squares(grid)
    return placed_words

def try_place_word(grid, word, start_row, start_col):
    """Attempt to place a word on the grid starting at the specified position."""
    for _ in range(8):  # Try up to 8 starting directions to place the word
        used_cells = set()
        row, col = start_row, start_col
        positions = [(row, col)]
        if not can_place_letter(grid, row, col, used_cells):
            continue
        used_cells.add((row, col))

        for letter in word[1:]:
            placed = False
            for _ in range(8):  # Try up to 8 directions to place the next letter
                direction = get_random_direction()
                new_row, new_col = row + direction[0], col + direction[1]
                if can_place_letter(grid, new_row, new_col, used_cells):
                    row, col = new_row, new_col
                    positions.append((row, col))
                    used_cells.add((row, col))
                    placed = True
                    break
            if not placed:
                break
        
        if len(positions) == len(word):
            for index, (row, col) in enumerate(positions):
                grid[row, col] = word[index]
            return True

    return False

def fill_empty_squares(grid):
    """Fill empty squares with random lowercase letters."""
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row, col] == '':
                grid[row, col] = chr(random.randint(97, 122))  # Fill with random lowercase letter

#TODO: Search functions are not working. Need to fix them.
#def verify_word_placement(grid, words):
#    """Verify that all placed words can be found on the grid."""
#    for word in words:
#        if not find_word_on_grid(grid, word):
#            logging.error(f"Word not found: {word}")
#            return False
#    return True

#def find_word_on_grid(grid, word):
#    """Find a word on the grid."""
#    for row in range(len(grid)):
#        for col in range(len(grid[row])):
#            if grid[row, col] == word[0]:  # Check if the first letter matches
#                if search_from_cell(grid, word, row, col):
#                    return True
#    return False

#def search_from_cell(grid, word, start_row, start_col):
#    """Search for the word starting from a specific cell."""
#    for direction in DIRECTIONS:
#        if search_in_direction(grid, word, start_row, start_col, direction):
#            return True
#    return False

#def search_in_direction(grid, word, start_row, start_col, direction):
#    """Search for the word in a specific direction using backtracking."""
#    dr, dc = direction
#    row, col = start_row, start_col
#    path = [(row, col)]
#    for letter in word[1:]:
#        row += dr
#        col += dc
#        if not (0 <= row < len(grid) and 0 <= col < len(grid)):
#            return False
#        if grid[row, col] != letter:
#            return False
#        path.append((row, col))
#    return True

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/new_grid')
def new_grid():
    """Generate a new word search grid and return it as JSON."""
    grid_size = 10
    num_words = random.randint(23, 90)
    selected_words = random.sample(word_list, num_words)
    grid = create_empty_grid(grid_size)
    placed_words = place_words(grid, selected_words)
    #if not verify_word_placement(grid, placed_words):
        #logging.error("Failed to place all words correctly.")
        #return jsonify(error="Failed to place words correctly"), 500
    grid = grid.tolist()
    return jsonify(grid=grid, words=placed_words, word_list=word_list)

if __name__ == '__main__':
    app.run(debug=True)
