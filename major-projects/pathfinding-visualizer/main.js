import {bfsShortestPathGrid, getEdgeKey} from './algorithms.js';

// Configuration
const ROWS = 15;
const COLS = 20;
let startPoint = [3, 3];
let endPoint = [11, 16];
let wallCells = new Set();
let currentMode = 'wall'; // 'start' || 'end' || 'wall'
let isMouseDown = false;
let isVisualizing = false;

// DOM Elements
const gridContainer = document.getElementById('grid');
const infoText = document.getElementById('info-text');
const btnStartMode = document.getElementById('btn-start-mode');
const btnEndMode = document.getElementById('btn-end-mode');
const btnWallMode = document.getElementById('btn-wall-mode');
const btnVisualize = document.getElementById('btn-visualize');
const btnReset = document.getElementById('btn-reset');

/**
 * Creates the grid of cell elements.
 */
function createGrid() {
    gridContainer.style.gridTemplateColumns = `repeat(${COLS}, 1fr)`;
    gridContainer.innerHTML = '';
    
    for (let r=0; r<ROWS; r++) {
        for (let c=0; c<COLS; c++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.row = r;
            cell.dataset.col = c;
            
            // Set cell colors based on start/end positions
            if (r===startPoint[0] && c===startPoint[1]) {
                cell.classList.add('start');
            } else if (r===endPoint[0] && c===endPoint[1]) {
                cell.classList.add('end');
            }
            
            // Mouse Event Listeners
            cell.addEventListener('mousedown', () => handleMouseDown(r, c));
            cell.addEventListener('mouseenter', () => handleMouseEnter(r, c));
            gridContainer.appendChild(cell);
        }
    }
}

/**
 * Handles mouse down events on grid cells to draw start, end, or walls.
 * @param {number} r - The grid row index of the clicked cell.
 * @param {number} c - The grid column index of the clicked cell.
 */
function handleMouseDown(r, c) {
    if (isVisualizing) return;
    
    // Clear existing path visualization (if present)
    const pathCells = gridContainer.querySelectorAll('.cell.path');
    if (pathCells.length>0) {
        clearPath();
        setMode(currentMode);
    }
    
    const isStart = r===startPoint[0] && c===startPoint[1];
    const isEnd = r===endPoint[0] && c===endPoint[1];
    if (currentMode==='start') {
        if (!isEnd) {
            removeCellClass(startPoint[0], startPoint[1], 'start');
            startPoint = [r, c];
            addCellClass(r, c, 'start');
            wallCells.delete(`${r},${c}`);
            removeCellClass(r, c, 'wall');
        }
    } else if (currentMode==='end') {
        if (!isStart) {
            removeCellClass(endPoint[0], endPoint[1], 'end');
            endPoint = [r, c];
            addCellClass(r, c, 'end');
            wallCells.delete(`${r},${c}`);
            removeCellClass(r, c, 'wall');
        }
    } else if (currentMode==='wall') {
        if (!isStart && !isEnd) {
            isMouseDown = true;
            const key = `${r},${c}`;
            if (wallCells.has(key)) {
                wallCells.delete(key);
                removeCellClass(r, c, 'wall');
            } else {
                wallCells.add(key);
                addCellClass(r, c, 'wall');
            }
        }
    }
}

/**
 * Handles mouse enter events on grid cells to allow drawing walls by dragging.
 * @param {number} r - The grid row index of the entered cell.
 * @param {number} c - The grid column index of the entered cell.
 */
function handleMouseEnter(r, c) {
    if (!isMouseDown || currentMode!=='wall' || isVisualizing) return;
    const isStart = r===startPoint[0] && c===startPoint[1];
    const isEnd = r===endPoint[0] && c===endPoint[1];
    if (!isStart && !isEnd) {
        const key = `${r},${c}`;
        wallCells.add(key);
        addCellClass(r, c, 'wall');
    }
}

