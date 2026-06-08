const piecesUnicode = {
    'WP': '♙', 'BP': '♟',
    'WN': '♘', 'BN': '♞',
    'WB': '♗', 'BB': '♝',
    'WR': '♖', 'BR': '♜',
    'WK': '♔', 'BK': '♚',
    'WQ': '♕', 'BQ': '♛',
    '  ': ''};

let pyodide = null;
/** @type {{row: number, col: number}|null} */
let selectedSquare = null;
/** @type {{sr: number, sc: number, er: number, ec: number}|null} */
let pendingMove = null;
/** @type {string[][]|null} */
let boardState = null;
/** @type {number[][]} */
let legalMoves = [];

/**
 * Initializes Pyodide and the chess web page.
 * @returns {Promise<void>}
 */
async function initPyodide() {
    try {
        pyodide = await loadPyodide();
        const response = await fetch('chess_text.py');
        const code = await response.text();
        pyodide.FS.writeFile('chess_text.py', code);
        pyodide.runPython('import chess_text');
        resetGame(); // Initialize the game
        document.getElementById('reset-btn').disabled = false;
    } catch (e) {
        console.error(e);
        alert('Failed to load the Python chess engine.');
    }
}

/**
 * Resets the chess game to the initial starting position.
 */
function resetGame() {
    const state = pyodide.runPython('chess_text.init_game()').toJs();
    updateState(state);
    selectedSquare = null;
    pendingMove = null;
    legalMoves = [];
}

/**
 * Updates the current game state and renders it to the web page
 * @param {Map|Object} state - The game state dictionary returned from Pyodide.
 */
function updateState(state) {
    boardState = state.get('board');
    const turn = state.get('turn');
    const status = state.get('status');
    const log = state.get('log');
    
    // Update turn indicator
    const turnInd = document.getElementById('turn-indicator');
    if (status==='G') {
        turnInd.textContent = turn==='W' ? 'White\'s Turn' : 'Black\'s Turn';
    } else if (status==='W') {
        turnInd.textContent = 'White wins by checkmate!';
    } else if (status==='B') {
        turnInd.textContent = 'Black wins by checkmate!';
    } else {
        let reason = 'Draw';
        if (status==='D-50') reason = 'Draw (50-move rule)';
        else if (status==='D-R') reason = 'Draw (Repetition)';
        else if (status==='D-S') reason = 'Draw (Stalemate)';
        else if (status==='D-I') reason = 'Draw (Insufficient material)';
        turnInd.textContent = reason;
    }
    
    document.getElementById('pgn-log').textContent = log || 'No moves yet.';
    renderBoard();
}

/**
 * Renders the board on the screen based on boardState, selectedSquare, and legalMoves.
 */
function renderBoard() {
    const boardEl = document.getElementById('board');
    boardEl.innerHTML = '';
    
    for (let r = 0; r<8; r++) {
        for (let c = 0; c<8; c++) {
            const square = document.createElement('div');
            const isLight = (r+c)%2===0;
            square.className = `square ${isLight ? 'light' : 'dark'}`;
            square.dataset.row = r;
            square.dataset.col = c;
            const piece = boardState[r][c];
            square.textContent = piecesUnicode[piece] || '';
            if (selectedSquare && selectedSquare.row===r && selectedSquare.col===c) {
                square.classList.add('selected');
            }
            
            // Check if this square is a legal move
            const isLegal = legalMoves.some(m => m[0]===r && m[1]===c);
            if (isLegal) {
                if (piece==='  ') {
                    const dot = document.createElement('div');
                    dot.className = 'legal-dot';
                    square.appendChild(dot);
                } else {
                    square.classList.add('legal-capture');
                }
            }
            
            square.addEventListener('click', () => handleSquareClick(r, c));
            boardEl.appendChild(square);
        }
    }
}

/**
 * Handles board click events. Selects a piece if none is selected, or attempts a move if a piece is selected.
 * @param {number} r - Row index (0-7) of the clicked square.
 * @param {number} c - Column index (0-7) of the clicked square.
 */
function handleSquareClick(r, c) {
    const piece = boardState[r][c];
    const turn = pyodide.runPython('chess_text.turn');
    const isOwnPiece = piece!=='  ' && piece.startsWith(turn);
    
    if (isOwnPiece && (selectedSquare===null || selectedSquare.row!==r || selectedSquare.col!==c)) {
        // Select or switch selection to the clicked piece
        selectedSquare = {row: r, col: c};
        legalMoves = pyodide.runPython(`chess_text.get_legal_moves(${r}, ${c})`).toJs();
        renderBoard();
    } else if (selectedSquare!==null) {
        if (selectedSquare.row===r && selectedSquare.col===c) {
            // Deselect
            selectedSquare = null;
            legalMoves = [];
            renderBoard();
        } else {
            // Try moving
            attemptMove(selectedSquare.row, selectedSquare.col, r, c);
        }
    }
}

/**
 * Attempts to make a move with Pyodide and handles promotion with a modal.
 * @param {number} sr - Starting row index (0-7).
 * @param {number} sc - Starting column index (0-7).
 * @param {number} er - Ending row index (0-7).
 * @param {number} ec - Ending column index (0-7).
 * @param {string|null} [promoPiece=null] - The piece type chosen for pawn promotion ('Q', 'R', 'B', 'N').
 */
function attemptMove(sr, sc, er, ec, promoPiece = null) {
    let pyCmd = `chess_text.web_move(${sr}, ${sc}, ${er}, ${ec}`;
    if (promoPiece) {
        pyCmd += `, '${promoPiece}'`;
    }
    pyCmd += `)`;
    
    const res = pyodide.runPython(pyCmd).toJs();
    
    if (res.get('success')) {
        if (res.get('promotion_required')) {
            pendingMove = {sr, sc, er, ec};
            const turn = pyodide.runPython('chess_text.turn');
            document.querySelectorAll('.promo-btn').forEach(btn => {
                const pieceType = btn.dataset.piece;
                btn.textContent = piecesUnicode[turn+pieceType];
            });
            document.getElementById('promo-modal').style.display = 'flex';
        } else {
            selectedSquare = null;
            pendingMove = null;
            legalMoves = [];
            updateState(res);
        }
    } else {
        // Invalid move
        selectedSquare = null;
        legalMoves = [];
        renderBoard();
    }
}

// Setup promotion buttons
document.querySelectorAll('.promo-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        const piece = e.target.dataset.piece;
        document.getElementById('promo-modal').style.display = 'none';
        if (pendingMove) {
            attemptMove(pendingMove.sr, pendingMove.sc, pendingMove.er, pendingMove.ec, piece);
        }
    });
});

document.getElementById('reset-btn').addEventListener('click', resetGame);

initPyodide();
