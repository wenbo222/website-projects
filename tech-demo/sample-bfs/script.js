function addLineNumbers(codeEl) {
    const lines = codeEl.innerHTML.split('\n');
    if (lines.length && lines[lines.length-1]==='') lines.pop(); // Prevent extra empty line
    codeEl.innerHTML = lines.map(line => `<span class="code-line">${line}</span>`).join('');
}

document.addEventListener('DOMContentLoaded', async () => {
    // Display Python code
    const codeElement = document.getElementById('python-code');
    const filenameElement = document.querySelector('.filename');
    const filePath = 'sample-bfs.py';
    const response = await fetch(filePath);
    const content = await response.text();
    codeElement.textContent = content;
    Prism.highlightElement(codeElement);
    addLineNumbers(codeElement);
    filenameElement.textContent = filePath;

    // Obtain Python output
    const outputElement = document.getElementById('code-output');
    outputElement.textContent = '';
    let pyodide = await loadPyodide({
        indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.29.3/full/',
        stdout: (text) => {
            outputElement.textContent += text+'\n'; // += to prevent overwrite
        }
    });
    await pyodide.runPythonAsync(content);
});