/**
 * Retrieves a cell's DOM element by its grid coordinates.
 * @param {number} r - The grid row index.
 * @param {number} c - The grid column index.
 * @returns {Element|null} The matching cell's DOM element, or null if not found.
 */
function getCellEl(r, c) {
    return gridContainer.querySelector(`[data-row="${r}"][data-col="${c}"]`);
}

/**
 * Adds a CSS class to a cell at the specified coordinates.
 * @param {number} r - The grid row index.
 * @param {number} c - The grid column index.
 * @param {string} className - The name of the CSS class to add.
 */
function addCellClass(r, c, className) {
    const el = getCellEl(r, c);
    if (el) el.classList.add(className);
}

/**
 * Removes a CSS class from a cell at the specified coordinates.
 * @param {number} r - The grid row index.
 * @param {number} c - The grid column index.
 * @param {string} className - The name of the CSS class to remove.
 */
function removeCellClass(r, c, className) {
    const el = getCellEl(r, c);
    if (el) el.classList.remove(className);
}

/**
 * Clears all path visual indicators from the grid.
 */
function clearPath() {
    const pathCells = gridContainer.querySelectorAll('.cell.path');
    pathCells.forEach(cell => cell.classList.remove('path'));
}

/**
 * Updates the current interaction mode, button highlights, and descriptions.
 * @param {string} mode - The interaction mode ('start' | 'end' | 'wall').
 */
function setMode(mode) {
    currentMode = mode;
    btnStartMode.classList.toggle('active', mode==='start');
    btnEndMode.classList.toggle('active', mode==='end');
    btnWallMode.classList.toggle('active', mode==='wall');
    
    if (mode==='start') {
        infoText.textContent = 'Click on the grid to place the start node.';
    } else if (mode==='end') {
        infoText.textContent = 'Click on the grid to place the end node.';
    } else {
        infoText.textContent = 'Click and drag on the grid to place walls.';
    }
}

// Stop painting walls
window.addEventListener('mouseup', () => {
    isMouseDown = false;
});

// Mode buttons event listeners
btnStartMode.addEventListener('click', () => setMode('start'));
btnEndMode.addEventListener('click', () => setMode('end'));
btnWallMode.addEventListener('click', () => setMode('wall'));

// Visualize shortest path using converted BFS
btnVisualize.addEventListener('click', () => {
    if (isVisualizing) return;
    isVisualizing = true;
    clearPath();
    
    // Construct edge-based walls set for algorithms.js
    const edges = new Set();
    for (const cellKey of wallCells) {
        const [r, c] = cellKey.split(',').map(Number);
        const offsets = [[-1, 0], [1, 0], [0, -1], [0, 1]];
        for (const [dr, dc] of offsets) {
            const nr = r+dr;
            const nc = c+dc;
            if (nr>=0 && nr<ROWS && nc>=0 && nc<COLS) {
                edges.add(getEdgeKey(r, c, nr, nc));
            }
        }
    }
    
    const path = bfsShortestPathGrid(ROWS, COLS, edges, startPoint, endPoint)
    if (path) {
        infoText.textContent = 'Shortest path found! Visualizing...';
        // Draw path
        path.forEach(([r, c], index) => {
            const isStart = r===startPoint[0] && c===startPoint[1];
            const isEnd = r===endPoint[0] && c===endPoint[1];
            if (!isStart && !isEnd) {
                setTimeout(() => {
                    addCellClass(r, c, 'path');
                }, index*30);
            }
        });
        setTimeout(() => {
            infoText.textContent = `Path found with ${path.length} steps (including start and end).`;
            isVisualizing = false;
        }, path.length*30);
    } else {
        infoText.textContent = 'No path is possible between start and end!';
        isVisualizing = false;
    }
});

// Reset Grid
btnReset.addEventListener('click', () => {
    if (isVisualizing) return;
    wallCells.clear();
    createGrid();
    setMode('wall');
});

// Initialize grid
createGrid();
setMode('wall');
