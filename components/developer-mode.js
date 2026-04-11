import {ProjectFilesMap} from './project-files-map.js';

class DeveloperMode extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({mode: 'open'});
    }

    async connectedCallback() {
        const currentPath = window.location.pathname;
        let matchKey = null;
        for (const key of Object.keys(ProjectFilesMap)) {
            if (currentPath.endsWith(key)) {
                matchKey = key;
                break;
            }
        }

        if (!matchKey) return;

        const files = ProjectFilesMap[matchKey];
        let html = `
            <style>
                @import url('https://cdn.jsdelivr.net/npm/prismjs@1.30.0/themes/prism-tomorrow.min.css');
                
                :host {
                    display: block;
                    max-width: 75rem;
                    margin: 3rem auto 2rem auto;
                    padding: 0 1rem;
                    font-family: Arial, Helvetica, sans-serif;
                }

                /* Code block styling */
                .dev-mode-title {
                    font-size: 1.5rem;
                    font-weight: 700;
                    margin-bottom: 1.5rem;
                    color: var(--page-text);
                    text-align: center;
                }
                .code-card {
                    background: var(--container-bg, #f9f9f9);
                    border: 1px solid var(--border-color, #cccccc);
                    border-radius: 0.75rem;
                    overflow: hidden;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                    margin-bottom: 2rem;
                }
                .code-header {
                    background: rgba(128, 128, 128, 0.05);
                    padding: 0.75rem 1.25rem;
                    border-bottom: 1px solid var(--border-color, #cccccc);
                }
                .filename {
                    opacity: 0.6;
                    font-size: 0.85rem;
                    font-family: monospace;
                    color: var(--page-text);
                }
                pre[class*="language-"] {
                    margin: 0 !important;
                    padding: 1.25rem !important;
                    background: transparent !important;
                    font-size: 0.95rem !important;
                }
                code[class*="language-"] {
                    text-shadow: none !important;
                    color: var(--page-text) !important;
                }
                
                /* Light mode */
                .token.comment { color: #6a737d !important; }
                .token.punctuation { color: var(--page-text) !important; }
                .token.keyword, .token.operator { color: #d73a49 !important; }
                .token.string { color: #032f62 !important; }
                .token.function { color: #6f42c1 !important; }
                .token.number { color: #005cc5 !important; }
                .token.class-name { color: #e36209 !important; }

                /* Dark mode */
                :host([data-theme="dark"]) .token.comment { color: #8b949e !important; }
                :host([data-theme="dark"]) .token.punctuation { color: var(--page-text) !important; }
                :host([data-theme="dark"]) .token.keyword, :host([data-theme="dark"]) .token.operator { color: #f97583 !important; }
                :host([data-theme="dark"]) .token.string { color: #9ecbff !important; }
                :host([data-theme="dark"]) .token.function { color: #b392f0 !important; }
                :host([data-theme="dark"]) .token.number { color: #79c0ff !important; }
                :host([data-theme="dark"]) .token.class-name { color: #ffab70 !important; }
            </style>
            
            <div class="dev-mode-container">
                <hr style="margin-bottom: 2rem; border: none; border-top: 1px solid var(--border-color, #cccccc);">
                <h2 class="dev-mode-title">Developer Mode: Source Code</h2>
        `;

        for (const file of files) {
            html += `
                <div class="code-card">
                    <div class="code-header">
                        <div class="filename">${file}</div>
                    </div>
                    <pre><code id="code-${file.replace(/\./g, '-')}" class="language-${this.getLanguage(file)}">Loading...</code></pre>
                </div>
            `;
        }
        
        html += `</div>`; // closing dev-mode-container
        this.shadowRoot.innerHTML = html;
        await this.loadPrism();

        // Fetch and display code
        for (const file of files) {
            try {
                // Ensure we fetch relative to the current html directory
                const response = await fetch(file);
                const codeEl = this.shadowRoot.getElementById(`code-${file.replace(/\./g, '-')}`);
                if (response.ok) {
                    const text = await response.text();
                    codeEl.textContent = text;
                    if (window.Prism) {
                        window.Prism.highlightElement(codeEl);
                    }
                } else {
                    codeEl.textContent = `Error loading ${file}: ${response.statusText}`;
                }
            } catch (err) {
                const codeEl = this.shadowRoot.getElementById(`code-${file.replace(/\./g, '-')}`);
                if (codeEl) {
                    codeEl.textContent = `Error loading ${file}: ${err.message}`;
                }
            }
        }

        // Keep theme in sync
        const updateTheme = () => {
            if (document.documentElement.getAttribute('data-theme')==='dark') {
                this.setAttribute('data-theme', 'dark');
            } else {
                this.removeAttribute('data-theme');
            }
        };
        updateTheme();
        const observer = new MutationObserver(updateTheme);
        observer.observe(document.documentElement, {attributes: true, attributeFilter: ['data-theme']});
    }

    getLanguage(filename) {
        if (filename.endsWith('.js')) return 'javascript';
        if (filename.endsWith('.css')) return 'css';
        if (filename.endsWith('.html')) return 'html';
        if (filename.endsWith('.py')) return 'python';
        return 'none';
    }

    async loadPrism() {
        if (window.Prism) return;
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/prismjs@1.30.0/prism.min.js';
            script.addEventListener('load', () => {
                const pyScript = document.createElement('script');
                pyScript.src = 'https://cdn.jsdelivr.net/npm/prismjs@1.30.0/components/prism-python.min.js';
                pyScript.addEventListener('load', resolve);
                pyScript.addEventListener('error', resolve); // Continue even if python fails
                document.head.appendChild(pyScript);
            });
            script.addEventListener('error', reject);
            document.head.appendChild(script);
        });
    }
}

customElements.define('developer-mode', DeveloperMode);
