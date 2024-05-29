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

def get_random_directions():
    """Get a shuffled list of directions for random placement."""
    directions = DIRECTIONS.copy()
    random.shuffle(directions)
    return directions

def can_place_word(grid, word, start_row, start_col):
    """Check if a word can be placed on the grid starting at the specified position."""
    for direction in get_random_directions():
        if try_place_word(grid, word, start_row, start_col, direction):
            return True
    return False

def try_place_word(grid, word, start_row, start_col, direction):
    """Attempt to place a word in a specific direction."""
    dr, dc = direction
    row, col = start_row, start_col
    for letter in word:
        if not (0 <= row < len(grid) and 0 <= col < len(grid)):
            return False
        if grid[row, col] != '' and grid[row, col] != letter:
            return False
        row += dr
        col += dc
    return True

def place_word(grid, word, start_row, start_col):
    """Place a word on the grid starting at the specified position."""
    for direction in get_random_directions():
        if try_place_word(grid, word, start_row, start_col, direction):
            dr, dc = direction
            row, col = start_row, start_col
            for letter in word:
                grid[row, col] = letter
                row += dr
                col += dc
            return

def place_words(grid, words):
    """Place multiple words on the grid and return the list of successfully placed words."""
    random.shuffle(words)
    placed_words = []
    for word in words:
        placed = False
        attempts = 0
        while not placed and attempts < 100:
            start_row, start_col = random.randint(0, len(grid) - 1), random.randint(0, len(grid) - 1)
            if can_place_word(grid, word, start_row, start_col):
                place_word(grid, word, start_row, start_col)
                placed = True
                placed_words.append(word)
                logging.debug(f"Placed word: {word} at ({start_row}, {start_col})")
            attempts += 1
    fill_empty_squares(grid)
    return placed_words

def fill_empty_squares(grid):
    """Fill empty squares with random lowercase letters."""
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row, col] == '':
                grid[row, col] = chr(random.randint(97, 122))  # Fill with random lowercase letter

def verify_word_placement(grid, words):
    """Verify that all placed words can be found on the grid."""
    for word in words:
        if not find_word_on_grid(grid, word):
            logging.error(f"Word not found: {word}")
            return False
    return True

def find_word_on_grid(grid, word):
    """Find a word on the grid."""
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row, col] == word[0]:  # Check if the first letter matches
                if search_from_cell(grid, word, row, col):
                    return True
    return False

def search_from_cell(grid, word, start_row, start_col):
    """Search for the word starting from a specific cell."""
    for direction in DIRECTIONS:
        if search_in_direction(grid, word, start_row, start_col, direction):
            return True
    return False

def search_in_direction(grid, word, start_row, start_col, direction):
    """Search for the word in a specific direction."""
    dr, dc = direction
    row, col = start_row, start_col
    for letter in word:
        if not (0 <= row < len(grid) and 0 <= col < len(grid)):
            return False
        if grid[row, col] != letter:
            return False
        row += dr
        col += dc
    return True

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
    if not verify_word_placement(grid, placed_words):
        logging.error("Failed to place all words correctly.")
        return jsonify(error="Failed to place words correctly"), 500
    grid = grid.tolist()
    return jsonify(grid=grid, words=placed_words, word_list=word_list)

if __name__ == '__main__':
    app.run(debug=True)
