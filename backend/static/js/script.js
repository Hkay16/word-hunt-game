let isMouseDown = false;
let selectedCells = [];
let dragLines = [];
let wordColors = {};
const pastelColors = ["orange", "blue", "red", "purple", "green", "brown"];

document.addEventListener('DOMContentLoaded', () => {
    createGrid(10);
    generateNewGrid();

    document.addEventListener('mousedown', (event) => {
        if (event.target.classList.contains('cell')) {
            isMouseDown = true;
            clearSelection();
            selectCell(event.target);
            updateDragLines();
        }
    });

    document.addEventListener('mouseup', () => {
        isMouseDown = false;
        checkSelectedWord();
    });

    document.addEventListener('mouseover', (event) => {
        if (isMouseDown && event.target.classList.contains('cell') && !selectedCells.includes(event.target)) {
            const lastCell = selectedCells[selectedCells.length - 1];
            if (isAdjacent(lastCell, event.target)) {
                selectCell(event.target);
                updateDragLines();
            }
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
        cell.dataset.row = Math.floor(i / size);
        cell.dataset.col = i % size;
        cell.dataset.colors = ''; // Store colors for blending
        gridElement.appendChild(cell);
    }
    const foundSvgElement = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    foundSvgElement.id = 'found-lines';
    foundSvgElement.style.position = 'absolute';
    foundSvgElement.style.top = '0';
    foundSvgElement.style.left = '0';
    foundSvgElement.style.width = '100%';
    foundSvgElement.style.height = '100%';
    foundSvgElement.style.pointerEvents = 'none';
    gridElement.appendChild(foundSvgElement);

    const dragSvgElement = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    dragSvgElement.id = 'drag-lines';
    dragSvgElement.style.position = 'absolute';
    dragSvgElement.style.top = '0';
    dragSvgElement.style.left = '0';
    dragSvgElement.style.width = '100%';
    dragSvgElement.style.height = '100%';
    dragSvgElement.style.pointerEvents = 'none';
    gridElement.appendChild(dragSvgElement);
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
            wordColors = assignColorsToWords(data.words);
            clearFoundWordHighlights();
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
    selectedCells.forEach(cell => cell.classList.remove('selected', 'dragging'));
    selectedCells = [];
    clearDragLines();
}

function clearFoundWordHighlights() {
    const cells = document.querySelectorAll('.cell');
    cells.forEach(cell => {
        cell.classList.remove('found', 'orange', 'blue', 'red', 'purple', 'green', 'brown', 'multiple');
        cell.style.backgroundColor = '';
        cell.dataset.colors = ''; // Clear stored colors
    });

    const foundSvgElement = document.getElementById('found-lines');
    while (foundSvgElement.firstChild) {
        foundSvgElement.removeChild(foundSvgElement.firstChild);
    }

    const dragSvgElement = document.getElementById('drag-lines');
    while (dragSvgElement.firstChild) {
        dragSvgElement.removeChild(dragSvgElement.firstChild);
    }

    const wordsListElement = document.getElementById('words-to-find');
    const words = wordsListElement.getElementsByTagName('li');
    for (let word of words) {
        word.style.textDecoration = '';
        word.style.color = '';
    }
}

function selectCell(cell) {
    cell.classList.add('selected', 'dragging');
    selectedCells.push(cell);
}

function checkSelectedWord() {
    const selectedWord = selectedCells.map(cell => cell.textContent).join('');
    const validWord = isValidWord(selectedWord);
    if (validWord) {
        selectedCells.forEach(cell => {
            cell.classList.add('found');
            cell.style.backgroundColor = '';
            cell.classList.add(wordColors[selectedWord]);
            updateCellColors(cell, wordColors[selectedWord]);
        });
        keepDragLinesAsFound(selectedWord);
        strikeThroughWord(selectedWord, wordColors[selectedWord]);
    }
    selectedCells.forEach(cell => cell.classList.remove('dragging'));
    clearSelection();
}

function isValidWord(word) {
    const wordsListElement = document.getElementById('words-to-find');
    const words = Array.from(wordsListElement.getElementsByTagName('li')).map(li => li.textContent);
    return words.includes(word);
}

function updateDragLines() {
    clearDragLines();
    const svgElement = document.getElementById('drag-lines');
    const gridRect = document.getElementById('grid').getBoundingClientRect();
    for (let i = 0; i < selectedCells.length - 1; i++) {
        const start = selectedCells[i].getBoundingClientRect();
        const end = selectedCells[i + 1].getBoundingClientRect();
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        line.setAttribute('x1', start.left + start.width / 2);
        line.setAttribute('y1', start.top + start.height / 2);
        line.setAttribute('x2', end.left + end.width / 2);
        line.setAttribute('y2', end.top + end.height / 2);
        line.setAttribute('stroke', 'black');
        line.setAttribute('stroke-width', '2');
        svgElement.appendChild(line);
        dragLines.push(line);
    }
}

function keepDragLinesAsFound(word) {
    const foundSvgElement = document.getElementById('found-lines');
    const dragSvgElement = document.getElementById('drag-lines');
    const lines = Array.from(dragSvgElement.querySelectorAll('line'));
    const colorClass = wordColors[word];
    const color = getComputedStyle(document.documentElement).getPropertyValue(`--${colorClass}`);
    lines.forEach(line => {
        line.setAttribute('stroke', color); // Use the color of the found word
        line.setAttribute('opacity', '0.5');
        foundSvgElement.appendChild(line);
    });
    clearDragLines();
}

function strikeThroughWord(word, colorClass) {
    const wordsListElement = document.getElementById('words-to-find');
    const words = wordsListElement.getElementsByTagName('li');
    for (let li of words) {
        if (li.textContent === word) {
            li.style.textDecoration = 'line-through';
            li.style.color = getComputedStyle(document.documentElement).getPropertyValue(`--${colorClass}`);
        }
    }
}

function clearDragLines() {
    const svgElement = document.getElementById('drag-lines');
    while (svgElement.firstChild) {
        svgElement.removeChild(svgElement.firstChild);
    }
    dragLines = [];
}

function isAdjacent(cell1, cell2) {
    const row1 = parseInt(cell1.dataset.row);
    const col1 = parseInt(cell1.dataset.col);
    const row2 = parseInt(cell2.dataset.row);
    const col2 = parseInt(cell2.dataset.col);

    const rowDiff = Math.abs(row1 - row2);
    const colDiff = Math.abs(col1 - col2);

    return (rowDiff <= 1 && colDiff <= 1);
}

function assignColorsToWords(words) {
    const wordColors = {};
    words.forEach(word => {
        let availableColors = pastelColors.slice();
        for (let char of word) {
            for (let overlappingWord in wordColors) {
                if (overlappingWord.includes(char)) {
                    availableColors = availableColors.filter(color => color !== wordColors[overlappingWord]);
                }
            }
        }
        wordColors[word] = availableColors[Math.floor(Math.random() * availableColors.length)];
    });
    return wordColors;
}

function updateCellColors(cell, colorClass) {
    const existingColors = cell.dataset.colors ? cell.dataset.colors.split(',') : [];
    if (!existingColors.includes(colorClass)) {
        existingColors.push(colorClass);
        cell.dataset.colors = existingColors.join(',');

        if (existingColors.length > 1) {
            cell.classList.add('multiple');
            cell.style.backgroundColor = blendColors(existingColors.map(c => getComputedStyle(document.documentElement).getPropertyValue(`--${c}`)));
        } else {
            cell.classList.add(colorClass);
            cell.style.backgroundColor = getComputedStyle(document.documentElement).getPropertyValue(`--${colorClass}`);
        }
    }
}

function blendColors(colors) {
    const blend = colors.reduce((prev, curr) => {
        const prevColor = parseColor(prev);
        const currColor = parseColor(curr);
        const blendedColor = {
            r: Math.floor((prevColor.r + currColor.r) / 2),
            g: Math.floor((prevColor.g + currColor.g) / 2),
            b: Math.floor((prevColor.b + currColor.b) / 2),
            a: (prevColor.a + currColor.a) / 2
        };
        return `rgba(${blendedColor.r}, ${blendedColor.g}, ${blendedColor.b}, ${blendedColor.a})`;
    });
    return blend;
}

function parseColor(color) {
    const rgba = color.replace(/^rgba?\(|\s+|\)$/g, '').split(',');
    return {
        r: parseInt(rgba[0], 10),
        g: parseInt(rgba[1], 10),
        b: parseInt(rgba[2], 10),
        a: parseFloat(rgba[3] || 1)
    };
}
