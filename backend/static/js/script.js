let isMouseDown = false;
let selectedCells = [];
let wordList = [];

document.addEventListener('DOMContentLoaded', () => {
    createGrid(10);
    generateNewGrid();

    document.addEventListener('mousedown', (event) => {
        if (event.target.classList.contains('cell')) {
            isMouseDown = true;
            clearSelection();
            event.target.classList.add('selected');
            selectedCells.push(event.target);
        }
    });

    document.addEventListener('mouseup', () => {
        isMouseDown = false;
        checkSelectedWord();
    });

    document.addEventListener('mouseover', (event) => {
        if (isMouseDown && event.target.classList.contains('cell') && !selectedCells.includes(event.target)) {
            event.target.classList.add('selected');
            selectedCells.push(event.target);
        }
    });
});

function createGrid(size) {
    const gridElement = document.getElementById('grid');
    gridElement.style.gridTemplateColumns = `repeat(${size}, 1fr)`;
    for (let i = 0; i < size * size; i++) {
        const cell = document.createElement('div');
        cell.classList.add('cell');
        cell.id = `cell-${i}`;
        gridElement.appendChild(cell);
    }
}

function populateGrid(grid) {
    for (let row = 0; row < grid.length; row++) {
        for (let col = 0; col < grid[row].length; col++) {
            const cell = document.getElementById(`cell-${row * grid.length + col}`);
            cell.textContent = grid[row][col];
        }
    }
}

function generateNewGrid() {
    fetch('/api/new_grid')
        .then(response => response.json())
        .then(data => {
            populateGrid(data.grid);
            displayWords(data.words);
            wordList = data.word_list;
        });
}

function displayWords(words) {
    const wordsListElement = document.getElementById('words-to-find');
    wordsListElement.innerHTML = '';
    words.forEach(word => {
        const li = document.createElement('li');
        li.textContent = word;
        wordsListElement.appendChild(li);
    });
}

function clearSelection() {
    selectedCells.forEach(cell => cell.classList.remove('selected'));
    selectedCells = [];
}

function checkSelectedWord() {
    const selectedWord = selectedCells.map(cell => cell.textContent).join('');
    const validWord = isValidWord(selectedWord);
    if (validWord) {
        selectedCells.forEach(cell => cell.classList.add('found'));
    }
    clearSelection();
}

function isValidWord(word) {
    return wordList.includes(word.toLowerCase());
}
