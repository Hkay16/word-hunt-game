from flask import Flask, render_template, jsonify
import numpy as np
import nltk
import logging
import secrets

# Download word list from nltk
nltk.download('words')
from nltk.corpus import words

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Filter the word list to include only words with 3 or more letters and convert to lowercase
word_list = [word.lower() for word in words.words() if len(word) >= 3]

# Preference for word lengths
def select_words(num_words):
    selected_words = []
    while len(selected_words) < num_words:
        word = secrets.choice(word_list)
        length = len(word)
        if 5 <= length <= 7 and secrets.SystemRandom().random() < 0.7:
            selected_words.append(word)
        elif length < 5 and secrets.SystemRandom().random() < 0.2:
            selected_words.append(word)
        elif length > 7 and secrets.SystemRandom().random() < 0.1:
            selected_words.append(word)
    return selected_words

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
    return secrets.choice(DIRECTIONS)

def can_place_letter(grid, row, col, used_cells, letter):
    """Check if a letter can be placed on the grid at the specified position."""
    return (0 <= row < len(grid) and 0 <= col < len(grid[0])
            and (row, col) not in used_cells
            and (grid[row, col] == '' or grid[row, col] == letter))

def get_valid_directions(grid, row, col, letter, used_cells):
    """Get valid directions to place the next letter."""
    valid_directions = []
    for direction in DIRECTIONS:
        new_row, new_col = row + direction[0], col + direction[1]
        if can_place_letter(grid, new_row, new_col, used_cells, letter):
            valid_directions.append(direction)
    return valid_directions

def place_words(grid, words):
    """Place multiple words on the grid and return the list of successfully placed words."""
    secrets.SystemRandom().shuffle(words)
    placed_words = []
    for word in words:
        placed = False
        attempts = 0
        while not placed and attempts < 100:
            start_row, start_col = secrets.SystemRandom().randint(0, len(grid) - 1), secrets.SystemRandom().randint(0, len(grid) - 1)
            if try_place_word(grid, word, start_row, start_col):
                placed_words.append(word)
                placed = True
                logging.debug(f"Placed word: {word} starting at ({start_row}, {start_col})")
            attempts += 1
        if not placed:
            logging.warning(f"Failed to place word: {word}")
    return placed_words

def try_place_word(grid, word, start_row, start_col):
    """Attempt to place a word on the grid starting at the specified position."""
    for _ in range(8):  # Try up to 8 starting directions to place the word
        used_cells = set()
        row, col = start_row, start_col
        positions = [(row, col)]
        if not can_place_letter(grid, row, col, used_cells, word[0]):
            continue
        used_cells.add((row, col))

        for letter in word[1:]:
            placed = False
            valid_directions = get_valid_directions(grid, row, col, letter, used_cells)
            if not valid_directions:
                break
            for _ in range(8):  # Try up to 8 directions to place the next letter
                if secrets.SystemRandom().random() < 0.75 and any(grid[row + dr, col + dc] == letter for dr, dc in valid_directions):
                    direction = secrets.choice([d for d in valid_directions if grid[row + d[0], col + d[1]] == letter])
                else:
                    direction = secrets.choice(valid_directions)
                new_row, new_col = row + direction[0], col + direction[1]
                if can_place_letter(grid, new_row, new_col, used_cells, letter):
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
                grid[row, col] = chr(secrets.SystemRandom().randint(97, 122))  # Fill with random lowercase letter
            
# Commented out verification code for now
# def verify_word_placement(grid, words):
#     """Verify that all placed words can be found on the grid."""
#     for word in words:
#         if not find_word_on_grid(grid, word):
#             logging.error(f"Word not found: {word}")
#             return False
#     return True

# def find_word_on_grid(grid, word):
#     """Find a word on the grid."""
#     for row in range(len(grid)):
#         for col in range(len(grid[row])):
#             if grid[row, col] == word[0]:  # Check if the first letter matches
#                 if search_from_cell(grid, word, row, col):
#                     return True
#     return False

# def search_from_cell(grid, word, start_row, start_col):
#     """Search for the word starting from a specific cell."""
#     for direction in DIRECTIONS:
#         if search_in_direction(grid, word, start_row, start_col, direction):
#             return True
#     return False

# def search_in_direction(grid, word, start_row, start_col, direction):
#     """Search for the word in a specific direction using backtracking."""
#     dr, dc = direction
#     row, col = start_row, start_col
#     path = [(row, col)]
#     for letter in word[1:]:
#         row += dr
#         col += dc
#         if not (0 <= row < len(grid) and 0 <= col < len(grid)):
#             return False
#         if grid[row, col] != letter:
#             return False
#         path.append((row, col))
#     return True

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/api/new_grid')
def new_grid():
    """Generate a new word search grid and return it as JSON."""
    grid_size = 10
    num_words = secrets.SystemRandom().randint(15, 30)  # Adjusted to reduce word density
    selected_words = select_words(num_words)
    grid = create_empty_grid(grid_size)
    placed_words = place_words(grid, selected_words)
    fill_empty_squares(grid)
    
    # Include only half of the placed words in the search list
    search_words = secrets.SystemRandom().sample(placed_words, len(placed_words) // 2)

    grid = grid.tolist()
    return jsonify(grid=grid, words=search_words, word_list=word_list)

if __name__ == '__main__':
    app.run(debug=True)
