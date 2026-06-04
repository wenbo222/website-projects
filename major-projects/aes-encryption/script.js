const modeSelect = document.getElementById('mode-select');
const actionSelect = document.getElementById('action-select');
const roundsSelect = document.getElementById('rounds-select');
const keyInput = document.getElementById('key-input');
const keyLabel = document.getElementById('key-label');
const ivInput = document.getElementById('iv-input');
const ivGroup = document.getElementById('iv-group');
const messageInput = document.getElementById('message-input');
const messageLabel = document.getElementById('message-label');
const processBtn = document.getElementById('process-btn');
const resultBox = document.getElementById('result-box');

// Load Python code
let pyodideInstance = null;
let pyProcessRequest = null;
processBtn.disabled = true;
processBtn.textContent = 'Loading Python code...';
resultBox.textContent = 'Loading Python environment via Pyodide, please wait...';
(async () => {
    try {
        const response = await fetch('AES.py');
        const pyCode = await response.text();
        pyodideInstance = await loadPyodide({
            indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.29.3/full/'
        });
        await pyodideInstance.runPythonAsync(pyCode); // Obtain Python context by running code
        pyProcessRequest = pyodideInstance.globals.get('process_request');
        processBtn.disabled = false;
        updateUI();
        resultBox.textContent = 'Python code Loaded. Ready for encryption/decryption.';
    } catch (error) {
        console.error('Failed to load Pyodide or run AES.py:', error);
        resultBox.textContent = 'Error: Failed to load the Python environment. Details: '+error.message;
        processBtn.textContent = 'Initialization Failed';
    }
})();

/**
 * Updates screen depending on changes in selected options.
 */
function updateUI() {
    if (!pyProcessRequest) return;
    const mode = modeSelect.value;
    const action = actionSelect.value;
    const rounds = parseInt(roundsSelect.value);
    
    // Update key length requirements in labels
    let keyLen = 16;
    if (rounds===13) keyLen = 24;
    else if (rounds===15) keyLen = 32;
    keyLabel.textContent = `Key (${keyLen} chars)`;
    keyInput.placeholder = `Enter ${keyLen}-character key...`;
    
    // Toggle IV group visibility based on mode of encryption used
    if (mode==='ECB' || mode==='EBC') {
        ivGroup.classList.add('hidden');
    } else {
        ivGroup.classList.remove('hidden');
    }
    
    // Update Message requirements based on action
    if (action==='encrypt') {
        messageLabel.textContent = 'Plaintext Message';
        messageInput.placeholder = 'Enter plaintext message here...';
        processBtn.textContent = 'Encrypt Message';
    } else {
        messageLabel.textContent = 'Ciphertext (hexadecimal separated by spaces)';
        messageInput.placeholder = 'E.g., 8c 8d 36 2c 14 c9 fe c0 ...';
        processBtn.textContent = 'Decrypt Message';
    }
}
modeSelect.addEventListener('change', updateUI);
actionSelect.addEventListener('change', updateUI);
roundsSelect.addEventListener('change', updateUI);

// Clear custom validity on input
keyInput.addEventListener('input', () => keyInput.setCustomValidity(''));
ivInput.addEventListener('input', () => ivInput.setCustomValidity(''));
messageInput.addEventListener('input', () => messageInput.setCustomValidity(''));

processBtn.addEventListener('click', () => {
    if (!pyProcessRequest) {
        resultBox.textContent = 'Error: Python code is not ready yet.';
        return;
    }
    
    const mode = modeSelect.value;
    const action = actionSelect.value;
    const rounds = parseInt(roundsSelect.value);
    const key = keyInput.value;
    const iv = ivInput.value;
    const message = messageInput.value;
    
    // Validation
    let requiredKeyLen = 16;
    if (rounds===13) requiredKeyLen = 24;
    else if (rounds===15) requiredKeyLen = 32;
    keyInput.setCustomValidity('');
    if (key.length!==requiredKeyLen) {
        keyInput.setCustomValidity(`Key must be exactly ${requiredKeyLen} characters long for this configuration.`);
        keyInput.reportValidity();
        return;
    }
    ivInput.setCustomValidity('');
    if (mode!=='ECB' && mode!=='EBC' && iv.length!==16) {
        ivInput.setCustomValidity('Initialization Vector (IV) must be exactly 16 characters long.');
        ivInput.reportValidity();
        return;
    }
    messageInput.setCustomValidity('');
    if (!message) {
        messageInput.setCustomValidity('Please enter a message to process.');
        messageInput.reportValidity();
        return;
    }
    
    // Call Python's process_request function
    try {
        const passIv = (mode==='ECB' || mode==='EBC') ? null : iv;
        const result = pyProcessRequest(mode, action, message, rounds, key, passIv);
        resultBox.textContent = result || '[Empty Output]';
    } catch (e) {
        console.error(e);
        resultBox.textContent = 'Error: An error occurred when executing Python code. Please double-check whether your message is valid.';
    }
});

updateUI();